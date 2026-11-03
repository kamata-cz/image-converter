# A. 競合・既存ツール調査（Claude 版、照合用）

- 確認日: 2026-11-04（すべての URL・価格・数値は確認時点）
- 方法: WebFetch でページを実際に開いた内容のみを根拠にした。WebSearch の要約文だけで知ったことは「検索要約のみ」と明記し、事実としては扱わない
- 記号: 【事実】=開いたページに書いてあること / 【推測】=調査者の推測 / 不明=確認できず
- 注意: WebFetch は要約モデル経由のため、数値の列の意味が曖昧なものは「列の意味が不明」と書いた

---

## 1. 一覧表

### 1-1. Web ツール（海外・汎用）

| # | 名前 | 運営元 | 料金 | 主な機能・上限 | 処理場所 | 収益化 | 利用者数（推定） | 日本語 | URL |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Squoosh | GoogleChromeLabs（GitHub 上の表記。運営者名はページに無し） | 無料。Apache-2.0。GitHub star 26.1k | 1 枚ずつ処理。比較表示。対応形式一覧はトップページでは不明。バッチ機能なし。CLI は廃止（ベンダー記事の記述） | ブラウザ内（「Images never leave your device」） | なし（不明）。基本的な訪問データに Google Analytics を使用 | Similarweb 推定: 直近 3 か月で約 1.8M 訪問、世界順位 27,331。日本比率 7.61% / 6.79%（列の意味不明） | 不明（未確認） | https://squoosh.app/ ・ https://github.com/GoogleChromeLabs/squoosh |
| 2 | TinyPNG / TinyJPG | Tinify（社名はトップページで未確認） | Web Free 無料: 1 セッション 20 枚・1 枚 5MB・変換 3 枚。Web Pro $3.25/月（年払い）: 75MB・変換 3 枚/セッション・広告なし。Web Ultra $12.42/月（年払い）: 150MB・変換無制限・フォルダアップロード | AVIF/JXL/WebP/PNG/JPG 圧縮、HEIC→JPG、メタデータ削除、API（リサイズ・変換・切り抜き）、WordPress/Figma プラグイン、背景削除 | 不明（アップロード後 最長 48 時間保持して削除と記載。サーバー処理と読めるが明言なし） | サブスク + API 課金 | Similarweb 推定: 3 か月 2.3M 訪問、世界順位 33,813、日本 5.52%（別列 8.57%、意味不明） | 言語は中・英・西・仏のみ。日本語なし | https://tinypng.com/ ・ https://tinypng.com/pricing/web |
| 3 | iLoveIMG | iLoveIMG / iLovePDF 系（運営会社は未確認） | Free 無料。Premium 年払い 525 円/月（6,300 円/年）、月払い 930 円/月。Business 要相談 | 圧縮・リサイズ・変換・回転・透かし・切り抜き・画像編集・背景削除・アップスケール・顔ぼかし・ミーム。一括は Free 30 枚 / Premium 120 枚（表の列が「一括上限」かはページ上で未ラベル）。ファイルサイズ Free 200MB / Premium 4GB（1 タスク） | 不明（地域別処理を Premium で選べるとあり、サーバー処理と読める） | サブスク（広告なしは Premium のみ） | Similarweb 推定: 3 か月 34.1M 訪問、世界順位 1,318、日本 5.93% / 1.35%（列の意味不明） | 不明（未確認） | https://www.iloveimg.com/pricing |
| 4 | CloudConvert | 運営会社は未確認 | 無料: 1 日 10 クレジット、1GB、5 分処理上限、同時 5。有料: 買い切りパック（価格はページに表示なし）、月 1,000 クレジットのサブスク（価格表示なし） | 多形式変換 API。通常変換 1 クレジット、PDF→Office 4 | サーバー（ファイルをアップロードして変換） | クレジット販売・サブスク・API・法人 | Similarweb 推定: 3 か月 23.2M 訪問。米 23%、インド 15.87%。日本は上位 5 に無し | 不明 | https://cloudconvert.com/pricing |
| 5 | Convertio | 運営会社は未確認 | 無料: 1 ファイル 100MB・同時 2・24 時間で 10 分（利用規約）。Lite $11.99/月（年払い換算 $6.99）、Basic $22.99（$13.99）、Pro $44.99（$25.99） | 多形式変換。有料は広告なし | サーバー（Germany、利用規約）。ファイルは保存・バックアップしないと記載 | サブスク | Similarweb 推定: 3 か月 19.8M 訪問。ロシア 14.84%、ブラジル 11.49%。日本は上位 5 に無し | 不明 | https://convertio.co/pricing/ ・ https://convertio.co/terms |
| 6 | FreeConvert | 不明 | 無料: 1 日 20 分、1 ファイル 5 分まで。Basic $12.99/月、Standard $24.99、Pro $29.99（最大 5GB） | 多形式変換、API、有料は広告なし | サーバー（アップロード型と読めるが明言なし） | サブスク・API | 不明 | 日本語ページあり（検索結果の URL。ページ自体は未開封） | https://www.freeconvert.com/pricing |
| 7 | I Love Compress（ilovecompress.com） | 不明 | 無料（有料プランの記載なし） | 40 以上のツール（PDF・画像）。一括 25 枚。サイズ上限の記載なし | ブラウザ内（「processed locally」。AI 機能は不明） | 不明 | 不明 | 不明 | https://www.ilovecompress.com/ |
| 8 | BIRME | 不明 | 無料、登録不要。寄付リンクあり | 一括リサイズ、スマートクロップ、JPEG/WebP/AVIF 出力、透かし、枠、一括リネーム、AI 背景削除、AI 超解像、設定保存、フォルダ保存 | ブラウザ内（「nothing gets uploaded」） | 寄付 | 不明 | 不明 | https://www.birme.net/ |
| 9 | Adobe Express の WebP→JPG | Adobe | 無料（クレジットカード不要） | PNG/WebP 入力 40MB まで。変換後に編集へ誘導 | 不明 | 自社サブスクへの導線 | 不明 | 日本語版サイトはある（変換ページの日本語化は不明） | https://www.adobe.com/express/feature/image/convert/webp-to-jpg |
| 10 | heictojpg.com | JPEGmini 系（ページ上の記述から。運営社名は未確認） | 無料。JPEGmini Pro で無制限と案内（価格はページに無し） | HEIC→JPG、1 回 200 枚まで、デスクトップ版は 500 枚以上、変換後すぐ削除と記載 | 不明（「アップロード後すぐ削除」と書かれ、サーバー処理と読める） | 自社有料アプリへの誘導 | 不明 | 不明 | https://heictojpg.com/ |

