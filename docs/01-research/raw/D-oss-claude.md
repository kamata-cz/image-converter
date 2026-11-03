# D: OSS 調査（Claude 担当）

確認日: 2026-11-04（すべての数値はこの日に GitHub API・npm レジストリで取得した値。変動する）

## 読み方

- スター・最終コミット: GitHub API（stargazers_count、pushed_at）。
- ライセンス: GitHub API の spdx_id をそのまま記載。NOASSERTION は GitHub が判定できなかった意味で、括弧内に実ファイル・npm の記載を補足した。
- 週DL: `api.npmjs.org/downloads/point/last-week/<pkg>` の値（2026-11-04 時点）。
- 容量: README に書いてあったものだけ。bundlephobia は開いていないので、ほとんど「不明」。
- 判定: 使える = MIT・Apache-2.0・BSD・ISC（著作権表示を残す）。参照のみ = GPL・AGPL・LGPL・ライセンス無し。古い = 最終コミットが 2 年以上前（2024-11-04 より前）。
- 商用利用: 使える判定のものは可（著作権・ライセンス表示が条件）。弁護士の判断ではなく、ライセンス名からの一般的な整理。
- 事実と推測: 「価値」列の評価は推測（担当者の意見）。それ以外は取得値。

## 一覧表（40 件）

