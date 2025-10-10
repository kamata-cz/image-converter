# AWS Bedrock セットアップガイド

**Claude APIキー不要でAIRSを利用する方法**

---

## 🎯 AWS Bedrockを使うメリット

| 項目 | Anthropic API | AWS Bedrock |
|------|--------------|-------------|
| **認証** | Claude APIキー必要 | AWS IAM認証 |
| **APIキー管理** | 必要 | **不要** |
| **請求** | Anthropic直接 | AWS請求に統合 |
| **GitHub Actions** | Secret管理必要 | **OIDC認証可能**（キーレス） |
| **既存AWS環境** | 別途管理 | **シームレス統合** |

### こんな場合におすすめ
- ✅ すでにAWSを使っている
- ✅ Claude APIキーを発行したくない
- ✅ AWSのIAMで権限管理したい
- ✅ AWS Cost Explorerでコスト管理したい
- ✅ GitHub ActionsでOIDC認証を使いたい

---

## 📋 前提条件

### 1. AWS Bedrockへのアクセス権限

AWS Bedrockでは、Claude 3.5モデルを使用するため、事前にモデルアクセスを有効化する必要があります。

```bash
# AWS Console → Bedrock → Model access
# "Anthropic Claude 3.5 Sonnet" を有効化
```

または、AWS CLIで：

```bash
aws bedrock list-foundation-models --region us-east-1 | grep "anthropic.claude-3-5"
```

### 2. IAMポリシー

以下の権限が必要です：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    }
  ]
}
```

---

## 🚀 セットアップ手順

### オプション A: ローカル開発（AWS Credentials）

**1. AWS認証情報を設定**

```bash
# Option 1: AWS CLI設定（推奨）
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: us-east-1

# Option 2: 環境変数
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1
```

**2. AIRS設定を更新**

```.env
# Enable Bedrock
USE_BEDROCK=true

# AWS設定
AWS_REGION=us-east-1

# 以下は不要（aws configureで設定済み）
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
```

**3. テスト**

```bash
# Claude clientのテスト
cd /path/to/image-converter
USE_BEDROCK=true python -m airs.generator.claude_client "Hello, test message"

# 期待される出力:
# ✓ Using AWS Bedrock for Claude API (no API key required)
# Using model: anthropic.claude-3-5-sonnet-20241022-v2:0
# Region: us-east-1
# ...
# Hello! How can I assist you today?
```

---

### オプション B: GitHub Actions（IAM Role推奨）

#### B-1: IAM Roleを使用（キーレス、推奨）

**1. AWS IAM Roleを作成**

```bash
# Trust policy for GitHub Actions OIDC
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:kamata-cz/image-converter:*"
        }
      }
    }
  ]
}
EOF

# Create IAM role
aws iam create-role \
  --role-name GitHubActionsAIRSRole \
  --assume-role-policy-document file://trust-policy.json

# Attach Bedrock policy
aws iam attach-role-policy \
  --role-name GitHubActionsAIRSRole \
  --policy-arn arn:aws:iam::YOUR_AWS_ACCOUNT_ID:policy/BedrockInvokeModelPolicy
```

**2. ワークフローを更新**

```.github/workflows/issue-handler.yml
jobs:
  analyze-issue:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
      contents: read

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/GitHubActionsAIRSRole
          aws-region: us-east-1

      - name: Analyze Issue
        env:
          USE_BEDROCK: true
          AWS_REGION: us-east-1
        run: |
          python -m airs.analyzer.issue_parser ...
```

#### B-2: Access Keysを使用（簡易）

**1. GitHub Secretsを設定**

```bash
# GitHub CLI
gh secret set USE_BEDROCK --body "true"
gh secret set AWS_REGION --body "us-east-1"
gh secret set AWS_ACCESS_KEY_ID --body "AKIA..."
gh secret set AWS_SECRET_ACCESS_KEY --body "..."

# または、GitHub Web UI:
# https://github.com/kamata-cz/image-converter/settings/secrets/actions
```

**2. ワークフローの環境変数**

各`env:`セクションに以下を追加：

```yaml
env:
  USE_BEDROCK: ${{ secrets.USE_BEDROCK }}
  AWS_REGION: ${{ secrets.AWS_REGION }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 🔧 トラブルシューティング

### エラー: "AccessDeniedException"

```
AWS Bedrock access denied. Ensure your IAM user/role has 'bedrock:InvokeModel' permission.
```

**解決策:**
1. IAMポリシーを確認
2. Bedrock Model Accessが有効か確認（AWS Console → Bedrock → Model access）

### エラー: "ValidationException: The provided model identifier is invalid"

```
Bedrock validation error: The provided model identifier is invalid
```

**解決策:**
モデルIDを確認：

```bash
# 利用可能なモデルを確認
aws bedrock list-foundation-models --region us-east-1 \
  --by-provider anthropic \
  --query "modelSummaries[?contains(modelId, 'claude-3-5')].[modelId,modelName]" \
  --output table
```

正しいモデルID: `anthropic.claude-3-5-sonnet-20241022-v2:0`

### エラー: "Model access not granted"

```
You don't have access to the model with the specified model ID.
```

**解決策:**
AWS Console → Bedrock → Model access → "Anthropic Claude 3.5 Sonnet"を有効化

---

## 💰 コスト比較

### Anthropic API
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

### AWS Bedrock (Claude 3.5 Sonnet)
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

**同じ価格**ですが、Bedrockの利点：
- AWS請求に統合
- AWS Cost Explorerでコスト分析
- AWS Budgets/Alertsでコスト管理

---

## 📊 動作確認

### 1. Pythonスクリプトでテスト

```python
# test_bedrock.py
from airs.generator.claude_client import ClaudeClient
import os

os.environ['USE_BEDROCK'] = 'true'
os.environ['AWS_REGION'] = 'us-east-1'

client = ClaudeClient()
response = client.send_message("Hello, Bedrock!")
print(response)
```

```bash
python test_bedrock.py
# ✓ Using AWS Bedrock for Claude API (no API key required)
# Hello! How can I assist you today?
```

### 2. GitHub Actions テスト

Issue #1にコメントして動作確認：

```bash
gh issue comment 1 --body "Testing AWS Bedrock integration"
```

GitHub Actions → Workflowログで以下を確認：
```
✓ Using AWS Bedrock for Claude API (no API key required)
Using model: anthropic.claude-3-5-sonnet-20241022-v2:0
Region: us-east-1
```

---

## 🔄 Anthropic APIに戻す方法

```bash
# .envまたは環境変数
USE_BEDROCK=false
CLAUDE_API_KEY=sk-ant-...

# GitHub Secrets
gh secret set USE_BEDROCK --body "false"
gh secret set CLAUDE_API_KEY --body "sk-ant-..."
```

---

## 📚 参考リンク

- [AWS Bedrock - Claude Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [GitHub Actions - OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

---

**🎉 これでClaude APIキーなしでAIRSが動作します！**
