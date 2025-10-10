#!/usr/bin/env python3
"""
Claude API Client (Supports both Anthropic API and AWS Bedrock)

Automatically detects which backend to use based on environment variables:
- If USE_BEDROCK=true: Uses AWS Bedrock (no Claude API key needed)
- Otherwise: Uses Anthropic Claude API (requires CLAUDE_API_KEY)
"""

import os

# Determine which backend to use
USE_BEDROCK = os.getenv("USE_BEDROCK", "false").lower() in ("true", "1", "yes")

if USE_BEDROCK:
    # Use AWS Bedrock backend
    from .claude_client_bedrock import ClaudeClientBedrock as ClaudeClient
    print("✓ Using AWS Bedrock for Claude API (no API key required)")
else:
    # Use Anthropic API backend (original implementation)
    from .claude_client_anthropic import ClaudeClientAnthropic as ClaudeClient
    print("✓ Using Anthropic Claude API (requires CLAUDE_API_KEY)")

# Export for easy importing
__all__ = ["ClaudeClient"]


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m airs.generator.claude_client <message>")
        print("\nBackend selection:")
        print("  USE_BEDROCK=false (default): Anthropic API")
        print("    Required: CLAUDE_API_KEY")
        print("  USE_BEDROCK=true: AWS Bedrock")
        print("    Required: AWS credentials (IAM role or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY)")
        print("    Optional: AWS_REGION (default: us-east-1)")
        sys.exit(1)

    try:
        client = ClaudeClient()
        response = client.send_message(sys.argv[1])
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
