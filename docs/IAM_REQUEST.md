# AWS IAM ポリシー追加依頼

**依頼日**: 2025-10-10
**依頼者**: kamata (IAM User: `arn:aws:iam::160736647928:user/kamata`)
**目的**: AI-Driven Issue Resolution System (AIRS) の動作に必要なAWS Bedrock API アクセス権限の付与

---

## 📋 依頼内容

IAM ユーザー `kamata` に対して、AWS Bedrock の Claude モデルを呼び出すための権限を付与してください。

### 実施していただきたい作業

#### 1. IAM ポリシーの作成

**ポリシー名**: `BedrockInvokeModelPolicy`

**ポリシーJSON**:
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

**CLI コマンド** (オプション):
```bash
aws iam create-policy \
  --policy-name BedrockInvokeModelPolicy \
  --policy-document file://docs/templates/bedrock-policy.json \
  --description "Allow invoking AWS Bedrock Claude models for AIRS"
```

#### 2. IAM ユーザーへのポリシーのアタッチ

**対象ユーザー**: `kamata`
**ポリシーARN**: `arn:aws:iam::160736647928:policy/BedrockInvokeModelPolicy`

**CLI コマンド** (オプション):
```bash
aws iam attach-user-policy \
  --user-name kamata \
  --policy-arn arn:aws:iam::160736647928:policy/BedrockInvokeModelPolicy
```

---

## 🎯 目的と背景

### プロジェクト概要

**プロジェクト名**: Image Converter + AIRS (AI-Driven Issue Resolution System)
**リポジトリ**: https://github.com/kamata-cz/image-converter

AIRSは、GitHub Issueを自動的に解決するシステムです。AWS Bedrock経由でClaude 3.5 Sonnetを使用し、以下を自動化します:

1. Issue の分析と実現可能性判断
2. TypeScript/React コードの自動生成
3. Pull Request の自動作成
4. コードレビューと品質チェック
5. レビューフィードバックへの対応（最大3回の反復修正）

### なぜAWS Bedrockを使用するのか

- **セキュリティ**: Anthropic API キーを管理する必要がない
- **IAM統合**: AWS IAM ロールとポリシーで権限管理が可能
- **監査**: CloudTrail でAPIコールを追跡可能
- **コスト**: 使用量ベースの課金で無駄がない

---

## 🔒 セキュリティ考慮事項

### 権限の範囲

このポリシーは、以下のリソースに対してのみアクセスを許可します:

1. **Anthropic Claude モデル** (`anthropic.claude-*`)
   - Claude 3 Haiku, Sonnet, Opus
   - Claude 3.5 Sonnet, Haiku
   - 将来リリースされる Claude モデル

2. **Inference Profiles** (us-east-1 リージョンのみ)
   - モデル呼び出しに必要
   - アカウント固有: `160736647928`

### 制約事項

- ✅ モデル呼び出し（`InvokeModel`, `InvokeModelWithResponseStream`）のみ
- ❌ モデルの作成・削除は不可
- ❌ カスタムモデルのトレーニングは不可
- ❌ 他のAWSリソースへのアクセスは不可

### 監査とコスト管理

```bash
# API呼び出しの監査 (CloudTrail)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=InvokeModel \
  --max-results 50

# Bedrock使用状況の確認
aws bedrock list-model-invocation-jobs --region us-east-1
```

---

## 💰 コスト見積もり

### AWS Bedrock 料金 (Claude 3.5 Sonnet)

- **Input**: $3.00 / 1M tokens
- **Output**: $15.00 / 1M tokens

### 想定使用量

| Issue 複雑度 | トークン数 (入力/出力) | コスト/Issue |
|-------------|---------------------|-------------|
| Simple      | 50K / 10K          | $0.30       |
| Medium      | 200K / 50K         | $1.35       |
| Complex     | 500K / 100K        | $3.00       |

**月間見積もり** (10 Issues/月):
- Simple (5件): $1.50
- Medium (3件): $4.05
- Complex (2件): $6.00
- **合計**: 約 $11.55/月

### コスト管理

```bash
# 予算アラートの設定（オプション）
aws budgets create-budget \
  --account-id 160736647928 \
  --budget file://bedrock-budget.json
```

---

## 🧪 テスト方法

### 管理者側での確認

ポリシーを適用した後、以下で確認可能です:

```bash
# ポリシーが作成されたか確認
aws iam get-policy --policy-arn arn:aws:iam::160736647928:policy/BedrockInvokeModelPolicy

# ユーザーにアタッチされたか確認
aws iam list-attached-user-policies --user-name kamata

# ポリシーの内容確認
aws iam get-policy-version \
  --policy-arn arn:aws:iam::160736647928:policy/BedrockInvokeModelPolicy \
  --version-id v1
```

### ユーザー側での確認

権限が付与された後、以下でテストします:

```bash
# モデルの可用性確認
aws bedrock get-foundation-model-availability \
  --region us-east-1 \
  --model-id "anthropic.claude-3-5-sonnet-20241022-v2:0"

# AIRSのテスト実行
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter
python -m airs.generator.claude_client "Hello, test message"
```

成功すると、Claudeからの応答が返ってきます。

---

## 📚 参考ドキュメント

プロジェクト内のドキュメント:
- `docs/BEDROCK_IAM_SETUP.md` - 詳細なIAMセットアップガイド
- `docs/templates/bedrock-policy.json` - ポリシーのテンプレートファイル
- `docs/QUICKSTART_IAM.md` - クイックスタートガイド
- `README.md` - プロジェクト全体のドキュメント

AWS公式ドキュメント:
- [AWS Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [IAM Policies for Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_service-with-iam.html)

---

## 📞 連絡先

**依頼者**: kamata
**Email**: [your-email@example.com]
**GitHub**: https://github.com/kamata-cz

質問や確認事項がありましたら、お気軽にご連絡ください。

---

## ✅ チェックリスト（管理者用）

作業完了時にチェックしてください:

- [ ] IAM ポリシー `BedrockInvokeModelPolicy` を作成
- [ ] ポリシーをユーザー `kamata` にアタッチ
- [ ] ポリシーの内容が正しいことを確認
- [ ] ユーザーに作業完了を通知
- [ ] (オプション) 予算アラートを設定

---

**ご対応いただき、ありがとうございます。**
