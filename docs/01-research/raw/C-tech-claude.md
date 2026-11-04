# C. 技術と規約の制約（Claude 担当）

- 確認日: 2026-11-04（この文書の数値・価格・対応状況はすべてこの日に確認した時点の値）
- 出典の種類: 【公式】ベンダー・標準化団体の文書／【仕様】WHATWG HTML 仕様／【公式データ】MDN browser-compat-data（BCD。MDN の互換表の元データ）と caniuse／【非公式】フォーラム・個人記事・バグ報告のコメント／【実測】この調査で Chrome 156（macOS、Playwright でヘッドレス起動）を使って確かめた結果
- 事実と推測を分けるため、推測には「推測:」と書く
- 補足: Safari・Firefox・Edge の実機での確認はしていない（実測は Chrome 156 だけ）

---

## ① 結論（10 行）

1. **WebP 書き出し — 条件付き**: Chrome・Edge・Firefox（96 以降）はできる。Safari（Mac・iOS）は canvas から WebP を書き出せない（BCD・caniuse で全バージョン未対応）。
2. **AVIF・JPEG XL・HEIC の書き出し — canvas ではできない**: Chrome 156 で試すと PNG にすり替わった【実測】。WebAssembly のエンコーダ（例: jSquash の AVIF エンコーダ、約 3.5MB、Apache-2.0）を使えばできる。
3. **HEIC の読み込み — 条件付き**: そのまま読めるのは Safari 17 以降（Mac・iOS）だけ。Chrome・Edge・Firefox では libheif-js（LGPL-3.0、wasm 約 1.5MB）などの WebAssembly が要る。
4. **大きな画像・大量一括 — 条件付き**: iOS は canvas が 4,096×4,096 px までという記載がある（MDN）。Worker と OffscreenCanvas による並列化は主要ブラウザすべてでできる（Safari は 16.4 以降）。ZIP にまとめるのは JS ライブラリでできる。フォルダごと処理（showDirectoryPicker）は Chrome・Edge だけ（Android 版 Chrome は 132 以降）。
5. **canvas を通すと失われるもの — できる（意図せず消える点に注意）**: EXIF・位置情報は書き出しで消える【実測】。透過を JPEG にすると背景が黒くなる【仕様・実測】。アニメーションは最初の 1 コマしか残らない【仕様】。色はプロファイルを持てない形式では sRGB に変換される【仕様】。
6. **PWA — 条件付き**: インストールとオフライン動作はできる。ただし、他のアプリから画像を受け取る Web Share Target は Chrome（Android 76 以降、デスクトップ 89 以降）だけで、iOS・Safari・Firefox ではできない。iOS にはインストールを促す表示が無く、利用者が手動で追加する。
7. **Chrome 拡張 — できる**: Manifest V3 で、右クリックメニュー（contextMenus の "image"）から変換して保存する作りにできる。WebAssembly は拡張に同梱すれば使える（外部から読み込むコードは禁止）。単一目的・最小権限のポリシーがあり、登録費は 1 回だけで、2020 年の公式ブログでは $5。
8. **GitHub Pages での収益化 — 条件付き（グレー）**: 「オンラインビジネス・商取引・商用 SaaS」に使うことは禁止。寄付ボタンは可と明記されているが、広告については記載が無い。Vercel の無料プラン（Hobby）は広告も課金も禁止と明記。Cloudflare Pages の無料プランには商用を制限する記載が見当たらない（ただし無料サービスのサイト上でカード情報を集めることは禁止）。
9. **AdSense — 条件付き**: 18 歳以上、独自で質の高いコンテンツ、HTML を編集できることが条件。登録する URL にはパス（/image-converter/ の部分）を含められない。ツールしか無い画面は「コンテンツが乏しい」と判断されるおそれがある。
10. **ブラウザ内ツールの課金 — 決済はできるが、有料機能はクライアントだけでは守れない**: 手数料は Stripe Payment Links が 3.6%（日本）、Lemon Squeezy が 5%+50¢、Gumroad が 10%+50¢。既存コードには、EXIF の二重回転・透過が黒になる・形式が知らないうちに差し替わる・HEIC で固まる、という不具合がある（⑦）。

---

## ② 項目ごとの結果と出典

### 1. ブラウザ別の読み込み・書き出し

#### 1-1. 書き出し（canvas.toBlob / OffscreenCanvas.convertToBlob）

| 形式 | Chrome / Edge | Firefox | Safari（Mac / iOS） | 根拠 |
|---|---|---|---|---|
| PNG | できる | できる | できる | 仕様で必須。BCD |
| JPEG | できる | できる | できる（11 以降） | BCD |
| WebP | できる（Chrome 50 以降） | できる（96 以降） | **できない**（26.6・27.x も未対応） | BCD・caniuse |
| WebP（convertToBlob） | できる（69 以降） | できる（105 以降） | **できない** | BCD |
| AVIF | **できない**（Chrome 156 で PNG になった【実測】） | **できない**（Mozilla のバグが未解決） | 記載が見つからない（BCD に項目なし） | 実測・Mozilla bug 1821907・BCD |
| JPEG XL / HEIC / GIF | **できない**（Chrome 156 で PNG になった【実測】） | 不明（記載なし） | 不明（記載なし） | 実測 |

- 仕様・MDN の記載: 対応していない type を指定すると、エラーにならず **PNG で出力される**。「If the file format is not specified, or if the given format is not supported, then the data will be exported as image/png.」【公式】
  - 実務上の注意: 書き出した後に `blob.type` を確かめないと、拡張子は .avif なのに中身は PNG、ということが起きる。
