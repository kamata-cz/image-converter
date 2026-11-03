# F. 既存コードと公開中サービスの棚卸し（Claude 担当）

確認日: 2026-11-04 / 対象: リポジトリ main（コミット fa6c2df）と https://kamata-cz.github.io/image-converter/
作業コピー: scratchpad/F-work/（リポジトリは無変更）。事実と推測は分けて書く。推測は「推測:」と明記。

## 要約（最重要）

1. 公開中サイトは Tailwind のスタイルがほぼ効いておらず、見た目が壊れている（事実。スクリーンショットで確認）。原因は `src/index.css` 1〜3 行目が Tailwind v3 の書き方（`@tailwind base/components/utilities`）のまま、導入済みは v4 であること。作業コピーで `@import "tailwindcss";` に置き換えるとビルド後の CSS が 12.37 kB から 29.24 kB になり `.text-5xl` が出力された（事実）。
2. AVIF を選ぶと、Chrome では .webp ファイルが出力される。画面に通知はない（事実。実操作で確認）。
3. 画像変換の中核（変換・リサイズ・EXIF・複数ファイル）は動作した。HEIC は非対応。

## ① 今できること（実際に動いたか）

| 機能 | 動作 | 根拠 |
|---|---|---|
| 画像の選択（ボタン）と複数選択 | 動いた（1 枚で確認。複数はコード上対応） | App.tsx:124-137 |
| ドラッグ＆ドロップ | 未実操作（ヘッドレスでは困難）。コード上は `image/*` のみ受理 | App.tsx:26-35 |
| PNG→WebP 変換とダウンロード | 動いた。`test_800x600.webp` が出た | shots/pc-out-test_800x600.webp |
| AVIF 指定 | 指定した形式では出ない。.webp になった | 下記④ |
| JPEG / PNG | 未実操作。PNG は既定。コード上は `image/jpeg` `image/png` を toBlob に渡すだけ | imageProcessor.ts:217 |
| リサイズ（幅・高さ・縦横比維持・contain/cover/stretch） | 未実操作。コードの確認のみ（⑤の②参照） | imageProcessor.ts:98-141 |
| 画質スライダー | 表示と値は動作。PNG では無効（toBlob の仕様） | ImageConverter.tsx:235-258 |
| プリセット 6 種（Original/Web Optimized/Thumbnail/Social Media/High Quality/Small File） | 表示は確認。変換結果は未確認 | ImageConverter.tsx:37-68 |
| EXIF 向き補正 | 未実操作（EXIF 付き画像を用意せず）。コード上は JPEG のみ | imageProcessor.ts:23-63 |
| 設定の保存（localStorage） | コード上あり。読み込みは画像を載せた後にだけ走る | ImageConverter.tsx:86-101 |
| ファイル名 | `{名前}_{幅}x{高さ}.{拡張子}`。日本語名は `_` に置換される | imageProcessor.ts:252-254 |
| 一括の出し方 | 1 枚ごとに別々にダウンロード。ZIP 無し | ImageConverter.tsx:128-142 |
| 言語 | 全て英語。日本語化なし。`<html lang="en">` | index.html:2 |

## ② 品質の問題

重大
- Tailwind が効かない: src/index.css:1-3。PC 幅でも h1 は 32px（意図は text-5xl=48px）、アップロード領域の SVG アイコンが画面幅いっぱいに巨大化（h-16 w-16 が効かない）、プレビュー画像が原寸大、ボタンは素のブラウザ既定。360〜390px のスマホでも同様に崩れる（shots 参照）。
- 白文字（text-white）のタイトルが薄い背景の上に乗り、コントラスト不足になりうる（推測: 本来は紫グラデの上に載る想定だが、現状は body 背景のグラデが見えている部分以外で読みにくい）。
- AVIF 指定時に黙って WebP になる: browserCompat.ts:137-157 と imageProcessor.ts:198。UI にエラーも注意もない。ファイル名は実際の形式で付くため、利用者は気づきにくい。