### 1-2. Web ツール（日本語の変換サイト）

| # | 名前 | 運営元 | 料金 | 主な機能・上限 | 処理場所 | 収益化 | 利用者数 | URL |
|---|---|---|---|---|---|---|---|---|
| 11 | はちのすWebツール WebP 変換 | 株式会社はちのす制作 | 無料・登録不要 | PNG/JPG/GIF/HEIC/WebP 入力、WebP/JPG/PNG/AVIF 出力。一括 100 枚、30MB/枚（HEIC は 10MB/枚）、品質スライダー、リサイズ（幅指定・SNS・メディア・LP プリセット）、EXIF 自動削除、ZIP。GIF は先頭 1 コマのみ | ブラウザ内（「画像はサーバーに送信されません」） | 自社サービスへの集客（LLMO Branding の宣伝あり）。第三者広告の記載なし | 不明 | https://hachinosu-seisaku.co.jp/tools/webp-converter |
| 12 | LIBRA Works 画像変換 | LIBRA Works（法人情報は不明） | 無料と表記、有料プランの記載なし | JPEG/PNG/WebP/AVIF 相互変換、HEIC 入力、50MB/枚・200 枚/バッチ、品質・可逆 WebP・ファイル名ルール、report.csv、長辺リサイズ、EXIF 削除、sRGB 出力、オフライン可。HEIC は主画像のみ。アニメ非対応 | ブラウザ内（WebAssembly） | 不明 | 不明 | https://tools.itlibra.com/ja/image-converter |
| 13 | ToolBox 画像一括変換 | ToolBox（運営情報は別ページ） | 無料 | JPG/PNG/WebP/AVIF 入力、20 枚以上の一括、用途別プリセット、最大幅指定、EXIF 削除、ZIP。HEIC は別ツール | ブラウザ内 | 広告あり（「広告」表示と自社アプリのバナー） | 不明 | https://www.toolboxjp.com/tools/image-converter |
| 14 | サルワカ Web ツール（WebP 変換・PNG→JPEG・画像サイズ変更ほか） | サルワカ | 無料 | JPEG/PNG/GIF→WebP 一括、ZIP、PC・スマホ対応。上限の記載なし | ブラウザ内（「サーバーなどにも画像は送信されない」） | 不明（ツール群を掲載するメディア運営。広告の記載なし） | 不明 | https://saruwakakun.com/tools/ ・ https://saruwakakun.com/tools/png-jpeg-to-webp/ |
| 15 | GetWebP | GetWebP（法人情報なし） | 各ツール「無料・登録不要」。料金セクションへのリンクはあるが内容は未確認 | 14 ツール（PNG/JPG/HEIC/AVIF/WebP）、MCP・CLI・API・Chrome 拡張へのリンク。上限の記載なし | ブラウザ内 | 有料プランの有無は不明 | 不明 | https://getwebp.com/ja/tools |

