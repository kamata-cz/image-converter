#!/usr/bin/env python3
"""
Claude API Client (AWS Bedrock Version)

Handles communication with Claude via AWS Bedrock instead of Anthropic API.
No Claude API key required - uses AWS IAM authentication.
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("Warning: boto3 not installed. Run: pip install boto3")
    boto3 = None


@dataclass
class Message:
    """Represents a message in conversation."""

    role: str  # "user" or "assistant"
    content: str


class ClaudeClientBedrock:
    """Client for interacting with Claude via AWS Bedrock."""

    # Bedrock inference profile IDs (required for on-demand throughput)
    # Format: us.anthropic.claude-3-5-sonnet-20241022-v2:0
    # NOT: anthropic.claude-3-5-sonnet-20241022-v2:0 (foundation model ID)
    DEFAULT_MODEL = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    DEFAULT_MAX_TOKENS = 8000
    DEFAULT_TEMPERATURE = 0.7

    def __init__(
        self,
        region_name: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        """
        Initialize Claude client with AWS Bedrock.

        Args:
            region_name: AWS region (defaults to AWS_REGION env var or us-east-1)
            model: Model ID (defaults to claude-3-5-sonnet on Bedrock)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0 to 1.0)
            aws_access_key_id: AWS access key (optional, can use IAM role)
            aws_secret_access_key: AWS secret key (optional, can use IAM role)
        """
        if boto3 is None:
            raise RuntimeError("boto3 not installed. Run: pip install boto3")

        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Initialize Bedrock Runtime client
        session_kwargs = {"region_name": self.region_name}

        # Use explicit credentials if provided
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key
        # Otherwise boto3 will use default credential chain:
        # - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        # - AWS credentials file (~/.aws/credentials)
        # - IAM role (if running on EC2, ECS, Lambda, GitHub Actions OIDC, etc.)

        try:
            self.client = boto3.client("bedrock-runtime", **session_kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Bedrock client: {e}. "
                "Ensure AWS credentials are configured (IAM role, env vars, or ~/.aws/credentials)"
            )

        self.conversation_history: List[Message] = []

    def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        reset_conversation: bool = False,
    ) -> str:
        """
        Send a message to Claude via Bedrock and get response.

        Args:
            message: User message to send
            system_prompt: Optional system prompt
            reset_conversation: If True, start fresh conversation

        Returns:
            Claude's response text
        """
        if reset_conversation:
            self.conversation_history = []

        # Add user message to history
        self.conversation_history.append(Message(role="user", content=message))

        # Prepare messages for Bedrock API (uses same format as Anthropic API)
        messages = [{"role": msg.role, "content": msg.content} for msg in self.conversation_history]

        # Build request body for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": messages,
        }

        if system_prompt:
            request_body["system"] = system_prompt

        try:
            # Call Bedrock API
            response = self.client.invoke_model(
                modelId=self.model,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body),
            )

            # Parse response
            response_body = json.loads(response["body"].read())

            # Extract response text
            response_text = response_body["content"][0]["text"]

            # Add assistant response to history
            self.conversation_history.append(Message(role="assistant", content=response_text))

            return response_text

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_msg = e.response.get("Error", {}).get("Message", str(e))

            if error_code == "AccessDeniedException":
                raise RuntimeError(
                    f"AWS Bedrock access denied: {error_msg}. "
                    "Ensure your IAM user/role has 'bedrock:InvokeModel' permission."
                )
            elif error_code == "ValidationException":
                raise RuntimeError(f"Bedrock validation error: {error_msg}")
            elif error_code == "ThrottlingException":
                raise RuntimeError(f"Bedrock rate limit exceeded: {error_msg}")
            else:
                raise RuntimeError(f"Bedrock API error ({error_code}): {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error calling Bedrock: {e}")

    def generate_code(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        language: str = "python",
    ) -> str:
        """
        Generate code based on prompt and context.

        Args:
            prompt: Description of what to generate
            context: Additional context (existing code, file structure, etc.)
            language: Programming language

        Returns:
            Generated code
        """
        system_prompt = self._build_code_generation_system_prompt(language, context)
        full_prompt = self._build_code_generation_prompt(prompt, context)
        return self.send_message(full_prompt, system_prompt=system_prompt, reset_conversation=True)

    def generate_tests(
        self,
        code: str,
        test_framework: str = "pytest",
        language: str = "python",
    ) -> str:
        """
        Generate tests for provided code.

        Args:
            code: Code to generate tests for
            test_framework: Test framework to use
            language: Programming language

        Returns:
            Generated test code
        """
        system_prompt = self._build_test_generation_system_prompt(test_framework, language)

        prompt = f"""Generate comprehensive tests for the following code:

