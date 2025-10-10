#!/bin/bash
# Check if AIRS + Image Converter setup is complete

set -e

echo "🔍 Checking Image Converter + AIRS Setup..."
echo ""

# Check Node.js
echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    exit 1
fi
node_version=$(node --version)
echo "  Node.js: $node_version"

# Check npm
echo "✓ Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found"
    exit 1
fi
npm_version=$(npm --version)
echo "  npm: $npm_version"

# Check Python version
echo "✓ Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python: $python_version"

# Check virtual environment
echo "✓ Checking Python virtual environment..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "  Virtual environment: Active ($VIRTUAL_ENV)"
elif [[ -d "venv" ]]; then
    echo "  ⚠️  Virtual environment exists but not active"
    echo "  Activate with: source venv/bin/activate"
else
    echo "  ⚠️  Virtual environment not found"
    echo "  Create with: python3 -m venv venv"
fi

# Check Node modules
echo "✓ Checking Node modules..."
if [[ -d "node_modules" ]]; then
    echo "  ✓ node_modules exists"
else
    echo "  ❌ node_modules not found (run: npm install)"
fi

# Check required Python packages for AIRS
echo "✓ Checking required Python packages..."
required_packages=("boto3" "github" "pydantic" "requests")
missing_packages=()

for package in "${required_packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo "  ✓ $package"
    else
        echo "  ❌ $package (missing)"
        missing_packages+=("$package")
    fi
done

# Check AWS CLI
echo "✓ Checking AWS CLI..."
if command -v aws &> /dev/null; then
    aws_version=$(aws --version 2>&1 | awk '{print $1}')
    echo "  ✓ AWS CLI: $aws_version"

    # Check AWS credentials
    if aws sts get-caller-identity &> /dev/null; then
        echo "  ✓ AWS credentials configured"
    else
        echo "  ⚠️  AWS credentials not configured (run: aws configure)"
    fi
else
    echo "  ⚠️  AWS CLI not found (optional for AIRS)"
fi

# Check environment files
echo "✓ Checking environment files..."
if [[ -f .env.example ]]; then
    echo "  ✓ .env.example exists"
else
    echo "  ❌ .env.example not found"
fi

if [[ -f .env ]]; then
    echo "  ✓ .env file exists"
else
    echo "  ⚠️  .env file not found (copy from .env.example if needed)"
fi

# Check directory structure
echo "✓ Checking directory structure..."
required_dirs=("airs/analyzer" "airs/generator" "airs/orchestrator" "airs/guardrails" "airs/rules" "airs/metrics" "src" "public" "docs" ".github/workflows")
missing_dirs=()
for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "  ✓ $dir"
    else
        echo "  ❌ $dir (missing)"
        missing_dirs+=("$dir")
    fi
done

# Check workflows
echo "✓ Checking GitHub Actions workflows..."
required_workflows=("issue-handler.yml" "pr-review.yml" "iterative-fix.yml" "merge-gate.yml")
missing_workflows=()
for workflow in "${required_workflows[@]}"; do
    if [[ -f ".github/workflows/$workflow" ]]; then
        echo "  ✓ $workflow"
    else
        echo "  ❌ $workflow (missing)"
        missing_workflows+=("$workflow")
    fi
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ ${#missing_packages[@]} -eq 0 ]] && [[ ${#missing_dirs[@]} -eq 0 ]] && [[ ${#missing_workflows[@]} -eq 0 ]] && [[ -d "node_modules" ]]; then
    echo "✅ Setup complete! You're ready to go."
    echo ""
    echo "Next steps:"
    echo ""
    echo "For Image Converter:"
    echo "  npm run dev           # Start development server"
    echo "  npm run build         # Build for production"
    echo ""
    echo "For AIRS:"
    echo "  1. Configure GitHub secrets:"
    echo "     gh secret set AWS_REGION --body 'us-east-1'"
    echo "     gh secret set AWS_ACCESS_KEY_ID --body '<your-key>'"
    echo "     gh secret set AWS_SECRET_ACCESS_KEY --body '<your-secret>'"
    echo ""
    echo "  2. Test Claude client:"
    echo "     source venv/bin/activate"
    echo "     python -m airs.generator.claude_client 'Hello'"
    echo ""
    echo "  3. Create an issue with 'ai-resolvable' label"
    echo "  4. Watch the automation run!"
else
    echo "⚠️  Setup incomplete. Please address the issues above."
    echo ""
    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        echo "Install missing Python packages:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        echo ""
    fi
    if [[ ! -d "node_modules" ]]; then
        echo "Install Node modules:"
        echo "  npm install"
        echo ""
    fi
    if [[ ${#missing_dirs[@]} -gt 0 ]] || [[ ${#missing_workflows[@]} -gt 0 ]]; then
        echo "Missing directories or workflows detected."
        echo "Please ensure you have the complete repository."
    fi
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