| # | 分野 | 名前（URL） | スター | 最終コミット | ライセンス | 技術 | できること | 容量 | 週DL | 土台・部品の価値（推測） | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | Squoosh https://github.com/GoogleChromeLabs/squoosh | 26,124 | 2026-10-22 | Apache-2.0 | TypeScript（Preact）+ wasm | 画像圧縮 Web アプリ。複数コーデック、並べて比較、PWA。画像は送信しない（README） | 不明 | - | 設計の手本として最高。単体画像向けで一括処理は無い（推測）。コーデック部分は #2 経由が楽 | 使える |
| 2 | A | svgomg https://github.com/jakearchibald/svgomg | 6,206 | 2025-09-29 | MIT | JavaScript + svgo | SVG 最適化の Web GUI | 不明 | - | SVG 対応を足すなら UI の参考 | 使える |
| 3 | A | filerobot-image-editor https://github.com/scaleflex/filerobot-image-editor | 1,929 | 2026-06-16 | MIT | JavaScript（React） | 切り抜き・回転・フィルタ・リサイズを持つ画像エディタ部品 | 不明 | 不明（未取得） | 編集機能を丸ごと足せるが、画面が大きく自作 UI と揃えにくい（推測） | 使える |
| 4 | A | tui.image-editor https://github.com/nhn/tui.image-editor | 7,667 | 2023-11-20 | MIT | JavaScript（canvas） | 多機能の画像エディタ | 不明 | - | 更新が止まっている | 古い |
| 5 | A | VERT https://github.com/VERT-sh/VERT | 16,197 | 2026-10-20 | AGPL-3.0 | TypeScript（Svelte 想定。README 未確認）+ wasm | ファイル変換 Web アプリ。「fully local」を掲げる | 不明 | - | 競合・見た目の参考。コードは使えない | 参照のみ |
| 6 | A | ImageOptim https://github.com/ImageOptim/ImageOptim | 10,025 | 2026-07-13 | GPL-2.0 | Mac アプリ | 画像最適化のデスクトップ GUI | - | - | 競合・機能の参考 | 参照のみ |
| 7 | A/C | ExifCleaner https://github.com/szTheory/exifcleaner | 2,854 | 2026-11-02 | MIT | TypeScript（Electron）+ ExifTool | メタデータ削除のデスクトップアプリ。一括処理（README） | - | - | 「EXIF 削除」需要の存在を示す競合。コードは Electron 前提でそのまま流用不可（推測） | 使える |
| 8 | B | jSquash https://github.com/jamsinclair/jSquash | 740 | 2026-01-05 | Apache-2.0 | TypeScript + wasm（Web Worker 向け） | Squoosh 由来の codec: avif・jpeg・jxl・oxipng・png・qoi・resize・webp の encode/decode。HEIC は含まない（README のパッケージ一覧） | 不明 | webp 911,041 / avif 215,085 / jpeg 465,789 / png 459,908 / resize 174,461 | Canvas の toBlob より小さく・高品質に変換できる。必要な形式だけ入れられる。npm から入れるだけで使える | 使える |
| 9 | B | pica https://github.com/nodeca/pica | 4,154 | 2026-08-15 | MIT | TypeScript（JS + wasm + WebWorker） | 高品質リサイズ（lanczos3 等） | 不明 | 1,647,611 | リサイズ画質の改善。Canvas 標準より縮小時の品質が良い（README の主張） | 使える |
| 10 | B | wasm-vips https://github.com/kleisauke/wasm-vips | 892 | 2026-10-25 | MIT | C++ → wasm | libvips をブラウザで。多形式・高機能 | 不明 | 192,508 | 強力だが SharedArrayBuffer が必要で、COOP/COEP ヘッダを要する（README）。GitHub Pages ではヘッダを設定できないはず（推測・未検証） | 使える |
| 11 | B | magick-wasm https://github.com/dlemstra/magick-wasm | 902 | 2026-11-03 | Apache-2.0（npm 側も Apache-2.0。本体 ImageMagick は GitHub 上 NOASSERTION・独自ライセンス） | TypeScript + wasm | ImageMagick をブラウザで。多形式 | 不明（大きいと思われる。推測） | 227,011 | 対応形式は最多級だが重い見込み | 使える（条件付き: ImageMagick ライセンス文面の確認が要る） |
| 12 | B | heic-to https://github.com/hoppergee/heic-to | 360 | 2026-10-27 | NOASSERTION（LICENSE 実文は LGPL-3.0、npm も LGPL-3.0） | JavaScript + libheif wasm | HEIC/HEIF を JPEG・PNG に変換。libheif の最新版に追従（README） | 不明 | 2,049,664 | iPhone 写真の変換が現役で保守されている点が強い。LGPL の扱いが条件 | 参照のみ（LGPL の wasm は条件付き: 差し替え可能な形で動的に読み込む等。要確認） |
| 13 | B | libheif-js https://github.com/catdad-experiments/libheif-js | 120 | 2026-10-04 | LGPL-3.0 | JavaScript（wasm） | libheif を npm モジュール化 | 不明 | 4,428,730 | #12 や #14 の下請け。単体でも使える | 参照のみ（LGPL の wasm は条件付き） |
| 14 | B | heic2any https://github.com/alexcorvi/heic2any | 896 | 2024-04-11 | MIT | TypeScript + wasm | HEIC/HEIF を PNG・GIF・JPEG に変換 | 不明 | 2,001,054 | 利用者は多いが、npm の最新版 0.0.4 は 2023-03-29 公開。更新が止まっている。内部の libheif のライセンス表記の扱いは不明 | 古い（MIT 表記は使える。内包物は要確認） |
| 15 | B | heic-convert https://github.com/catdad-experiments/heic-convert | 323 | 2024-12-02 | none（API。npm は ISC と表記） | JavaScript | HEIC を JPEG・PNG に変換 | 不明 | 2,391,689 | GitHub と npm でライセンス表示が食い違う | 参照のみ（ライセンス無し判定。npm の ISC と食い違うため要確認） |
| 16 | B | libheif https://github.com/strukturag/libheif | 2,414 | 2026-10-26 | NOASSERTION（COPYING に「ライブラリ本体は LGPL」） | C++ | HEIF/HEIC/AVIF のデコーダ・エンコーダ本体 | - | - | #12〜#14 の元。直接は使わない | 参照のみ（LGPL） |
| 17 | B | browser-image-compression https://github.com/Donaldcwl/browser-image-compression | 1,723 | 2024-03-08 | MIT | JavaScript | ブラウザ内の画像圧縮（サイズ上限指定、Web Worker） | 不明 | 1,931,123 | 手軽だが更新が 2 年以上無い | 古い |
| 18 | B | compressorjs https://github.com/fengyuanchen/compressorjs | 5,783 | 2026-10-01 | MIT | JavaScript | Canvas ベースの画像圧縮。EXIF 向き補正あり（機能名のみ README で未確認） | 不明 | 641,963 | 軽い圧縮部品。今の Canvas 実装と役割が重なる | 使える |
| 19 | B | photon https://github.com/silvia-odwyer/photon | 3,913 | 2026-09-18 | Apache-2.0 | Rust + wasm | フィルタ・リサイズなどの画像処理 | 不明 | 不明（未取得） | 変換より加工向き。必要性は低い（推測） | 使える |
| 20 | B | ffmpeg.wasm https://github.com/ffmpegwasm/ffmpeg.wasm | 17,944 | 2026-09-29 | MIT | C → wasm | ブラウザ内 FFmpeg。画像・動画 | 不明（大きい。推測） | 1,095,598（@ffmpeg/ffmpeg） | 動画・GIF まで広げる場合のみ。画像だけなら過剰（推測） | 使える（内包する FFmpeg 側のライセンスは別途確認） |
| 21 | B | sharp https://github.com/lovell/sharp | 32,819 | 2026-10-29 | Apache-2.0 | JavaScript（Node.js 用） | libvips を使う高速変換 | - | 不明 | ブラウザでは動かない。サーバー型にする場合のみ | 使える（ブラウザ不可） |
| 22 | C | exifr https://github.com/MikeKovarik/exifr | 1,253 | 2024-03-29 | MIT | JavaScript | EXIF・XMP・ICC 等の高速読み取り。向き・GPS 取得 | 不明 | 2,837,727 | 読み取り専用。書き換え・削除は不可（推測、README 未確認）。更新が 2 年以上無い | 古い |
| 23 | C | ExifReader https://github.com/mattiasw/ExifReader | 1,004 | 2026-11-03 | MPL-2.0 | JavaScript | EXIF 等の読み取り。現役保守 | 不明 | 414,165 | 読み取り用。MPL-2.0 は弱いコピーレフト（ファイル単位）。改変せず使う分には扱いやすい（一般的整理） | 使える（条件付き: MPL-2.0 の条件を確認） |
| 24 | C | piexifjs https://github.com/hMatoba/piexifjs | 617 | 2021-07-13 | MIT | JavaScript | JPEG の EXIF を読み・書き・削除 | 不明 | 220,811 | JPEG 限定だが書き換えができる数少ない部品 | 古い |
| 25 | C | exif-js https://github.com/exif-js/exif-js | 4,978 | 2024-05-31 | MIT | JavaScript | EXIF 読み取り | 不明 | 235,587 | 古い設計で、#22 のほうが良い（推測） | 古い |
| 26 | C | exif-reader https://github.com/devongovett/exif-reader | 174 | 2025-12-12 | MIT | JavaScript | EXIF バッファの小さな読み取り器 | 不明 | 不明（未取得） | 小さいが機能は限定的 | 使える |
| 27 | D | fflate https://github.com/101arrowz/fflate | 3,078 | 2026-05-16 | MIT | TypeScript | 高速な圧縮・展開。ZIP 作成可。「8kB」（説明文） | 約 8kB（GitHub 説明文） | 145,644,507 | 一括ダウンロードの ZIP 化に最適 | 使える |
| 28 | D | JSZip https://github.com/Stuk/jszip | 10,394 | 2026-09-09 | NOASSERTION（LICENSE に「MIT または GPLv3 を選択」。npm も MIT OR GPL-3.0-or-later） | JavaScript | ZIP の作成・読み・編集 | 不明 | 68,984,277 | 定番。MIT を選んで使う | 使える（MIT を選択） |
| 29 | D | client-zip https://github.com/Touffy/client-zip | 449 | 2026-09-14 | MIT | TypeScript | ストリーミング ZIP 作成（作成のみ） | 不明（軽量を謳う。README 未確認） | 904,842 | 大量ファイルのメモリ節約向き | 使える |
| 30 | D | zip.js https://github.com/gildas-lormeau/zip.js | 3,905 | 2026-10-22 | BSD-3-Clause | JavaScript | 並列圧縮・Web Worker 対応の ZIP | 不明 | 8,600,632（@zip.js/zip.js） | 暗号化 ZIP など高機能。通常は過剰（推測） | 使える |
| 31 | E | react-easy-crop https://github.com/ValentinH/react-easy-crop | 2,783 | 2026-10-27 | MIT | TypeScript（React） | ドラッグ・ズーム・回転の切り抜き UI | 不明 | 5,129,335 | React 前提で組み込みやすく、タッチ対応 | 使える |
| 32 | E | react-image-crop https://github.com/dominictobias/react-image-crop | 4,108 | 2026-06-21 | ISC | TypeScript（React） | 矩形選択の切り抜き。依存なし（README 未確認） | 不明 | 4,230,741 | 比率固定・自由矩形の UI に向く | 使える |
| 33 | E | cropperjs https://github.com/fengyuanchen/cropperjs | 13,911 | 2026-10-16 | MIT | TypeScript | フレームワーク非依存の切り抜き | 不明 | 2,847,652 | 実績は最大。React 用ラッパーは別途 | 使える |
| 34 | E | react-advanced-cropper https://github.com/advanced-cropper/react-advanced-cropper | 885 | 2026-07-25 | NOASSERTION（npm は MIT） | TypeScript（React） | 高機能な切り抜き（ストックリリース） | 不明 | 244,714 | 高機能だが GitHub のライセンス判定が不明。npm と食い違わないか要確認 | 使える（要確認: LICENSE 実文） |
| 35 | F | @primer/react https://github.com/primer/react | 3,931 | 2026-11-03 | MIT | TypeScript（React） | GitHub の Primer の React 部品 | 不明（大きめと思われる。推測） | 61,293 | GitHub 風の本格的な UI。初心者 1 人・20 時間には重いかもしれない（推測） | 使える |
| 36 | F | @primer/css https://github.com/primer/css | 13,052 | 2026-11-02 | MIT | SCSS | Primer の CSS 実装 | 不明 | 58,685 | CSS だけなので既存の Tailwind と混在させる設計が要る。今後の保守方針は不明 | 使える |
| 37 | F | @primer/octicons https://github.com/primer/octicons | 8,775 | 2026-11-02 | MIT | TypeScript（SVG） | GitHub のアイコン集 | 不明 | 720,960（octicons）/ 172,280（octicons-react） | アイコンだけ使うのが最も軽く確実 | 使える |
| 38 | その他 | vite-plugin-pwa https://github.com/vite-pwa/vite-plugin-pwa | 4,309 | 2026-10-09 | MIT | TypeScript | Vite 用の PWA 化（Service Worker・マニフェスト） | 不明 | 7,114,534 | 既存の Vite 構成を PWA にする最短手段 | 使える |
| 39 | その他 | browser-fs-access https://github.com/GoogleChromeLabs/browser-fs-access | 1,591 | 2026-06-22 | Apache-2.0 | JavaScript | File System Access API と代替実装。フォルダ一括保存など | 不明 | 1,744,605 | 一括変換の保存先を選ばせる用途 | 使える |
| 40 | その他 | Squoosh-with-CLI（参考） https://github.com/frostoven/Squoosh-with-CLI | 111 | 検索の更新日のみ 2026-10-14（pushed_at 未取得） | apache-2.0（検索結果の key） | TypeScript | Squoosh の CLI 版フォーク | - | - | 一括処理の考え方の参考程度 | 使える（優先度低） |

