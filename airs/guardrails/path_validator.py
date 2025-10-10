#!/usr/bin/env python3
"""
Path Validator Module

Validates file paths against allowed/blocked lists.
"""

import fnmatch
from typing import List, Dict, Any


class PathValidator:
    """Validates file paths against rules."""

    def __init__(
        self,
        allowed_paths: List[str] = None,
        blocked_paths: List[str] = None,
    ):
        """
        Initialize path validator.

        Args:
            allowed_paths: List of allowed path patterns (e.g., ["src/", "tests/"])
            blocked_paths: List of blocked path patterns (e.g., ["*.key", "secrets/"])
        """
        self.allowed_paths = allowed_paths or ["src/", "tests/", "docs/"]
        self.blocked_paths = blocked_paths or [
            ".github/workflows/",
            "*.pem",
            "*.key",
            ".env",
            ".env.*",
            "secrets/",
            "credentials/",
        ]

    def validate(self, path: str) -> Dict[str, Any]:
        """
        Validate a file path.

        Args:
            path: File path to validate

        Returns:
            Dictionary with validation results
        """
        # Check if blocked (higher priority)
        blocked = self._is_blocked(path)

        # Check if allowed
        allowed = self._is_allowed(path)

        return {
            "path": path,
            "allowed": allowed and not blocked,
            "blocked": blocked,
            "reason": self._get_reason(path, allowed, blocked),
        }

    def _is_allowed(self, path: str) -> bool:
        """Check if path matches any allowed pattern."""
        for pattern in self.allowed_paths:
            # Exact prefix match or glob match
            if path.startswith(pattern) or fnmatch.fnmatch(path, pattern):
                return True
        return False

    def _is_blocked(self, path: str) -> bool:
        """Check if path matches any blocked pattern."""
        for pattern in self.blocked_paths:
            # Exact prefix match or glob match
            if path.startswith(pattern) or fnmatch.fnmatch(path, pattern):
                return True
        return False

    def _get_reason(self, path: str, allowed: bool, blocked: bool) -> str:
        """Get reason for validation result."""
        if blocked:
            return "Path is explicitly blocked"
        if not allowed:
            return f"Path not in allowed list: {', '.join(self.allowed_paths)}"
        return "OK"


# Example usage
if __name__ == "__main__":
    validator = PathValidator()

    test_paths = [
        "src/main.py",  # Should be allowed
        "tests/test_main.py",  # Should be allowed
        ".github/workflows/ci.yml",  # Should be blocked
        "secrets/api_key.txt",  # Should be blocked
        "config.py",  # Not in allowed paths
        "private.key",  # Blocked by pattern
    ]

    for path in test_paths:
        result = validator.validate(path)
        status = "✅" if result["allowed"] else "❌"
        print(f"{status} {path}: {result['reason']}")
