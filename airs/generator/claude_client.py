#!/usr/bin/env python3
"""
Claude API Client (AWS Bedrock Only)

Uses AWS Bedrock exclusively - no Anthropic API key required.
Authentication via AWS IAM (role or access keys).
"""

from .claude_client_bedrock import ClaudeClientBedrock as ClaudeClient

# Export for easy importing
__all__ = ["ClaudeClient"]

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m airs.generator.claude_client <message>")
        print("\nAuthentication:")
        print("  Requires AWS credentials (IAM role or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY)")
        print("  Optional: AWS_REGION (default: us-east-1)")
        sys.exit(1)

    try:
        client = ClaudeClient()
        print(f"✓ Using AWS Bedrock")
        print(f"  Model: {client.model}")
        print(f"  Region: {client.region_name}\n")

        response = client.send_message(sys.argv[1])
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