- 【実測】Chrome 156.0.8078.80（headless, macOS）の結果:
  - toBlob: png→image/png、jpeg→image/jpeg、webp→image/webp、avif→**image/png**、jxl→**image/png**、heic→**image/png**、gif→**image/png**
  - convertToBlob: webp→image/webp、avif→**image/png**、jxl→**image/png**
- Mozilla bug 1821907「Support AVIF encoding? (e.g. canvas.toBlob('image/avif'))」: 状態は NEW。報告者は「Blink（Chrome の描画エンジン）にも無い」と書いている。1 か月前のコメントに「Chrome は対応」という記述があるが、上の実測と食い違う【非公式】。
- 出典:
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob 【公式】
  - https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas/convertToBlob 【公式】
  - https://caniuse.com/mdn-api_htmlcanvaselement_toblob_type_parameter_webp 【公式データ】
  - https://raw.githubusercontent.com/mdn/browser-compat-data/main/api/HTMLCanvasElement.json 、 https://raw.githubusercontent.com/mdn/browser-compat-data/main/api/OffscreenCanvas.json 【公式データ】
  - https://bugzilla.mozilla.org/show_bug.cgi?id=1821907 【非公式（バグ報告）】

#### 1-2. 読み込み（表示・デコード）

| 形式 | Chrome | Edge | Firefox | Safari Mac | Safari iOS | 根拠 |
|---|---|---|---|---|---|---|
| WebP | できる | できる | できる | できる（14 以降。かつ macOS 11 以降） | できる | MDN |
| AVIF | 85 以降 | 121 以降 | 93 以降 | 16.4 以降（16.1〜16.3 は一部） | 16.0 以降 | caniuse |
| HEIC/HEIF | **できない** | **できない** | **できない** | 17 以降 | 17 以降 | caniuse |
| JPEG XL | 155 以降（145〜154 は既定で無効） | **できない**（155 まで） | 158 以降 | 17 以降（一部対応） | 17 以降（一部対応） | caniuse・MDN |
| APNG | 59 以降 | 12 以降 | 3 以降 | 8 以降 | — | MDN |

- JPEG XL: Safari の「一部対応」の中身は caniuse に書かれていない。MDN には「Safari does not support progressive download of JPEG XL files」とある。
- WebKit（Safari 17）の公式ブログ: 「With support for HEIC in Safari, Safari View Controller, and WKWebView」。
- iOS で HEIC 写真を `<input type="file">` で選んだときの挙動 【非公式・情報が食い違う】:
  - WebKit Bug 303803: Safari 17 以降、`accept="image/*,image/heic"` のように指定すると、PNG や JPEG が HEIC に変換されてしまう不具合。2026-01-08 に修正済み（RESOLVED FIXED）。
  - Zenn の記事: iOS Safari では accept の値にかかわらず JPEG に変換されたと報告。
  - 推測: iPhone の Safari で HEIC を選んでも、ツールに届く時点で JPEG になっている場合がある。実機での確認が必要。
- 出典:
  - https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types 【公式】
  - https://caniuse.com/avif 、 https://caniuse.com/heif 、 https://caniuse.com/jpegxl 【公式データ】
  - https://webkit.org/blog/14445/webkit-features-in-safari-17-0/ 【公式】
  - https://bugs.webkit.org/show_bug.cgi?id=303803 【非公式（バグ報告）】
  - https://zenn.dev/link/comments/c356d4558e16ad （検索結果の要約だけで、本文は開いていない）【非公式】

#### 1-3. 書き出せないブラウザでの代替（WebAssembly）

npm の値は 2026-11-04 時点。サイズは jsDelivr でファイル一覧を確認した値。

| ライブラリ | できること | ライセンス | 主なファイルの大きさ | 週間 DL・最終更新 | 備考 |
|---|---|---|---|---|---|
| @jsquash/avif 2.1.1 | AVIF の書き出し・読み込み（libavif） | Apache-2.0 | avif_enc.wasm 3.49MB、avif_dec.wasm 1.17MB | 215,085・2025-05-20 | マルチスレッドを使うには COOP/COEP ヘッダーが必要（後述） |
| @jsquash/webp 1.5.0 | WebP の書き出し・読み込み（libwebp） | Apache-2.0 | webp_enc.wasm 0.28MB（SIMD 版 0.35MB） | 不明 | **Safari で WebP を作る代替になる** |
| @jsquash/jxl 1.3.0 | JPEG XL | Apache-2.0 | パッケージ全体 5.8MB | 不明 | |
| @jsquash/jpeg・png・oxipng | MozJPEG・PNG の最適化 | Apache-2.0 | 0.2〜0.5MB | 不明 | |
| libheif-js 1.23.5 | HEIC の読み込み（libheif + libde265） | **LGPL-3.0** | libheif.wasm 1.46MB（wasm を内蔵した bundle 版は 2.04MB） | 4,428,730・2026-10-04 | |
| heic2any 0.0.4 | HEIC → JPEG/PNG | MIT（ただし中身は libheif 由来。推測） | 1.35MB | 2,001,054・2023-03-29 | 3 年以上更新が無い |
| heic-to 1.6.7 | HEIC の変換 | LGPL-3.0 | パッケージ全体 26.2MB | 2,049,664・2026-10-27 | |
| wasm-vips 0.0.19 | libvips 一式（HEIF・JXL・リサイズ等） | MIT | vips.wasm 5.15MB（HEIF を使うなら +3.80MB、JXL なら +2.22MB） | 192,508・2026-09-29 | **SharedArrayBuffer が必須（COOP/COEP ヘッダーが必要）**。Chrome 95・Firefox 100・Safari 16.4 以降 |

