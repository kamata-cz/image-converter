#!/bin/bash
# Run all quality checks for AIRS

set -e

echo "🔍 Running Quality Checks..."
echo ""

# Linting
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Linting (ruff)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if ruff check src/ tests/; then
    echo "✅ Linting passed"
else
    echo "❌ Linting failed"
    exit 1
fi

echo ""

# Formatting
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Formatting (black)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if black --check src/ tests/; then
    echo "✅ Formatting passed"
else
    echo "❌ Formatting failed"
    echo "Run: black src/ tests/"
    exit 1
fi

echo ""

# Type checking
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Type Checking (mypy)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if mypy src/; then
    echo "✅ Type checking passed"
else
    echo "⚠️  Type checking has warnings (non-blocking)"
fi

echo ""

# Security scanning
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Security Scanning (bandit)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if bandit -r src/ -f screen; then
    echo "✅ Security scan passed"
else
    echo "❌ Security issues found"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All quality checks passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
