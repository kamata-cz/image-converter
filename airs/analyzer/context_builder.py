#!/usr/bin/env python3
"""
Context Builder Module

Builds implementation context by analyzing repository structure and related code.
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional

from github import Github, GithubException

from .issue_parser import ParsedIssue
from .feasibility import FeasibilityResult


@dataclass
class FileContext:
    """Context for a single file."""

    path: str
    language: str
    content: Optional[str] = None
    relevance_score: float = 0.0
    reason: str = ""


@dataclass
class ImplementationContext:
    """Complete context for implementing a solution."""

    issue: ParsedIssue
    feasibility: FeasibilityResult

    # Repository information
    repo_name: str
    default_branch: str
    languages: Dict[str, int]  # language -> bytes

    # Relevant files
    related_files: List[FileContext]
    similar_files: List[FileContext]

    # Code patterns
    coding_style: Optional[Dict[str, Any]] = None
    test_framework: Optional[str] = None

    # Implementation plan
    implementation_steps: List[str] = None


class ContextBuilder:
    """Build implementation context from repository and issue."""

    MAX_FILE_SIZE = 100000  # 100KB max file size to read

    LANGUAGE_EXTENSIONS = {
        "python": [".py"],
        "javascript": [".js", ".jsx"],
        "typescript": [".ts", ".tsx"],
        "go": [".go"],
        "rust": [".rs"],
        "java": [".java"],
        "ruby": [".rb"],
    }

    TEST_PATTERNS = {
        "python": ["pytest", "unittest", "test_*.py", "*_test.py"],
        "javascript": ["jest", "mocha", "*.test.js", "*.spec.js"],
        "typescript": ["jest", "*.test.ts", "*.spec.ts"],
        "go": ["*_test.go"],
    }

    def __init__(self, github_token: str):
        """Initialize builder with GitHub token."""
        self.github = Github(github_token)

    def build_context(
        self, repo_name: str, parsed_issue: ParsedIssue, feasibility: FeasibilityResult
    ) -> ImplementationContext:
        """
        Build complete implementation context.

        Args:
            repo_name: Repository name (owner/repo)
            parsed_issue: Parsed issue data
            feasibility: Feasibility analysis result

        Returns:
            ImplementationContext with all necessary information
        """
        try:
            repo = self.github.get_repo(repo_name)
        except GithubException as e:
            print(f"Error fetching repository: {e}", file=sys.stderr)
            raise

        # Get repository metadata
        default_branch = repo.default_branch
        languages = repo.get_languages()

        # Identify related files
        related_files = self._identify_related_files(repo, parsed_issue, languages)

        # Find similar files (for context)
        similar_files = self._find_similar_files(repo, related_files, languages)

        # Detect coding style and test framework
        coding_style = self._detect_coding_style(repo, languages)
        test_framework = self._detect_test_framework(repo, languages)

        # Generate implementation steps
        steps = self._generate_implementation_steps(parsed_issue, feasibility, related_files)

        return ImplementationContext(
            issue=parsed_issue,
            feasibility=feasibility,
            repo_name=repo_name,
            default_branch=default_branch,
            languages=languages,
            related_files=related_files,
            similar_files=similar_files,
            coding_style=coding_style,
            test_framework=test_framework,
            implementation_steps=steps,
        )

    def _identify_related_files(
        self, repo, parsed_issue: ParsedIssue, languages: Dict[str, int]
    ) -> List[FileContext]:
        """Identify files mentioned in the issue or likely to be modified."""
        related = []

        # Files explicitly mentioned in issue
        if parsed_issue.related_files:
            for file_path in parsed_issue.related_files:
                try:
                    file_content = repo.get_contents(file_path)
                    if file_content.size <= self.MAX_FILE_SIZE:
                        content = file_content.decoded_content.decode("utf-8")
                    else:
                        content = None

                    related.append(
                        FileContext(
                            path=file_path,
                            language=self._detect_language(file_path, languages),
                            content=content,
                            relevance_score=1.0,
                            reason="Explicitly mentioned in issue",
                        )
                    )
                except Exception as e:
                    print(f"Warning: Could not fetch {file_path}: {e}", file=sys.stderr)

        # Search for files based on keywords in issue
        keywords = self._extract_keywords(parsed_issue)
        if keywords:
            search_results = self._search_files_by_keywords(repo, keywords, languages)
            related.extend(search_results[:5])  # Limit to top 5 results

        return related

    def _find_similar_files(
        self, repo, related_files: List[FileContext], languages: Dict[str, int]
    ) -> List[FileContext]:
        """Find similar files for additional context."""
        if not related_files:
            return []

        similar = []
        primary_language = max(languages, key=languages.get) if languages else None

        if not primary_language:
            return similar

        # Look for test files if main file is not a test
        for file_ctx in related_files[:3]:  # Limit to first 3 related files
            if not self._is_test_file(file_ctx.path):
                test_file = self._find_corresponding_test(repo, file_ctx.path, primary_language)
                if test_file:
                    similar.append(test_file)

        return similar

    def _detect_coding_style(self, repo, languages: Dict[str, int]) -> Dict[str, Any]:
        """Detect coding style from repository."""
        style = {
            "formatter": None,
            "linter": None,
            "indentation": "unknown",
        }

        try:
            # Check for common config files
            config_files = [
                ".editorconfig",
                ".prettierrc",
                "pyproject.toml",
                ".eslintrc",
                "tslint.json",
            ]

            for config_file in config_files:
                try:
                    content = repo.get_contents(config_file)
                    if "prettier" in config_file:
                        style["formatter"] = "prettier"
                    elif "eslint" in config_file or "tslint" in config_file:
                        style["linter"] = "eslint"
                    elif "pyproject.toml" in config_file:
                        config_content = content.decoded_content.decode("utf-8")
                        if "black" in config_content:
                            style["formatter"] = "black"
                        if "ruff" in config_content or "flake8" in config_content:
                            style["linter"] = "ruff" if "ruff" in config_content else "flake8"
                except:
                    pass

        except Exception as e:
            print(f"Warning: Could not detect coding style: {e}", file=sys.stderr)

        return style

    def _detect_test_framework(self, repo, languages: Dict[str, int]) -> Optional[str]:
        """Detect test framework used in repository."""
        primary_language = max(languages, key=languages.get) if languages else None

        if not primary_language:
            return None

        try:
            # Check common files
            if primary_language.lower() == "python":
                # Check for pytest.ini, setup.cfg, pyproject.toml
                try:
                    repo.get_contents("pytest.ini")
                    return "pytest"
                except:
                    pass

                try:
                    content = repo.get_contents("pyproject.toml")
                    if b"pytest" in content.decoded_content:
                        return "pytest"
                except:
                    pass

                return "pytest"  # Default for Python

            elif primary_language.lower() in ["javascript", "typescript"]:
                try:
                    content = repo.get_contents("package.json")
                    pkg_json = json.loads(content.decoded_content.decode("utf-8"))
                    deps = {**pkg_json.get("dependencies", {}), **pkg_json.get("devDependencies", {})}

                    if "jest" in deps:
                        return "jest"
                    elif "mocha" in deps:
                        return "mocha"
                except:
                    pass

        except Exception as e:
            print(f"Warning: Could not detect test framework: {e}", file=sys.stderr)

        return None

    def _generate_implementation_steps(
        self, parsed_issue: ParsedIssue, feasibility: FeasibilityResult, related_files: List[FileContext]
    ) -> List[str]:
        """Generate high-level implementation steps."""
        steps = []

        # Step 1: Understand current code
        if related_files:
            steps.append(f"Review existing code in: {', '.join(f.path for f in related_files[:3])}")
        else:
            steps.append("Identify files to modify based on issue requirements")

        # Step 2: Implement changes
        if parsed_issue.ai_instructions:
            steps.append(f"Implement changes: {parsed_issue.ai_instructions}")
        else:
            steps.append("Implement changes to address the issue")

        # Step 3: Add tests
        if feasibility.complexity.value != "simple":
            steps.append("Write unit tests for new/modified code")

        # Step 4: Verify acceptance criteria
        if parsed_issue.acceptance_criteria:
            steps.append(f"Verify all acceptance criteria: {len(parsed_issue.acceptance_criteria)} items")

        # Step 5: Final checks
        steps.append("Run linter and formatter")
        steps.append("Ensure all tests pass")

        return steps

    def _extract_keywords(self, parsed_issue: ParsedIssue) -> List[str]:
        """Extract keywords from issue for file search."""
        keywords = []

        # Extract from title
        title_words = [w for w in parsed_issue.title.split() if len(w) > 3]
        keywords.extend(title_words[:5])

        # Extract from AI instructions if available
        if parsed_issue.ai_instructions:
            instruction_words = [w for w in parsed_issue.ai_instructions.split() if len(w) > 3]
            keywords.extend(instruction_words[:5])

        return list(set(keywords))[:10]  # Limit to 10 unique keywords

    def _search_files_by_keywords(self, repo, keywords: List[str], languages: Dict[str, int]) -> List[FileContext]:
        """Search for files containing keywords."""
        results = []

        # Note: GitHub API search is limited, this is a simplified version
        # In production, you'd want to use more sophisticated search

        for keyword in keywords[:3]:  # Limit keywords to avoid rate limits
            try:
                search_results = repo.get_contents("", ref=repo.default_branch)
                # This is a simplified search - production version would be more comprehensive
            except Exception as e:
                print(f"Warning: Search failed for keyword '{keyword}': {e}", file=sys.stderr)

        return results

    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file."""
        path_lower = file_path.lower()
        return any(
            pattern in path_lower
            for pattern in ["test_", "_test.", ".test.", ".spec.", "/tests/", "/test/"]
        )

    def _find_corresponding_test(self, repo, file_path: str, language: str) -> Optional[FileContext]:
        """Find corresponding test file for a source file."""
        # This is a simplified version
        path_obj = Path(file_path)
        possible_test_paths = [
            f"tests/test_{path_obj.name}",
            f"test/test_{path_obj.name}",
            path_obj.with_name(f"test_{path_obj.name}"),
        ]

        for test_path in possible_test_paths:
            try:
                content = repo.get_contents(str(test_path))
                return FileContext(
                    path=str(test_path),
                    language=language,
                    content=None,  # Don't load content for similar files
                    relevance_score=0.7,
                    reason="Corresponding test file",
                )
            except:
                pass

        return None

    def _detect_language(self, file_path: str, languages: Dict[str, int]) -> str:
        """Detect language from file extension."""
        ext = Path(file_path).suffix

        for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
            if ext in extensions:
                return lang

        # Fallback to most common language in repo
        return max(languages, key=languages.get) if languages else "unknown"

    def to_dict(self, context: ImplementationContext) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return asdict(context)

    def to_json(self, context: ImplementationContext) -> str:
        """Convert context to JSON string."""
        return json.dumps(self.to_dict(context), indent=2, ensure_ascii=False, default=str)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Build implementation context for AI code generation")
    parser.add_argument("--issue-number", type=int, required=True, help="Issue number")
    parser.add_argument("--repo", required=True, help="Repository name (owner/repo)")
    parser.add_argument("--issue-json", help="Path to parsed issue JSON (optional)")
    parser.add_argument("--feasibility-json", help="Path to feasibility result JSON (optional)")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Load or create parsed issue and feasibility
    # For now, create minimal versions if not provided
    from .issue_parser import IssueParser
    from .feasibility import FeasibilityAnalyzer, Complexity

    parser_obj = IssueParser(github_token)
    parsed_issue = parser_obj.parse_issue(args.repo, args.issue_number)

    analyzer = FeasibilityAnalyzer()
    feasibility = analyzer.analyze(parsed_issue)

    # Build context
    builder = ContextBuilder(github_token)
    context = builder.build_context(args.repo, parsed_issue, feasibility)

    # Save to file
    json_output = builder.to_json(context)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json_output)

    print(f"Implementation context built successfully. Output: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