```{language}
{code}
```

Requirements:
- Use {test_framework} testing framework
- Include unit tests for all functions/methods
- Test edge cases and error conditions
- Follow {language} testing best practices
- Include clear test names and docstrings
"""

        return self.send_message(prompt, system_prompt=system_prompt, reset_conversation=True)

    def review_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Review code and provide suggestions.

        Args:
            code: Code to review
            language: Programming language

        Returns:
            Dictionary with review results
        """
        system_prompt = """You are an expert code reviewer. Review code for:
- Code quality and readability
- Potential bugs
- Security issues
- Performance concerns
- Best practices

Provide structured feedback in JSON format:
{
  "overall_quality": "good|fair|poor",
  "issues": [
    {
      "severity": "critical|warning|info",
      "type": "bug|security|performance|style",
      "description": "...",
      "suggestion": "..."
    }
  ],
  "positive_aspects": ["..."],
  "summary": "..."
}
"""

        prompt = f"""Review the following {language} code:

```{language}
{code}
```
"""

        response = self.send_message(prompt, system_prompt=system_prompt, reset_conversation=True)

        # Try to parse JSON response
        try:
            # Extract JSON from response (might be wrapped in markdown)
            json_match = response
            if "```json" in response:
                json_match = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_match = response.split("```")[1].split("```")[0].strip()

            return json.loads(json_match)
        except:
            # If parsing fails, return raw response
            return {"raw_response": response}

    def _build_code_generation_system_prompt(self, language: str, context: Optional[Dict[str, Any]]) -> str:
        """Build system prompt for code generation."""
        base_prompt = f"""You are an expert {language} developer. Generate high-quality, production-ready code that:
- Follows {language} best practices and conventions
- Is well-documented with clear comments and docstrings
- Handles errors appropriately
- Is testable and maintainable
- Uses type hints/annotations where applicable

Provide ONLY the code in your response, wrapped in ```{language} code blocks.
Do not include explanations outside the code block unless specifically asked.
"""

        if context and context.get("coding_style"):
            style = context["coding_style"]
            if style.get("formatter"):
                base_prompt += f"\n- Code is formatted using {style['formatter']}"
            if style.get("linter"):
                base_prompt += f"\n- Code follows {style['linter']} guidelines"

        return base_prompt

    def _build_code_generation_prompt(self, prompt: str, context: Optional[Dict[str, Any]]) -> str:
        """Build complete prompt for code generation."""
        full_prompt = prompt

        if context:
            if context.get("related_files"):
                full_prompt += "\n\n### Related Files for Context:\n"
                for file in context["related_files"][:3]:  # Limit to 3 files
                    full_prompt += f"\n**{file['path']}**:\n"
                    if file.get("content"):
                        full_prompt += f"```\n{file['content'][:2000]}\n```\n"  # Limit content length

            if context.get("implementation_steps"):
                full_prompt += "\n\n### Implementation Steps:\n"
                for i, step in enumerate(context["implementation_steps"], 1):
                    full_prompt += f"{i}. {step}\n"

        return full_prompt

    def _build_test_generation_system_prompt(self, test_framework: str, language: str) -> str:
        """Build system prompt for test generation."""
        return f"""You are an expert {language} test engineer. Generate comprehensive tests using {test_framework} that:
- Cover all functions/methods
- Test edge cases and error conditions
- Use clear, descriptive test names
- Include appropriate fixtures and mocks
- Follow {test_framework} best practices

Provide ONLY the test code in your response, wrapped in ```{language} code blocks.
"""

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Note: This is a rough estimation.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Rough estimation: ~4 characters per token
        return len(text) // 4

    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return [{"role": msg.role, "content": msg.content} for msg in self.conversation_history]


# Alias for backward compatibility - can be imported as ClaudeClient
ClaudeClient = ClaudeClientBedrock


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python claude_client_bedrock.py <message>")
        print("\nEnvironment variables:")
        print("  AWS_REGION (default: us-east-1)")
        print("  AWS_ACCESS_KEY_ID (optional if using IAM role)")
        print("  AWS_SECRET_ACCESS_KEY (optional if using IAM role)")
        sys.exit(1)

    try:
        client = ClaudeClientBedrock()
        print(f"Using model: {client.model}")
        print(f"Region: {client.region_name}")
        print("\nSending message...\n")

        response = client.send_message(sys.argv[1])
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