注意: #40 は最終コミットを pushed_at ではなく検索結果の updatedAt で記載（精度が低い）。

## 分野ごとの推奨上位 3 件

### A. ブラウザ内の画像変換・圧縮アプリ全体

1. Squoosh（#1）: Apache-2.0。最も完成度の高い手本で PWA 化の例にもなる。コードをそのまま土台にすると大きすぎるので、UI・比較表示・設計の参考と、コーデックの考え方を得る用途。
2. filerobot-image-editor（#3）: MIT。編集機能（切り抜き・回転）を一式足したい場合の候補。見た目の統一は難しい見込み。
3. svgomg（#2）: MIT。SVG 最適化という別の需要を足す場合の UI 参考。

補足: ほか VERT（#5、AGPL）は同分野の有力競合で、「ローカル処理・無料」を掲げている。コードは使えないが市場調査の対象。

### B. WebAssembly のエンコーダ／デコーダ・変換部品

1. jSquash（#8）: Apache-2.0。webp・avif・jpeg・png・resize を個別に導入でき、週 DL も多い。今の Canvas 実装を置き換えて画質・容量を上げる第一候補。HEIC は含まない。
2. pica（#9）: MIT。リサイズの画質改善が目的ならこれ。単体で完結。
3. wasm-vips（#10）: MIT。高機能だが、COOP/COEP ヘッダの要件があり GitHub Pages では難しい見込み（推測）。Cloudflare Pages 等でヘッダを設定できるなら有力。

