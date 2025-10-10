# AWS Bedrock IAM セットアップガイド

## 問題

現在のエラー:
```
AWS Bedrock access denied: You don't have access to the model with the specified model ID.
```

**原因**: IAM ユーザー `kamata` に `bedrock:InvokeModel` 権限が付与されていない

## 解決方法

### オプション1: AWS Console で手動設定（推奨）

#### 1. IAM ポリシーの作成

1. **AWS Console にログイン**
   - https://console.aws.amazon.com/

2. **IAM サービスに移動**
   - 検索バーで "IAM" を検索
   - "IAM" をクリック

3. **ポリシーを作成**
   - 左メニュー → "Policies"
   - "Create policy" をクリック
   - "JSON" タブをクリック
   - 以下のJSONを貼り付け:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvokeModel",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
        "arn:aws:bedrock:us-east-1:160736647928:inference-profile/*"
      ]
    }
  ]
}
```

4. **ポリシーの保存**
   - "Next" → "Next"
   - Policy name: `BedrockInvokeModelPolicy`
   - Description: `Allow invoking AWS Bedrock models for AIRS`
   - "Create policy" をクリック

#### 2. ポリシーをユーザーにアタッチ

1. **ユーザーページに移動**
   - 左メニュー → "Users"
   - ユーザー `kamata` をクリック

2. **ポリシーをアタッチ**
   - "Permissions" タブ
   - "Add permissions" → "Attach policies directly"
   - 検索ボックスで "BedrockInvokeModelPolicy" を検索
   - チェックボックスをオンにする
   - "Next" → "Add permissions" をクリック

#### 3. 確認

ターミナルで以下を実行して確認:

```bash
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter
source venv/bin/activate
python -m airs.generator.claude_client "こんにちは"
```

成功すれば、Claudeからの応答が返ってきます。

---

### オプション2: 管理者権限があるAWSアカウントを使用

管理者用のAWSプロファイルがある場合:

```bash
# 管理者プロファイルに切り替え
export AWS_PROFILE=admin  # または管理者プロファイル名

# ポリシーを作成
aws iam create-policy \
  --policy-name BedrockInvokeModelPolicy \
  --policy-document file://docs/templates/bedrock-policy.json \
  --description "Allow invoking AWS Bedrock models for AIRS"

# ポリシーARNを取得（出力から確認）
POLICY_ARN="arn:aws:iam::160736647928:policy/BedrockInvokeModelPolicy"

# ユーザーにポリシーをアタッチ
aws iam attach-user-policy \
  --user-name kamata \
  --policy-arn $POLICY_ARN

# 元のプロファイルに戻す
export AWS_PROFILE=default
```

---

## 次のステップ

ポリシーが適用されたら:

### 1. ローカルテスト

```bash
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter
source venv/bin/activate
python -m airs.generator.claude_client "こんにちは、テストです"
```

### 2. GitHub Secrets を設定

```bash
# リポジトリに移動
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter

# GitHub Secrets を設定
gh secret set AWS_REGION --body "us-east-1"
gh secret set AWS_ACCESS_KEY_ID --body "$(aws configure get aws_access_key_id)"
gh secret set AWS_SECRET_ACCESS_KEY --body "$(aws configure get aws_secret_access_key)"

# 確認
gh secret list
```

### 3. Issue でエンドツーエンドテスト

```bash
# テスト用Issueを作成（または既存のIssue #1を使用）
gh issue create \
  --title "[AI] Test: Add loading spinner" \
  --label "ai-resolvable" \
  --body "Add a loading spinner component during image conversion.

## 期待する動作
- User uploads image
- Loading spinner appears
- Conversion completes
- Result is displayed

## 受入基準
- [ ] Loading spinner component created
- [ ] Shows during conversion
- [ ] Hides when complete"

# Workflowの実行を確認
gh run list --workflow=issue-handler.yml --limit 5
```

---

## トラブルシューティング

### エラー: "Model access denied"

**解決方法**:
1. AWS Console → Bedrock → Model access
2. "Manage model access" をクリック
3. "Anthropic Claude 3.5 Sonnet v2" を有効化
4. "Save changes"

### エラー: "ValidationException"

モデルIDを確認:
```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId, 'claude')]"
```

### 確認コマンド

```bash
# ユーザー情報
aws sts get-caller-identity

# アタッチされたポリシー（管理者権限が必要）
aws iam list-attached-user-policies --user-name kamata

# モデルの可用性
aws bedrock get-foundation-model-availability \
  --region us-east-1 \
  --model-id "anthropic.claude-3-5-sonnet-20241022-v2:0"
```

---

## 参考

- **IAM Policy**: `docs/templates/bedrock-policy.json`
- **README**: セットアップガイド全体
- **BEDROCK_SETUP.md**: Bedrock 詳細ガイド
- **Issue #1**: https://github.com/kamata-cz/image-converter/issues/1
