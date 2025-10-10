#!/usr/bin/env python3
"""
Code Generator Module

Generates code changes based on issue analysis and implementation context.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional

from .claude_client import ClaudeClient
from ..guardrails.guards import GuardRailValidator
from ..rules.naming import NamingRules
from ..rules.templates import PRTemplate
from ..metrics.collector import MetricsCollector


@dataclass
class FileChange:
    """Represents a change to a file."""

    action: str  # "create", "modify", "delete"
    path: str
    original_content: Optional[str] = None
    new_content: Optional[str] = None
    language: str = "python"
    description: str = ""


@dataclass
class GeneratedChanges:
    """Complete set of generated changes."""

    issue_number: int
    changes: List[FileChange]
    summary: str
    test_files: List[str]
    warnings: List[str]


class CodeGenerator:
    """Generate code changes from implementation context."""

    def __init__(self, claude_api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize generator with Claude client and guardrails."""
        self.claude = ClaudeClient(api_key=claude_api_key)
        self.guardrails = GuardRailValidator(config=config)
        self.metrics = MetricsCollector()

    def generate_from_context(self, context: Dict[str, Any]) -> GeneratedChanges:
        """
        Generate code changes from implementation context.

        Args:
            context: Implementation context from ContextBuilder

        Returns:
            GeneratedChanges with all file modifications
        """
        issue = context["issue"]
        feasibility = context["feasibility"]
        related_files = context.get("related_files", [])

        # Start metrics tracking
        self.metrics.start_issue(issue["number"])
        import time
        start_time = time.time()

        changes = []
        test_files = []
        warnings = []

        # Generate main implementation
        main_changes = self._generate_implementation(issue, feasibility, context)
        changes.extend(main_changes)

        # Record implementation time
        impl_time = time.time() - start_time

        # IMPORTANT: Validate against guardrails BEFORE proceeding
        violations = self.guardrails.validate_changes([asdict(c) for c in changes])

        if self.guardrails.is_blocking(violations):
            # Convert violations to warnings and mark for escalation
            warnings.append("⚠️ **GUARDRAIL VIOLATIONS DETECTED** - Human review required")
            warnings.append(self.guardrails.format_violations(violations))
            self.metrics.record_escalation(issue["number"], "Guardrail violations")
            # Still return changes for human review, but mark as needing escalation
        else:
            # Non-blocking violations become warnings
            if violations:
                warnings.append(self.guardrails.format_violations(violations))

        # Generate tests if needed
        if feasibility["complexity"] != "simple":
            test_changes = self._generate_tests(main_changes, context)
            changes.extend(test_changes)
            test_files = [c.path for c in test_changes]

        # Check for potential issues
        warnings = self._validate_changes(changes, context)

        # Generate summary
        summary = self._generate_summary(issue, changes)

        return GeneratedChanges(
            issue_number=issue["number"],
            changes=changes,
            summary=summary,
            test_files=test_files,
            warnings=warnings,
        )

    def _generate_implementation(
        self,
        issue: Dict[str, Any],
        feasibility: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[FileChange]:
        """Generate main implementation changes."""
        changes = []

        # Build prompt for Claude
        prompt = self._build_implementation_prompt(issue, feasibility, context)

        # Get implementation from Claude
        response = self.claude.generate_code(
            prompt=prompt,
            context=context,
            language=self._detect_primary_language(context),
        )

        # Parse response and extract file changes
        parsed_changes = self._parse_code_response(response, context)
        changes.extend(parsed_changes)

        return changes

    def _generate_tests(self, implementation_changes: List[FileChange], context: Dict[str, Any]) -> List[FileChange]:
        """Generate test files for implementation."""
        test_changes = []
        test_framework = context.get("test_framework", "pytest")
        language = self._detect_primary_language(context)

        for change in implementation_changes:
            if change.action == "delete":
                continue

            # Generate tests for this file
            test_code = self.claude.generate_tests(
                code=change.new_content or "",
                test_framework=test_framework,
                language=language,
            )

            # Determine test file path
            test_path = self._get_test_file_path(change.path, language)

            test_changes.append(
                FileChange(
                    action="create",
                    path=test_path,
                    new_content=test_code,
                    language=language,
                    description=f"Tests for {change.path}",
                )
            )

        return test_changes

    def _build_implementation_prompt(
        self,
        issue: Dict[str, Any],
        feasibility: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        """Build prompt for implementation generation."""
        prompt = f"""# Issue #{issue['number']}: {issue['title']}

## Problem Description
{issue.get('problem_description') or issue.get('body', 'No description provided')}

## Expected Behavior
{issue.get('expected_behavior', 'Not specified')}

## Acceptance Criteria
"""

        if issue.get("acceptance_criteria"):
            for criterion in issue["acceptance_criteria"]:
                prompt += f"- {criterion}\n"
        else:
            prompt += "Not specified\n"

        # Add AI instructions if provided
        if issue.get("ai_instructions"):
            prompt += f"\n## Implementation Instructions\n{issue['ai_instructions']}\n"

        # Add implementation steps
        if context.get("implementation_steps"):
            prompt += "\n## Implementation Steps\n"
            for i, step in enumerate(context["implementation_steps"], 1):
                prompt += f"{i}. {step}\n"

        # Add existing code context
        if context.get("related_files"):
            prompt += "\n## Existing Code Context\n"
            for file_ctx in context["related_files"][:3]:
                prompt += f"\n### {file_ctx['path']}\n"
                if file_ctx.get("content"):
                    prompt += f"```{file_ctx.get('language', 'python')}\n{file_ctx['content'][:3000]}\n```\n"

        prompt += """

## Requirements
- Provide complete, working code
- Follow existing code style and conventions
- Handle errors appropriately
- Add clear comments and documentation
- For each file, use this format:

### File: path/to/file.py
```python
# Complete file content here
```

### File: path/to/another_file.py
```python
# Complete file content here
```
"""

        return prompt

    def _parse_code_response(self, response: str, context: Dict[str, Any]) -> List[FileChange]:
        """Parse Claude's response and extract file changes."""
        changes = []

        # Pattern to match file sections
        file_pattern = r"###\s+File:\s+([^\n]+)\n```(\w+)?\n(.*?)```"
        matches = re.finditer(file_pattern, response, re.DOTALL)

        for match in matches:
            file_path = match.group(1).strip()
            language = match.group(2) or self._detect_primary_language(context)
            content = match.group(3).strip()

            # Determine if this is a new file or modification
            action = "create"
            original_content = None

            # Check if file exists in related files
            for related_file in context.get("related_files", []):
                if related_file["path"] == file_path:
                    action = "modify"
                    original_content = related_file.get("content")
                    break

            changes.append(
                FileChange(
                    action=action,
                    path=file_path,
                    original_content=original_content,
                    new_content=content,
                    language=language,
                    description=f"Implementation for issue #{context['issue']['number']}",
                )
            )

        return changes

    def _validate_changes(self, changes: List[FileChange], context: Dict[str, Any]) -> List[str]:
        """Validate generated changes and return warnings."""
        warnings = []

        # Check file count
        if len(changes) > 20:
            warnings.append(f"Large number of files modified ({len(changes)}). Consider breaking into smaller PRs.")

        # Check for security-sensitive files
        sensitive_patterns = [
            r"\.env",
            r"secret",
            r"password",
            r"credential",
            r"key",
            r"token",
            r"config\.prod",
        ]

        for change in changes:
            for pattern in sensitive_patterns:
                if re.search(pattern, change.path, re.IGNORECASE):
                    warnings.append(f"Modifying security-sensitive file: {change.path}")

        # Check for missing tests
        has_implementation = any(c.action in ["create", "modify"] and not self._is_test_file(c.path) for c in changes)
        has_tests = any(self._is_test_file(c.path) for c in changes)

        if has_implementation and not has_tests:
            warnings.append("No test files generated. Tests should be added.")

        return warnings

    def _generate_summary(self, issue: Dict[str, Any], changes: List[FileChange]) -> str:
        """Generate summary of changes."""
        created = sum(1 for c in changes if c.action == "create")
        modified = sum(1 for c in changes if c.action == "modify")
        deleted = sum(1 for c in changes if c.action == "delete")

        summary = f"Implemented solution for issue #{issue['number']}: {issue['title']}\n\n"
        summary += f"**Changes:**\n"
        if created:
            summary += f"- {created} file(s) created\n"
        if modified:
            summary += f"- {modified} file(s) modified\n"
        if deleted:
            summary += f"- {deleted} file(s) deleted\n"

        summary += f"\n**Modified Files:**\n"
        for change in changes[:10]:  # Limit to first 10
            summary += f"- `{change.path}` ({change.action})\n"

        if len(changes) > 10:
            summary += f"- ... and {len(changes) - 10} more files\n"

        return summary

    def _detect_primary_language(self, context: Dict[str, Any]) -> str:
        """Detect primary language from context."""
        languages = context.get("languages", {})
        if not languages:
            return "python"

        return max(languages, key=languages.get).lower()

    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file."""
        path_lower = file_path.lower()
        return any(pattern in path_lower for pattern in ["test_", "_test.", ".test.", ".spec.", "/tests/", "/test/"])

    def _get_test_file_path(self, source_path: str, language: str) -> str:
        """Generate test file path for source file."""
        path = Path(source_path)

        # Language-specific test conventions
        if language.lower() == "python":
            # tests/test_module.py
            return f"tests/test_{path.name}"
        elif language.lower() in ["javascript", "typescript"]:
            # module.test.js or module.spec.ts
            return f"{path.stem}.test{path.suffix}"
        elif language.lower() == "go":
            # module_test.go
            return f"{path.stem}_test{path.suffix}"
        else:
            return f"tests/test_{path.name}"

    def to_dict(self, changes: GeneratedChanges) -> Dict[str, Any]:
        """Convert changes to dictionary."""
        return asdict(changes)

    def to_json(self, changes: GeneratedChanges) -> str:
        """Convert changes to JSON."""
        return json.dumps(self.to_dict(changes), indent=2, ensure_ascii=False)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate code from implementation context")
    parser.add_argument("--plan", required=True, help="Path to implementation plan JSON")
    parser.add_argument("--issue-number", type=int, required=True, help="Issue number")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--output", default="generated_changes.json", help="Output file path")

    args = parser.parse_args()

    # Load implementation plan
    try:
        with open(args.plan, "r", encoding="utf-8") as f:
            context = json.load(f)
    except Exception as e:
        print(f"Error loading implementation plan: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate code
    generator = CodeGenerator()
    try:
        changes = generator.generate_from_context(context)

        # Save changes
        json_output = generator.to_json(changes)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)

        print(f"Code generation complete. Changes saved to: {args.output}", file=sys.stderr)
        print(f"Summary:\n{changes.summary}", file=sys.stderr)

        if changes.warnings:
            print(f"\nWarnings:", file=sys.stderr)
            for warning in changes.warnings:
                print(f"  - {warning}", file=sys.stderr)

    except Exception as e:
        print(f"Error generating code: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
