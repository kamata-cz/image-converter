#!/usr/bin/env python3
"""
Feasibility Analyzer Module

Determines whether an issue can be automatically resolved by AI.
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional, Dict, Any

from .issue_parser import ParsedIssue


class Complexity(Enum):
    """Issue complexity levels."""

    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    HUMAN_REQUIRED = "human_required"


@dataclass
class FeasibilityResult:
    """Result of feasibility analysis."""

    feasible: bool
    complexity: Complexity
    confidence: float  # 0.0 to 1.0
    reasoning: str
    estimated_time_minutes: Optional[int]
    blockers: List[str]
    warnings: List[str]
    recommended_approach: Optional[str] = None


class FeasibilityAnalyzer:
    """Analyze whether an issue can be AI-resolved."""

    # Keywords that indicate human intervention required
    HUMAN_REQUIRED_KEYWORDS = [
        "production database",
        "delete all",
        "drop table",
        "security vulnerability",
        "authentication",
        "authorization",
        "payment",
        "billing",
        "gdpr",
        "compliance",
    ]

    # Keywords that indicate complexity
    COMPLEXITY_INDICATORS = {
        Complexity.SIMPLE: [
            "typo",
            "fix spelling",
            "update comment",
            "documentation",
            "readme",
            "format",
            "style",
            "lint",
        ],
        Complexity.MEDIUM: [
            "add function",
            "refactor",
            "improve",
            "optimize",
            "add test",
            "bug fix",
            "error handling",
        ],
        Complexity.COMPLEX: [
            "architecture",
            "design pattern",
            "migration",
            "breaking change",
            "api change",
            "database schema",
            "large scale",
        ],
    }

    # File count thresholds
    MAX_FILES_SIMPLE = 3
    MAX_FILES_MEDIUM = 10
    MAX_FILES_COMPLEX = 20

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize analyzer with optional configuration."""
        self.config = config or {}

    def analyze(self, parsed_issue: ParsedIssue, repo_context: Optional[Dict[str, Any]] = None) -> FeasibilityResult:
        """
        Analyze issue feasibility.

        Args:
            parsed_issue: Parsed issue data
            repo_context: Optional repository context (file count, languages, etc.)

        Returns:
            FeasibilityResult with analysis
        """
        blockers = []
        warnings = []

        # Check for human-required keywords
        if self._contains_human_required_keywords(parsed_issue):
            return FeasibilityResult(
                feasible=False,
                complexity=Complexity.HUMAN_REQUIRED,
                confidence=0.95,
                reasoning="Issue contains security/critical operations requiring human review",
                estimated_time_minutes=None,
                blockers=["Security-critical or high-risk operation detected"],
                warnings=[],
            )

        # Determine complexity
        complexity = self._determine_complexity(parsed_issue, repo_context)

        # Check if too complex for AI
        if complexity == Complexity.HUMAN_REQUIRED:
            return FeasibilityResult(
                feasible=False,
                complexity=complexity,
                confidence=0.85,
                reasoning="Issue complexity exceeds AI capabilities",
                estimated_time_minutes=None,
                blockers=["Complexity too high for automated resolution"],
                warnings=[],
            )

        # Estimate time
        time_estimate = self._estimate_time(complexity, parsed_issue)

        # Check for missing information
        missing_info = self._check_missing_information(parsed_issue)
        if missing_info:
            warnings.extend([f"Missing: {info}" for info in missing_info])

        # Determine confidence
        confidence = self._calculate_confidence(parsed_issue, complexity, missing_info)

        # Generate recommended approach
        approach = self._generate_approach(parsed_issue, complexity)

        return FeasibilityResult(
            feasible=True,
            complexity=complexity,
            confidence=confidence,
            reasoning=f"Issue is {complexity.value} and suitable for AI resolution",
            estimated_time_minutes=time_estimate,
            blockers=blockers,
            warnings=warnings,
            recommended_approach=approach,
        )

    def _contains_human_required_keywords(self, issue: ParsedIssue) -> bool:
        """Check if issue contains keywords requiring human intervention."""
        content = f"{issue.title} {issue.body}".lower()
        return any(keyword in content for keyword in self.HUMAN_REQUIRED_KEYWORDS)

    def _determine_complexity(self, issue: ParsedIssue, repo_context: Optional[Dict[str, Any]]) -> Complexity:
        """Determine issue complexity."""
        content = f"{issue.title} {issue.body}".lower()

        # Check complexity indicators
        for complexity_level, keywords in self.COMPLEXITY_INDICATORS.items():
            if any(keyword in content for keyword in keywords):
                return complexity_level

        # Check file count if available
        if issue.related_files:
            file_count = len(issue.related_files)
            if file_count > self.MAX_FILES_COMPLEX:
                return Complexity.HUMAN_REQUIRED
            elif file_count > self.MAX_FILES_MEDIUM:
                return Complexity.COMPLEX
            elif file_count > self.MAX_FILES_SIMPLE:
                return Complexity.MEDIUM
            else:
                return Complexity.SIMPLE

        # Check labels
        if any("simple" in label.lower() or "good first issue" in label.lower() for label in issue.labels):
            return Complexity.SIMPLE

        # Default to medium if unclear
        return Complexity.MEDIUM

    def _estimate_time(self, complexity: Complexity, issue: ParsedIssue) -> int:
        """Estimate time in minutes based on complexity."""
        base_times = {
            Complexity.SIMPLE: 5,
            Complexity.MEDIUM: 15,
            Complexity.COMPLEX: 30,
        }

        base_time = base_times.get(complexity, 15)

        # Adjust based on acceptance criteria count
        if issue.acceptance_criteria:
            base_time += len(issue.acceptance_criteria) * 2

        # Adjust based on related files
        if issue.related_files:
            base_time += len(issue.related_files) * 3

        return min(base_time, 45)  # Cap at 45 minutes

    def _check_missing_information(self, issue: ParsedIssue) -> List[str]:
        """Check for missing critical information."""
        missing = []

        if not issue.problem_description and not issue.body:
            missing.append("Problem description")

        if not issue.expected_behavior:
            missing.append("Expected behavior")

        if not issue.acceptance_criteria:
            missing.append("Acceptance criteria")

        return missing

    def _calculate_confidence(
        self, issue: ParsedIssue, complexity: Complexity, missing_info: List[str]
    ) -> float:
        """Calculate confidence score (0.0 to 1.0)."""
        base_confidence = {
            Complexity.SIMPLE: 0.9,
            Complexity.MEDIUM: 0.75,
            Complexity.COMPLEX: 0.6,
        }

        confidence = base_confidence.get(complexity, 0.5)

        # Reduce confidence for missing information
        confidence -= len(missing_info) * 0.1

        # Increase confidence if AI instructions provided
        if issue.ai_instructions:
            confidence += 0.1

        # Increase confidence if acceptance criteria provided
        if issue.acceptance_criteria:
            confidence += 0.05

        return max(0.0, min(1.0, confidence))

    def _generate_approach(self, issue: ParsedIssue, complexity: Complexity) -> str:
        """Generate recommended implementation approach."""
        if complexity == Complexity.SIMPLE:
            return "Direct implementation with minimal testing"
        elif complexity == Complexity.MEDIUM:
            return "Incremental implementation with unit tests and integration tests"
        elif complexity == Complexity.COMPLEX:
            return "Phased implementation with comprehensive testing and review checkpoints"
        return "Manual implementation recommended"

    def to_dict(self, result: FeasibilityResult) -> Dict[str, Any]:
        """Convert result to dictionary."""
        data = asdict(result)
        data["complexity"] = result.complexity.value
        return data

    def to_json(self, result: FeasibilityResult) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(result), indent=2, ensure_ascii=False)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Analyze issue feasibility for AI resolution")
    parser.add_argument("--issue-json", required=True, help="Path to parsed issue JSON file")
    parser.add_argument("--output", help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Load parsed issue
    try:
        with open(args.issue_json, "r", encoding="utf-8") as f:
            issue_data = json.load(f)
        parsed_issue = ParsedIssue(**issue_data)
    except Exception as e:
        print(f"Error loading issue JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Analyze feasibility
    analyzer = FeasibilityAnalyzer()
    result = analyzer.analyze(parsed_issue)

    # Output result
    json_output = analyzer.to_json(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Feasibility analysis complete. Output: {args.output}", file=sys.stderr)
    else:
        print(json_output)

    # Set GitHub Actions output
    if os.getenv("GITHUB_ACTIONS"):
        with open(os.getenv("GITHUB_OUTPUT", "/dev/stdout"), "a") as f:
            f.write(f"feasible={str(result.feasible).lower()}\n")
            f.write(f"complexity={result.complexity.value}\n")
            f.write(f"estimation={result.estimated_time_minutes}min\n")

    sys.exit(0 if result.feasible else 1)


if __name__ == "__main__":
    main()
