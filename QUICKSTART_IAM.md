# 🚀 AIRS クイックスタート（IAM設定）

## 現在の状況

✅ **完了済み**:
- Bedrock model ID 修正（inference profile 形式に変更）
- コード実装完了（AWS Bedrock 統合）
- ドキュメント作成完了
- AWS CLI 認証設定済み

⏳ **残りの作業**:
- **IAM ポリシーの適用**（これを今やります！）
- ローカルテスト実行
- GitHub Secrets 設定
- エンドツーエンドテスト

---

## 次にやること（5分で完了）

### ステップ1: AWS Console でIAMポリシーを追加

#### 1-1. AWS Console にログイン
https://console.aws.amazon.com/iam/

#### 1-2. ポリシーを作成
1. 左メニュー → **Policies**
2. **Create policy** ボタンをクリック
3. **JSON** タブをクリック
4. 以下をコピー＆ペースト:

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

5. **Next** → **Next**
6. Policy name: `BedrockInvokeModelPolicy`
7. **Create policy** ボタンをクリック

#### 1-3. ユーザーにポリシーをアタッチ
1. 左メニュー → **Users**
2. ユーザー **kamata** をクリック
3. **Permissions** タブ
4. **Add permissions** → **Attach policies directly**
5. 検索ボックスで `BedrockInvokeModelPolicy` を検索
6. チェックボックスをオンにする
7. **Next** → **Add permissions** をクリック

### ステップ2: ローカルテスト（1分）

ターミナルで以下を実行:

```bash
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter
source venv/bin/activate
python -m airs.generator.claude_client "こんにちは"
```

✅ **成功**: Claudeからの応答が返ってくる
❌ **失敗**: エラーが出る場合は `docs/BEDROCK_IAM_SETUP.md` を確認

### ステップ3: GitHub Secrets 設定（1分）

```bash
cd /Users/kamatakeito/Documents/credorz-task/00_asobi/image-converter

# AWS認証情報を設定
gh secret set AWS_REGION --body "us-east-1"
gh secret set AWS_ACCESS_KEY_ID --body "$(aws configure get aws_access_key_id)"
gh secret set AWS_SECRET_ACCESS_KEY --body "$(aws configure get aws_secret_access_key)"

# 確認
gh secret list
```

### ステップ4: エンドツーエンドテスト（自動実行）

Issue #1 がトリガーされて、AIが自動的に解決を試みます:
- https://github.com/kamata-cz/image-converter/issues/1

または新しいテストIssueを作成:

```bash
gh issue create \
  --title "[AI] Test: Add dark mode toggle" \
  --label "ai-resolvable" \
  --body "Add a dark mode toggle button to the UI.

## 期待する動作
- Toggle button in header
- Switches between light and dark themes
- Preference is saved to localStorage

## 受入基準
- [ ] Dark mode toggle component created
- [ ] Applies dark mode CSS
- [ ] Persists user preference"
```

**AIが自動的に**:
1. Issue を分析（30秒）
2. コード生成（1-5分）
3. PR を作成
4. テスト実行（ESLint, TypeScript, Build）
5. レビュー待ち状態

**あなたがやること**:
- PRをレビュー
- 必要に応じてフィードバック（AIが最大3回まで修正）
- Approve & Merge

---

## トラブルシューティング

### エラー: "AccessDeniedException"
→ ステップ1を再確認してください（IAMポリシーが正しく適用されているか）

### エラー: "Model not found"
→ AWS Console → Bedrock → Model access で "Claude 3.5 Sonnet v2" を有効化

### エラー: GitHub Actions が動かない
→ Settings → Actions → General → "Read and write permissions" を選択

---

## 詳細ドキュメント

- **[BEDROCK_IAM_SETUP.md](docs/BEDROCK_IAM_SETUP.md)** - IAM詳細設定ガイド
- **[BEDROCK_SETUP.md](docs/BEDROCK_SETUP.md)** - Bedrock全体セットアップ
- **[README.md](README.md)** - プロジェクト全体のドキュメント

---

**🎉 セットアップが完了したら、AIに任せてコーヒーを飲みながら待ちましょう！**