### 1-3. Chrome 拡張

| # | 名前 | 運営元 | 料金 | 主な機能 | 処理場所 | 利用者数・評価 | URL |
|---|---|---|---|---|---|---|---|
| 16 | Save Image As Type | 個人（saveimageastype） | 無料（価格表示なし） | 右クリックで JPG/PNG/WebP 保存。JPG/WebP は品質調整可（JPG 既定 85%）。v1.5.9、最終更新 2026-09-12。英語のみ | 不明（「Website content」を収集と開示。同名の別 ID が複数あり、1 つは評価 1.0 と注意あり） | 約 70,000 ユーザー、4.7（175 件） | https://chromewebstore.google.com/detail/save-image-as-type/aninmieokgdbdcgoiglchhhhbpnpolja |

補足: 「Convert WebP to PNG」拡張のページは読み込めず内容不明。検索要約では「Save Image As PNG/JPG」（約 1,000 ユーザー、オフスクリーンキャンバスでローカル変換）等が存在するとあったが、ページは開いていない（検索要約のみ）。

### 1-4. OS 標準機能・デスクトップアプリ

| # | 名前 | 形 | 運営元 | 料金 | 主な機能・制限 | URL |
|---|---|---|---|---|---|---|
| 17 | Mac Finder クイックアクション「イメージを変換」 | OS 標準 | Apple | 無料 | Control クリック→クイックアクション→その他→「Convert Image」。形式とサイズを選択。例は HEIC→JPEG/PNG。複数ファイル対応・対応形式一覧は当該ページに記載なし（検索要約では複数一括可とあるが、公式ページでは未確認） | https://support.apple.com/guide/mac-help/perform-quick-actions-in-the-finder-on-mac-mchl97ff9142/mac |
| 18 | Mac プレビュー | OS 標準 | Apple | 無料 | 「画像ファイルの種類を変換」「書き出し」「サイズ変更」の項目がある（目次のみ確認。詳細ページは開けず） | https://support.apple.com/guide/preview/convert-and-export-image-files-prvw2dc3a8a8/mac |
| 19 | iPhone カメラ形式（HEIF / 互換優先） | OS 標準 | Apple | 無料 | 設定 > カメラ > フォーマット > 互換性優先で JPEG 撮影。Mac/PC への取り込み時に JPEG へ変換される場合があるが「保証はない」。共有経由でも変換される場合あり | https://support.apple.com/en-us/116944 |
| 20 | iPhone ショートカット | OS 標準 | Apple | 無料 | 公式ガイドのトップに画像変換アクションの言及なし（アクションの有無は不明） | https://support.apple.com/guide/shortcuts/welcome/ios |
| 21 | PowerToys Image Resizer | Windows 拡張 | Microsoft | 無料（OSS） | エクスプローラー右クリックで一括リサイズ。Fill/Fit/Stretch、単位は px/cm/inch/%、メタデータ削除、JPEG 品質、CLI あり。形式変換ツールではない（フォールバック符号化のみ） | https://learn.microsoft.com/en-us/windows/powertoys/image-resizer |
| 22 | ImageOptim | Mac アプリ | 個人（OSS） | 無料（寄付任意、GPL v2+） | JPEG/PNG/SVG/GIF の最適化、EXIF・GPS 削除、ドラッグ＆ドロップ。macOS 11 以降。Mac のみ | https://imageoptim.com/mac.html |
| 23 | XnConvert | Win/Mac/Linux アプリ | XnSoft | 個人・教育・非営利は無料。業務利用は 1 ライセンス 15 ユーロ（台数割引あり） | 500 以上の形式を読み込み、約 70 形式に書き出し。80 以上のアクション、プリセット、ウォッチフォルダ、CLI（NConvert） | https://www.xnview.com/en/xnconvert/ |
| 24 | ShortPixel | Web/プラグイン | ShortPixel | 無料プランあり（内容は不明）。月額無制限または買い切りクレジット（価格はページに無し） | 圧縮、WebP/AVIF 変換、BMP/TIFF→JPEG、CMYK→RGB | https://shortpixel.com/pricing |

