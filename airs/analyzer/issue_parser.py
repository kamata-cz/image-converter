#!/usr/bin/env python3
"""
Issue Parser Module

Parses GitHub Issues and extracts structured information for AI analysis.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

from github import Github, GithubException


@dataclass
class ParsedIssue:
    """Structured representation of a GitHub Issue."""

    number: int
    title: str
    body: str
    author: str
    labels: List[str]
    created_at: str

    # Extracted sections
    problem_description: Optional[str] = None
    expected_behavior: Optional[str] = None
    reproduction_steps: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    ai_instructions: Optional[str] = None

    # Metadata
    complexity_hint: Optional[str] = None
    related_files: Optional[List[str]] = None
    related_issues: Optional[List[int]] = None


class IssueParser:
    """Parse GitHub Issues and extract structured information."""

    SECTION_PATTERNS = {
        "problem": r"###?\s*(?:問題の説明|Problem Description|Issue)(.*?)(?=###|$)",
        "expected": r"###?\s*(?:期待する動作|Expected Behavior|Expected)(.*?)(?=###|$)",
        "reproduction": r"###?\s*(?:再現手順|Reproduction Steps|Steps to Reproduce)(.*?)(?=###|$)",
        "acceptance": r"###?\s*(?:受入基準|Acceptance Criteria|Checklist)(.*?)(?=###|$)",
        "ai_instructions": r"###?\s*(?:AIへの指示|AI Instructions|Instructions)(.*?)(?=###|$)",
    }

    def __init__(self, github_token: str):
        """Initialize parser with GitHub token."""
        self.github = Github(github_token)

    def parse_issue(self, repo_name: str, issue_number: int) -> ParsedIssue:
        """
        Parse a GitHub Issue and extract structured information.

        Args:
            repo_name: Repository name (e.g., "owner/repo")
            issue_number: Issue number

        Returns:
            ParsedIssue object with extracted information

        Raises:
            GithubException: If issue cannot be fetched
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
        except GithubException as e:
            print(f"Error fetching issue: {e}", file=sys.stderr)
            raise

        # Basic information
        parsed = ParsedIssue(
            number=issue.number,
            title=issue.title,
            body=issue.body or "",
            author=issue.user.login,
            labels=[label.name for label in issue.labels],
            created_at=issue.created_at.isoformat(),
        )

        # Extract structured sections
        self._extract_sections(parsed)

        # Extract metadata
        self._extract_metadata(parsed)

        return parsed

    def _extract_sections(self, parsed: ParsedIssue) -> None:
        """Extract structured sections from issue body."""
        body = parsed.body

        # Problem description
        match = re.search(self.SECTION_PATTERNS["problem"], body, re.DOTALL | re.IGNORECASE)
        if match:
            parsed.problem_description = match.group(1).strip()

        # Expected behavior
        match = re.search(self.SECTION_PATTERNS["expected"], body, re.DOTALL | re.IGNORECASE)
        if match:
            parsed.expected_behavior = match.group(1).strip()

        # Reproduction steps
        match = re.search(self.SECTION_PATTERNS["reproduction"], body, re.DOTALL | re.IGNORECASE)
        if match:
            steps_text = match.group(1).strip()
            # Extract numbered or bulleted list items
            steps = re.findall(r"(?:^\s*(?:\d+\.|-|\*)\s+(.+)$)", steps_text, re.MULTILINE)
            parsed.reproduction_steps = [s.strip() for s in steps if s.strip()]

        # Acceptance criteria
        match = re.search(self.SECTION_PATTERNS["acceptance"], body, re.DOTALL | re.IGNORECASE)
        if match:
            criteria_text = match.group(1).strip()
            # Extract checkboxes or bulleted items
            criteria = re.findall(r"(?:^\s*(?:-\s*\[[ x]\]|-|\*)\s+(.+)$)", criteria_text, re.MULTILINE)
            parsed.acceptance_criteria = [c.strip() for c in criteria if c.strip()]

        # AI instructions
        match = re.search(self.SECTION_PATTERNS["ai_instructions"], body, re.DOTALL | re.IGNORECASE)
        if match:
            parsed.ai_instructions = match.group(1).strip()

    def _extract_metadata(self, parsed: ParsedIssue) -> None:
        """Extract metadata hints from issue content."""
        body = parsed.body.lower()

        # Complexity hints from labels or content
        complexity_keywords = {
            "simple": ["typo", "formatting", "documentation", "comment"],
            "medium": ["refactor", "improve", "enhance", "add feature"],
            "complex": ["architecture", "migration", "large scale", "breaking change"],
        }

        for level, keywords in complexity_keywords.items():
            if any(kw in body or kw in parsed.title.lower() for kw in keywords):
                parsed.complexity_hint = level
                break

        # Extract file references
        file_pattern = r"`([a-zA-Z0-9_/.-]+\.[a-zA-Z0-9]+)`"
        files = re.findall(file_pattern, parsed.body)
        if files:
            parsed.related_files = list(set(files))

        # Extract issue references (#123)
        issue_pattern = r"#(\d+)"
        issues = re.findall(issue_pattern, parsed.body)
        if issues:
            parsed.related_issues = [int(i) for i in issues if int(i) != parsed.number]

    def to_dict(self, parsed: ParsedIssue) -> Dict[str, Any]:
        """Convert ParsedIssue to dictionary."""
        return asdict(parsed)

    def to_json(self, parsed: ParsedIssue) -> str:
        """Convert ParsedIssue to JSON string."""
        return json.dumps(self.to_dict(parsed), indent=2, ensure_ascii=False)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Parse GitHub Issue for AI analysis")
    parser.add_argument("--issue-number", type=int, required=True, help="Issue number")
    parser.add_argument("--repo", required=True, help="Repository name (owner/repo)")
    parser.add_argument("--output", help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Parse issue
    issue_parser = IssueParser(github_token)
    try:
        parsed = issue_parser.parse_issue(args.repo, args.issue_number)
        json_output = issue_parser.to_json(parsed)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"Issue parsed successfully. Output: {args.output}", file=sys.stderr)
        else:
            print(json_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