中
- 失敗時は `alert('Failed to process images...')` のみ: ImageConverter.tsx:149。原因の説明なし。
- HEIC/HEIF を選んでも `image/*` は通るが、createImageBitmap が Chrome・Firefox で失敗する見込み（推測: 未実操作）。エラー時は上記 alert のみ。
- 画像一覧の key が index: App.tsx:165。削除時の表示ずれの原因になりうる。
- 画像の読み込みで FileReader の onerror を処理していない: App.tsx:44-63。壊れた画像で Promise が解決せず、読み込みが止まる。
- 設定の復元が不完全: ImageConverter.tsx:86-96。`selectedPreset` は保存されず、保存値の型検証もない。また画像を載せるまでコンポーネントが描画されないため、保存設定は画像を載せた後に反映される。
- 一括変換が複数ダウンロードを連続で発火するため、ブラウザが複数ダウンロードの許可を求める可能性（推測）。ZIP が必要。
- 大きい画像の処理がメインスレッドで、UI が固まる（Worker 未使用。browserCompat は Worker を検出するだけで使っていない）。
- Quality スライダーのバー（absolute の div）が幅 % で重なる実装で、つまみ位置とずれる: ImageConverter.tsx:249-252。

アクセシビリティ
- フォーカスリングは既定の auto のまま（ボタンでは見える）。Tab 順は「Select Images」の後にドキュメント外へ抜けるなど不自然（実測: 2 回目の Tab で BODY に落ちた。ただし再読み込み後の計測で、原因は未調査）。
- フォーマット・リサイズモード・プリセットのトグルボタンに `aria-pressed` がない: ImageConverter.tsx:180-193, 218-230, 317-335。
- `<label>` と入力の対応（htmlFor）がない: ImageConverter.tsx:213, 237, 267, 280。スライダー・数値入力が支援技術で名前なし。
- 削除ボタンの aria-label は英語の固定文言で、どの画像か不明: App.tsx:178。
- 進捗に aria-live や role=progressbar がない。成功トーストも role=status がない: ImageConverter.tsx:366-386。
- ドロップ領域は `div` で、キーボードで開けるのは中のボタンだけ（許容範囲）。

スマホ
- 横スクロールは出ない（scrollWidth 390 で一致）。ただし Tailwind 崩れのため、見た目は未完成。
- 設定画面が縦に非常に長い。変換ボタンが最下部で、画像が増えるほど遠くなる。
- 操作系は iOS Safari で未検証（実機・WebKit なし）。

コンソール
- PC 幅の初回読み込みで 404 が 1 件（`/favicon.ico`。index.html:27）。スマホ幅の計測では 0 件。JS 例外はなし。

## ③ 技術の負債と名残のファイル

- `.env.example`（64 行）: 別プロジェクト（AI 自動 Issue 解決システム。AWS Bedrock、Slack、メール設定）の名残。本アプリは環境変数を使わない。削除候補。
- `netlify.toml`: Netlify 用。実際の公開は GitHub Pages なので不要。かつ SPA リダイレクトも不要。削除候補。
- `tailwind.config.js` と `postcss.config.js` 内の `autoprefixer`: v4 では tailwind.config.js は自動検出されない。不要（content 指定は無視される）。
- `src/App.css`: コメント 1 行のみ。`src/assets/react.svg`: 未使用。`public/vite.svg`: テンプレートの既定アイコン。
- `src/index.css`（443 行）: v3 構文、ベンダープレフィックスの重複、未使用クラス（`.glass-dark`、`.hide-mobile`、`.hide-desktop`、`.animate-slideIn`、`.animate-pulse-slow`、`.gradient-text`、`--gradient-1〜4` など）が大量。`* { margin:0; padding:0 }` が v4 のレイヤ設計と衝突する可能性（推測）。
- `src/utils/browserCompat.ts`（288 行）: 使用されているのは `getOptimalImageFormat` と `detectBrowserFeatures` ほか。`getBrowserInfo`、`applyBrowserFixes`（Arc、Safari 用の CSS 注入）、`showCompatibilityWarning` は過剰。さらに `detectBrowserFeatures` は呼ぶたびに canvas を 2 回作って判定する（毎回の変換で実行）。
- `index.html`: IE11 向けのポリフィル、Promise ポリフィルの CDN 読み込み（`document.write`）、`X-UA-Compatible`、Google Fonts の preconnect（フォントは読み込んでいない）、Permissions-Policy の meta（meta では無効）。title と description が英語のみで、OGP・canonical なし。すべて見直し対象。
- ESLint: `npm run lint` は失敗（下記）。`eslint-plugin-prettier` は設定に未使用。
- `README.md`: 絵文字入り。ブラウザ対応の記載（Chrome 110+ など）は実測に基づかない。`CLAUDE.md` の行番号参照（imageProcessor.ts:22 など）は現行コードとずれている。AVIF も「対応」と書かれているが実際はそうではない。
- テストは 0 件。`package.json` に test スクリプトなし。
- `logs` を .gitignore しているため、logs/ 配下はコミットされない。