HEIC 変換は別枠: 使える MIT の heic2any（#14）は更新が止まっており（古い）、現役の heic-to（#12）は LGPL-3.0 で条件付き。どちらを採るかは「古い MIT」か「現役 LGPL」の二択で、方針判断が必要。

### C. EXIF の読み書き・削除

1. exifr（#22）: MIT。読み取りの定番だが 2 年以上更新なし（古い）。向き補正の取得などに使える。
2. ExifReader（#23）: MPL-2.0。現役で保守されている読み取り。ライセンス条件の確認が要る。
3. piexifjs（#24）: MIT。JPEG の EXIF 書き込み・削除ができる。古い（2021）。

補足（推測）: Canvas で再描画して書き出せば EXIF は落ちるはずで、「削除」だけなら部品なしで可能。再エンコードなしの無劣化削除には別の部品が必要。

### D. 一括処理と ZIP

1. fflate（#27）: MIT。約 8kB と軽量で週 DL も桁違い。
2. client-zip（#29）: MIT。ストリーミングで大量ファイル向き。作成のみ。
3. JSZip（#28）: MIT を選択して使う。定番だが、ライセンスが二択表記である点に注意。

### E. 切り抜き・トリミング UI

1. react-easy-crop（#31）: MIT。React 向けでタッチ操作に強い。
2. react-image-crop（#32）: ISC。矩形選択の UI が簡素で比率固定にも向く。
3. cropperjs（#33）: MIT。実績最大で、React 用ラッパーは別途必要。

