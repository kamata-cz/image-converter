# Image Converter

English: [README.en.md](README.en.md)

ブラウザの中だけで画像を変換する Web ツールです。画像はサーバーに送信しません。処理はすべて手元のブラウザで行います。

- 公開 URL: https://kamata-cz.github.io/image-converter/
- 注意: いま、このツールは企画し直しの途中です。くわしくは「今後」を見てください。

## できること

画面の文言は英語のみです（日本語化はしていません）。

### 実際に動作を確認したもの

2026-11-04 に、公開中のサイトを Chrome（ヘッドレス）で操作して確認しました。

- 画像ファイルをボタンで選ぶ（1 枚）
- PNG から WebP への変換とダウンロード
- 画質スライダーの表示と値の変化（PNG では画質は効きません。ブラウザの仕様です）

### コード上はあるが、動作は未確認のもの

次の機能はコードに書かれていますが、実際に動かして確かめていません。

- ドラッグ＆ドロップでの画像の追加
- JPEG と PNG への出力
- リサイズ（幅・高さ指定、縦横比の維持、contain / cover / stretch の 3 モード）。なお cover は、切り抜かずに拡大した寸法のまま出力する作りになっています。
- 6 種類のプリセット（Original / Web Optimized / Thumbnail / Social Media / High Quality / Small File）
- EXIF の向き補正（EXIF＝写真に埋め込まれた撮影情報。JPEG のみ対象）
- 複数枚の一括変換（1 枚ずつ別々にダウンロードされます。ZIP にはまとまりません）
- 設定の保存と復元（ブラウザの LocalStorage を使います）

ファイル名は `{元の名前}_{幅}x{高さ}.{拡張子}` になります。日本語のファイル名は `_` に置き換わります。

## 出力形式とブラウザ別の対応表

ブラウザの canvas（画像を描く仕組み）から書き出せるかどうかの表です。

| 形式 | Chrome / Edge | Firefox | Safari（Mac / iOS） |
|---|---|---|---|
| PNG | 書き出せる | 書き出せる | 書き出せる |
| JPEG | 書き出せる | 書き出せる | 書き出せる |
| WebP | 書き出せる | 書き出せる（96 以降） | 書き出せない |
| AVIF | 書き出せない | 書き出せない | 書き出せる記載は見つからず、未確認 |

- 出典: MDN browser-compat-data、caniuse、Chrome 156 での実測（調査メモ `docs/01-research/raw/C-tech-claude.md` の 1-1）。実測したのは Chrome だけです。Edge、Firefox、Safari は実機で確認していません。
- 補足: AVIF は、どのブラウザでも canvas から書き出せることを確認できていません。Chrome 156 で試すと、PNG になりました。
- 補足: このツールは、書き出せない形式を選ぶと、別の形式に切り替えます（下の「既知の不具合」を参照）。
  - Chrome で AVIF を選ぶと、WebP が出ます（実際に確認しました）。
  - Safari で WebP や AVIF を選ぶと、JPEG になるはずです。これはコードの分岐からの推測で、Safari では未確認です。

## 既知の不具合

調査メモ（`docs/01-research/raw/F-existing-claude.md`、`docs/01-research/raw/C-tech-claude.md`）にあるものです。

- AVIF を選んでも、通知なしで別の形式（Chrome では WebP）で出力されます。画面に注意はなく、気づきにくいです。
- EXIF の向きを二重に補正する可能性があります。ブラウザがすでに回転した画像を、コードがもう一度回転するためです。Chrome 156 では、向き 6 の画像で再現しました。iPhone の縦写真が横倒しになるおそれがあります。Safari と Firefox は未確認です。
- 透過のある画像を JPEG にすると、背景が黒くなります（Chrome 156 で実測）。
- HEIC（iPhone の写真形式）は非対応です。Chrome などでは読み込めません。読めない画像が 1 枚でもあると、選んだ画像が一覧に出ない可能性があります（コードからの推測で、実行は未確認です）。
- 変換に失敗すると、原因の説明がない `alert` が出るだけです。
- 大きい画像の処理は、画面を操作するメインの処理と同じところで行います。そのため、画面が固まることがあります。iOS では canvas が 4,096×4,096 px までという記載があり、超えると描けない可能性があります（未確認）。
- UI が英語のみで、アクセシビリティ（ラベルや aria 属性）も不足しています。
- `npm run lint` は 2 件のエラーで失敗します（`src/utils/browserCompat.ts` の 38 行目と 93 行目の未使用変数 `e`）。
- テストはありません。
- `.env.example`、`netlify.toml` など、使っていない古いファイルが残っています。

## 開発の始め方

Node.js は 20 を基準にしてください（公開用の `.github/workflows/deploy.yml` が 20 を使っています）。

```bash
npm ci            # 依存パッケージをインストール
npm run dev       # 開発サーバー（http://localhost:5173）
npm run build     # 本番用ビルド（dist/ に出力）
npm run lint      # ESLint（現状は 2 件のエラーで失敗します）
npm run preview   # ビルド結果の確認
npm run format    # Prettier で整形
```

主なファイルは次のとおりです。

- `src/App.tsx`: ファイルの選択とドラッグ＆ドロップ
- `src/components/ImageConverter.tsx`: 変換の設定画面
- `src/utils/imageProcessor.ts`: 変換・リサイズ・EXIF の処理

技術は React 19、TypeScript、Vite、TailwindCSS 4 です。

## 公開の仕組み

`main` ブランチに push すると、GitHub Actions が自動でビルドし、GitHub Pages に公開します。

- 公開前に lint やテストは実行しません。lint が失敗していても公開されます。
- `vite.config.ts` の `base` は `/image-converter/` です。別のドメインの直下に移すときは変更が必要です。
- 注意: 公開リポジトリなので、push した内容は誰でも読めます。

## 今後

この既存ツールを土台に、企画し直している最中です。経緯と調査結果は `docs/` に記録しています。

- [docs/decisions.md](docs/decisions.md): 決めたことの記録
- [docs/01-research/summary.md](docs/01-research/summary.md): 先行研究のまとめ
- [docs/00-brief.md](docs/00-brief.md): 目的の確認

方向が変わる可能性があります。この README の「できること」も、変わることがあります。

## ライセンス

未定（検討中）。LICENSE ファイルはまだありません。収益化の形を決めるときに、あわせて決めます。