- ライセンスの注意:
  - libheif は LGPL（README:「The libheif is distributed under the terms of the GNU Lesser General Public License.」）。LGPL の部分を利用者が差し替えられるようにする義務がある。推測: wasm を別ファイルのまま配り、ライセンス表記を載せれば対応しやすい。法的な判断はしていない。
  - HEIC の書き出しに使う x265 は GPL（libheif README:「note that x265 is GPL」）。HEIC 形式で書き出す機能は避けるのが安全（推測）。
  - HEVC の特許については公式文書を開いていないため **不明**。
- libheif README（2026 年 10 月時点）の記載: 「maintained by a single independent developer ... 89 security advisories had to be investigated, fixed and released in 2026 alone」。開発者 1 人で、脆弱性の修正が多い。依存する場合は更新を追う必要がある。
- 速度: 公式のベンチマークは見つからなかったため **不明**。端末ごとに実測が必要。
- jSquash README: マルチスレッドを使うには「Cross-Origin-Opener-Policy: same-origin」と「Cross-Origin-Embedder-Policy: require-corp」が必要。対応していない環境では単一スレッドで動く。
- GitHub Pages ではレスポンスヘッダーを自分で設定できない【非公式: Stack Overflow・coi-serviceworker の README による。GitHub 公式の記載は未確認】。回避策として、Service Worker でヘッダーを付ける coi-serviceworker がある。Cloudflare Pages は `_headers` ファイルでヘッダーを設定できる（ルールは最大 100 件）【公式】。
  - 推測: COEP: require-corp にすると、AdSense のような外部の広告スクリプトや iframe が読み込めなくなる可能性が高い。広告と WASM のマルチスレッドは両立しにくい。
- 出典:
  - https://raw.githubusercontent.com/jamsinclair/jSquash/main/README.md 、 https://raw.githubusercontent.com/jamsinclair/jSquash/main/packages/avif/README.md 【非公式（OSS の README）】
  - https://raw.githubusercontent.com/kleisauke/wasm-vips/master/README.md 【非公式（OSS）】
  - https://raw.githubusercontent.com/catdad-experiments/libheif-js/master/README.md 、 https://raw.githubusercontent.com/strukturag/libheif/master/README.md 【非公式（OSS）】
  - https://registry.npmjs.org/ （各パッケージ）、 https://api.npmjs.org/downloads/point/last-week/ 、 https://data.jsdelivr.com/v1/packages/npm/ 【公式データ】
  - https://developers.cloudflare.com/pages/configuration/headers/ 【公式】
  - https://www.github.com/gzuidhof/coi-serviceworker （検索結果の要約）【非公式】

### 2. ブラウザ内処理の限界

- **canvas の大きさの上限**: MDN に「in most cases the maximum dimensions exceed 10,000 x 10,000 pixels, notably iOS devices limit the canvas size to only 4,096 x 4,096 pixels」とある。上限を超えると canvas は何も描けなくなり、エラーも出ない（「Exceeding the maximum dimensions or area renders the canvas unusable」）【公式】。ブラウザ別の詳しい値は canvas-size の結果ページにあるが、JS で描画されるページのため取得できなかった（不明）。
  - 注意: 4,096×4,096 は約 1,677 万画素。iPhone の 4,800 万画素の写真をそのまま canvas に描くと上限を超えうる（推測。実機での確認が必要）。
- **iOS Safari の canvas メモリの合計上限**: WebKit のバグ報告やフォーラムに「Total canvas memory use exceeds the maximum limit」という警告の報告がある。値は 224〜576MB と端末や版によってばらつく。対策として、使い終えた canvas の幅・高さを 0 にすると解放される、という報告がある。Apple の公式文書には記載が無い【非公式: https://bugs.webkit.org/show_bug.cgi?id=195325 ほか。検索結果の要約】。
- **Web Worker・OffscreenCanvas**: OffscreenCanvas は Chrome 69・Firefox 105・Safari 16.4 から使える。MDN は「Baseline: Widely available（since March 2023）」としている。Worker の中で描画と convertToBlob ができる。createImageBitmap の resizeWidth/resizeHeight は Chrome 54・Firefox 98・Safari 15 から、resizeQuality は Firefox が 149 から対応【公式データ】。
- **ZIP でまとめてダウンロード**: ブラウザの標準 API には無いため、JS ライブラリを使う。fflate 0.8.3（MIT、0.8MB）、client-zip 2.5.1（MIT）、JSZip 3.10.2（MIT または GPL-3.0）、@zip.js/zip.js 2.24.0（BSD-3-Clause）【公式データ: npm】。
  - 一括ダウンロードの注意: Chrome には「Automatic downloads（自動ダウンロード）」というサイトごとの設定があり、複数ファイルを続けてダウンロードすると許可を求められることがある【公式: https://support.google.com/chrome/answer/114662 。検索結果の要約で、本文は開いていない】。
