#!/usr/bin/env python3
"""
Secret Scanner Module

Detects potential secrets in code.
"""

import re
from typing import List, Dict, Any


class SecretScanner:
    """Scans for potential secrets in code."""

    # Secret patterns (regex)
    PATTERNS = [
        {
            "name": "AWS Access Key",
            "pattern": r"AKIA[0-9A-Z]{16}",
            "severity": "critical",
        },
        {
            "name": "AWS Secret Key",
            "pattern": r"aws[_-]?secret[_-]?access[_-]?key['\"]?\s*[:=]\s*['\"]([A-Za-z0-9/+=]{40})['\"]",
            "severity": "critical",
        },
        {
            "name": "GitHub Token",
            "pattern": r"gh[pousr]_[A-Za-z0-9]{36,}",
            "severity": "critical",
        },
        {
            "name": "Generic API Key",
            "pattern": r"(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]([A-Za-z0-9]{32,})['\"]",
            "severity": "high",
        },
        {
            "name": "Generic Secret",
            "pattern": r"(?i)(secret[_-]?key|secretkey)['\"]?\s*[:=]\s*['\"]([A-Za-z0-9]{20,})['\"]",
            "severity": "high",
        },
        {
            "name": "Password",
            "pattern": r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
            "severity": "high",
        },
        {
            "name": "Private Key",
            "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE KEY-----",
            "severity": "critical",
        },
        {
            "name": "Bearer Token",
            "pattern": r"[Bb]earer\s+[A-Za-z0-9\-\._~\+\/]+=*",
            "severity": "high",
        },
        {
            "name": "Slack Token",
            "pattern": r"xox[baprs]-[0-9]{12}-[0-9]{12}-[A-Za-z0-9]{24,}",
            "severity": "critical",
        },
        {
            "name": "Generic Token",
            "pattern": r"(?i)(token)['\"]?\s*[:=]\s*['\"]([A-Za-z0-9]{32,})['\"]",
            "severity": "medium",
        },
    ]

    # Exceptions (patterns that look like secrets but aren't)
    EXCEPTIONS = [
        r"example[_-]?key",
        r"your[_-]?key",
        r"placeholder",
        r"dummy[_-]?token",
        r"test[_-]?secret",
        r"<your[_-]",
        r"\$\{",  # Environment variable reference
        r"ENV\[",  # Environment variable reference
        r"os\.getenv",  # Environment variable access
        r"process\.env",  # Environment variable access
    ]

    def scan(self, content: str) -> List[Dict[str, Any]]:
        """
        Scan content for potential secrets.

        Args:
            content: Text content to scan

        Returns:
            List of detected secrets
        """
        secrets = []

        lines = content.split("\n")

        for pattern_def in self.PATTERNS:
            pattern = pattern_def["pattern"]
            matches = re.finditer(pattern, content, re.MULTILINE)

            for match in matches:
                # Get line number
                line_num = content[: match.start()].count("\n") + 1
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                # Check if it's an exception
                if self._is_exception(line_content):
                    continue

                secrets.append(
                    {
                        "type": pattern_def["name"],
                        "severity": pattern_def["severity"],
                        "line": line_num,
                        "match": match.group(0)[:50],  # Truncate for safety
                        "line_content": line_content.strip()[:100],
                    }
                )

        return secrets

    def _is_exception(self, line: str) -> bool:
        """Check if line matches exception patterns."""
        line_lower = line.lower()

        for exception_pattern in self.EXCEPTIONS:
            if re.search(exception_pattern, line_lower):
                return True

        return False


# Example usage
if __name__ == "__main__":
    scanner = SecretScanner()

    test_code = """
    # This should NOT be detected (environment variable)
    api_key = os.getenv("API_KEY")

    # This SHOULD be detected
    api_key = "sk-1234567890abcdef1234567890abcdef"

    # This should NOT be detected (placeholder)
    token = "your_token_here"

    # This SHOULD be detected
    aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
    """

    secrets = scanner.scan(test_code)
    for secret in secrets:
        print(f"Found {secret['type']} on line {secret['line']}: {secret['match']}")
