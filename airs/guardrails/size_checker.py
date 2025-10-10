#!/usr/bin/env python3
"""
Size Checker Module

Validates change sizes against limits.
"""

from typing import List, Dict, Any


class SizeChecker:
    """Checks if changes exceed size limits."""

    def __init__(
        self,
        max_files: int = 10,
        max_lines_per_file: int = 500,
        max_total_lines: int = 2000,
    ):
        """
        Initialize size checker.

        Args:
            max_files: Maximum number of files that can be changed
            max_lines_per_file: Maximum lines per file
            max_total_lines: Maximum total lines across all files
        """
        self.max_files = max_files
        self.max_lines_per_file = max_lines_per_file
        self.max_total_lines = max_total_lines

    def validate(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate changes against size limits.

        Args:
            changes: List of file changes

        Returns:
            Dictionary with validation results
        """
        file_count = len(changes)
        total_lines = 0
        file_violations = []

        for change in changes:
            # Count lines in new content
            content = change.get("new_content", "")
            if content:
                line_count = len(content.split("\n"))
                total_lines += line_count

                if line_count > self.max_lines_per_file:
                    file_violations.append(
                        {"path": change.get("path", "unknown"), "lines": line_count}
                    )

        return {
            "file_count": file_count,
            "total_lines": total_lines,
            "file_count_exceeded": file_count > self.max_files,
            "total_lines_exceeded": total_lines > self.max_total_lines,
            "file_violations": file_violations,
        }


# Example usage
if __name__ == "__main__":
    checker = SizeChecker(max_files=5, max_lines_per_file=100, max_total_lines=300)

    test_changes = [
        {"path": "file1.py", "new_content": "\n".join([f"line {i}" for i in range(50)])},
        {"path": "file2.py", "new_content": "\n".join([f"line {i}" for i in range(150)])},  # Too large
        {"path": "file3.py", "new_content": "\n".join([f"line {i}" for i in range(50)])},
    ]

    result = checker.validate(test_changes)
    print("Validation result:")
    print(f"  File count: {result['file_count']} (exceeded: {result['file_count_exceeded']})")
    print(f"  Total lines: {result['total_lines']} (exceeded: {result['total_lines_exceeded']})")
    if result["file_violations"]:
        print("  File violations:")
        for v in result["file_violations"]:
            print(f"    - {v['path']}: {v['lines']} lines")