- **File System Access API（フォルダごと処理）**:
  - showDirectoryPicker・showOpenFilePicker・showSaveFilePicker が使えるのは Chrome 86 以降（Edge も同じ）と Chrome Android 132 以降。**Firefox と Safari は未対応**【公式データ: BCD】。
  - 条件: 安全な接続（HTTPS）で、利用者の操作（クリックなど）から呼ぶこと。書き込みには `{ mode: 'readwrite' }` と利用者の許可が必要【公式】。
  - 代替: `<input webkitdirectory>` でフォルダを読み込むだけなら Chrome 7・Firefox 50・Safari 11.1・iOS Safari 18.4 以降でできる（BCD）。書き戻しはできないので、ダウンロードか ZIP で渡すことになる。
- 出典:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas 【公式】
  - https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas 【公式】
  - https://developer.chrome.com/docs/capabilities/web-apis/file-system-access 【公式】
  - BCD の api/Window.json・api/HTMLInputElement.json・api/_globals/createImageBitmap.json 【公式データ】

### 3. canvas を通すと失われるもの

- **EXIF・位置情報**:
  - 仕様: 書き出す画像の画素は canvas の画素そのもので、メタデータとして決められているのは解像度 96dpi と色プロファイルだけ【仕様】。
  - 【実測】Chrome 156 で、EXIF を含む JPEG を createImageBitmap で読み、canvas から JPEG・WebP・PNG に書き出した。どの形式にも "Exif" の文字列は無かった（先頭 4KB を文字列で検索）。
  - つまり、位置情報を消す機能は再エンコードだけで実現できる。逆に、撮影日時や著作権表記を残したい利用者にとっては欠点になる。
- **向き（Orientation）**: createImageBitmap の imageOrientation は既定値が "from-image"（EXIF に従って回転する）。値 "from-image" は Chrome 112・Firefox 111・Safari 16 から対応【仕様・公式データ】。
  - 【実測】Chrome 156 で、EXIF の Orientation=6 を付けた 40×20 の JPEG を読むと 20×40（回転済み）で返ってきた。HTMLImageElement の naturalWidth/naturalHeight も 20×40。
  - つまり、**自前で回転処理を足すと二重に回転する**（⑦-1）。
- **透過**: 仕様に「For image types that do not support an alpha component, the serialized image must be the bitmap image composited onto an opaque black background」とある。
  - 【実測】半透明と透明部分を持つ canvas を JPEG にすると、透明部分は rgba(1,0,2,255)（ほぼ黒）になった。
  - 白背景にしたい場合は、描く前に fillRect で白く塗る必要がある。
- **色空間（ICC プロファイル）**:
  - 仕様: 描画時に画像は canvas の色空間（既定は srgb。display-p3 も指定できる）に変換される。書き出しでは「For image types that support color profiles, the serialized image must include a color profile ... For image types that do not support color profiles, the serialized image must be converted to the 'srgb' color space」【仕様】。
  - 元の ICC プロファイル（Adobe RGB など）はそのままは残らない。srgb の canvas を使うと、広い色域の写真は sRGB に丸められる。
  - 【実測】Chrome の JPEG 出力には ICC_PROFILE が付いていた。WebP と PNG の出力では iCCP/ICC の文字列は見つからなかった（簡易検索）。
- **アニメーション（GIF・APNG・アニメ WebP）**: 仕様上、drawImage も createImageBitmap も「the default image of the animation ... or ... the first frame」を使う。**canvas では 1 コマ目しか扱えない**【仕様】。アニメーションを保ったまま変換するには、WebCodecs の ImageDecoder や WASM のライブラリが必要。推測: 実装の難しさが大きく上がる。ImageDecoder の対応状況は今回確認していない（不明）。
- 出典:
  - https://html.spec.whatwg.org/multipage/canvas.html （4.12.5.5 Serializing bitmaps to a file、drawImage）【仕様】
  - https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html 【仕様】
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/createImageBitmap 【公式】

### 4. PWA

- **インストール**:
  - デスクトップの Chrome・Edge: アドレスバーにインストールのアイコンが出る。
  - iOS・iPadOS: インストールを促す表示は無く、共有メニューの「ホーム画面に追加」から手動で追加する（web.dev）。iOS 26 以降は、ホーム画面に追加したサイトが既定で Web アプリとして開く（WebKit の Safari 26.0 の記事）。
  - macOS の Safari 17 以降: 「ファイル > Dock に追加」で、どのサイトでも Web アプリにできる（WebKit の Safari 17.0 の記事）。
  - 注意: web.dev の文章には「Safari for macOS does not support installability」と古い記述が残っている。
- **オフライン**: Service Worker を使う。Safari の Web アプリも Service Worker と manifest に対応している（WebKit の Safari 17.0 の記事）。
  - 保存領域: ブラウザのアプリでは 1 オリジンあたり最大でディスクの 60%。ホーム画面の Web アプリも同じ上限。既定では消去されうる（best-effort）。ホーム画面の Web アプリは永続化が認められやすい（WebKit の Storage Policy）【公式】。
- **Web Share Target（他のアプリから画像を受け取る）**:
  - 対応: Chrome Android 76 以降、デスクトップ Chrome 89 以降。Firefox と Safari（iOS を含む）は未対応（BCD に impl_url として webkit.org/b/194593 がある）。
  - 条件: インストール済みであること。manifest の share_target で `method: "POST"`・`enctype: "multipart/form-data"`・`files` を指定し、POST の中身は Service Worker の fetch で受け取る【公式】。
  - **iOS では、写真アプリから共有して PWA で受け取ることはできない。**
  - 推測: iOS で「共有から変換」を実現するにはネイティブアプリ（共有拡張）が必要で、今回の範囲外。