### 1-5. 画像 CDN（参考）

| # | 名前 | 料金 | メモ | URL |
|---|---|---|---|---|
| 25 | Cloudinary | Free 無料（25 クレジット/月）、Plus $99/月（年払い $89）、Advanced $249/月（年払い $224） | 1 クレジット = 変換 1,000 回 / 保存 1GB / 帯域 1GB のいずれか | https://cloudinary.com/pricing |
| 26 | imgix | Starter $25/月（100 クレジット）、Basic $75、Midrange $150、Growth $300、Growth Plus $500 | 恒久無料プランなし（30 日・100 クレジットの試用）。Growth Plus の 1 クレジット単価の列は逆順に見えるとページ要約にあり、不確か | https://imgix.com/pricing |

### 1-6. 開けなかった・不明な対象（件数 5）

| 対象 | 状況 |
|---|---|
| ラッコツールズ（rakko.tools） | HTTP 429 で取得不可。検索でも実体を確認できず。不明 |
| PDF24 Tools の画像変換 | URL が 404。不明 |
| Compressor.io | HTTP 403。不明 |
| Windows ペイント / フォト | 公式サポート URL が 404。標準機能の詳細は不明 |
| Convert WebP to PNG（Chrome 拡張） | ページが読み込めず。不明 |

---

## 2. 料金と収益化の相場のまとめ

