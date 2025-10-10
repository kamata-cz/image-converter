# Image Converter + AIRS (AI-Driven Issue Resolution System)

A browser-based image conversion tool with AI-powered automatic issue resolution via AWS Bedrock.

---

## 🎯 Features

### Image Converter
- **Format Conversion**: Convert between PNG, JPEG, WebP, and AVIF
- **Image Resize**: Resize images with aspect ratio control
- **Quality Control**: Adjust compression quality
- **EXIF Orientation**: Automatic handling of image orientation
- **Batch Processing**: Process multiple images at once
- **Local Processing**: All processing happens in the browser - no uploads required
- **Settings Persistence**: Your settings are saved locally

### AIRS (AI-Driven Issue Resolution System)
- **🤖 Automatic Issue Resolution**: AI analyzes and implements fixes for GitHub Issues
- **🔒 AWS Bedrock**: Uses AWS IAM authentication (no API key management)
- **✅ Quality Checks**: Automated linting, type checking, and build verification
- **🔄 Iterative Fixes**: AI can address review feedback (up to 3 iterations)
- **👨‍💻 Human Approval**: Final approval required before merge
- **🛡️ Guardrails**: Path restrictions, size limits, secret detection

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- **For AIRS**: AWS credentials with Bedrock access

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Linting & Formatting

```bash
npm run lint
npm run format
```

---

## 🤖 AIRS Setup (AI Issue Resolution)

### 1. AWS Bedrock Setup

**Enable Bedrock Model Access:**

1. Go to AWS Console → Bedrock → Model access
2. Enable "Anthropic Claude 3.5 Sonnet"

**Create IAM Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["bedrock:InvokeModel"],
    "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
  }]
}
```

### 2. Local Development

```bash
# Configure AWS CLI
aws configure
# Access Key: AKIA...
# Secret Key: ...
# Region: us-east-1

# Test AIRS
python -m airs.generator.claude_client "Hello, test message"
```

### 3. GitHub Actions Setup

**Option A: IAM Role (Recommended - Keyless)**

```bash
# Create IAM role for GitHub Actions OIDC
aws iam create-role \
  --role-name GitHubActionsAIRSRole \
  --assume-role-policy-document file://trust-policy.json

# Attach Bedrock policy
aws iam attach-role-policy \
  --role-name GitHubActionsAIRSRole \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/BedrockInvokeModelPolicy
```

**Option B: Access Keys (Simple)**

```bash
# Set GitHub Secrets
gh secret set AWS_REGION --body "us-east-1"
gh secret set AWS_ACCESS_KEY_ID --body "AKIA..."
gh secret set AWS_SECRET_ACCESS_KEY --body "..."
```

### 4. Create Labels

```bash
gh label create "ai-resolvable" --color "1d76db"
gh label create "ai-generated" --color "d4c5f9"
gh label create "needs-review" --color "d93f0b"
gh label create "ai-reviewed" --color "0075ca"
```

### 5. Create Test Issue

```bash
gh issue create \
  --title "[AI] Test: Add loading indicator" \
  --label "ai-resolvable" \
  --body "Add loading spinner during image conversion..."
```

**AIRS will automatically:**
1. Analyze the issue
2. Generate code (TypeScript/React)
3. Create a PR
4. Run quality checks
5. Wait for your approval

---

## 📖 Usage

### Image Converter

1. **Upload Images**: Drag and drop images or click to select files
2. **Configure Settings**:
   - Choose output format (PNG, JPEG, WebP, AVIF)
   - Adjust quality slider
   - Set resize dimensions (optional)
   - Select resize mode
3. **Convert**: Click the convert button to process and download images

### AIRS (AI Issue Resolution)

**Create AI-Resolvable Issue:**

```markdown
## 問題の説明
[Specific problem description]

## 期待する動作
[Expected behavior]

## 再現手順
1. Step 1
2. Step 2

## 受入基準
- [ ] Criterion 1
- [ ] Criterion 2

## AIへの指示
[Specific instructions for AI]
```

Add label: `ai-resolvable`

**AI will:**
- Analyze feasibility (30 seconds)
- Generate code (1-5 minutes)
- Create draft PR
- Run quality checks (ESLint, TypeScript, Build)
- Request your review

**You:**
- Review the PR
- Request changes (AI will fix, max 3 iterations)
- Approve and merge

---

## 🛡️ AIRS Guardrails

### Path Restrictions
- ✅ Allowed: `src/`, `tests/`, `docs/`
- ❌ Blocked: `.github/workflows/`, `*.pem`, `.env`

### Size Limits
- Max 10 files per PR
- Max 500 lines per file
- Max 2000 total lines

### Security
- Secret detection (AWS keys, API keys, passwords)
- Dangerous operation blocking (`eval()`, `os.system()`, `DROP TABLE`)

---

## 💰 Costs

### AWS Bedrock (Claude 3.5 Sonnet)
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

**Estimated costs per issue:**
- Simple: ~$0.01-0.05
- Medium: ~$0.05-0.20
- Complex: ~$0.20-0.50

---

## 📚 Documentation

- **[BEDROCK_IAM_SETUP.md](docs/BEDROCK_IAM_SETUP.md)** - IAM権限設定ガイド（必須）
- **[BEDROCK_SETUP.md](docs/BEDROCK_SETUP.md)** - Complete AWS Bedrock setup guide
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Full AIRS deployment guide (if exists)
- **[TEAM_GUIDE.md](docs/TEAM_GUIDE.md)** - Team usage guide (if exists)

---

## 🔧 Technology Stack

### Image Converter
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS 4** - Styling
- **Canvas API** - Image processing
- **createImageBitmap** - High-performance image decoding

### AIRS
- **Python 3.11** - Core logic
- **AWS Bedrock** - Claude 3.5 Sonnet via AWS
- **boto3** - AWS SDK
- **PyGithub** - GitHub API integration
- **GitHub Actions** - Workflow automation

---

## 🌐 Browser Support

- Chrome 110+
- Firefox 116+
- Safari 16.4+
- Edge 110+

---

## 🔒 Privacy & Security

### Image Converter
All image processing is done locally in your browser. No images are uploaded to any server.

### AIRS
- All operations logged and auditable
- Human approval required for all merges
- Guardrails prevent dangerous operations
- AWS IAM for secure authentication

---

## 📄 License

MIT

---

## 🆘 Troubleshooting

### AIRS: "AccessDeniedException"

**Solution:**
1. Check IAM policy has `bedrock:InvokeModel` permission
2. Verify Bedrock Model Access is enabled for Claude 3.5
3. Ensure AWS credentials are configured

### AIRS: Workflow not running

**Solution:**
```bash
# Check GitHub Actions permissions
# Settings → Actions → General → Workflow permissions
# Select "Read and write permissions"

# Verify labels exist
gh label list | grep ai-resolvable
```

---

**🤖 Built with AI-Driven Issue Resolution System powered by AWS Bedrock**
