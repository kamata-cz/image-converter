#!/usr/bin/env python3
"""
GitHub Client Module

Handles all GitHub API interactions.
"""

import os
from typing import List, Dict, Any, Optional
from github import Github, GithubException


class GitHubClient:
    """Client for GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.

        Args:
            token: GitHub personal access token (defaults to GITHUB_TOKEN env var)
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable or pass token parameter.")

        self.github = Github(self.token)

    def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Get issue details.

        Args:
            repo_name: Repository name (owner/repo)
            issue_number: Issue number

        Returns:
            Issue data as dictionary
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)

            return {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "author": issue.user.login,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
            }
        except GithubException as e:
            raise RuntimeError(f"Failed to get issue: {e}")

    def create_comment(self, repo_name: str, issue_number: int, comment: str) -> None:
        """
        Create a comment on an issue or PR.

        Args:
            repo_name: Repository name
            issue_number: Issue/PR number
            comment: Comment text
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            issue.create_comment(comment)
        except GithubException as e:
            raise RuntimeError(f"Failed to create comment: {e}")

    def add_labels(self, repo_name: str, issue_number: int, labels: List[str]) -> None:
        """
        Add labels to an issue or PR.

        Args:
            repo_name: Repository name
            issue_number: Issue/PR number
            labels: List of label names
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            issue.add_to_labels(*labels)
        except GithubException as e:
            raise RuntimeError(f"Failed to add labels: {e}")

    def remove_labels(self, repo_name: str, issue_number: int, labels: List[str]) -> None:
        """Remove labels from an issue or PR."""
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            for label in labels:
                try:
                    issue.remove_from_labels(label)
                except:
                    pass  # Ignore if label doesn't exist
        except GithubException as e:
            raise RuntimeError(f"Failed to remove labels: {e}")

    def get_pull_request(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """Get PR details."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            return {
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "mergeable": pr.mergeable,
                "merged": pr.merged,
                "labels": [label.name for label in pr.labels],
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
            }
        except GithubException as e:
            raise RuntimeError(f"Failed to get PR: {e}")

    def get_pr_reviews(self, repo_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Get all reviews for a PR."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            reviews = pr.get_reviews()

            return [
                {
                    "id": review.id,
                    "user": review.user.login,
                    "state": review.state,
                    "body": review.body,
                    "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None,
                }
                for review in reviews
            ]
        except GithubException as e:
            raise RuntimeError(f"Failed to get PR reviews: {e}")

    def get_pr_comments(self, repo_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Get all comments on a PR."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            # Get issue comments
            issue_comments = pr.get_issue_comments()
            # Get review comments
            review_comments = pr.get_review_comments()

            all_comments = []

            for comment in issue_comments:
                all_comments.append(
                    {
                        "id": comment.id,
                        "type": "issue_comment",
                        "user": comment.user.login,
                        "body": comment.body,
                        "created_at": comment.created_at.isoformat(),
                    }
                )

            for comment in review_comments:
                all_comments.append(
                    {
                        "id": comment.id,
                        "type": "review_comment",
                        "user": comment.user.login,
                        "body": comment.body,
                        "path": comment.path,
                        "line": comment.line,
                        "created_at": comment.created_at.isoformat(),
                    }
                )

            return sorted(all_comments, key=lambda x: x["created_at"])

        except GithubException as e:
            raise RuntimeError(f"Failed to get PR comments: {e}")

    def create_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
        draft: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a pull request.

        Args:
            repo_name: Repository name
            title: PR title
            body: PR description
            head: Branch to merge from
            base: Branch to merge into (default: main)
            draft: Create as draft PR

        Returns:
            Created PR data
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.create_pull(title=title, body=body, head=head, base=base, draft=draft)

            return {
                "number": pr.number,
                "url": pr.html_url,
                "head": pr.head.ref,
                "base": pr.base.ref,
            }
        except GithubException as e:
            raise RuntimeError(f"Failed to create PR: {e}")

    def update_pull_request(
        self,
        repo_name: str,
        pr_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
    ) -> None:
        """Update PR title, body, or state."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            if title:
                pr.edit(title=title)
            if body:
                pr.edit(body=body)
            if state:
                pr.edit(state=state)

        except GithubException as e:
            raise RuntimeError(f"Failed to update PR: {e}")

    def get_file_contents(self, repo_name: str, file_path: str, ref: str = "main") -> str:
        """Get file contents from repository."""
        try:
            repo = self.github.get_repo(repo_name)
            content = repo.get_contents(file_path, ref=ref)
            return content.decoded_content.decode("utf-8")
        except GithubException as e:
            raise RuntimeError(f"Failed to get file contents: {e}")

    def check_branch_exists(self, repo_name: str, branch_name: str) -> bool:
        """Check if a branch exists."""
        try:
            repo = self.github.get_repo(repo_name)
            repo.get_branch(branch_name)
            return True
        except GithubException:
            return False

    def get_repo_info(self, repo_name: str) -> Dict[str, Any]:
        """Get repository information."""
        try:
            repo = self.github.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "default_branch": repo.default_branch,
                "languages": repo.get_languages(),
                "private": repo.private,
            }
        except GithubException as e:
            raise RuntimeError(f"Failed to get repo info: {e}")

    def close_issue(self, repo_name: str, issue_number: int, comment: Optional[str] = None) -> None:
        """Close an issue with optional comment."""
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)

            if comment:
                issue.create_comment(comment)

            issue.edit(state="closed")
        except GithubException as e:
            raise RuntimeError(f"Failed to close issue: {e}")


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python github_client.py <repo> <issue_number>")
        sys.exit(1)

    client = GitHubClient()
    issue = client.get_issue(sys.argv[1], int(sys.argv[2]))
    print(f"Issue #{issue['number']}: {issue['title']}")
    print(f"State: {issue['state']}")
    print(f"Labels: {', '.join(issue['labels'])}")
