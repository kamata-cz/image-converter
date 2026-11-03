確認した範囲では、**一括処理の手間、HEIC・WebPの互換性、外部へのアップロード不安**に具体的な困りごとがありました。有料利用の体験談も確認できましたが、日本の検索需要や課金する人の割合を示す調査値は確認できていません。

確認日はすべて **2026-11-04** です。体験談は本人の申告として扱い、現在の製品仕様や市場全体の傾向とは区別しています。

## 1. 数字のまとめ表

### 利用環境・需要に関する数字

| 項目 | 確認できた値 | 調査主体・時期 | サンプル数・対象 | URL・注意点 |
|---|---|---|---|---|
| ホームページの画像転送量 | 中央値：デスクトップ **1,058KB**、モバイル **911KB** | HTTP Archive／Web Almanac 2025。原則2025年7月測定 | データセット全体は16,213,084サイト。デスクトップ12,155,374、モバイル15,426,398。個別指標の有効件数は本文に明記なし | [Page Weight](https://almanac.httparchive.org/en/2025/page-weight)、[測定方法](https://almanac.httparchive.org/en/2025/methodology) |
| 内部ページの画像転送量 | 中央値：デスクトップ **442KB**、モバイル **354KB** | 同上 | 同上 | [Page Weight](https://almanac.httparchive.org/en/2025/page-weight)。ホームページより少なく、画像が常に最大の構成要素とは限らない |
| ページ全体の転送量 | ホームページ中央値：デスクトップ **2,862KB**、モバイル **2,559KB** | 同上 | 同上 | [Page Weight](https://almanac.httparchive.org/en/2025/page-weight)。画像中央値をこの値で割っても「各ページの画像割合の中央値」にはならないため、割合は算出しない |
| WebP採用率 | **23.1%のWebサイト** | W3Techs／Q-Success。確認時点の表示値、日次更新 | 調査全体は2,000万サイト超。画像形式別の正確な母数は明記なし | [WebP](https://w3techs.com/technologies/details/im-webp)、[調査方法](https://w3techs.com/technologies)。画像ファイル数や利用者数の割合ではない |
| AVIF採用率 | **1.7%のWebサイト** | 同上 | 同上 | [AVIF](https://w3techs.com/technologies/details/im-avif)。ブラウザ対応率とは別の指標 |
| 日本の画像変換・圧縮・リサイズの月間検索数 | **不明：`not_found`** | 公表値を複数の語で検索したが、条件を確認できる値は見つからず | 不明 | キーワードツールの紹介は見つかったが、対象語の実測結果は取得できなかった |
| Googleトレンドでの需要比較 | **不明：`retrieval_failed`** | 日本を対象に比較ページを開こうとしたが、グラフ取得に失敗 | 不明 | なお、トレンドは原則0〜100の相対値であり、月間検索数ではない。[Google公式説明](https://support.google.com/trends/answer/4365533?hl=ja) |
| HEICで困る日本人の人数・割合 | **不明：`not_found`** | 人数・調査条件付きの公開調査は確認できず | 不明 | 下記の体験談から問題の存在は確認できるが、発生率は推定できない |

注意: HTTP Archiveは世界のWebサイトを対象とする実験室測定です。日本の利用者調査ではなく、空キャッシュ・ログアウト状態での測定です。[測定方法](https://almanac.httparchive.org/en/2025/methodology)

### 用途ごとの公式要件・料金

以下は調査統計ではなく、**確認時点の公式仕様・価格**です。サンプル数は該当しません。

| 用途・サービス | 確認できた数字・条件 | 利用者調査上の意味 | URL |
|---|---|---|---|
| BASEの商品画像 | 推奨 **1280×1280px**、**10MB以下／枚**、商品あたり20枚まで。登録形式はJPG・PNG・GIF | 容量だけでなく、形式と正方形への調整が必要になる | [商品登録方法](https://help.thebase.in/hc/ja/articles/43743736635161) |
| Shopifyの商品画像 | **20MB未満**、最大5000×5000pxまたは25メガピクセル。正方形は通常2048×2048pxを推奨 | 一貫した縦横比が必要。一方、HEIC・WebPを受け付け、表示形式・各サイズを自動処理する | [商品メディアの種類](https://help.shopify.com/ja/manual/products/product-media/product-media-types) |
| マイナンバーカードのオンライン申請 | JPEG/JPG、**20KB〜7MB**、幅・高さそれぞれ480〜6000px。**HEIC不可** | 「軽くする」だけでなく、形式・容量の上下限・寸法の同時確認が必要 | [写真データの制限](https://www.kojinbango-card.go.jp/faq_photo2/) |
| TinyPNG無料Web版 | 圧縮 **20枚／セッション**、**5MB／枚**。形式変換3件／セッション | 一括枚数・元画像容量が有料版との境界になっている | [公式料金](https://tinypng.com/pricing/web) |
| TinyPNG Web Pro | **月額換算US$3.25、年払い**。圧縮無制限、75MB／枚、広告なし | 上限解除・待ち時間・広告の削減を商品化 | [公式料金](https://tinypng.com/pricing/web) |
| TinyPNG Web Ultra | **月額換算US$12.42、年払い**。150MB／枚、変換無制限、フォルダ取り込みなど | 大量処理と作業工程の短縮を商品化 | [公式料金](https://tinypng.com/pricing/web) |
| Tinify API | 月500圧縮無料。その次の9,500圧縮は **US$0.009／圧縮** | WordPress連携など、手動操作を省く用途で従量課金 | [API料金](https://tinypng.com/pricing/api) |

## 2. 悩みの一覧

以下は、今回確認した資料で根拠が重なるものから並べています。市場全体の発生頻度を示す順位ではありません。

### 一括処理の枚数制限と、繰り返し操作が負担になる

- **ブログ利用者の体験**：WordPress用画像をTinyPNGで処理していた利用者が、「20枚ずつしか圧縮できない」「時々エラーが出る」と記載。圧縮待ちで更新が滞ることもあったと報告しています。2026年6月8日。[体験記事](https://note.com/usagi_artteacher/n/nc1164da2fb1b)
- **実際の有料利用**：写真の多いブログ運営者が、無料版では処理量が足りず有料版に移行。「100枚を超える画像も一遍に圧縮」できることを評価しています。2022年4月26日。[うみブログ](https://www2.kataseumi.com/entry/money-blogunei1)
- **教育現場の体験を記した制作者の記事**：保護者会資料用の40枚を、1枚ずつJPEGに保存し直したと報告しています。2026年6月9日。[学校でのHEIC変換体験](https://note.com/aki_6392/n/n2f5f6825843e)
- **開発者側の要望**：Squooshの公式FAQは、一括処理を「most-popular request」と説明しています。ただしFAQの更新は2021年で、現在の要望件数ではありません。2024年には一括処理を追加するPRも提出されています。[FAQ](https://github.com/GoogleChromeLabs/squoosh/wiki/FAQ)、[一括処理PR](https://github.com/GoogleChromeLabs/squoosh/pull/1428)

**事実から言えること**：単純な変換能力に加え、まとめて投入し、まとめて受け取る工程に不満があります。  
**不明なこと**：何枚から有料でも使いたくなるか、平均処理枚数。

### HEICは「閲覧できても、使いたい先で使えない」

- **個人の体験**：iPhone写真をクラウド経由でPCに取り込むとHEICになり、「HEICになって困ってた」と記載。「互換性優先」設定に変更して対処しています。2023年7月26日。[あお氏の記事](https://note.com/ao_life/n/na952a01b2d14)
- **学校での体験**：Windowsのフォトでは表示できた写真が、PowerPointのアルバム作成時には選べなかったと報告。これは当人の環境での経験で、現在の全Office環境に一般化できません。[学校でのHEIC変換体験](https://note.com/aki_6392/n/n2f5f6825843e)
- **同僚からの相談を解決した記事**：「他のPCでうまく開けない・使えない」という相談に対し、JPEG変換アプリを作成し、継続利用していると記載。2026年9月16日。[たっちゃん氏の記事](https://note.com/d04gt/n/ned11b70ea524)
- **公式要件でも存在**：マイナンバーカード申請はHEIC不可です。[公式FAQ](https://www.kojinbango-card.go.jp/faq_photo2/)

**事実から言えること**：「HEICを開く」と「提出・貼り付け先で使える形式にする」は別の課題です。  
**不明なこと**：日本での発生人数・頻度。

### WebPで保存すると、その後の編集・貼り付けが止まる

- **EC担当者の体験**：楽天画像がWebPで保存され、「そのままだ他のツールで使えなかったり」と記載。以前はChrome拡張で変換し、その後Macの自動処理に切り替えています。2026年3月16日。[EC担当者の記事](https://note.com/hanasanai_lab/n/n39aabc203b44)
- **素材配布者への問い合わせ**：配布画像を使えない場合の対処として、WebPからJPGへの変換方法を案内しています。2024年の記事、同年4月に対処法を追記。[配布素材のQ&A](https://note.com/clever_panda260/n/nfb8183ce8ed1)
- **日本語Reddit**：拡張子だけPNG/JPGに書き換えている投稿があり、本人も「二度手間になることもしばしば」と説明しています。[日本語の投稿](https://www.reddit.com/r/lowlevelaware/comments/1p6dr3m/)
- **海外参考**：NotabilityにWebPを貼れない不便さを訴える投稿があります。投稿当時の体験で、現在の対応状況は未確認です。[Reddit](https://www.reddit.com/r/notabilityapp/comments/1cqs698/support_for_webp_images/)

**事実から言えること**：「WebPへ変換する需要」と「WebPから戻す需要」の両方があります。  
**推測**：形式の説明を読ませるより、「資料に貼れる画像にする」など、目的で入口を示す方が伝わる可能性があります。

### 個人写真を変換サイトへ送った後、削除や悪用が心配になる

- **相談掲示板**：身分証と自撮り写真をオンラインでリサイズした利用者が、「本当に削除されているのか」と不安を投稿しています。実際の流出・被害は確認できていないと本人が記載。ページの最終更新表示は2025年4月28日です。[WEB110の相談](https://web110.com/forums/topic/オンライン画像圧縮サイトについて/)
- **学校での体験**：児童の顔写真を外部サーバーへ送れず、ソフトや拡張機能の導入にも管理者の制約があったと報告しています。[学校でのHEIC変換体験](https://note.com/aki_6392/n/n2f5f6825843e)
- **位置情報への関心を示す公式FAQ**：noteは、画像アップロード時にGPS等のEXIFを自動削除すると説明しています。ただし、このFAQだけから不安を持つ人数は分かりません。[note公式](https://www.help-note.com/hc/ja/articles/900000134923)

注意: WEB110の投稿にある暗号化・運営会社・脆弱性への疑念は、相談者の認識です。対象サービスの危険性を検証した結果ではありません。

### SNSは、画像寸法を合わせても表示時に見切れる

- **仕事でInstagramを使い始めた人の体験**：「4:5」に整えても上下が切れ、最終的に投稿画面の比率選択で解決しています。2026年9月8日。[初心者の投稿体験](https://note.com/proper_iris4198/n/na6ef50fc4022)
- **デザイン業務の体験**：プロフィール表示の変更でグリッド画像がずれ、Canvaに見切れ範囲のガイドを設定して対処しています。2025年1月26日。[制作担当者の記事](https://note.com/yu_toro/n/n6d659f9b048a)

**事実から言えること**：投稿画像そのもののサイズと、投稿先の表示・操作設定は別です。  
**推測**：リサイズだけでは解決せず、表示範囲のプレビューや投稿時の案内が必要になる場合があります。

### 品質スライダーでは、必要な容量に合わせにくい

Squooshには、形式ごとに品質設定の意味が違い、同容量で比較しにくいという要望があります。投稿者は「100kb」などの目標容量を入力し、品質を自動調整する機能と、達成できない場合の表示を求めています。2024年7月9日。[GitHub Issue #1422](https://github.com/GoogleChromeLabs/squoosh/issues/1422)

申請用途では、容量と形式の制限が実際にあります。ただし、このIssue自体は申請書類の相談ではなく、形式間の画質比較を目的とした要望です。[申請仕様](https://www.kojinbango-card.go.jp/faq_photo2/)

### 開発者は自動化できても、実行環境のトラブルが残る

Squoosh CLIでフォルダ内のJPGをWebPへ一括変換しようとして、Node.js環境に関連するエラーが出た報告があります。回避策の提案後も投稿者は解決しなかったと記載しています。2022年12月の事例です。[GitHub Issue #1304](https://github.com/GoogleChromeLabs/squoosh/issues/1304)

これは過去の特定環境の不具合です。現在のCLI全般が不安定だという根拠にはしません。

## 3. 今の工夫と、その工夫で解決していないこと

| 今の工夫 | 解決していること | 残っていること・限界 |
|---|---|---|
| iPhoneを「互換性優先」に設定する | 以後の撮影画像を扱いやすくする | 既存HEICは別途変換が必要。他人から受け取る写真にも対応できない。[体験記事](https://note.com/ao_life/n/na952a01b2d14) |
| フォト等で1枚ずつJPEG保存 | 必要な形式へ変換できる | 大量処理で操作が繰り返される。[40枚の事例](https://note.com/aki_6392/n/n2f5f6825843e) |
| 無料Webツールで小分けに圧縮 | 導入せず処理できる | 枚数制限、待ち時間、エラーへの対処。[ブログ利用者](https://note.com/usagi_artteacher/n/nc1164da2fb1b) |
| 有料Web版へ移行する | 大量処理・容量上限を緩和 | 継続費用。新ツールに乗り換える理由があるかは別途検証が必要。[有料利用体験](https://www2.kataseumi.com/entry/money-blogunei1) |
| Chrome拡張・Macの自動処理を使う | 保存後のWebP変換を省力化 | 導入・設定の負担。拡張が使えなくなる場合もある。[EC担当者](https://note.com/hanasanai_lab/n/n39aabc203b44) |
| 拡張子だけ書き換える | ファイル名は変わる | 中身の形式は変わらず、後で二度手間になる。[日本語Reddit](https://www.reddit.com/r/lowlevelaware/comments/1p6dr3m/) |
| WordPressプラグイン・APIを使う | 投稿時や既存画像の処理を自動化 | 費用、生成サムネイルの処理、二重圧縮への配慮。単体Webツールだけでは置き換えにくい。[運営者の体験](https://iwaimotors.com/blog/tinypng/) |
| Canvaのガイド・投稿側の比率選択を使う | 見切れを避けやすくする | 投稿先の仕様変更や操作理解が必要。[ガイドの例](https://note.com/yu_toro/n/n6d659f9b048a)、[投稿設定の例](https://note.com/proper_iris4198/n/na6ef50fc4022) |
| CLIを組み込む | 繰り返し処理を自動化 | 実行環境・コマンド・依存関係の管理。[過去の不具合例](https://github.com/GoogleChromeLabs/squoosh/issues/1304) |

### 有料でも払う理由

**支払いの体験として確認できたもの**

- **一括処理の制限を外すため**：うみブログの運営者は、100枚超をまとめて処理できることを評価し、当時TinyPNGへ年US$25を支払っていたと記載しています。これは2022年の記事中の支払額で、現在価格ではありません。[体験記事](https://www2.kataseumi.com/entry/money-blogunei1)
- **無料枠では既存画像を処理し終えられないため**：別のWordPress運営者は、有料圧縮を約2,900円分試したと記載しています。一方、速度評価の改善には満足しきれておらず、支払いと効果への納得は別問題です。2017年公開、2021年更新の記事です。[体験記事](https://iwaimotors.com/blog/tinypng/)

**販売条件として確認できたもの**

広告なし、大容量、フォルダ取り込み、変換無制限、API自動化は現行の有料商品に含まれます。ただし、今回確認した体験談では、**広告除去・透かし除去だけを理由に払った人は確認できませんでした**。[Web料金](https://tinypng.com/pricing/web)、[API料金](https://tinypng.com/pricing/api)

### 外部ツールが不要になる場面もある

- **note**：公式に画像を最適化すると説明しています。利用者の画像1枚の比較でも、事前圧縮の有無による最終容量の差は小さく、本人は事前圧縮をやめています。[公式仕様](https://www.help-note.com/hc/ja/articles/900000134923)、[個人の比較](https://note.com/usagi_artteacher/n/nc1164da2fb1b)
- **Shopify**：HEIC・WebPを受け付け、表示形式や各サイズを自動処理します。「ECだからWebP変換が必要」と一括りにはできません。[公式仕様](https://help.shopify.com/ja/manual/products/product-media/product-media-types)
- **メルカリ**：公式ガイドで確認できたのは、実物・細部・傷などを明確に示す要件です。今回、容量・ピクセル上限の確かな公式値は確認できませんでした。圧縮を主要課題と判断する根拠は不足しています。[出品者ガイドライン](https://help.jp.mercari.com/guide/articles/2015/)

## 4. 想定利用者像 4人

以下は実在人物のプロフィールではなく、確認した事実を基にした仮説です。

| 想定利用者 | 根拠として確認した事実 | 推測する利用場面・価値 | 未確認事項 |
|---|---|---|---|
| 写真の多いブログを運営する人 | 枚数制限・待ち時間への不満と、一括処理への有料支払いがある。[根拠](https://www2.kataseumi.com/entry/money-blogunei1) | 記事用写真をまとめて投入し、同じ幅・形式で一括保存したい | 現行の無料ツールから乗り換える理由、許容価格 |
| iPhone・iPad写真をWindowsの資料に使う人 | HEICの閲覧・貼り付け問題、1枚ずつの保存、導入権限の制約が報告されている。[根拠](https://note.com/aki_6392/n/n2f5f6825843e) | インストールせず、外部送信せず、写真を一括JPEG化したい | 個人で払えるか、組織の承認が必要か。対象環境での実動作 |
| 複数の販売先へ商品画像を準備する小規模EC担当 | WebP再利用の手間があり、BASEには形式・容量・正方形推奨がある。[体験](https://note.com/hanasanai_lab/n/n39aabc203b44)、[仕様](https://help.thebase.in/hc/ja/articles/43743736635161) | 商品を切らずに余白を付け、販売先ごとの画像をまとめて作りたい | 複数販路への加工頻度、既存編集ソフトでの充足度 |
| 申請・提出写真を一度だけ整えたい人 | 公的申請に形式・容量・寸法条件があり、身分証写真の外部送信を不安に思う相談もある。[仕様](https://www.kojinbango-card.go.jp/faq_photo2/)、[相談](https://web110.com/forums/topic/オンライン画像圧縮サイトについて/) | 条件を入力すると適否を確認でき、端末内で処理できると助かる | 利用頻度、支払意思。単発用途で継続課金が成立するか |

**企画上の推測**：今回の根拠では、課金の材料が比較的具体的なのは「写真を多く扱う人の繰り返し作業の短縮」です。プライバシーは利用可否を左右する条件ですが、それだけで支払うかは不明です。学校の事例では拡張機能も制限されており、Chrome拡張への移行が常に有利とは言えません。

## 5. 出典一覧

以下はすべて実際に開いて本文を確認したページです。**確認日：2026-11-04**。同じ出典の重複掲載は省いています。

| 分類 | 出典・URL |
|---|---|
| 統計 | [HTTP Archive：Page Weight 2025](https://almanac.httparchive.org/en/2025/page-weight) |
| 統計の条件 | [HTTP Archive：Methodology 2025](https://almanac.httparchive.org/en/2025/methodology) |
| 普及率 | [W3Techs：WebP](https://w3techs.com/technologies/details/im-webp) |
| 普及率 | [W3Techs：AVIF](https://w3techs.com/technologies/details/im-avif) |
| 普及率の条件 | [W3Techs：調査方法](https://w3techs.com/technologies) |
| 検索指標の説明 | [Googleトレンド：データに関するFAQ](https://support.google.com/trends/answer/4365533?hl=ja) |
| EC仕様 | [BASE：商品の登録方法](https://help.thebase.in/hc/ja/articles/43743736635161) |
| EC仕様 | [Shopify：商品メディアの種類](https://help.shopify.com/ja/manual/products/product-media/product-media-types) |
| フリマ仕様 | [メルカリ：出品者ガイドライン](https://help.jp.mercari.com/guide/articles/2015/) |
| 申請仕様 | [マイナンバーカード：写真データの制限](https://www.kojinbango-card.go.jp/faq_photo2/) |
| 投稿サービス仕様 | [note：画像について](https://www.help-note.com/hc/ja/articles/900000134923) |
| 現行価格 | [TinyPNG：Web料金](https://tinypng.com/pricing/web) |
| 現行価格 | [Tinify：API料金](https://tinypng.com/pricing/api) |
| 圧縮・一括処理 | [うさぎのりんご：note用画像の事前圧縮比較](https://note.com/usagi_artteacher/n/nc1164da2fb1b) |
| 有料利用 | [うみブログ：ブログ運営にかかるお金](https://www2.kataseumi.com/entry/money-blogunei1) |
| 有料利用・WordPress | [いわいともひさ：画像最適化の体験](https://iwaimotors.com/blog/tinypng/) |
| HEIC | [あお：iPhoneからクラウド経由で取り込む写真の形式](https://note.com/ao_life/n/na952a01b2d14) |
| HEIC・外部送信・導入制約 | [Akkyo：学校写真を一括JPEG変換するまでの体験](https://note.com/aki_6392/n/n2f5f6825843e) |
| HEIC・業務利用 | [たっちゃん：iPad写真を使えない相談への対応](https://note.com/d04gt/n/ned11b70ea524) |
| WebP・EC | [hanasan：楽天画像のWebP保存と自動変換](https://note.com/hanasanai_lab/n/n39aabc203b44) |
| WebP・素材配布 | [いつき：配布画像ダウンロードのQ&A](https://note.com/clever_panda260/n/nfb8183ce8ed1) |
| WebP・日本語の声 | [Reddit：拡張子を書き換える作業](https://www.reddit.com/r/lowlevelaware/comments/1p6dr3m/) |
| WebP・海外参考 | [Reddit：NotabilityへのWebP対応要望](https://www.reddit.com/r/notabilityapp/comments/1cqs698/support_for_webp_images/) |
| 外部送信への不安 | [WEB110：オンライン画像圧縮サイトについて](https://web110.com/forums/topic/オンライン画像圧縮サイトについて/) |
| SNS | [ひよっこエンジニアS：Instagram投稿時の見切れ](https://note.com/proper_iris4198/n/na6ef50fc4022) |
| SNS | [ゆうとろ：Instagram表示変更とガイド設定](https://note.com/yu_toro/n/n6d659f9b048a) |
| 一括処理要望 | [Squoosh公式FAQ](https://github.com/GoogleChromeLabs/squoosh/wiki/FAQ) |
| 一括処理の実装提案 | [Squoosh PR #1428](https://github.com/GoogleChromeLabs/squoosh/pull/1428) |
| 目標容量の要望 | [Squoosh Issue #1422](https://github.com/GoogleChromeLabs/squoosh/issues/1422) |
| 開発者の過去の不具合 | [Squoosh Issue #1304](https://github.com/GoogleChromeLabs/squoosh/issues/1304) |

補足: Xの直接投稿、知恵袋の利用者投稿については、今回の根拠として採用できる本文確認済み資料を確保できていません。声の収集は日本語note・ブログ・相談掲示板・Reddit・GitHubに偏っており、代表性のあるアンケート調査ではありません。