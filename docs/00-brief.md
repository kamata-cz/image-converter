# 00 目的の確認（2026-11-04 確定）

| 項目 | 内容 | 決め方 |
|---|---|---|
| 対象 | 既存の画像変換ツール（https://viewpilla-wq.github.io/image-converter/ 、GitHub Pages で公開中。ライセンスは未定〔LICENSE ファイル無し、5 で決める〕）を土台に企画し直す。調査次第で方向転換もありうる | ユーザー回答 |
| 開発の流れ | `app-dev-lifecycle` の 11 段階（0 目的の確認〜10 運用改善）。段階の終わりごとに承認 | ユーザー回答 |
| ゴール | 公開して収益化（原案に「マネタイズまで」とあるため） | 原案から判断 |
| 期限と時間 | 1 か月以内（2026-12-04 目安）・週 5 時間程度＝合計 20 時間前後 | ユーザー回答 |
| 提供形態 | Web のまま進め、先行研究で PWA・Chrome 拡張が有利と分かれば提案 | ユーザー回答 |
| 運用費 | 要相談。5 お金の設計で案ごとの費用を出して決める | ユーザー回答 |
| 利用者・場面 | 先行研究の後で決める | ユーザー回答 |
| UI・動き | 「GitHub を完コピ」＝ GitHub 社の見た目（Primer）に寄せる。ロゴ・名称は使わない（スキル `github-primer-artifact`） | ユーザー回答 |
| 体制 | 一人。成果物はこのリポジトリの `docs/`（公開リポジトリなので push すると誰でも読める） | ユーザー回答 |

## 既存資産（2026-11-04 時点）
- React 19 + TypeScript + Vite 7 + TailwindCSS 4、src は約 1,160 行（App.tsx・ImageConverter.tsx・imageProcessor.ts・browserCompat.ts）
- 機能: PNG/JPEG/WebP/AVIF 変換、リサイズ（cover/contain/stretch）、画質、EXIF 向き補正、一括処理、設定の LocalStorage 保存。処理はすべてブラウザ内
- 公開: GitHub Actions（.github/workflows/deploy.yml）で main への push ごとに GitHub Pages へ。netlify.toml も残っている
- 注意: `.env.example` は削除済みの「AI Issue 自動解決システム」の名残（値は空）。整理するかは 7 実装の前に確認する

## 未決事項
- 運用費の上限（5 で決める）
- 利用者・場面、最終的な形（2 案出し・3 ヒアリングで決める）
- 名前を変えるか（3 で聞く）