- 既存サイトの状態: 公開中の https://kamata-cz.github.io/image-converter/ には manifest も Service Worker も無く、PWA ではない【実測: curl で確認】。
- 出典:
  - https://web.dev/learn/pwa/installation 【公式】
  - https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ 【公式】
  - https://webkit.org/blog/14445/webkit-features-in-safari-17-0/ 【公式】
  - https://webkit.org/blog/14403/updates-to-storage-policy/ 【公式】
  - https://developer.chrome.com/docs/capabilities/web-apis/web-share-target 【公式】
  - BCD の manifests/webapp/share_target.json 【公式データ】

### 5. Chrome 拡張（Manifest V3）

- **右クリックで変換して保存 — できる**:
  - contextMenus（権限名 "contextMenus"）の ContextType に "image" がある。クリックした画像の URL は OnClickData.srcUrl で取れる。Service Worker では onclick が使えないので contextMenus.onClicked で受ける【公式】。
  - 変換処理: Service Worker には DOM が無い。DOM が必要なら offscreen ドキュメント（権限 "offscreen"、Chrome 109 以降、同時に 1 つだけ、使える拡張 API は runtime だけ）を使う【公式】。推測: OffscreenCanvas と createImageBitmap は Worker でも使えるので、Service Worker の中だけで変換できる可能性がある（未検証）。
  - 画像の取得: 別のサイトの画像を fetch するには host_permissions が必要。"https://*/" は最も広い権限になる【公式】。activeTab（インストール時に警告が出ない）は右クリックメニューの実行でも有効になる。ただし、どこからでも fetch できるようになるかは文書に書かれていない（不明）。
  - 保存: chrome.downloads を使う想定。ただし downloads API のページは今回開いていない（不明）。
- **ウェブストアのポリシー**【公式】:
  - 単一目的:「An extension must have a single purpose that is narrow and easy to understand.」
  - 権限:「Request access to the narrowest permissions necessary」
  - リモートコード:「Execution of logic from a remote source is permissible only when accomplished through a documented API」。リモートホストコードとは「anything that is executed by the browser that is loaded from someplace other than the extension's own files」（JS と WASM を含む）。**WASM は拡張に同梱すればよい。**
  - CSP: 拡張ページの最低限の CSP は「script-src 'self' 'wasm-unsafe-eval'; object-src 'self';」。WASM を使うには 'wasm-unsafe-eval' を明示する必要がある。
  - 広告:「Ads are considered part of your Product」「Ads must also be easily removable」
- **登録費**: 1 回だけ払う（公式の登録ページ）。金額は 2020-03-12 の Chromium 公式ブログで「The Chrome Web Store charges a $5.00 fee」。現在の金額は登録ページに書かれておらず、**現行額は未確認**。
- **課金**: 開発者契約 3.2 で、有料の製品は開発者が取引・税の全責任を負い、Google は決済に関与しない（「Google will have no obligations with respect to such Products」）。拡張でも、Stripe などを自分で組み込む必要がある。
- 出典:
  - https://developer.chrome.com/docs/extensions/reference/api/contextMenus 【公式】
  - https://developer.chrome.com/docs/extensions/reference/api/offscreen 【公式】
  - https://developer.chrome.com/docs/extensions/develop/concepts/network-requests 【公式】
  - https://developer.chrome.com/docs/extensions/develop/concepts/activeTab 【公式】
  - https://developer.chrome.com/docs/webstore/program-policies/policies 【公式】
  - https://developer.chrome.com/docs/extensions/develop/migrate/remote-hosted-code 【公式】
  - https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy 【公式】
  - https://developer.chrome.com/docs/webstore/register 【公式】
  - https://blog.chromium.org/2020/03/new-developer-dashboard-and.html 【公式（2020 年）】
  - https://developer.chrome.com/docs/webstore/program-policies/terms/?hl=EN 【公式】

### 6. 公開と収益化の規約

#### 6-1. GitHub Pages

- GitHub Docs「GitHub Pages limits」の原文:
  - 「GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS).」
  - 「sending passwords or credit card numbers」のような機微な取引にも使うべきではない、とある。
- GitHub Terms for Additional Products の原文:「Some monetization efforts are permitted on Pages, such as donation buttons and crowdfunding links.」
- 広告（AdSense）について明記は無い。
  - 推測: 「主目的が商取引・商用 SaaS」と見なされると違反。広告だけのツールなら直ちに違反とは言い切れないが、グレー。有料機能を売るなら、GitHub Pages から移すのが安全。
- 容量などの上限: 公開サイトは 1GB まで。転送量は月 100GB（ソフトリミット）。ビルドは 1 時間に 10 回（Actions で公開する場合は対象外）。
- 出典:
  - https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits 【公式】
  - https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features 【公式】

#### 6-2. 代わりの無料ホスティング

