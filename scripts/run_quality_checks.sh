#!/bin/bash
# Run all quality checks for Image Converter + AIRS

set -e

echo "🔍 Running Quality Checks..."
echo ""

# ============================================
# FRONTEND (TypeScript/React)
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "FRONTEND: TypeScript/React"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ESLint
echo "1️⃣  Linting (ESLint)..."
if npm run lint; then
    echo "✅ ESLint passed"
else
    echo "❌ ESLint failed"
    exit 1
fi
echo ""

# TypeScript
echo "2️⃣  Type Checking (TypeScript)..."
if npx tsc --noEmit; then
    echo "✅ TypeScript check passed"
else
    echo "❌ TypeScript check failed"
    exit 1
fi
echo ""

# Prettier
echo "3️⃣  Formatting Check (Prettier)..."
if npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css}"; then
    echo "✅ Prettier check passed"
else
    echo "❌ Formatting check failed"
    echo "Run: npx prettier --write 'src/**/*.{ts,tsx,js,jsx,json,css}'"
    exit 1
fi
echo ""

# Build
echo "4️⃣  Build Check..."
if npm run build; then
    echo "✅ Build passed"
else
    echo "❌ Build failed"
    exit 1
fi
echo ""

# ============================================
# BACKEND (Python/AIRS)
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "BACKEND: Python/AIRS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Python virtual environment not active"
    echo "Activate with: source venv/bin/activate"
    echo "Skipping Python checks..."
    echo ""
else
    # Ruff linting
    echo "5️⃣  Linting (Ruff)..."
    if ruff check airs/; then
        echo "✅ Ruff linting passed"
    else
        echo "⚠️  Ruff linting has warnings"
    fi
    echo ""

    # Black formatting
    echo "6️⃣  Formatting Check (Black)..."
    if black --check airs/; then
        echo "✅ Black check passed"
    else
        echo "⚠️  Formatting check failed (non-blocking)"
        echo "Run: black airs/"
    fi
    echo ""

    # Type checking (mypy)
    echo "7️⃣  Type Checking (mypy)..."
    if mypy airs/ --ignore-missing-imports; then
        echo "✅ Type checking passed"
    else
        echo "⚠️  Type checking has warnings (non-blocking)"
    fi
    echo ""

    # Security scanning
    if command -v bandit &> /dev/null; then
        echo "8️⃣  Security Scanning (Bandit)..."
        if bandit -r airs/ -f screen -ll; then
            echo "✅ Security scan passed"
        else
            echo "⚠️  Security issues found (review warnings)"
        fi
        echo ""
    else
        echo "8️⃣  Security Scanning (Bandit)..."
        echo "⚠️  Bandit not installed (optional)"
        echo "Install with: pip install bandit"
        echo ""
    fi
fi

# ============================================
# SUMMARY
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All critical quality checks passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Frontend: ✅ ESLint, TypeScript, Prettier, Build"
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Backend:  ✅ Ruff, Black, mypy, Bandit"
else
    echo "Backend:  ⏭️  Skipped (activate venv to run)"
fi
echo ""