## 実行結果（作業コピー。そのまま記録）

- `npm ci`: 成功。警告: 16 件の脆弱性（low 1・moderate 3・high 11・critical 1。内訳は開発依存のみで、例は tar が critical、vite・rollup・postcss・minimatch が high）。また、esbuild・@tailwindcss/oxide・fsevents のインストールスクリプトが「allowScripts 未許可でブロック」と警告されたが、ビルドは通った。
- `npm run build`: 成功（`tsc -b && vite build`、756 ms）。出力: index.html 4.76 kB、CSS 12.37 kB（gzip 2.91）、JS 213.86 kB（gzip 66.75）。警告: baseline-browser-mapping と caniuse-lite が古い。
- `npm run lint`: 失敗。2 エラー: browserCompat.ts:38:12 と 93:12 の `'e' is defined but never used`（@typescript-eslint/no-unused-vars）。
- `npm outdated`: 20 パッケージが古い（例: tailwindcss 4.1.14→4.3.4、vite 7.1.9→7.3.7（最新 8.3.5）、react 19.2.0→19.3.1、typescript 5.9.3（最新 7.0.2））。
- `npm audit --omit=dev`: 本番依存の脆弱性 0 件（react・react-dom のみのため）。全体 audit は上記の 16 件。
- 補足: Tailwind の置換を検証するため、作業コピーだけで `src/index.css` の 1〜3 行目を `@import "tailwindcss";` に変え、ビルドが通り CSS が 29.24 kB になることを確認した。表示（スクリーンショット）までは確認していない。

## ④ 対応ブラウザと形式の実際（コード上の判定）

- 入力: `accept="image/*"` とドロップ時の `file.type.startsWith('image/')` だけで判定。実際に読めるかはブラウザの createImageBitmap（なければ Image 要素）次第。UI の文言は「JPEG, PNG, WebP, AVIF, GIF, SVG」。HEIC は表記も処理もない。
- 出力形式の決定: `getOptimalImageFormat`（browserCompat.ts:137-157）。`checkImageFormatSupport` は 1x1 の canvas で `toDataURL('image/avif')` の戻りの先頭が `data:image/avif` か（`indexOf(...) === 5`）で判断する。
  - AVIF: 判定が偽なら「フォールバック連鎖」へ落ち、avif が偽なら webp、webp が偽なら jpeg。実測では Chrome（Chrome for Testing 143 相当）の canvas は AVIF を書き出せず、WebP が出た。
  - PNG・JPEG: `default` 分岐でそのまま返す（判定なし）。
  - toBlob が null を返したときの二段目のフォールバックは JPEG（imageProcessor.ts:209）。
- 推測（未検証）: Safari の canvas は WebP の書き出し可否がバージョンで異なり、AVIF は書き出せない見込み。Firefox も AVIF は書き出せない見込み。実際のブラウザ別の可否は別担当の調査で確認が必要。
- EXIF: JPEG のみ手書きパーサで Orientation を読む。`createImageBitmap(file)` は多くのブラウザで既定で EXIF 回転を適用する（推測）ため、二重に回転される恐れがある。未検証（imageProcessor.ts:149-195 周辺）。
- 透過 PNG → JPEG で背景が黒になる可能性（白で塗っていない）。未検証。
- README の「Chrome 110+ / Firefox 116+ / Safari 16.4+」は実測根拠がない（コードに版数判定は無い）。

## ⑤ 公開の仕組み