| サービス | 無料枠での商用（広告・課金） | 無料枠の主な上限 | 出典 |
|---|---|---|---|
| Cloudflare Pages | 商用を制限する記載は見当たらない。ただし「process or collect personal or business credit card information on any web property that is receiving Free Services」は禁止。Stripe の決済ページへ移動させる方式なら当たらない（推測） | 静的アセットへのリクエストは「free and unlimited」。ビルドは月 500 回。1 サイト 20,000 ファイル、1 ファイル 25MiB。`_headers` でヘッダーを設定できる | https://www.cloudflare.com/terms/ 、 https://developers.cloudflare.com/pages/platform/limits/ 、 https://developers.cloudflare.com/workers/platform/pricing/ 【公式】 |
| Netlify | **不明**（料金ページと利用規約に記載が無い。Self-Serve Subscription Agreement は未読） | Free は月 300 クレジットで、超えても追加購入できない（hard limit）。1GB の転送 = 20 クレジット、本番デプロイ 1 回 = 15 クレジット、1 万リクエスト = 2 クレジット | https://www.netlify.com/pricing/ 、 https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/ 【公式】 |
| Vercel Hobby | **できない**。「Hobby teams are restricted to non-commercial personal use only」。商用の例に「Any method of requesting or processing payment from visitors」「The inclusion of advertisements, including ... Google AdSense」がある。寄付は商用にあたらない | 転送 100GB など | https://vercel.com/docs/limits/fair-use-guidelines 【公式】 |

- 推測（試算）: Netlify は 300 クレジット ÷ 20 = 月 15GB 程度。デプロイの回数でもクレジットが減る。

#### 6-3. Google AdSense

- 条件:「at least 18 years of age」「Your content must be high-quality, original, and attract an audience」「access the HTML source code of the site」【公式】。
- 登録する URL:「a standard domain that doesn't contain a path, parameter, fragment, or port number」。example.com/directory のようなパスは不可。自分のドメインのサブドメインも不可【公式: answer/2784438】。
  - 別のヘルプ（answer/12170421）では「Subdomains on platforms that are already part of the public suffix list」を追加できるとしている。
  - github.io は Public Suffix List に GitHub, Inc. の名前で載っている【公式データ: publicsuffix.org で確認】。そのため kamata-cz.github.io 単位なら追加できる可能性がある。ただし 2 つのヘルプの記述が食い違うので **条件付き・要確認**。
  - /image-converter/ というパスのままでは登録できない。
  - 推測: ads.txt はドメインの直下に置く必要があるため、kamata-cz.github.io のユーザーサイト用リポジトリが別に要る。
- 独自ドメインが必須という記載は、公式ヘルプには見当たらない。
- コンテンツ量: 最低何ページという公式の数値は無い。Google Publisher Policies に、広告を出せない画面として「without publisher-content or with low-value content」「under construction」「used for alerts, navigation or other behavioral purposes」がある【公式】。
  - 推測: アップロード欄とボタンだけの画面はこれに当たるおそれがある。使い方・形式の解説記事など、文章のコンテンツを併せて用意する必要がある。
- AdSense コミュニティ（非公式。トップ投稿者の解説）: ツールサイトや無料ホスティングのサイトは最初の審査で落ちやすい、という意見がある。不承認率を「95〜96%」とする記述もあるが、根拠は示されていない【非公式】。
- 出典:
  - https://support.google.com/adsense/answer/9724?hl=en 【公式】
  - https://support.google.com/adsense/answer/2784438 【公式】
  - https://support.google.com/adsense/answer/12170421?hl=en 【公式】
  - https://support.google.com/adsense/answer/10502938?hl=en （Google Publisher Policies）【公式】
  - https://publicsuffix.org/list/public_suffix_list.dat 【公式データ】
  - https://support.google.com/adsense/community-guide/241032356/ （検索結果の要約）【非公式】

#### 6-4. ブラウザ内ツールで課金する方法

| 方法 | 手数料（2026-11-04 時点） | 税の処理 | ライセンスキー | 出典 |
|---|---|---|---|---|
| Stripe Payment Links | 国内カードは 3.6%（固定費・月額なし）。通貨の換算が要る場合は +2%。Payment Links 自体は無料（独自ドメインはオプションで月 $10） | 自分で行う（Stripe Tax あり） | **標準では発行しない**。支払い後に自分の Webhook などで発行する必要がある（推測） | https://stripe.com/jp/pricing 、 https://docs.stripe.com/payment-links 【公式】 |
| Lemon Squeezy | 5% + 50¢（米国外の取引などで追加手数料があり、額は未確認） | Merchant of Record（販売者として税を代行） | 購入ごとに自動で発行。License API（activate・validate・deactivate、1 分 60 回まで） | https://www.lemonsqueezy.com/pricing 、 https://docs.lemonsqueezy.com/api/license-api 【公式】 |
| Gumroad | 直販は 10% + $0.50。Discover（Gumroad 内の販売一覧）経由は 30% | 2025-01-01 から Gumroad が税を代行 | **未確認**（ヘルプのページが JS で描画され、本文を取得できなかった） | https://gumroad.com/pricing 【公式】 |

- Lemon Squeezy の validate の例では Authorization ヘッダーを付けていない。ただし、クライアントから直接呼んでよいかは文書に書かれていない（不明）。
- **クライアントだけで有料機能を守ることの限界（推測を含む）**:
  - ブラウザに配った JS と WASM は、利用者がすべて手元で読めて書き換えられる。「キーを確かめたら有料機能を有効にする」判定は、開発者ツールで外せる。クライアントだけで機能を **確実に** 守ることは **できない**。
  - 現実的な選択肢は次の 3 つ。
    - (a) 抜け道があることを受け入れ、寄付・応援購入として売る
    - (b) 価値の高い処理（例: 大量一括、AVIF の WASM 版）を、キー確認の後に別ファイルとして配る。ただし、取得したファイルはコピーされうる
    - (c) サーバー側の処理（Cloudflare Workers など）で、キーを確かめた利用者にだけ機能を出す。ただし「画像をサーバーに送らない」という既存の売りとぶつかる
  - 法令: 日本で有料の販売をするなら、特定商取引法の表示（販売価格、事業者の氏名・住所・電話番号、返品の条件など）が要る。住所と電話番号は「請求があれば遅滞なく提供する」と書けば省略できるが、返品に関する事項は省略できない【公式: https://www.no-trouble.caa.go.jp/what/mailorder/ 】。