【事実】
- 無料の範囲: 海外の大手アップロード型は「1 回 20〜30 枚程度」「ファイルサイズ 5〜200MB」「1 日あたりの処理量制限」が基本。TinyPNG は 20 枚・5MB、iLoveIMG は 30 枚（Premium 120 枚）、Convertio は 100MB・同時 2・24 時間で 10 分、FreeConvert は 1 日 20 分、CloudConvert は 1 日 10 クレジット。
- ブラウザ内処理の無料ツールは、枚数・サイズ制限が緩い。はちのす 100 枚/30MB、LIBRA Works 200 枚/50MB、BIRME は上限記載なし。
- 課金の境目: 大量一括、大きなファイル、広告なし、同時処理数、API。個人向けの価格帯は、TinyPNG Web Pro $3.25/月（年払い）〜Ultra $12.42/月、iLoveIMG 525 円/月（年払い）〜930 円/月、Convertio $6.99〜$25.99/月（年払い換算）、FreeConvert $12.99〜$29.99/月。
- 開発者向け CDN は桁が違う: Cloudinary $89〜$249/月、imgix $25〜$500/月。
- ローカルアプリは無料または買い切りが多い。ImageOptim 無料、XnConvert 個人無料・業務 15 ユーロ、Compresto は買い切り（金額未確認、ベンダー記事）。
- 広告で回しているサイトの特徴（確認できた範囲）: ToolBox は広告表示と自社アプリのバナー。はちのすは第三者広告ではなく自社サービスの宣伝。heictojpg.com や Adobe Express は自社有料製品への誘導。純粋に広告のみで回していると確認できた例は ToolBox のみで、他は「別の本業への集客」型が多い。
- 無料で寄付のみ: BIRME（Buy me a coffee）。

【推測】
- 日本語の変換サイトは「自社の別事業への集客」「ツール群による SEO 流入」で成立しており、変換機能そのものを売る例は今回の範囲では見つからなかった。単体での課金は、TinyPNG・iLoveIMG のような大手でも「広告なし + 大量処理」が主因と考える。

---

## 3. 不満の上位

調査上の限界: Trustpilot は 5 つ星に偏る（Convertio 4.9/10,639 件、TinyPNG 4.7/31 件、iLoveIMG 4.9/1,534 件、CloudConvert 4.1/75 件）うえ、各社とも「最近レビュー依頼をしていない」と表示されており、不満の根拠としては弱い。Reddit・Twitter(X)・Qiita 等の実スレッドは開けておらず（検索結果は要約・ミラーのみ）、日本語の個人の不満は未収集。確認できたものだけ挙げる。

| 順位 | 不満 | 根拠（開いたページ） |
|---|---|---|
| 1 | Squoosh で一括処理ができない | 【事実】GitHub issue #1406「Bulk image upload & processing」は 2024-03-18 から未解決。冒頭投稿に 👍 約 11・🚀 約 9。引用: 「I often have to compress & resize lots of files with the same compression settings.」「Only issue is it lacks bulk processing...」。issue #1259 #1405 も未解決。有志フォーク（squoosh-multiple-export、bulk-squoosh、Squiish）が存在。https://github.com/GoogleChromeLabs/squoosh/issues/1406 、一覧 https://github.com/GoogleChromeLabs/squoosh/issues?q=is%3Aissue+batch 。日本語記事も「画像を複数変換する必要があると、web上だけだと少し面倒」と記述 https://zenn.dev/spalice/articles/485b05b6091c33 |
| 2 | Windows で画像形式変換 + リサイズを右クリックでやりたい | 【事実】PowerToys issue #2686「Offer option to encode images to another format」は 2020-05 から未解決、元投稿に 👍 88、コメントで約 50 追加。引用: 「All AI images produced in ComfyUI are .png by default, having to resize and convert them to .jpg is a pain.」 https://github.com/microsoft/PowerToys/issues/2686 。WebP 対応要望の issue（#36904, #34690, #23230）は閉じられている |
| 3 | 無料枠の上限に当たる | 【事実】CloudConvert の Trustpilot で「the website said that I had used up my free trial」「commonly limits you even when you havent used it for weeks」（4.1/75 件のサンプル）。https://www.trustpilot.com/review/cloudconvert.com 。Convertio の無料枠は 100MB・同時 2・24 時間 10 分（規約）。https://convertio.co/terms |
| 4 | サブスクの自動更新・解約忘れ | 【事実】TinyPNG の Trustpilot で複数レビューが自動更新に言及（「forgot to do it before my card was charged」等、いずれもサポートで解決と記載）。https://www.trustpilot.com/review/tinypng.com |
| 5 | 変換品質・動作不良 | 【事実】iLoveIMG の Trustpilot の AI 要約が「回転・背景削除・リサイズで期待どおり動かない」と記載（個別引用は開いたページに無し）。https://www.trustpilot.com/review/iloveimg.com |