### F. GitHub 風の見た目の部品

1. @primer/octicons（#37）: MIT。アイコンだけ使うのが最も低リスク。
2. @primer/css（#36）: MIT。見た目を寄せるなら CSS だけ取り込む。
3. @primer/react（#35）: MIT。本格的に作り替えるなら。既存の Tailwind との併用方針を先に決める必要あり。

## 参照のみだが参考になるもの

- VERT（#5、AGPL-3.0）: 同じ「ローカル変換」を掲げる競合。機能範囲・見せ方の調査対象。
- ImageOptim（#6、GPL-2.0）: Mac の最適化アプリ。機能と UX の参考。
- libheif（#16、LGPL）と libheif-js（#13、LGPL-3.0）: HEIC 対応の仕組みの理解。
- heic-to（#12、LGPL-3.0）: 現役の HEIC 変換。LGPL の wasm は「差し替え可能な形で提供する」等の条件付きで使える可能性がある。法的な確認は未了。
- heic-convert（#15）: GitHub と npm でライセンス表示が食い違うため参照のみ。

## 不明点

1. 容量（バンドルサイズ）: README に書かれていた fflate 以外は不明。bundlephobia は未確認。
2. heic2any（#14）の内部にある libheif のライセンス表記の扱い: 未確認。
3. heic-convert（#15）のライセンス: GitHub は無し、npm は ISC。どちらが正かは未確認。
4. @primer/css・@primer/react の今後の保守方針と、既存 Tailwind との相性: 未確認。
5. wasm-vips が GitHub Pages で動くか（ヘッダ設定の可否）: 推測のみで未検証。
6. react-advanced-cropper の LICENSE 実文: 未確認（npm は MIT）。

## 検索語句の一覧

GitHub 検索（gh search repos）: "browser image converter"、"image compressor browser webassembly"、"heic converter browser"、"exif remove browser javascript"、"image cropper react"、"client-side image resize webp avif"、"browser image converter react typescript"、"heic to jpg wasm"、"squoosh"、"heic2any"、"jsquash"、"wasm image codec"、"image converter wasm"、"pwa image compressor"、"avif encoder wasm"、"heic converter"、"exif"、"image resizer react"。語句によっては 0 件（長い英語句）か、スター 0 の個人作の量産リポジトリしか出なかったため、既知のライブラリ名を gh api repos/<owner>/<repo> で直接確認した。

直接確認した主なリポジトリ: squoosh、jSquash、libheif、libheif-js、heic2any、heic-to、heic-convert、wasm-vips、magick-wasm、pica、browser-image-compression、compressorjs、photon、ffmpeg.wasm、sharp、exifr、ExifReader、piexifjs、exif-js、exif-reader、fflate、JSZip、client-zip、zip.js、react-easy-crop、react-image-crop、cropperjs、react-advanced-cropper、filerobot-image-editor、tui.image-editor、primer/react・css・octicons、vite-plugin-pwa、browser-fs-access、VERT、svgomg、ImageOptim、ExifCleaner。

npm 週間ダウンロード: `https://api.npmjs.org/downloads/point/last-week/<pkg>`、ライセンス・バージョン: `https://registry.npmjs.org/<pkg>/latest`（2026-11-04 取得）。
