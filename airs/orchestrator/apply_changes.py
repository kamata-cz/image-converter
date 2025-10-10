#!/usr/bin/env python3
"""
Apply Changes Module

Applies generated code changes to the file system.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List


class ChangeApplicator:
    """Apply code changes to files."""

    def __init__(self, repo_root: str = "."):
        """
        Initialize applicator.

        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = Path(repo_root).absolute()

    def apply_changes(self, changes_file: str) -> Dict[str, Any]:
        """
        Apply changes from generated changes JSON file.

        Args:
            changes_file: Path to generated_changes.json

        Returns:
            Dictionary with results
        """
        # Load changes
        try:
            with open(changes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load changes file: {e}")

        changes = data.get("changes", [])

        results = {
            "applied": [],
            "failed": [],
            "skipped": [],
        }

        for change in changes:
            try:
                result = self._apply_single_change(change)
                if result["status"] == "success":
                    results["applied"].append(change["path"])
                elif result["status"] == "skipped":
                    results["skipped"].append(change["path"])
                else:
                    results["failed"].append({"path": change["path"], "error": result.get("error")})
            except Exception as e:
                results["failed"].append({"path": change.get("path", "unknown"), "error": str(e)})

        return results

    def _apply_single_change(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a single file change."""
        action = change.get("action")
        path = change.get("path")
        new_content = change.get("new_content")

        if not path:
            return {"status": "failed", "error": "No path specified"}

        file_path = self.repo_root / path

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if action == "create":
            if file_path.exists():
                # File already exists, treat as modify
                return self._modify_file(file_path, new_content)
            else:
                return self._create_file(file_path, new_content)

        elif action == "modify":
            if not file_path.exists():
                # File doesn't exist, create it
                return self._create_file(file_path, new_content)
            else:
                return self._modify_file(file_path, new_content)

        elif action == "delete":
            return self._delete_file(file_path)

        else:
            return {"status": "failed", "error": f"Unknown action: {action}"}

    def _create_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Create a new file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "action": "created"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _modify_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Modify an existing file."""
        try:
            # Backup original
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if file_path.exists():
                import shutil

                shutil.copy2(file_path, backup_path)

            # Write new content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {"status": "success", "action": "modified"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _delete_file(self, file_path: Path) -> Dict[str, Any]:
        """Delete a file."""
        try:
            if file_path.exists():
                file_path.unlink()
                return {"status": "success", "action": "deleted"}
            else:
                return {"status": "skipped", "reason": "File doesn't exist"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Apply generated code changes to files")
    parser.add_argument("--changes", required=True, help="Path to generated_changes.json")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")

    args = parser.parse_args()

    applicator = ChangeApplicator(repo_root=args.repo_root)

    try:
        results = applicator.apply_changes(args.changes)

        print("=" * 60)
        print("Change Application Results")
        print("=" * 60)

        print(f"\n✅ Successfully applied: {len(results['applied'])} file(s)")
        for path in results["applied"]:
            print(f"   - {path}")

        if results["skipped"]:
            print(f"\n⏭️  Skipped: {len(results['skipped'])} file(s)")
            for path in results["skipped"]:
                print(f"   - {path}")

        if results["failed"]:
            print(f"\n❌ Failed: {len(results['failed'])} file(s)")
            for failure in results["failed"]:
                print(f"   - {failure['path']}: {failure['error']}")
            sys.exit(1)

        print("\n✨ All changes applied successfully!")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