### 7. 既存コード（src/）の問題（「ファイル:行」は 2026-11-04 時点）

| # | 場所 | 問題 | 根拠 | 重要度 |
|---|---|---|---|---|
| 7-1 | src/utils/imageProcessor.ts:149, 156, 176-190 | **EXIF の向きを二重に適用している。** createImageBitmap(file) は既定で EXIF に従って回転済み（"from-image"）。その上で getExifOrientation と applyOrientation でもう一度回している。同じ処理を Chrome 156 で再現すると、Orientation=6・40×20 の画像が 40×20（正しくは 20×40）で出力された。ファイル名の `{w}x{h}`（:227 の newWidth/newHeight）と実際の大きさも食い違う | 仕様・BCD（from-image は Chrome 112・Firefox 111・Safari 16 から）・【実測】 | 高（iPhone の縦写真がすべて横倒しになる可能性がある。Safari・Firefox は未実測） |
| 7-2 | src/utils/imageProcessor.ts:192-195 | **透過のある画像を JPEG にすると背景が黒くなる。** 描く前に白で塗りつぶす処理が無い | 仕様・【実測】rgba(1,0,2,255) | 中 |
| 7-3 | src/utils/browserCompat.ts:137-157 と imageProcessor.ts:198 | **選んだ形式が知らないうちに差し替わる。** Chrome で AVIF を選ぶと WebP に、Safari で WebP や AVIF を選ぶと JPEG になる（コードの分岐から導いた結果。Safari は未実測）。UI に知らせる表示が無い（ImageConverter.tsx:217 は 4 形式を常に表示） | コード・【実測】Chrome は avif→png（判定が false になり webp へ） | 高（「AVIF に変換」をうたえない） |
| 7-4 | src/utils/imageProcessor.ts:203-215 | toBlob が null を返したら JPEG に切り替える、という作りだが、対応していない形式は null ではなく **PNG で返る**ため、この分岐はほぼ働かない。`blob.type` を確かめていない | MDN・仕様 | 中 |
| 7-5 | src/App.tsx:47-61 | プレビューを作るとき、`img.onerror` と `reader.onerror` が無い。読めない画像（Chrome などでの HEIC）が 1 枚でもあると Promise.all が終わらず、**選んだ画像がすべて一覧に出ない** | コード（実行は未確認）・caniuse（Chrome は HEIC 非対応） | 高（iPhone 利用者が最初に当たる） |
| 7-6 | src/App.tsx:61 | プレビューを readAsDataURL（base64 の文字列）で作っている。大量・大きい画像でメモリを多く使う。URL.createObjectURL を使うのが一般的 | 推測（base64 は元の約 4/3 の大きさ） | 中 |
| 7-7 | src/components/ImageConverter.tsx:128-139、imageProcessor.ts:234-243 | 1 枚ずつ `<a download>` を続けてクリックしている。Chrome では「自動ダウンロード」の許可が求められうる。クリック直後に revokeObjectURL しているため、ブラウザによっては保存に失敗するおそれがある（推測。未確認） | Chrome ヘルプ（要約）・推測 | 中（ZIP にまとめる案の根拠） |
| 7-8 | src/utils/imageProcessor.ts:178-195 | 大きさの上限を確かめていない。iOS の 4,096×4,096 を超えると描けないが、エラーにならず空の画像になりうる。メインスレッドで処理しているので、大きな画像では画面が固まる | MDN | 中 |
| 7-9 | src/components/ImageConverter.tsx:87, 100 | localStorage を try の外で読み書きしている。ストレージが使えない環境では例外になりうる（推測） | 推測 | 低 |
| 7-10 | index.html:27 | `/favicon.ico` を参照しているが、公開サイトでは https://kamata-cz.github.io/favicon.ico が 404。manifest と Service Worker が無い（PWA ではない） | 【実測】curl | 低 |

---

## ③ 形の比較と推奨

| 観点 | Web（今の形） | PWA（Web + manifest + Service Worker） | Chrome 拡張 |
|---|---|---|---|
| できること | 変換・リサイズ・一括・ZIP。WebP は Safari 以外。AVIF・HEIC は WASM が必要 | Web と同じ + オフライン + ホーム画面への追加。Android の Chrome では「共有」から画像を受け取れる | Web ページ上の画像を右クリックで変換して保存。Chrome と Edge のみ。iPhone では使えない |
| 難しさ（初心者・20 時間） | 低い（既存の不具合修正が中心） | 低〜中（vite-plugin-pwa などで数時間。推測） | 中〜高（MV3・権限・審査・ストアの掲載文） |
| 公開の費用 | 0 円（GitHub Pages / Cloudflare Pages） | 0 円 | 登録費 1 回（2020 年時点で $5、現行額は未確認） |
| 課金のしやすさ | 広告（AdSense は文章のコンテンツと、パスを含まない URL が必要）、寄付、Stripe/Lemon Squeezy のリンク | Web と同じ | ストアの課金は無く、自分で組み込む。広告は「簡単に外せること」が条件 |
| 規約の危うさ | GitHub Pages での広告・課金はグレー、Vercel Hobby は不可。Cloudflare Pages が無難（推測） | Web と同じ | 単一目的・最小権限。全サイト分の host 権限は審査で目立つ（推測）。外部コードは禁止 |
| 日本の利用者との相性（推測） | iPhone の利用者にも届く | iPhone はインストールが手動で、共有からの受け取りもできない | パソコンの Chrome 利用者に限られる |

