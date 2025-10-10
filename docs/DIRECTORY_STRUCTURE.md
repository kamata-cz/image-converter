# ディレクトリ構造

このドキュメントは、Image Converter + AIRS プロジェクトのディレクトリ構造を説明します。

**最終更新**: 2025-10-10

---

## 📁 プロジェクト概要

```
image-converter/
├── .github/              # GitHub 設定・ワークフロー
├── airs/                 # AIRS (AI自動Issue解決システム)
├── docs/                 # プロジェクトドキュメント
├── public/               # 静的ファイル (画像など)
├── scripts/              # セットアップ・ユーティリティスクリプト
├── src/                  # React/TypeScript フロントエンドコード
├── dist/                 # ビルド出力 (gitignore)
├── node_modules/         # npm パッケージ (gitignore)
└── venv/                 # Python 仮想環境 (gitignore)
```

---

## 📂 ディレクトリ詳細

### `.github/` - GitHub 設定

GitHub Actions ワークフローと設定ファイル。

```
.github/
└── workflows/
    ├── issue-handler.yml     # Issue自動解決ワークフロー
    ├── pr-review.yml         # PR自動レビューワークフロー
    ├── iterative-fix.yml     # レビューフィードバック対応
    └── merge-gate.yml        # マージゲート (承認確認)
```

**説明**:
- **issue-handler.yml**: `ai-resolvable` ラベル付きIssueを自動で解決
- **pr-review.yml**: AI生成PRの品質チェック (ESLint, TypeScript, Build)
- **iterative-fix.yml**: レビューフィードバックに基づく自動修正 (最大3回)
- **merge-gate.yml**: PR承認状態・テスト状態の確認とマージ可否判定

---

### `airs/` - AIRS システム

AI-Driven Issue Resolution System の Python コード。

```
airs/
├── analyzer/                 # Issue分析・コンテキスト構築
│   ├── __init__.py
│   ├── issue_parser.py       # Issue内容のパース
│   └── context_builder.py    # 実装コンテキストの構築
│
├── generator/                # コード生成
│   ├── __init__.py
│   ├── claude_client.py      # Claude API クライアント (メイン)
│   ├── claude_client_bedrock.py  # AWS Bedrock統合
│   ├── code_generator.py     # コード生成ロジック
│   └── test_generator.py     # テストコード生成
│
├── orchestrator/             # ワークフロー制御
│   ├── __init__.py
│   ├── review_handler.py     # レビュー処理
│   └── apply_changes.py      # 変更適用
│
├── guardrails/               # セキュリティ・制約
│   ├── __init__.py
│   ├── path_validator.py     # パス検証 (src/, docs/ のみ許可)
│   ├── size_validator.py     # サイズ制限 (max 10 files, 500 lines/file)
│   └── secret_detector.py    # シークレット検出 (API key, password など)
│
├── rules/                    # ルールエンジン
│   ├── __init__.py
│   └── rules_engine.py       # カスタムルール実行
│
└── metrics/                  # メトリクス収集
    ├── __init__.py
    └── metrics_collector.py  # 成功率・所要時間などの収集
```

**主要コンポーネント**:

1. **analyzer/** - Issue の内容を解析し、実装に必要なコンテキストを構築
2. **generator/** - AWS Bedrock 経由で Claude API を呼び出し、コードを生成
3. **orchestrator/** - Issue → PR の全体フローを制御
4. **guardrails/** - セキュリティリスクを防ぐための制約を実装
5. **rules/** - プロジェクト固有のルールをカスタマイズ可能
6. **metrics/** - AIRS の性能指標を収集・レポート

---

### `docs/` - ドキュメント

プロジェクトの各種ドキュメント。

```
docs/
├── templates/                    # テンプレートファイル
│   └── bedrock-policy.json       # AWS IAM ポリシー テンプレート
│
├── BEDROCK_IAM_SETUP.md          # AWS Bedrock IAM 設定ガイド
├── BEDROCK_SETUP.md              # AWS Bedrock 詳細セットアップ
├── DIRECTORY_STRUCTURE.md        # 本ドキュメント
├── IAM_REQUEST.md                # 管理者向けIAM権限追加依頼
├── PROGRESS_REPORT.md            # 作業進捗報告書
└── QUICKSTART_IAM.md             # IAM設定5分ガイド
```

**ドキュメントの用途**:

| ドキュメント | 対象読者 | 内容 |
|------------|---------|------|
| `BEDROCK_IAM_SETUP.md` | 開発者 | IAM権限設定の詳細手順 |
| `BEDROCK_SETUP.md` | 開発者 | Bedrock全般のセットアップ |
| `DIRECTORY_STRUCTURE.md` | 開発者 | プロジェクト構造の説明 |
| `IAM_REQUEST.md` | 管理者 | IAM権限追加の正式依頼書 |
| `PROGRESS_REPORT.md` | 管理者/PM | 作業進捗の詳細報告 |
| `QUICKSTART_IAM.md` | 開発者 | IAM設定クイックガイド |
| `templates/bedrock-policy.json` | 管理者 | IAMポリシーのテンプレート |

---

### `public/` - 静的ファイル

Vite によってそのまま配信される静的ファイル。

```
public/
└── (画像ファイルなど)
```

---

### `scripts/` - ユーティリティスクリプト

セットアップや品質チェック用のシェルスクリプト。

```
scripts/
├── check_setup.sh                  # セットアップ状態の確認
├── run_quality_checks.sh           # 品質チェック実行
└── setup-terraform-backend.sh     # Terraform バックエンド設定 (未使用)
```

**主要スクリプト**:
- **check_setup.sh**: Python/Node.js の依存関係が正しくインストールされているか確認
- **run_quality_checks.sh**: ESLint, TypeScript, Prettier, pytest を一括実行

---

### `src/` - フロントエンドコード

React + TypeScript による画像変換アプリのソースコード。

```
src/
├── components/              # Reactコンポーネント
├── hooks/                   # カスタムフック
├── utils/                   # ユーティリティ関数
├── types/                   # TypeScript型定義
├── App.tsx                  # メインアプリコンポーネント
├── main.tsx                 # エントリーポイント
└── index.css                # グローバルスタイル
```

**主な機能**:
- 画像フォーマット変換 (PNG, JPEG, WebP, AVIF)
- 画像リサイズ
- 品質調整
- EXIF方向補正
- バッチ処理

---

### `dist/` - ビルド出力 (gitignore)

`npm run build` の出力先。本番デプロイ用の最適化されたファイル。

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   └── index-[hash].css
└── (その他の静的ファイル)
```

---

### `node_modules/` - npm パッケージ (gitignore)

npm でインストールされた Node.js パッケージ。

---

### `venv/` - Python 仮想環境 (gitignore)

AIRS 用の Python 仮想環境。

```bash
# 仮想環境の作成
python3 -m venv venv

# アクティベート
source venv/bin/activate

# パッケージインストール
pip install -r requirements.txt
```

---

## 📄 ルートディレクトリのファイル

### 設定ファイル

| ファイル | 用途 |
|---------|------|
| `.env.example` | 環境変数のテンプレート |
| `.gitignore` | Git除外ファイル設定 |
| `.prettierrc` | Prettier設定 |
| `eslint.config.js` | ESLint設定 |
| `package.json` | npm パッケージ設定 |
| `package-lock.json` | npm 依存関係ロック |
| `postcss.config.js` | PostCSS設定 |
| `requirements.txt` | Python 依存関係 |
| `tailwind.config.js` | TailwindCSS設定 |
| `tsconfig.json` | TypeScript設定 (メイン) |
| `tsconfig.app.json` | TypeScript設定 (アプリ) |
| `tsconfig.node.json` | TypeScript設定 (Node.js) |
| `vite.config.ts` | Vite設定 |
| `netlify.toml` | Netlify デプロイ設定 |

### ドキュメント

| ファイル | 用途 |
|---------|------|
| `README.md` | プロジェクトのメインドキュメント |
| `CLAUDE.md` | Claude Code 用の設定・ガイダンス |

---

## 🔍 重要なファイルパス

### AIRS 関連

| 目的 | パス |
|------|------|
| Claude API クライアント | `airs/generator/claude_client.py` |
| Bedrock 実装 | `airs/generator/claude_client_bedrock.py` |
| Issue パーサー | `airs/analyzer/issue_parser.py` |
| コード生成 | `airs/generator/code_generator.py` |
| ワークフロー | `.github/workflows/issue-handler.yml` |

### ドキュメント

| 目的 | パス |
|------|------|
| メインドキュメント | `README.md` |
| IAM設定ガイド | `docs/BEDROCK_IAM_SETUP.md` |
| 管理者向け依頼書 | `docs/IAM_REQUEST.md` |
| 進捗報告 | `docs/PROGRESS_REPORT.md` |
| IAMポリシーテンプレート | `docs/templates/bedrock-policy.json` |

### 設定

| 目的 | パス |
|------|------|
| 環境変数例 | `.env.example` |
| Python依存関係 | `requirements.txt` |
| npm パッケージ | `package.json` |

---

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/kamata-cz/image-converter.git
cd image-converter
```

### 2. Node.js セットアップ

```bash
npm install
npm run dev  # 開発サーバー起動
```

### 3. Python セットアップ (AIRS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. AWS Bedrock セットアップ

`docs/BEDROCK_IAM_SETUP.md` を参照してIAM権限を設定。

### 5. GitHub Secrets 設定

```bash
gh secret set AWS_REGION --body "us-east-1"
gh secret set AWS_ACCESS_KEY_ID --body "..."
gh secret set AWS_SECRET_ACCESS_KEY --body "..."
```

---

## 📚 関連ドキュメント

- [README.md](../README.md) - プロジェクト全体のドキュメント
- [BEDROCK_IAM_SETUP.md](BEDROCK_IAM_SETUP.md) - IAM権限設定
- [IAM_REQUEST.md](IAM_REQUEST.md) - 管理者向けIAM依頼
- [PROGRESS_REPORT.md](PROGRESS_REPORT.md) - 進捗報告

---

## 🔄 最近の変更履歴

### 2025-10-10: ディレクトリ構造整理

- ✅ `QUICKSTART_IAM.md` → `docs/QUICKSTART_IAM.md` に移動
- ✅ `bedrock-policy.json` → `docs/templates/bedrock-policy.json` に移動
- ✅ `airs_config/` 削除 (古い設定ディレクトリ)
- ✅ `airs_system/` 削除 (古い実装ディレクトリ)
- ✅ ドキュメント内のパス参照を更新
- ✅ `docs/templates/` ディレクトリ作成

**目的**: ルートディレクトリをクリーンに保ち、ドキュメントとテンプレートを適切な場所に配置。

---

**このドキュメントは随時更新されます。プロジェクト構造に変更があった場合は、このファイルも更新してください。**
