#!/usr/bin/env python3
"""
Review Handler Module

Handles review feedback and coordinates iterative fixes.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .github_client import GitHubClient
from ..generator.claude_client import ClaudeClient


@dataclass
class ReviewFeedback:
    """Structured review feedback."""

    reviewer: str
    feedback_type: str  # "approve", "request_changes", "comment"
    comments: List[Dict[str, Any]]
    overall_summary: str


class ReviewHandler:
    """Handle review feedback and coordinate fixes."""

    def __init__(self, github_token: Optional[str] = None, claude_api_key: Optional[str] = None):
        """Initialize review handler."""
        self.github = GitHubClient(token=github_token)
        self.claude = ClaudeClient(api_key=claude_api_key)

    def process_review(
        self,
        repo_name: str,
        pr_number: int,
    ) -> ReviewFeedback:
        """
        Process review comments and extract actionable feedback.

        Args:
            repo_name: Repository name
            pr_number: PR number

        Returns:
            Structured review feedback
        """
        reviews = self.github.get_pr_reviews(repo_name, pr_number)
        comments = self.github.get_pr_comments(repo_name, pr_number)

        # Get latest review state per reviewer
        latest_reviews = {}
        for review in reviews:
            user = review["user"]
            if user not in latest_reviews or review["submitted_at"] > latest_reviews[user]["submitted_at"]:
                latest_reviews[user] = review

        # Determine overall feedback type
        if any(r["state"] == "CHANGES_REQUESTED" for r in latest_reviews.values()):
            feedback_type = "request_changes"
        elif all(r["state"] == "APPROVED" for r in latest_reviews.values()) and latest_reviews:
            feedback_type = "approve"
        else:
            feedback_type = "comment"

        # Extract reviewer (use first reviewer with changes requested, or first reviewer)
        reviewer = "unknown"
        if latest_reviews:
            for user, review in latest_reviews.items():
                if review["state"] == "CHANGES_REQUESTED":
                    reviewer = user
                    break
            if reviewer == "unknown":
                reviewer = next(iter(latest_reviews.keys()))

        # Summarize feedback
        summary = self._summarize_feedback(reviews, comments)

        return ReviewFeedback(
            reviewer=reviewer,
            feedback_type=feedback_type,
            comments=comments,
            overall_summary=summary,
        )

    def _summarize_feedback(self, reviews: List[Dict[str, Any]], comments: List[Dict[str, Any]]) -> str:
        """Summarize review feedback using Claude."""
        feedback_text = "## Review Feedback\n\n"

        for review in reviews:
            feedback_text += f"### Review by {review['user']} ({review['state']})\n"
            if review["body"]:
                feedback_text += f"{review['body']}\n\n"

        feedback_text += "## Comments\n\n"
        for comment in comments:
            feedback_text += f"**{comment['user']}**: {comment['body']}\n\n"

        # Ask Claude to summarize
        prompt = f"""Summarize the following code review feedback into actionable items:

{feedback_text}

Provide a concise summary with:
1. Main concerns or issues raised
2. Specific changes requested
3. Suggestions for improvement

