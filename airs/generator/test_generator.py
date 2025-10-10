#!/usr/bin/env python3
"""
Test Generator Module

Generates comprehensive tests for code changes.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from .claude_client import ClaudeClient
from .code_generator import FileChange


class TestGenerator:
    """Generate tests for code changes."""

    TEST_FRAMEWORKS = {
        "python": "pytest",
        "javascript": "jest",
        "typescript": "jest",
        "go": "testing",
        "rust": "cargo test",
        "java": "junit",
        "ruby": "rspec",
    }

    def __init__(self, claude_api_key: Optional[str] = None):
        """Initialize test generator."""
        self.claude = ClaudeClient(api_key=claude_api_key)

    def generate_tests(
        self,
        changes: List[Dict[str, Any]],
        language: str = "python",
        test_framework: Optional[str] = None,
    ) -> List[FileChange]:
        """
        Generate tests for code changes.

        Args:
            changes: List of file changes
            language: Programming language
            test_framework: Test framework to use (auto-detected if None)

        Returns:
            List of test file changes
        """
        test_framework = test_framework or self.TEST_FRAMEWORKS.get(language.lower(), "pytest")

        test_changes = []

        for change in changes:
            # Skip if already a test file
            if self._is_test_file(change["path"]):
                continue

            # Skip deleted files
            if change["action"] == "delete":
                continue

            # Generate test for this file
            test_change = self._generate_test_for_file(change, language, test_framework)

            if test_change:
                test_changes.append(test_change)

        return test_changes

    def _generate_test_for_file(
        self,
        change: Dict[str, Any],
        language: str,
        test_framework: str,
    ) -> Optional[FileChange]:
        """Generate test for a single file."""
        code = change.get("new_content")
        if not code:
            return None

        # Build test generation prompt
        prompt = self._build_test_prompt(change, language, test_framework)

        # Generate test code
        test_code = self.claude.generate_tests(code=code, test_framework=test_framework, language=language)

        # Extract just the code if wrapped in markdown
        test_code = self._extract_code_from_response(test_code, language)

        # Determine test file path
        test_path = self._get_test_path(change["path"], language)

        return FileChange(
            action="create",
            path=test_path,
            new_content=test_code,
            language=language,
            description=f"Tests for {change['path']}",
        )

    def _build_test_prompt(self, change: Dict[str, Any], language: str, test_framework: str) -> str:
        """Build prompt for test generation."""
        prompt = f"""Generate comprehensive tests for the following {language} code using {test_framework}.

**File**: {change['path']}

**Code**:
```{language}
{change['new_content']}
```

**Requirements**:
1. Test all public functions/methods
2. Test edge cases and error conditions
3. Use clear, descriptive test names
4. Include docstrings/comments explaining what each test does
5. Mock external dependencies
6. Achieve high code coverage

**Test Framework**: {test_framework}

Generate complete, runnable test code.
"""
        return prompt

    def _extract_code_from_response(self, response: str, language: str) -> str:
        """Extract code from Claude's response."""
        # Try to find code block
        patterns = [
            f"```{language}\n(.*?)\n```",
            "```\n(.*?)\n```",
        ]

        import re

        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()

        # If no code block found, return as-is
        return response.strip()

    def _get_test_path(self, source_path: str, language: str) -> str:
        """Generate test file path for source file."""
        path = Path(source_path)

        if language.lower() == "python":
            # src/module.py -> tests/test_module.py
            # src/package/module.py -> tests/package/test_module.py
            if "src/" in source_path:
                test_path = source_path.replace("src/", "tests/")
                test_path = Path(test_path)
                return str(test_path.parent / f"test_{test_path.name}")
            else:
                return f"tests/test_{path.name}"

        elif language.lower() in ["javascript", "typescript"]:
            # module.js -> module.test.js
            return f"{path.stem}.test{path.suffix}"

        elif language.lower() == "go":
            # module.go -> module_test.go
            return f"{path.stem}_test.go"

        elif language.lower() == "rust":
            # Tests are typically in the same file or in tests/ directory
            return f"tests/{path.stem}_test.rs"

        else:
            return f"tests/test_{path.name}"

    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file."""
        path_lower = file_path.lower()
        return any(
            pattern in path_lower
            for pattern in ["test_", "_test.", ".test.", ".spec.", "/tests/", "/test/", "_spec."]
        )

    def generate_integration_tests(
        self,
        changes: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> Optional[FileChange]:
        """Generate integration tests that test multiple components together."""
        # Only generate if changes involve multiple files
        if len(changes) < 2:
            return None

        language = self._detect_language(context)
        test_framework = self.TEST_FRAMEWORKS.get(language.lower(), "pytest")

        # Build prompt for integration tests
        prompt = f"""Generate integration tests for the following code changes.

These tests should verify that the components work together correctly.

**Changes**:
"""

        for change in changes[:5]:  # Limit to first 5 files
            prompt += f"\n### {change['path']}\n```{language}\n{change.get('new_content', '')[:1000]}\n```\n"

        prompt += f"""

**Requirements**:
1. Test interactions between components
2. Test data flow through the system
3. Test error propagation
4. Use appropriate mocks for external services
5. Clear test scenarios and assertions

Use {test_framework} framework.
"""

        response = self.claude.send_message(prompt, reset_conversation=True)

        test_code = self._extract_code_from_response(response, language)

        return FileChange(
            action="create",
            path=f"tests/integration/test_integration.{self._get_extension(language)}",
            new_content=test_code,
            language=language,
            description="Integration tests for changes",
        )

    def _detect_language(self, context: Dict[str, Any]) -> str:
        """Detect language from context."""
        languages = context.get("languages", {})
        if not languages:
            return "python"
        return max(languages, key=languages.get).lower()

    def _get_extension(self, language: str) -> str:
        """Get file extension for language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "go": "go",
            "rust": "rs",
            "java": "java",
            "ruby": "rb",
        }
        return extensions.get(language.lower(), "py")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate tests for code changes")
    parser.add_argument("--changes", required=True, help="Path to generated changes JSON")
    parser.add_argument("--output", default="test_changes.json", help="Output file path")

    args = parser.parse_args()

    # Load changes
    try:
        with open(args.changes, "r", encoding="utf-8") as f:
            data = json.load(f)
            changes = data.get("changes", [])
    except Exception as e:
        print(f"Error loading changes: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate tests
    generator = TestGenerator()
    try:
        # Detect language from first change
        language = changes[0].get("language", "python") if changes else "python"

        test_changes = generator.generate_tests(changes, language=language)

        # Save test changes
        output_data = {"test_changes": [vars(tc) for tc in test_changes]}

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"Test generation complete. Tests saved to: {args.output}", file=sys.stderr)
        print(f"Generated {len(test_changes)} test file(s)", file=sys.stderr)

    except Exception as e:
        print(f"Error generating tests: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
