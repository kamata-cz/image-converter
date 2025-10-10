#!/bin/bash
# Check if AIRS setup is complete

set -e

echo "🔍 Checking AIRS Setup..."
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Python: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Check virtual environment
echo "✓ Checking virtual environment..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "  Virtual environment: Active ($VIRTUAL_ENV)"
else
    echo "⚠️  Virtual environment: Not active (recommended to activate)"
fi

# Check required packages
echo "✓ Checking required packages..."
required_packages=("anthropic" "github" "pytest" "ruff" "black" "mypy")
missing_packages=()

for package in "${required_packages[@]}"; do
    if python -c "import $package" 2>/dev/null; then
        echo "  ✓ $package"
    else
        echo "  ❌ $package (missing)"
        missing_packages+=("$package")
    fi
done

# Check environment variables
echo "✓ Checking environment variables..."
if [[ -f .env ]]; then
    echo "  ✓ .env file exists"

    if grep -q "GITHUB_TOKEN=" .env && ! grep -q "GITHUB_TOKEN=your" .env; then
        echo "  ✓ GITHUB_TOKEN configured"
    else
        echo "  ❌ GITHUB_TOKEN not configured"
    fi

    if grep -q "CLAUDE_API_KEY=" .env && ! grep -q "CLAUDE_API_KEY=your" .env; then
        echo "  ✓ CLAUDE_API_KEY configured"
    else
        echo "  ❌ CLAUDE_API_KEY not configured"
    fi
else
    echo "  ❌ .env file not found (copy from .env.example)"
fi

# Check directory structure
echo "✓ Checking directory structure..."
required_dirs=("src/analyzer" "src/generator" "src/orchestrator" "src/guardrails" "src/rules" "src/metrics" "tests" ".github/workflows")
for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "  ✓ $dir"
    else
        echo "  ❌ $dir (missing)"
    fi
done

# Check workflows
echo "✓ Checking GitHub Actions workflows..."
required_workflows=("issue-handler.yml" "pr-review.yml" "iterative-fix.yml" "merge-gate.yml")
for workflow in "${required_workflows[@]}"; do
    if [[ -f ".github/workflows/$workflow" ]]; then
        echo "  ✓ $workflow"
    else
        echo "  ❌ $workflow (missing)"
    fi
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ ${#missing_packages[@]} -eq 0 ]] && [[ -f .env ]]; then
    echo "✅ Setup complete! You're ready to go."
    echo ""
    echo "Next steps:"
    echo "  1. Ensure GitHub secrets are configured:"
    echo "     gh secret set GITHUB_TOKEN"
    echo "     gh secret set CLAUDE_API_KEY"
    echo "  2. Create an issue with 'ai-resolvable' label"
    echo "  3. Watch the automation run!"
else
    echo "⚠️  Setup incomplete. Please address the issues above."
    echo ""
    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        echo "Install missing packages:"
        echo "  pip install -r requirements.txt"
    fi
    if [[ ! -f .env ]]; then
        echo "Create .env file:"
        echo "  cp .env.example .env"
        echo "  # Edit .env with your credentials"
    fi
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