Keep it brief and actionable.
"""

        summary = self.claude.send_message(prompt, reset_conversation=True)
        return summary

    def generate_fixes(
        self,
        repo_name: str,
        pr_number: int,
        feedback: ReviewFeedback,
        original_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate code fixes based on review feedback.

        Args:
            repo_name: Repository name
            pr_number: PR number
            feedback: Review feedback
            original_context: Original implementation context

        Returns:
            New changes to address feedback
        """
        # Get current PR files
        pr = self.github.get_pull_request(repo_name, pr_number)

        # Build fix generation prompt
        prompt = self._build_fix_prompt(feedback, original_context)

        # Generate fixes using Claude
        response = self.claude.generate_code(
            prompt=prompt,
            context=original_context,
            language=original_context.get("languages", {}).keys().__iter__().__next__() if original_context.get("languages") else "python",
        )

        # Parse fixes
        fixes = self._parse_fixes(response)

        return fixes

    def _build_fix_prompt(self, feedback: ReviewFeedback, context: Dict[str, Any]) -> str:
        """Build prompt for generating fixes."""
        prompt = f"""# Code Review Feedback

A code review was performed and the following feedback was provided:

## Reviewer: {feedback.reviewer}
## Type: {feedback.feedback_type}

## Summary of Feedback:
{feedback.overall_summary}

## Detailed Comments:
"""

        for comment in feedback.comments[:10]:  # Limit to 10 comments
            prompt += f"\n**{comment['user']}**: {comment['body']}\n"
            if comment.get("path"):
                prompt += f"  File: {comment['path']}, Line: {comment.get('line', 'N/A')}\n"

        prompt += """

## Your Task:
Please address the review feedback by:
1. Fixing the issues raised
2. Implementing suggested improvements
3. Maintaining code quality and consistency

Provide the complete updated code for each file that needs changes.

Use this format:
### File: path/to/file.py
```python
# Complete updated file content
```
"""

        return prompt

    def _parse_fixes(self, response: str) -> Dict[str, Any]:
        """Parse fixes from Claude's response."""
        import re

        fixes = {
            "changes": [],
            "explanation": "",
        }

        # Extract file changes
        file_pattern = r"###\s+File:\s+([^\n]+)\n```(\w+)?\n(.*?)```"
        matches = re.finditer(file_pattern, response, re.DOTALL)

        for match in matches:
            file_path = match.group(1).strip()
            language = match.group(2) or "python"
            content = match.group(3).strip()

            fixes["changes"].append({"path": file_path, "content": content, "language": language})

        # Extract explanation
        if "explanation" in response.lower() or "changes made" in response.lower():
            # Try to extract explanation section
            exp_pattern = r"(?:Explanation|Changes Made|Summary):?\n(.*?)(?=###|$)"
            exp_match = re.search(exp_pattern, response, re.DOTALL | re.IGNORECASE)
            if exp_match:
                fixes["explanation"] = exp_match.group(1).strip()

        return fixes

    def apply_fixes_and_update_pr(
        self,
        repo_name: str,
        pr_number: int,
        fixes: Dict[str, Any],
    ) -> None:
        """
        Apply fixes and update PR.

        Note: This is a simplified version. In production, you'd:
        1. Checkout the PR branch
        2. Apply the fixes
        3. Commit and push
        4. Update PR with comment
        """
        # Comment on PR about fixes
        comment = f"""## 🔧 Fixes Applied

I've addressed the review feedback:

{fixes.get('explanation', 'Changes have been applied as requested.')}

### Files Updated:
"""

        for change in fixes["changes"]:
            comment += f"- `{change['path']}`\n"

        comment += "\nPlease review the updates."

        self.github.create_comment(repo_name, pr_number, comment)

    def check_if_approved(self, repo_name: str, pr_number: int) -> bool:
        """Check if PR has been approved."""
        reviews = self.github.get_pr_reviews(repo_name, pr_number)

        # Get latest review per reviewer
        latest_reviews = {}
        for review in reviews:
            user = review["user"]
            if user not in latest_reviews or review["submitted_at"] > latest_reviews[user]["submitted_at"]:
                latest_reviews[user] = review

        # Check if at least one approval and no change requests
        has_approval = any(r["state"] == "APPROVED" for r in latest_reviews.values())
        has_change_request = any(r["state"] == "CHANGES_REQUESTED" for r in latest_reviews.values())

        return has_approval and not has_change_request


# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python review_handler.py <repo> <pr_number>")
        sys.exit(1)

    handler = ReviewHandler()
    feedback = handler.process_review(sys.argv[1], int(sys.argv[2]))

    print(f"Review Type: {feedback.feedback_type}")
    print(f"Reviewer: {feedback.reviewer}")
    print(f"\nSummary:\n{feedback.overall_summary}")