補足: 「アップロード型のプライバシー懸念」は、競合ツールのブログ（比較記事）での主張が中心で、第三者の一次的な不満の引用は開けなかった。ここには数えない。

---

## 4. 既存ツールが手薄な点（機会）

### 4-1. 根拠となる事実

1. 日本語で「ブラウザ内処理 + HEIC 入力 + 一括 + リサイズ + EXIF 削除 + ZIP」を揃えた無料ツールは既に複数ある（はちのす: 100 枚・HEIC・SNS プリセット・EXIF 削除、LIBRA Works: 200 枚・HEIC・report.csv・オフライン可）。現行の画像コンバーターの機能単体では差別化しにくい。
2. 大手アップロード型（TinyPNG・iLoveIMG・Convertio・CloudConvert）は日本語対応が確認できないものが多く（TinyPNG は日本語なし）、日本の検索流入では日本語サイトが優位になりうる。ただし Similarweb 上は iLoveIMG の日本比率 5.93%、TinyPNG 5.52% と、日本からの利用自体は一定ある（列の意味は不明で推定）。
3. Squoosh は需要が大きい（3 か月 1.8M 訪問、star 26.1k）が、一括処理は 2022 年から未実装のまま、CLI も廃止（ベンダー記事の記述）。
4. PowerToys Image Resizer は形式変換ができない（公式ドキュメントに「This isn't a file type conversion tool」）。要望は 5 年以上未解決。
5. Mac は Finder のクイックアクションで HEIC→JPEG/PNG ができる（公式）。Windows の標準の形式変換は確認できず（ペイント/フォトのページは取得不可）。
6. 設定の保存は BIRME が対応。多くの日本語ツールは設定保存の記載なし。
7. 有料化は「大量処理・サイズ上限・広告なし・API」が境目。個人向けは $3〜$13/月が相場。
8. 日本語ツールの収益化は、別事業への集客か広告で、変換機能単体の課金例は見つからなかった。

### 4-2. 調査者の推測（根拠は上の事実）

- 無料ブラウザ内ツールは飽和気味で、「変換できる」だけでは有料化が難しい。課金するなら、機能ではなく「繰り返し作業の手間削減」（プリセット保存、命名規則、フォルダ保存、ウォッチ）か、「用途別の仕上げ（例: EC 向け・ブログ向け・SNS 向けのサイズ・容量の目標値に自動で合わせる）」が候補になる。
- Squoosh の「一括なし」への不満は強いが、有志フォークが複数あるため、「Squoosh 級の画質比較 + 一括」は競合が出始めている（2026 年 1 月の Squiish など）。
- PWA 化（ホーム画面追加、ファイル共有からの受け取り）は、iPhone の HEIC 変換・SNS サイズ合わせの場面で有利かもしれないが、今回の調査では市場の需要を裏付ける数値は取れていない。
- Chrome 拡張は「右クリックで WebP→JPG」の需要が約 7 万ユーザー規模で存在する（Save Image As Type）。ただし単機能で、課金の例は確認できていない。
- 日本語の不満の声（Yahoo!知恵袋、X、Qiita 等）は未収集のため、次の調査（利用者の声）で補う必要がある。

---

## 5. 出典一覧（すべて確認日 2026-11-04、実際に開いたページ）

