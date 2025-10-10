#!/usr/bin/env python3
"""
Metrics Collector Module

Collects metrics about the automation system.
"""

import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class IssueMetrics:
    """Metrics for a single issue resolution."""

    issue_number: int
    started_at: str
    completed_at: Optional[str] = None

    # Timing metrics (seconds)
    analysis_time: Optional[float] = None
    implementation_time: Optional[float] = None
    review_time: Optional[float] = None
    total_time: Optional[float] = None

    # Outcome metrics
    success: Optional[bool] = None
    pr_number: Optional[int] = None
    iterations: int = 0
    human_escalated: bool = False
    escalation_reason: Optional[str] = None

    # Quality metrics
    files_changed: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    tests_added: int = 0

    # Review metrics
    copilot_approved: bool = False
    human_approved: bool = False
    changes_requested_count: int = 0


@dataclass
class SystemMetrics:
    """System-wide metrics."""

    period_start: str
    period_end: Optional[str] = None

    # Volume metrics
    total_issues: int = 0
    auto_resolved: int = 0
    human_escalated: int = 0
    failed: int = 0

    # Success rates
    success_rate: float = 0.0
    first_pass_success_rate: float = 0.0

    # Timing metrics
    avg_total_time: float = 0.0
    avg_iterations: float = 0.0

    # Quality metrics
    avg_files_changed: float = 0.0
    avg_test_coverage: float = 0.0


class MetricsCollector:
    """Collects and stores metrics."""

    def __init__(self, storage_path: str = "metrics"):
        """
        Initialize metrics collector.

        Args:
            storage_path: Path to store metrics
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # In-memory metrics (current session)
        self.current_issues: Dict[int, IssueMetrics] = {}

    def start_issue(self, issue_number: int) -> IssueMetrics:
        """
        Start tracking an issue.

        Args:
            issue_number: Issue number

        Returns:
            IssueMetrics object
        """
        metrics = IssueMetrics(
            issue_number=issue_number,
            started_at=datetime.now().isoformat(),
        )
        self.current_issues[issue_number] = metrics
        return metrics

    def record_analysis(self, issue_number: int, duration: float):
        """Record analysis completion."""
        if issue_number in self.current_issues:
            self.current_issues[issue_number].analysis_time = duration

    def record_implementation(self, issue_number: int, duration: float, changes: Dict[str, Any]):
        """Record implementation completion."""
        if issue_number in self.current_issues:
            metrics = self.current_issues[issue_number]
            metrics.implementation_time = duration
            metrics.files_changed = len(changes.get("changes", []))
            # Calculate lines changed
            for change in changes.get("changes", []):
                content = change.get("new_content", "")
                if content:
                    lines = len(content.split("\n"))
                    if change.get("action") == "create":
                        metrics.lines_added += lines
                    else:
                        metrics.lines_added += lines  # Simplified

    def record_review(self, issue_number: int, duration: float, approved: bool):
        """Record review completion."""
        if issue_number in self.current_issues:
            metrics = self.current_issues[issue_number]
            metrics.review_time = duration
            metrics.copilot_approved = approved

    def record_iteration(self, issue_number: int):
        """Record a fix iteration."""
        if issue_number in self.current_issues:
            self.current_issues[issue_number].iterations += 1

    def record_escalation(self, issue_number: int, reason: str):
        """Record human escalation."""
        if issue_number in self.current_issues:
            metrics = self.current_issues[issue_number]
            metrics.human_escalated = True
            metrics.escalation_reason = reason
            self.complete_issue(issue_number, success=False)

    def complete_issue(
        self,
        issue_number: int,
        success: bool,
        pr_number: Optional[int] = None,
    ):
        """
        Mark issue as completed.

        Args:
            issue_number: Issue number
            success: Whether resolution was successful
            pr_number: PR number if created
        """
        if issue_number in self.current_issues:
            metrics = self.current_issues[issue_number]
            metrics.completed_at = datetime.now().isoformat()
            metrics.success = success
            metrics.pr_number = pr_number

            # Calculate total time
            start = datetime.fromisoformat(metrics.started_at)
            end = datetime.fromisoformat(metrics.completed_at)
            metrics.total_time = (end - start).total_seconds()

            # Save to disk
            self._save_issue_metrics(metrics)

    def _save_issue_metrics(self, metrics: IssueMetrics):
        """Save issue metrics to disk."""
        date_str = datetime.now().strftime("%Y-%m")
        file_path = self.storage_path / f"issues-{date_str}.jsonl"

        with open(file_path, "a") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")

    def load_period_metrics(self, start_date: str, end_date: Optional[str] = None) -> SystemMetrics:
        """
        Load metrics for a time period.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD), defaults to now

        Returns:
            SystemMetrics for the period
        """
        # Load all issue metrics for the period
        issues = []

        # Read all metric files
        for file_path in self.storage_path.glob("issues-*.jsonl"):
            with open(file_path, "r") as f:
                for line in f:
                    issue = json.loads(line)
                    # Filter by date
                    if issue["started_at"] >= start_date:
                        if not end_date or issue["started_at"] <= end_date:
                            issues.append(issue)

        # Calculate system metrics
        system_metrics = SystemMetrics(
            period_start=start_date,
            period_end=end_date or datetime.now().isoformat(),
        )

        if not issues:
            return system_metrics

        system_metrics.total_issues = len(issues)
        system_metrics.auto_resolved = sum(1 for i in issues if i.get("success"))
        system_metrics.human_escalated = sum(1 for i in issues if i.get("human_escalated"))
        system_metrics.failed = sum(1 for i in issues if not i.get("success") and not i.get("human_escalated"))

        # Success rate
        if system_metrics.total_issues > 0:
            system_metrics.success_rate = system_metrics.auto_resolved / system_metrics.total_issues

            # First pass success (no iterations)
            first_pass = sum(1 for i in issues if i.get("success") and i.get("iterations", 0) == 0)
            system_metrics.first_pass_success_rate = first_pass / system_metrics.total_issues

        # Average timing
        total_times = [i["total_time"] for i in issues if i.get("total_time")]
        if total_times:
            system_metrics.avg_total_time = sum(total_times) / len(total_times)

        # Average iterations
        iterations = [i.get("iterations", 0) for i in issues]
        if iterations:
            system_metrics.avg_iterations = sum(iterations) / len(iterations)

        # Average files changed
        files_changed = [i.get("files_changed", 0) for i in issues]
        if files_changed:
            system_metrics.avg_files_changed = sum(files_changed) / len(files_changed)

        return system_metrics


# Example usage
if __name__ == "__main__":
    collector = MetricsCollector()

    # Simulate issue resolution
    metrics = collector.start_issue(123)
    time.sleep(0.1)
    collector.record_analysis(123, 5.2)
    collector.record_implementation(123, 120.5, {"changes": [{"path": "test.py"}]})
    collector.record_review(123, 30.0, True)
    collector.complete_issue(123, success=True, pr_number=456)

    print("Issue metrics recorded")

    # Load period metrics
    system_metrics = collector.load_period_metrics("2025-01-01")
    print(f"\nSystem metrics: {asdict(system_metrics)}")