- `.github/workflows/deploy.yml`: `main` への push で発火。Node 20、`npm ci`、`npm run build`、`./dist` を Pages へ公開（actions/deploy-pages@v4）。lint・テストは通さない。よって main へ push した時点で即公開される。lint が失敗していても公開される。
- `vite.config.ts`: `base: '/image-converter/'`。ルート直下で配信する別ドメインに移す場合は変更が必要。
- 公開 URL の応答: https://kamata-cz.github.io/image-converter/ は HTTP 200。`https://kamata-cz.github.io/vite.svg` は 404、`/image-converter/vite.svg` は 200。
- ビルドの index.html では favicon が `/image-converter/vite.svg` に書き換えられ、有効。`/favicon.ico` は存在せず 404（コンソールの 404 の原因）。
- カスタムドメイン、アナリティクス、広告、課金の仕組みは、コード内に無い。

## ⑥ 土台として活かせる部分と作り直しが要る部分

活かせる
- 変換の中核ロジック `processImage` の流れ（ImageBitmap→Canvas→toBlob）と、リサイズ計算の考え方（contain/cover/stretch）。ただし cover は現在「はみ出した寸法で出力する」だけで、切り抜かない（calculateDimensions の cover は縮尺だけ返し、キャンバスは拡大寸法のまま）。ここは正しい仕様に直す必要がある。
- ブラウザ内完結（サーバー不要）という構成と、Pages への自動公開の流れ。
- ビルド・Vite・React・TS の構成そのもの（ビルドは通る）。
- 本番依存が react・react-dom のみで、軽い（JS 66.75 kB gzip）。

作り直し・要対応
- スタイル全体（index.css は作り直しが早い。Tailwind v4 の `@import "tailwindcss";` へ）。UI は全面的に日本語化。
- 出力形式の扱い（AVIF の可否表示、無通知フォールバックの廃止）、HEIC 入力の対応（ライブラリが必要。推測: heic2any や libheif 系の WASM。要調査）。
- 一括出力（ZIP）、変換前後のサイズ比較、Worker 化（大量・大画像）。
- エラー表示、アクセシビリティ（label、aria、フォーカス）、title・description・OGP の日本語化。
- 不要ファイル（.env.example、netlify.toml、tailwind.config.js、未使用 CSS、react.svg、browserCompat の大半）の整理、lint 修正、テスト追加。
- 規模感（推測）: 現行は約 1,160 行の TS/TSX。UI を作り直し、中核を再利用する方針なら、初心者 1 人でも扱える大きさ。

## ⑦ スクリーンショットと所見

保存先: 作業用の一時フォルダ（リポジトリには含めない）
- pc-1-top.png / pc-2-loaded.png / pc-3-after.png（幅 1280。fullPage）
- sp-1-top.png / sp-2-loaded.png / sp-3-after.png（幅 390、DPR 2）
- test.png（テスト入力 800x600 のグラデーション）、pc-out-test_800x600.webp / sp-out-test_800x600.webp（変換結果）

所見（pc-2-loaded.png、sp-2-loaded.png を目視）
- PC: ヘッダーが 1 行に潰れ、アップロード領域のアイコンが縦 800px 超に膨張、プレビュー画像が原寸で全幅に出る。プリセットや設定ボタンは素のブラウザ既定の見た目。紫のグラデは背景のごく一部だけ。
- スマホ: 同様に崩れる。横スクロールなし。変換ボタンが設定の最下部に。
- 実操作: 画像選択→WebP→変換でダウンロードまで成功。AVIF 指定は .webp で出力。コンソールの JS エラーなし（404 は favicon.ico のみ）。

## 試せなかったこと

- ドラッグ＆ドロップの実操作、JPEG/PNG 出力、リサイズ各モード、EXIF 付き JPEG（orientation 6/8）、HEIC、透過 PNG→JPEG、複数枚の一括、設定の保存と復元。
- Safari・Firefox・iOS 実機（Chromium のみ。Playwright 1.49.1 のブラウザは未取得だったため、キャッシュ済みの Chrome for Testing 1208 を playwright-core 1.57 から使用）。
- コントラスト比の数値計測（表示崩れが先に問題となるため目視のみ）。