**推奨（推測を含む）**: **Web を主にし、軽い PWA 化を足す**。

- 理由:
  1. 公開費が 0 円で、既存資産をそのまま使える
  2. iPhone と HEIC の需要（日本で優先）に届くのは Web だけ
  3. PWA 化は数時間で、オフライン動作と Android の共有受け取りが付いてくる
  4. Chrome 拡張は iPhone に届かず、審査と権限の作業が 20 時間の予算を圧迫する
- 収益化を本気でやる場合: ホスティングを GitHub Pages から Cloudflare Pages（独自ドメイン）へ移すのが前提になる（規約のグレーさを避けるため。独自ドメインは AdSense の登録 URL の条件を満たしやすい）。
- 拡張は、Web 版が使われてから「右クリック保存」を足す 2 段目の案として残す。

---

## ④ 案出しで注意する制約

1. **「AVIF に変換」「HEIC を変換」は WASM が前提**。AVIF エンコーダは約 3.5MB、HEIC デコーダは約 1.5〜2MB。初回の読み込みが重くなるので、必要になったときにだけ読み込む設計が要る。
2. **Safari では WebP を作れない**。iPhone の利用者に「WebP に軽量化」を出すなら @jsquash/webp（約 0.3MB）が必要。
3. **iPhone の HEIC は、Safari で選んだ時点で JPEG になっている可能性がある**（非公式情報が食い違う）。「HEIC → JPEG」案の需要は、パソコンの Chrome・Edge（Windows を含む）利用者で考える。iPhone での挙動は実機で確かめる必要がある。
4. **アニメーション（GIF・アニメ WebP）の変換は canvas ではできない**。1 コマ目だけになる。案に入れるなら難しさを高く見積もる。
5. **位置情報の削除は再エンコードだけで実現できる**（売りにできる）。逆に「EXIF を残す」機能は作るのが難しい。
6. **フォルダごと処理は Chrome・Edge だけ**。Firefox と Safari には ZIP でダウンロードさせる代替が要る。
7. **iOS は canvas が 4,096×4,096 px までという記載**がある。高画素の写真は縮小を前提にし、上限を確かめる処理が必要。
8. **WASM のマルチスレッドには COOP/COEP ヘッダーが必要**。GitHub Pages では設定できず、広告スクリプトとぶつかるおそれがある（推測）。
9. **有料機能はクライアントだけでは守れない**。「寄付・応援購入」「ライセンスキー（抜け道は許容）」「サーバー処理（画像を送らない、という売りを失う）」のどれかを選ぶ必要がある。日本で販売するなら特定商取引法の表示が要る。
10. **AdSense は、ツールの画面だけでは審査・掲載ともに不利**。形式の解説などの文章コンテンツと、パスを含まない URL（独自ドメインか github.io のルート）が必要。
11. **既存の不具合（7-1・7-3・7-5）は、どの案でも最初に直す必要がある**。縦写真が横倒しになる、HEIC で固まる、形式が知らないうちに変わる。

---

## ⑤ 不明点（10 件）

1. Safari（Mac・iOS）と Firefox で、canvas から AVIF を書き出せるか。BCD に項目が無く、Safari は実測もしていない。Firefox はバグが未解決なので未対応と見られる。
2. iOS Safari で HEIC 写真を `<input type="file">` で選んだとき、JPEG に変換されて届くかどうか（非公式情報が食い違う。実機での確認が必要）。
3. 7-1（EXIF の二重回転）が Safari と Firefox でも起きるか（Chrome 156 だけ実測。仕様と BCD からは起きると見られる）。
4. 現在の Chrome ウェブストアの登録費の額（公式の登録ページに金額が書かれていない。$5 は 2020 年の公式ブログの値）。
5. Netlify の無料プランで商用利用（広告・課金）が認められるか（Self-Serve Subscription Agreement と Acceptable Use Policy は未読）。
6. AdSense に kamata-cz.github.io（Public Suffix List に載っているサブドメイン）を登録できるか（2 つの公式ヘルプの記述が食い違う）。
7. WASM エンコーダ（jSquash の AVIF・WebP、libheif-js）の端末ごとの速度とメモリ使用量（公式のベンチマークが無い）。
8. Gumroad のライセンスキーの仕組みと、確認 API の条件（ヘルプが JS で描画され取得できなかった）。Lemon Squeezy の License API を、ブラウザから直接呼んでよいか。
9. ブラウザ別の canvas の大きさ・面積の上限値（canvas-size の結果ページを取得できなかった）と、iOS の canvas メモリ合計上限の現行値（公式の記載が無い）。
10. HEVC（HEIC）のデコーダを Web で配布するときの特許・ライセンス上の扱い（公式文書は未確認）。WebCodecs の ImageDecoder でアニメーション画像を扱えるブラウザの範囲（未確認）。
