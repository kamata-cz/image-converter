"""
System Settings Module

Centralized configuration for the AI-Driven Issue Resolution System.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """System configuration settings."""

    # GitHub Configuration
    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_repository: Optional[str] = Field(None, env="GITHUB_REPOSITORY")

    # Claude API Configuration
    claude_api_key: str = Field(..., env="CLAUDE_API_KEY")
    claude_model: str = Field("claude-3-5-sonnet-20241022", env="CLAUDE_MODEL")

    # System Configuration
    automation_env: str = Field("dev", env="AUTOMATION_ENV")
    max_concurrent_issues: int = Field(5, env="MAX_CONCURRENT_ISSUES")
    max_pr_per_day: int = Field(50, env="MAX_PR_PER_DAY")

    # Security Settings
    enable_security_scanning: bool = Field(True, env="ENABLE_SECURITY_SCANNING")
    block_on_security_issues: bool = Field(True, env="BLOCK_ON_SECURITY_ISSUES")

    # Notification Settings
    slack_webhook_url: Optional[str] = Field(None, env="SLACK_WEBHOOK_URL")
    enable_slack_notifications: bool = Field(False, env="ENABLE_SLACK_NOTIFICATIONS")

    # Observability
    enable_detailed_logging: bool = Field(True, env="ENABLE_DETAILED_LOGGING")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Feature Flags
    enable_iterative_fixes: bool = Field(True, env="ENABLE_ITERATIVE_FIXES")
    enable_auto_generate_tests: bool = Field(True, env="ENABLE_AUTO_GENERATE_TESTS")
    enable_ai_code_review: bool = Field(True, env="ENABLE_AI_CODE_REVIEW")

    # Rate Limiting
    max_issues_per_hour: int = Field(10, env="MAX_ISSUES_PER_HOUR")
    min_retry_interval_seconds: int = Field(300, env="MIN_RETRY_INTERVAL_SECONDS")

    # Review Settings
    required_approvals: int = Field(1, env="REQUIRED_APPROVALS")
    auto_merge_enabled: bool = Field(False, env="AUTO_MERGE_ENABLED")
    max_fix_iterations: int = Field(3, env="MAX_FIX_ITERATIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get settings singleton instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
