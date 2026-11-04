**今回の条件なら、まず OFUSE、オープンソース活動として受け付けるなら GitHub Sponsors が候補です。** Stripe Payment Links を日本の個人向け「寄付箱」として使う案は外します。Stripe の公式規定では、日本の「個人への寄付」が禁止・制限対象に含まれています。[Stripe 禁止業種・制限付き業種](https://stripe.com/jp/legal/restricted-businesses)

以下、**確認日はすべて2026年11月4日**。新規登録する日本在住の個人、成人向けコンテンツなし、ブラウザからの支援を前提とします。「不明」は、今回開けた公式資料では確定できなかった項目です。

## 1. 比較表

### 料金・出金・支払い方法

「サービス手数料」と「決済手数料」を分けて記載しています。日本円で受け取り、日本円で出金できる取引には、通常、為替換算は発生しません。

| サービス | サービス・決済手数料 | 日本の銀行への出金・最低額 | 出金・為替の費用 | 支援者の主な支払い方法 |
|---|---|---|---|---|
| **GitHub Sponsors** | 個人アカウントからの支援は手数料なし。組織からの支援には最大6%の料金 | 日本対応。Stripe Connect経由。規約上、原則として残高額にかかわらず月次送金。ただし越境送金には最低額が適用される場合あり | 日本への出金・通貨換算の個別料率は不明。支援プランは米ドル | クレジット・デビットカード。PayPalは非対応 |
| **Ko-fi** | 単発Tipsは無料モードならサービス料0%。新規のStandard設定では5%。月額Tips・会員・販売等は原則5%。**決済会社の料金が別途必要** | Ko-fi内に残高を持たず、PayPal／Stripeへ直接入金。銀行への最低額は接続先に従う | PayPal利用例：国内商用決済3.6%＋40円、標準出金は5万円未満250円。外貨換算は別途 | PayPal、カード、条件によりApple Pay・Google Pay等。日本のコンビニ対応は未確認 |
| **Buy Me a Coffee** | サービス料5%＋決済2.9%＋US$0.30。米国外取引は追加1%、継続支払いは追加0.5% | 日本対応、Stripe経由。初回US$10到達後に審査 | 出金処理0.5%。換算料・日本向けの最終適用額は不明 | 主要カード、Apple Pay、Google Pay。単発支援は支援者登録不要 |
| **OFUSE** | **単発16%＝サービス11%＋決済5%**。継続13%＝サービス8%＋決済5%。税込。2026年10月改定 | 国内銀行対応。売上500円以上で申請可能。口座登録後に審査 | **275円／出金**。海外カードの支援者側換算費は不明 | カード、Vプリカ、Apple Pay、Google Pay。**コンビニ支払いは受付停止中** |
| **Stripe Payment Links** | 一般のカード決済は3.6%。今回の個人寄付用途には採用しない | 一般の事業決済では国内銀行に対応。今回の用途としては対象外 | 通貨換算が必要なカード決済は追加2%。今回の寄付としての出金条件は該当なし | 一般機能ではカード・ウォレット等。金額自由入力方式ごとの利用可能手段は別確認が必要 |
| **PayPal.Me** | リンク作成無料。国内円建ての適格な個人間送金は無料。商用取引は3.6%＋40円、海外受取は追加0.5% | 国内銀行対応。**最低251円**。本人確認必要 | 標準出金は5万円未満250円、5万円以上無料。換算は種類により基本レートに3%／4%上乗せ | 個人間送金は残高・銀行口座。**カードは商品・サービスの購入用** |
| **Patreon** | 新規はサービス料10%。USD受取・カード決済例は追加2.9%＋US$0.30。受取通貨と支払通貨が異なる場合は換算2.5% | 日本の銀行へUSD→JPY送金に対応。最低US$10 | USD→現地通貨の銀行出金は**1.55%＋US$0.25**。別経路のPayPal／Payoneerにも料金あり | カード、PayPal、Apple Pay等。日本のコンビニ決済は未確認 |
| **pixivFANBOX** | 全年齢設定は10%。決済料の別加算は料金ページに記載なし | 国内銀行対応。5,000円未満でも「お急ぎ振込」が利用可能。最小申請額そのものは不明 | 銀行振込：3万円未満200円、3万円以上300円。PayPalへの送金は無料 | カード、PayPal、pixivcoban、コンビニ。コンビニは支援者に120円／決済 |
| **Amazonほしい物リスト** | 現金の受領ではなく物品のプレゼント。商品代・送料等が発生 | **銀行出金不可**。最低出金額は該当なし | 現金受取手数料は該当なし。外貨カードの費用はカード会社等による | 商品ごとの条件に従い、カード、ギフトカード、コンビニ等 |
| **note チップ** | 決済事務料：カード5%、PayPal6.5%、PayPay／Amazon Pay7%、キャリア15%、noteポイント10%。さらに**事務料控除後の10%** | 国内銀行対応。未振込売上合計1,000円以上から申請 | **270円／振込**。外貨受取の公式条件は不明 | 左記手段。ただし記事購入とチップでの利用条件の差は未確認 |

料金・出金の根拠：[GitHub料金](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/about-github-sponsors-for-open-source-contributors)、[GitHub追加規約](https://docs.github.com/en/site-policy/github-terms/github-sponsors-additional-terms)、[Ko-fi料金](https://ko-fi.com/pricing)、[Buy Me a Coffee手数料](https://help.buymeacoffee.com/en/articles/8105744-how-to-calculate-charges-on-your-payment)、[OFUSE料金改定](https://support.ofuse.me/hc/ja/articles/61615952263449-2026年10月1日から手数料はどう変わりますか)、[Stripe料金](https://stripe.com/jp/pricing)、[PayPal料金](https://www.paypal.com/jp/business/paypal-business-fees?locale.x=en_AD)、[Patreon料金](https://support.patreon.com/hc/en-gb/articles/11111747095181-Creator-fees-overview)、[FANBOX料金](https://fanbox.pixiv.help/hc/ja/articles/360003726293-手数料はいくらかかりますか)、[note料金](https://help-note.com/hc/ja/articles/360011358873)。

### 登録・個人情報・設置・用途

**運営会社に提出する本人情報と、支援者に公開される情報は別です。** 「本名を登録する必要がある」だけで「本名が一般公開される」とは判断していません。

| サービス | 登録・本人確認／本名・住所の公開 | 日本語対応 | リンク・ボタン | 無料ツールへの応援／特典付きの場合 |
|---|---|---|---|---|
| **GitHub Sponsors** | GitHub、銀行・税務情報、2段階認証、申請審査。非米国個人はW-8BEN。本当の身元で登録する必要あり。本名・住所の支援者への表示範囲は不明 | 日本語公式Docsあり。全画面の日本語化は未確認 | 承認後のSponsorsページへリンク。リポジトリには`.github/FUNDING.yml` | **OSSへの貢献が条件**。無料公開だけで自動的に対象とはならない。特典は公式に対応し、対価付き支援は規約上Subscriptionとして区別 |
| **Ko-fi** | Ko-fi登録＋PayPal／Stripe。Ko-fiの表示名は本名不要。ただし決済会社が氏名等を共有する場合あり | 確認した料金・ヘルプは英語。日本語UIは不明 | 公開ページURL、公式ウィジェット・埋め込み | 規約は見返りを期待しないTipsを明記。特典・商品提供は会員・販売等に分かれる。**接続先決済会社の規約も適用** |
| **Buy Me a Coffee** | アカウント、銀行・税務情報、Stripe側の本人確認、出金審査。支援者への本名・住所表示範囲は不明 | 今回確認した料金・ヘルプは英語。日本語UIは不明 | クリエイターページURLを設置 | 単発応援のみで利用可能。外部Webツールへの適用を明示した条項は未確認。特典・販売内容の履行責任は本人にある |
| **OFUSE** | 氏名、生年月日、性別、電話、住所、メール、振込口座。出金審査あり。本人確認書類の必須条件と一般公開範囲は不明 | 日本語 | 公開ページへのリンク、HTML埋め込みボタン | **Webサービス運営者も利用可能と明記**。ただし規約はメッセージ等を含む「有償サービス」の提供として構成され、税務上の純粋な贈与を保証するものではない |
| **Stripe Payment Links** | 事業・代表者・銀行情報等の審査。今回の個人寄付用途では登録候補から除外 | 日本語 | 管理画面で作った決済リンク | 日本の個人への寄付は対象外。将来の機能販売は別途審査する事業決済。名称だけ「チップ」に変えて利用可能とは判断できない |
| **PayPal.Me** | PayPal、本人確認、銀行口座。規約上、ページに**名前または事業者名、市区町村名等**を表示 | 日本語 | `paypal.me/ユーザー名`。金額・通貨指定も可能 | 個人・事業の支払いに使えるが、無料ツールへの不特定多数の応援を無料の個人間送金として扱えるかは不明。特典代金に個人間送金を使わない |
| **Patreon** | アカウント、出金・税務情報、求められる本人確認。確認済み本名は内部確認用でプロフィールには非表示。住所の公開範囲は不明 | 日本語料金ページあり。ヘルプは英語部分あり | クリエイターページURL | 創作活動への支援・有料会員・販売に対応。無料Webツールへの特典なし単発寄付を明示的に認める条項は未確認 |
| **pixivFANBOX** | アカウントと振込先等。本人確認書類の一律要件、本名・住所の支援者への公開範囲は不明 | 日本語 | FANBOXページ・プランURL | **月額支援が基本**。無料Webツールへの適用の明示は未確認。限定コンテンツ等は提供可能だが、特典の法的扱いは実態による |
| **Amazonほしい物リスト** | Amazonアカウントと配送先氏名・住所等。第三者への住所開示の現行詳細は公式ヘルプを取得できず不明 | 日本語 | リストを共有してURL設置 | 物品支援として利用できる。個人開発ツールへの支援を明示した規定は未確認。ツールの権利と交換する使い方は今回確認できず |
| **note チップ** | noteアカウント、公開記事、振込口座。本人確認書類の一律要件、本名・住所の公開範囲は不明 | 日本語 | 開発・使い方の記事を公開し、その記事へリンク。チップ設定を有効化 | 公開記事が必要。**規約上、チップはデジタルコンテンツの販売価格に加算される構成**。純粋な贈与専用の仕組みとは扱わない |

主な根拠：[GitHub登録条件](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account)、[GitHub税務情報](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/tax-information-for-github-sponsors)、[Ko-fi規約](https://more.ko-fi.com/terms)、[Ko-fi個人情報](https://help.ko-fi.com/hc/en-us/articles/115004001294-What-personal-information-is-shared-on-Ko-fi-as-a-creator)、[Buy Me a Coffee規約](https://buymeacoffee.com/terms)、[OFUSE対象者](https://support.ofuse.me/hc/ja/articles/4408188567065-どんな人がOFUSEで応援を受け取れますか)、[OFUSE登録情報](https://ofuse.me/beginner/creator)、[OFUSE規約](https://ofuse.me/terms)、[PayPal.Me規約](https://www.paypal.com/paypalme/pages/terms?country.x=JP&locale.x=ja_JP)、[Patreon本人確認](https://support.patreon.com/hc/en-us/articles/34582075437069-Account-Identity-Verification-FAQ)、[note規約](https://terms.help-note.com/hc/ja/articles/44943817565465-note-ご利用規約)。

**共通する判断：**「特典を付けたら必ず販売」「特典がなければ必ず贈与」とは断定できません。ただし、支払った人だけに処理上限解除・設定保存・限定版を提供する場合は、機能・利用権の対価として検討すべきです。サービス側の呼称と、日本の税法・特商法上の区分は一致するとは限りません。

## 2. 500円・1,000円・3,000円の計算例

税金、返金、チャージバック、支援者側の追加料金は含めません。固定の出金手数料は**寄付1件ごとではなく出金1回ごと**です。

### 日本円で計算できるケース

`A＝支援額`、`⌊x⌋＝小数点以下切り捨て`。

| サービス・条件 | 出金前に残る額の式 | 500円 | 1,000円 | 3,000円 |
|---|---|---:|---:|---:|
| Ko-fi無料モード＋PayPal国内商用料金 | `A－3.6%×A－40` | 442円 | 924円 | 2,852円 |
| 同上、各金額を1回ずつ銀行へ標準出金 | 上記－250円 | 192円 | 674円 | 2,602円 |
| OFUSE単発 | `A×(1－16%)` | 420円 | 840円 | 2,520円 |
| OFUSE継続 | `A×(1－13%)` | 435円 | 870円 | 2,610円 |
| FANBOX全年齢・1か月分 | `A－⌊A×10%⌋` | 450円 | 900円 | 2,700円 |
| 同上、銀行振込手数料控除後 | 上記－200円 | 250円 | 700円 | 2,500円 |
| note・カード | `A－⌊A×5%⌋－⌊(A－⌊A×5%⌋)×10%⌋` | 428円 | 855円 | 2,565円 |
| 同上、銀行振込手数料控除後 | 上記－270円 | 単独では通常申請不可 | 585円 | 2,295円 |
| PayPal.Me・適格な国内個人間送金 | `A` | 500円 | 1,000円 | 3,000円 |
| 同上、銀行へ標準出金 | `A－250` | 250円 | 750円 | 2,750円 |

注意点は次のとおりです。

- **Ko-fi：** Standardの5%が有効なら、さらに25円・50円・150円が引かれます。PayPalの国内商用料金を適用する比較例であり、今回の支援の取引区分を保証するものではありません。
- **OFUSE：** 出金できる場合は、上表からさらに275円。単発1,000円なら `840－275＝565円`、3,000円なら `2,520－275＝2,245円`。500円支援だけで出金できるかは、「売上500円以上」の判定が手数料控除前後のどちらか公式説明で確定できず不明です。
- **FANBOX：** 5,000円未満はお急ぎ振込を使う前提。最小申請額は不明のため、表は振込可能な場合の計算です。
- **PayPal.Me：** **今回の応援を無料の個人間送金として扱えるとは確認できていません。** 商用扱いなら、受取時にも3.6%＋40円が必要です。

出金条件の根拠：[OFUSE最低額](https://support.ofuse.me/hc/ja/articles/4408214374937-出金方法を知りたい)、[OFUSE出金料](https://support.ofuse.me/hc/ja/articles/4408207215641-出金時に手数料はかかりますか)、[FANBOXお急ぎ振込](https://fanbox.pixiv.help/hc/ja/articles/4409180384409-自分の好きなタイミングで支援金を受け取れますか)、[note計算例](https://help-note.com/hc/ja/articles/360011358873)、[note最低額](https://www.help-note.com/hc/ja/articles/360010430873)、[PayPal出金](https://www.paypal.com/jp/cshelp/article/paypalアカウントから資金を引き出すにはどうすればよいですか-help394)。

### 米ドル建て・現金以外・利用対象外

為替レートを作らず、`r＝適用される1米ドル当たりの円換算額`として示します。**支援者の円支払額と、開発者の円受取額では適用レートが異なる可能性があります。**

| サービス | 500円相当 | 1,000円相当 | 3,000円相当 | 計算の限界 |
|---|---:|---:|---:|---|
| GitHub Sponsors・個人から | 手数料控除前後で500円相当 | 1,000円相当 | 3,000円相当 | USD支援のため、円での銀行実受取額は不明 |
| Buy Me a Coffee・米国外の単発カード | `455.5－0.30r`円相当 | `911－0.30r`円相当 | `2,733－0.30r`円相当 | `A－5%A－2.9%A－1%A－US$0.30`。さらに出金0.5%・換算等。0.5%の計算基礎が不明のため銀行実額は不明 |
| Patreon・USD受取、USDカード支払い | `435.5－0.30r`円相当 | `871－0.30r`円相当 | `2,613－0.30r`円相当 | `A－10%A－2.9%A－US$0.30`。銀行出金時は残高から1.55%＋US$0.25。異通貨支払いなら換算2.5%等も加算 |
| Stripe Payment Links | 該当なし | 該当なし | 該当なし | 今回の日本の個人寄付用途には採用しない |
| Amazonほしい物リスト | 現金受取なし | 現金受取なし | 現金受取なし | 商品を受領。商品価値と送料を現金手取りに置き換えない |

Buy Me a CoffeeとPatreonは最低出金額にも達する必要があります。上記は料金構造の比較用で、銀行への着金を保証する見積額ではありません。[Buy Me a Coffee手数料](https://help.buymeacoffee.com/en/articles/8105744-how-to-calculate-charges-on-your-payment)、[Patreon出金](https://support.patreon.com/hc/en-us/articles/39694936541965-Payouts-guide-for-creators-outside-of-the-US)

## 3. 初心者1人への推奨

### OFUSE：日本向けにまず検討する候補

**確認できた事実**

- Webサービス運営者も利用対象。
- 日本語で登録・案内ができ、国内銀行へ出金できる。
- 外部リンクやHTMLボタンで受け付けられる。
- 単発16%＋出金275円。少額では負担が大きい。
- 利用規約は有償サービスとして構成されている。

**今回の条件からの判断**

日本の利用者向けで、20時間程度の開発時間を優先するなら、導入・説明の負担を小さくできる候補です。ただし、**「税務上も純粋な寄付になるから簡単」という理由では勧めません。** まず特典なしの「開発を応援する」リンク1つで始め、出金をまとめる運用が適しています。[対象者](https://support.ofuse.me/hc/ja/articles/4408188567065-どんな人がOFUSEで応援を受け取れますか)、[リンク・ボタン機能](https://ofuse.me/lp/creator)、[規約](https://ofuse.me/terms)

### GitHub Sponsors：OSSとして継続する場合の候補

**確認できた事実**

- OSSへの貢献が参加条件。
- 個人アカウントからの支援は100%が開発者に渡る。
- 日本対応。税務情報・2段階認証・審査が必要。
- 金額は米ドルで、支援者にもGitHubの利用が必要になる。

**今回の条件からの判断**

コードをOSSとして公開・保守する予定なら、開発活動と支援先が結び付き、料金面でも有利です。一方、写真ブログ運営者がGitHubに不慣れなら、支援までの負担が増える可能性があります。**OSSの条件を満たす場合の第2候補**です。[登録条件](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account)、[料金](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/about-github-sponsors-for-open-source-contributors)

サイトの案内文は、例えば次の内容にできます。

> このツールは無料で利用できます。気に入った方は、開発の継続を任意で応援できます。支援の有無によって使える機能は変わりません。

これは表示案です。この文言だけで、サービス規約・税務上の区分が決まるわけではありません。

## 4. 税・法律の注意

### 「寄付」という名前だけでは贈与税にならない

国税庁は、**個人から贈与で取得した財産は贈与税、法人から贈与で取得した財産は所得税**の対象と説明しています。暦年課税の基礎控除110万円は、**その年に受けた贈与全体の合計**についての控除です。支援者1人ごと、サービス1つごとの110万円ではありません。[国税庁 No.4402](https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4402.htm)

一方、国税庁はアプリ作成・配信等による収入について、原則として事業所得または雑所得として申告するよう案内しています。雑所得の基本計算は `総収入金額－必要経費` です。[申告漏れへの注意](https://www.nta.go.jp/taxes/shiraberu/shinkoku/tokushu/shinkoku-tyuui/index.htm)、[No.1500 雑所得](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1500.htm)

**今回への当てはめは未確定です。** 継続的な開発活動への応援、サービス契約上の収益、機能の対価などの実態を確認する必要があります。「特典なしだから年間110万円までは無条件に非課税」とは判断できません。受取日・総額・手数料・契約内容・出金額を保存し、税務署へこの条件を示して確認するのが適切です。

給与所得者の「20万円」の扱いも、一定条件での**所得税の申告要否**の話で、寄付全般の非課税枠ではありません。[国税庁 No.1900](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm)

### 特商法は物品販売だけでなく、有料機能・サービスにも関係する

消費者庁は通信販売の対象を、商品・権利の販売や有償の役務提供と説明しています。反復継続して営利目的の取引を行う場合、**個人も販売業者・役務提供事業者になり得ます。**[消費者庁 通信販売のルール](https://www.no-trouble.caa.go.jp/what/mailorder/rule.html)、[通信販売の定義](https://www.no-trouble.caa.go.jp/what/mailorder/)

したがって、次のように分けて考えます。

| 受け付け方 | 今回の判断 |
|---|---|
| 完全任意で、支払わなくても機能・権利が変わらない支援 | 真に贈与だけなら、通信販売の定義には通常当てはまらないと考えられる。ただし今回の契約への適用は未確定 |
| 支払った人だけ200枚超の処理や設定保存を使える | 有料機能・利用権の提供として、通信販売の表示等を検討する |
| OFUSE・note等を経由する応援 | サービス側が有償契約として構成している点も確認する。外部サービス利用だけで表示義務が消えるわけではない |

通信販売に該当する場合、氏名・住所・電話番号等の表示が基本です。一部を省略できる制度はありますが、**請求があれば申込み前に十分な余裕をもって開示できる措置**などが条件です。単に「個人なので非公開」とする制度ではありません。[消費者庁 表示事項の省略](https://www.no-trouble.caa.go.jp/what/mailorder/)

### 支援者に寄附金控除を案内しない

国税庁の寄附金控除は、国・地方公共団体・特定公益増進法人等への「特定寄附金」が対象です。今回の個人開発者への通常の応援を、控除対象と案内する根拠はありません。[国税庁 No.1150](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1150.htm)

### GitHub Pagesの制限は別に残る

GitHub Pagesは、オンライン事業、電子商取引、商取引を主目的とするサイト、商用SaaSの無料ホスティングとして使えません。**外部決済リンクにすれば、有料機能の提供も許可されるとは読めません。** また、無料OSSツールへの任意支援リンクについての明示的な許可・禁止は、今回開いた制限ページでは確認できませんでした。[GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

初版の無料機能と任意応援を維持し、有料機能を始める段階でホスティングの条件も再確認する、という分岐が必要です。

## 5. 出典一覧

以下はすべて公式ページ。**確認日：2026年11月4日**です。

| 対象 | 開いて確認した主な資料 |
|---|---|
| GitHub Sponsors | [対象・料金](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/about-github-sponsors-for-open-source-contributors)、[登録](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account)、[追加規約・出金](https://docs.github.com/en/site-policy/github-terms/github-sponsors-additional-terms)、[税務情報](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/tax-information-for-github-sponsors)、[支払い方法](https://docs.github.com/ja/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes) |
| Ko-fi | [料金](https://ko-fi.com/pricing)、[手数料・対応通貨](https://help.ko-fi.com/hc/en-us/articles/360002506494-Does-Ko-fi-take-a-fee)、[受取方法](https://help.ko-fi.com/hc/en-us/articles/115003980093-How-do-I-get-paid)、[個人情報](https://help.ko-fi.com/hc/en-us/articles/115004001294-What-personal-information-is-shared-on-Ko-fi-as-a-creator)、[規約](https://more.ko-fi.com/terms) |
| Buy Me a Coffee | [料金内訳](https://help.buymeacoffee.com/en/articles/8105744-how-to-calculate-charges-on-your-payment)、[日本を含む出金対応国](https://help.buymeacoffee.com/en/articles/6258038-supported-countries-for-payouts-on-buy-me-a-coffee)、[最低額・支払い方法](https://help.buymeacoffee.com/en/articles/4539170-frequently-asked-questions)、[規約](https://buymeacoffee.com/terms)、[プライバシー](https://buymeacoffee.com/privacy-policy) |
| OFUSE | [料金改定](https://support.ofuse.me/hc/ja/articles/61615952263449-2026年10月1日から手数料はどう変わりますか)、[最低出金額](https://support.ofuse.me/hc/ja/articles/4408214374937-出金方法を知りたい)、[出金手数料](https://support.ofuse.me/hc/ja/articles/4408207215641-出金時に手数料はかかりますか)、[支払い方法](https://support.ofuse.me/hc/ja/articles/4408196995097-利用可能な決済方法には何がありますか)、[対象者](https://support.ofuse.me/hc/ja/articles/4408188567065-どんな人がOFUSEで応援を受け取れますか)、[登録](https://ofuse.me/beginner/creator)、[規約](https://ofuse.me/terms) |
| Stripe | [料金](https://stripe.com/jp/pricing)、[日本の個人寄付に関する制限](https://stripe.com/jp/legal/restricted-businesses) |
| PayPal.Me | [機能・受取](https://pep.paypal.com/jp/cshelp/article/paypalmeとは何ですか-help432)、[規約・公開情報](https://www.paypal.com/paypalme/pages/terms?country.x=JP&locale.x=ja_JP)、[支払い方法の制限](https://www.paypal.com/jp/cshelp/article/送金方法を教えてください。-help293?locale.x=ja_JP)、[料金](https://www.paypal.com/jp/business/paypal-business-fees?locale.x=en_AD)、[出金](https://www.paypal.com/jp/cshelp/article/paypalアカウントから資金を引き出すにはどうすればよいですか-help394) |
| Patreon | [日本語料金](https://www.patreon.com/ja-JP/pricing)、[詳細手数料](https://support.patreon.com/hc/en-gb/articles/11111747095181-Creator-fees-overview)、[日本への出金](https://support.patreon.com/hc/en-us/articles/39694936541965-Payouts-guide-for-creators-outside-of-the-US)、[本人確認](https://support.patreon.com/hc/en-us/articles/34582075437069-Account-Identity-Verification-FAQ)、[規約](https://www.patreon.com/policy/legal) |
| pixivFANBOX | [料金](https://fanbox.pixiv.help/hc/ja/articles/360003726293-手数料はいくらかかりますか)、[お急ぎ振込](https://fanbox.pixiv.help/hc/ja/articles/4409180384409-自分の好きなタイミングで支援金を受け取れますか)、[支払い方法](https://fanbox.pixiv.help/hc/ja/articles/360003698754-どのような支払い方法がありますか)、[プラン・特典の注意](https://fanbox.pixiv.help/hc/ja/articles/4508413752089-プランを作るときの注意点) |
| Amazon | [ほしい物リスト作成・共有の公式案内](https://www.aboutamazon.jp/news/disaster-relief/how-to-create-a-wish-list-for-disaster-area-support)、[登録・配送先・支払い方法](https://www.aboutamazon.jp/news/guide/how-to-shop-in-amazon) |
| note | [料金・計算方法](https://help-note.com/hc/ja/articles/360011358873)、[出金条件](https://www.help-note.com/hc/ja/articles/360010430873)、[売上金・預かり期限](https://www.help-note.com/hc/ja/articles/360011270774-売上金について)、[チップ設定](https://www.help-note.com/hc/ja/articles/900001329223-チップ-サポート-機能のオン・オフを切り替える)、[規約](https://terms.help-note.com/hc/ja/articles/44943817565465-note-ご利用規約) |
| 公的資料 | 国税庁 [贈与税](https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4402.htm)、[雑所得](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1500.htm)、[ネット収入の申告](https://www.nta.go.jp/taxes/shiraberu/shinkoku/tokushu/shinkoku-tyuui/index.htm)、[給与所得者の申告](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm)、[寄附金控除](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1150.htm)。消費者庁 [通信販売](https://www.no-trouble.caa.go.jp/what/mailorder/)、[インターネット通販のルール](https://www.no-trouble.caa.go.jp/what/mailorder/rule.html) |

取得上の限界：FANBOXの利用規約本文とAmazonの詳細ヘルプは取得できず、該当する規約・公開情報は不明としました。Stripeの寄付ヘルプも取得エラーとなりましたが、個人寄付の制限は別の公式規定本文で確認しています。