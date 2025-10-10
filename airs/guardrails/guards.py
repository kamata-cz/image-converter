#!/usr/bin/env python3
"""
Guardrails Module

Enforces safety constraints on AI-generated changes.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

from .secret_scanner import SecretScanner
from .size_checker import SizeChecker
from .path_validator import PathValidator


class ViolationSeverity(Enum):
    """Severity levels for violations."""

    CRITICAL = "critical"  # Block immediately
    HIGH = "high"  # Block unless override
    MEDIUM = "medium"  # Warn but allow
    LOW = "low"  # Info only


@dataclass
class GuardRailViolation:
    """Represents a guardrail violation."""

    rule: str
    severity: ViolationSeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


class GuardRailValidator:
    """Validates changes against safety guardrails."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize validator with configuration.

        Args:
            config: Configuration dict with guardrail settings
        """
        self.config = config or {}
        self.secret_scanner = SecretScanner()
        self.size_checker = SizeChecker(
            max_files=self.config.get("max_files", 10),
            max_lines_per_file=self.config.get("max_lines_per_file", 500),
            max_total_lines=self.config.get("max_total_lines", 2000),
        )
        self.path_validator = PathValidator(
            allowed_paths=self.config.get("allowed_paths", ["src/", "tests/", "docs/"]),
            blocked_paths=self.config.get(
                "blocked_paths",
                [".github/workflows/", "*.pem", "*.key", ".env", "secrets/"],
            ),
        )

    def validate_changes(self, changes: List[Dict[str, Any]]) -> List[GuardRailViolation]:
        """
        Validate all changes against guardrails.

        Args:
            changes: List of file changes

        Returns:
            List of violations (empty if all checks pass)
        """
        violations = []

        # 1. Path validation
        violations.extend(self._validate_paths(changes))

        # 2. Size validation
        violations.extend(self._validate_sizes(changes))

        # 3. Secret detection
        violations.extend(self._detect_secrets(changes))

        # 4. Dangerous operations
        violations.extend(self._check_dangerous_operations(changes))

        return violations

    def _validate_paths(self, changes: List[Dict[str, Any]]) -> List[GuardRailViolation]:
        """Validate file paths against allowed/blocked lists."""
        violations = []

        for change in changes:
            path = change.get("path", "")
            result = self.path_validator.validate(path)

            if not result["allowed"]:
                violations.append(
                    GuardRailViolation(
                        rule="path_restriction",
                        severity=ViolationSeverity.CRITICAL,
                        message=f"Path not allowed: {path}",
                        file_path=path,
                        suggestion=f"Only changes to {', '.join(self.path_validator.allowed_paths)} are permitted",
                    )
                )

            if result.get("blocked"):
                violations.append(
                    GuardRailViolation(
                        rule="blocked_path",
                        severity=ViolationSeverity.CRITICAL,
                        message=f"Path explicitly blocked: {path}",
                        file_path=path,
                        suggestion="This file cannot be modified by automation",
                    )
                )

        return violations

    def _validate_sizes(self, changes: List[Dict[str, Any]]) -> List[GuardRailViolation]:
        """Validate change sizes against limits."""
        violations = []

        result = self.size_checker.validate(changes)

        if result["file_count_exceeded"]:
            violations.append(
                GuardRailViolation(
                    rule="max_files_exceeded",
                    severity=ViolationSeverity.HIGH,
                    message=f"Too many files changed: {result['file_count']} (max: {self.size_checker.max_files})",
                    suggestion="Break into smaller changes or request human review",
                )
            )

        if result["total_lines_exceeded"]:
            violations.append(
                GuardRailViolation(
                    rule="max_total_lines_exceeded",
                    severity=ViolationSeverity.HIGH,
                    message=f"Too many total lines changed: {result['total_lines']} (max: {self.size_checker.max_total_lines})",
                    suggestion="Break into smaller changes or request human review",
                )
            )

        for file_violation in result.get("file_violations", []):
            violations.append(
                GuardRailViolation(
                    rule="max_lines_per_file_exceeded",
                    severity=ViolationSeverity.MEDIUM,
                    message=f"File too large: {file_violation['path']} ({file_violation['lines']} lines)",
                    file_path=file_violation["path"],
                    suggestion=f"Keep files under {self.size_checker.max_lines_per_file} lines",
                )
            )

        return violations

    def _detect_secrets(self, changes: List[Dict[str, Any]]) -> List[GuardRailViolation]:
        """Detect secrets in changes."""
        violations = []

        for change in changes:
            content = change.get("new_content", "")
            if not content:
                continue

            secrets = self.secret_scanner.scan(content)

            for secret in secrets:
                violations.append(
                    GuardRailViolation(
                        rule="secret_detected",
                        severity=ViolationSeverity.CRITICAL,
                        message=f"Potential secret detected: {secret['type']}",
                        file_path=change.get("path"),
                        line_number=secret.get("line"),
                        suggestion="Never commit secrets. Use environment variables or secret management",
                    )
                )

        return violations

    def _check_dangerous_operations(self, changes: List[Dict[str, Any]]) -> List[GuardRailViolation]:
        """Check for dangerous code patterns."""
        violations = []

        dangerous_patterns = [
            {
                "pattern": r"os\.system\(",
                "message": "Direct os.system() call detected",
                "suggestion": "Use subprocess with explicit arguments",
            },
            {
                "pattern": r"\beval\(",
                "message": "eval() usage detected",
                "suggestion": "Avoid eval() for security reasons",
            },
            {
                "pattern": r"\bexec\(",
                "message": "exec() usage detected",
                "suggestion": "Avoid exec() for security reasons",
            },
            {
                "pattern": r"DROP\s+TABLE",
                "message": "DROP TABLE detected",
                "suggestion": "Database schema changes require manual review",
            },
            {
                "pattern": r"DELETE\s+FROM.*WHERE\s+1\s*=\s*1",
                "message": "Bulk DELETE detected",
                "suggestion": "Mass deletions require manual review",
            },
            {
                "pattern": r"subprocess\.call\(.*shell=True",
                "message": "subprocess with shell=True detected",
                "suggestion": "Use shell=False for security",
            },
        ]

        import re

        for change in changes:
            content = change.get("new_content", "")
            if not content:
                continue

            for pattern_def in dangerous_patterns:
                matches = re.finditer(pattern_def["pattern"], content, re.IGNORECASE)
                for match in matches:
                    # Find line number
                    line_num = content[: match.start()].count("\n") + 1

                    violations.append(
                        GuardRailViolation(
                            rule="dangerous_operation",
                            severity=ViolationSeverity.CRITICAL,
                            message=pattern_def["message"],
                            file_path=change.get("path"),
                            line_number=line_num,
                            suggestion=pattern_def["suggestion"],
                        )
                    )

        return violations

    def is_blocking(self, violations: List[GuardRailViolation]) -> bool:
        """
        Check if violations should block the change.

        Args:
            violations: List of violations

        Returns:
            True if change should be blocked
        """
        return any(
            v.severity in [ViolationSeverity.CRITICAL, ViolationSeverity.HIGH] for v in violations
        )

    def format_violations(self, violations: List[GuardRailViolation]) -> str:
        """Format violations for display."""
        if not violations:
            return "✅ All guardrail checks passed"

        output = "## 🚨 Guardrail Violations\n\n"

        # Group by severity
        by_severity = {}
        for v in violations:
            severity = v.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(v)

        # Display in severity order
        for severity in ["critical", "high", "medium", "low"]:
            if severity not in by_severity:
                continue

            severity_violations = by_severity[severity]
            emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}[severity]

            output += f"\n### {emoji} {severity.upper()} ({len(severity_violations)})\n\n"

            for v in severity_violations:
                output += f"**{v.rule}**: {v.message}\n"
                if v.file_path:
                    location = v.file_path
                    if v.line_number:
                        location += f":{v.line_number}"
                    output += f"  - Location: `{location}`\n"
                if v.suggestion:
                    output += f"  - Suggestion: {v.suggestion}\n"
                output += "\n"

        return output