### 開いて内容を確認したもの
- https://tinypng.com/ ・ https://tinypng.com/pricing/web
- https://squoosh.app/ ・ https://github.com/GoogleChromeLabs/squoosh
- https://www.iloveimg.com/pricing
- https://cloudconvert.com/pricing
- https://convertio.co/pricing/ ・ https://convertio.co/terms
- https://www.freeconvert.com/pricing
- https://www.ilovecompress.com/
- https://www.birme.net/
- https://www.adobe.com/express/feature/image/convert/webp-to-jpg
- https://heictojpg.com/
- https://hachinosu-seisaku.co.jp/tools/webp-converter
- https://tools.itlibra.com/ja/image-converter
- https://www.toolboxjp.com/tools/image-converter
- https://getwebp.com/ja/tools
- https://saruwakakun.com/ ・ https://saruwakakun.com/tools/ ・ https://saruwakakun.com/tools/png-jpeg-to-webp/
- https://chromewebstore.google.com/detail/save-image-as-type/aninmieokgdbdcgoiglchhhhbpnpolja
- https://support.apple.com/guide/mac-help/perform-quick-actions-in-the-finder-on-mac-mchl97ff9142/mac
- https://support.apple.com/guide/preview/convert-and-export-image-files-prvw2dc3a8a8/mac （目次のみ）
- https://support.apple.com/guide/preview/convert-image-file-types-prvw0b16d3ff/mac （目次のみ）
- https://support.apple.com/en-us/116944
- https://support.apple.com/guide/shortcuts/welcome/ios
- https://learn.microsoft.com/en-us/windows/powertoys/image-resizer
- https://imageoptim.com/mac.html
- https://www.xnview.com/en/xnconvert/
- https://shortpixel.com/pricing
- https://cloudinary.com/pricing ・ https://imgix.com/pricing
- Similarweb（推定値）: https://www.similarweb.com/website/tinypng.com/ ・ .../squoosh.app/ ・ .../iloveimg.com/ ・ .../convertio.co/ ・ .../cloudconvert.com/
- Trustpilot: https://www.trustpilot.com/review/convertio.co ・ .../tinypng.com ・ .../iloveimg.com ・ .../cloudconvert.com
- GitHub: https://github.com/GoogleChromeLabs/squoosh/issues?q=is%3Aissue+batch ・ https://github.com/GoogleChromeLabs/squoosh/issues/1406 ・ https://github.com/microsoft/PowerToys/issues/2686 ・ https://github.com/microsoft/PowerToys/issues?q=is%3Aissue+image+resizer+convert+format+webp
- https://compresto.app/blog/squoosh-alternative-mac （ベンダー記事。Squoosh の CLI 廃止・価格情報は自社比較の主張として扱う）
- https://zenn.dev/spalice/articles/485b05b6091c33
- https://lifestyle.assist-all.co.jp/?p=24414 （第三者の解説記事。サルワカ WebP の説明。数値は出典不明の宣伝的記述が含まれ、事実としては採用せず）

### 取得に失敗したもの
- https://tools.rakko.tools/ （名前解決失敗）、https://rakko.tools/ ・ https://rakko.tools/tools/ （429）
- https://tools.pdf24.org/ja/image-converter （404）
- https://compressor.io/ （403）
- https://support.microsoft.com/en-us/windows/resize-an-image-in-paint 他（404）
- https://chromewebstore.google.com/detail/convert-webp-to-png/egmjalgmmolinfenecmfaeognbjbiipi （内容なし）
- https://saruwakakun.com/tools/image-converter ・ https://www.iloveimg.com/privacy-policy （404）

### 検索要約のみで、ページ本体は開いていない（事実としては不採用、参考情報）
- Convertio の Lite $9.99/月・500MB という記述（料金ページの $11.99/月・1GB と食い違う。料金ページ側を採用。差の理由は不明）
- heictojpg.com の 1 日 50 枚制限（競合サイトの比較表の主張）
- ILoveCompress・BIRME 等の第三者評価
- 「Reddit では Squoosh は単一ファイルのみと批判される」というブログの要約（実スレッドは未確認）
