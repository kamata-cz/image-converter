# アクセス計測の調査（Claude 担当）

確認日: 2026-11-04（料金・上限は確認時点の値）。前提: ブラウザ内だけで画像を処理する静的サイト、GitHub Pages（独自ドメインなし）、日本の個人運営・初心者、初版は全部無料。
凡例: 「事実」は実際に開いたページに書かれていたこと。「推測」は私の判断。「不明」は今回確認できなかったこと。

## ① 比較表

| サービス | 無料の範囲 | 有料の最安 | 商用で無料のまま | Cookie・端末の識別子 | GitHub Pages で使えるか（1 行で入るか） | データの保存場所 | 日本語 | スクリプトの大きさ | 広告ブロッカー |
|---|---|---|---|---|---|---|---|---|---|
| GoatCounter（goatcounter.com） | 個人サイト・中小事業は無料。閲覧数の数値上限は書かれていない（「1 日に数百万」は不可） | なし（寄付: GitHub Sponsors） | 可。規約に「Running your personal website or small-to-medium business on it is fine」 | Cookie も localStorage もキャッシュも使わない。IP・User-Agent・サイト名から作る乱数 ID はメモリ上に最大 8 時間だけ | 可。1 行（`<script data-goatcounter=... async src="//gc.zgo.at/count.js">`） | Hetzner（フィンランド・ドイツ）。運営者はアイルランド | 管理画面の翻訳の項目はある。対応言語は不明 | 公式の説明で約 3.5KB | 止まることがある（公式ヘルプに、表示されないときは広告ブロッカーを疑う旨の注意） |
| Umami Cloud | Hobby: 月 10 万イベント、サイト 1 つ、データ 6 か月 | Pro 月 20 ドル（月 100 万イベント、14 日トライアル） | 不明（規約は未確認） | 不明（プライバシーページに Cookie の記載なし。IP は分析データの項目として保存しないが、ログには残り得ると記載） | 可（`<script defer data-website-id=...>` の 1 行。DNT 設定あり） | 不明（サブプロセッサ一覧を参照とだけ書かれていた） | 不明 | 不明 | 不明（標準のスクリプトは止まりやすいと一般に言われるが、公式で確認していない） |
| Plausible | 無料プランなし。30 日トライアル（カード不要） | Starter 月 9 ドル（月 1 万閲覧まで） | 有料のため該当せず | Cookie・キャッシュ・localStorage を使わない。1 日で捨てる塩を使ったハッシュでその日の訪問者を数える | 可（head に 1 行貼る） | EU 内のみ（エストニアの法人） | 不明 | 公式の主張で 2.5KB（Google アナリティクスは 135KB gzip と比較） | 止まることがある（公式がプロキシで回避する方法を案内しているため） |
| Simple Analytics | Free: サイト 5 つ、履歴 1 か月、バッジ表示が必須、閲覧数は無制限（公正利用） | 月 20 ドル（月 10 万閲覧のあたりから） | Free が商用可かどうか規約は未確認（「hobby sites 向け」と表記） | Cookie なし。端末を特定できる情報は取らないと記載 | 可（2 行のスクリプト） | EU と言われているが今回のページでは未確認で不明 | 不明 | 「圧縮している」とあるが数値は不明。軽量版（/light）あり | 回避機能あり（機能名のみ確認。詳細ページは 404 で未確認） |
| Counter.dev | 無料（寄付で運営） | なし | 不明（商用条件の記載を確認できなかった） | Cookie は使わない。ただし重複判定に sessionStorage・ブラウザキャッシュ・参照元を使う。公式 FAQ は「Cookie バナーを避けられるかは分からない」と書いている | 可（小さなインラインのスクリプト。実際の記述は未確認） | 不明（Redis と SQL。サーバーの場所の記載なし） | 不明 | 不明 | 不明 |
| Tinylytics | 無料プランなし。14 日トライアル（カード不要） | Zen 月 7 ドル（2 サイト、閲覧数は無制限だが 100 万超は公正利用） | 有料のため該当せず | Cookie・フィンガープリントなし | 可（`<script defer src=".../script.js" data-site=...>` の 1 行） | 不明 | 不明 | 不明 | 不明 |
| Fathom | 無料プランなし。7 日トライアル（カード必要） | 月 15 ドル（月 10 万閲覧、50 サイト） | 有料のため該当せず | Cookie なし。個人データを保存しないと記載 | 可（defer の 1 行） | EU の訪問者は欧州の事業者のインフラ経由。会社はカナダ | 不明 | 数値なし（軽量と記載） | 不明（回避方法の説明なし） |
| Cloudflare Web Analytics | 無料。Cloudflare のアカウントが必要。サイト数に上限あり（数値は未確認） | 不要（高度なエッジ分析は Pro 以上） | 不明（無料の規約は未確認） | Cookie・localStorage など端末側の保存を使わない。IP と User-Agent でのフィンガープリントもしないと記載 | 可。Cloudflare を通さないサイトは JS スニペットを貼る方式（`type="module"`、body の閉じタグの直前）。Referer ヘッダが必要 | 不明（海外へ個人情報を共有する同意項目あり） | 不明 | 不明 | 止まることがある（公式 FAQ に「一部の拡張機能が JS を止める」と明記） |

補足:
- 表の内容はそれぞれの公式ページ（④の出典）で確認した。「不明」は、ページに書かれていなかったか、開けなかった項目。
- Plausible の料金ページ（/pricing）は 404 だったため、トップページの記載（月 9 ドル〜）を使った。
- 「GitHub Pages で使えるか」は、いずれもスクリプトタグを貼るだけで動く仕様であることから、事実として「貼れる」と判断した。実際に表示されるかの動作確認は、Counter.dev と Umami と Tinylytics では行っていない（推測）。

## ② 推奨（初心者 1 人・無料・Cookie なし・GitHub Pages）

### 推奨 1: GoatCounter

事実:
- 無料で、規約に個人サイトも中小事業も可と書いてある。有料プランがなく、料金が突然発生する心配がない。
- 端末側には Cookie も localStorage も何も保存しない（公式のプライバシー説明）。
- 1 行のスクリプトで入る。スクリプトは約 3.5KB（公式の説明）。
- データは Hetzner（フィンランド・ドイツ）に置かれ、第三者へ共有しないと書かれている。オープンソースで、あとから自分でホストもできる。

推測:
- 初心者が 20 時間の予算の中で設定に使う時間は、30 分程度で済むはず。
- 欠点は、広告ブロッカーで数字が実際より少なく出ること。画像ツールの使い手（ブログ運営者）は広告ブロッカーを使う人が多いかもしれないので、数字は「最低でもこれだけ」と読む。
- 有料化して商用にした後も「中小事業は可」の範囲に収まりそうだが、規約が変わり得るので、その時点で再確認する。

### 推奨 2: Umami Cloud（Hobby）。ただし未確認の項目が多い

事実: 無料で月 10 万イベント・1 サイト・6 か月保存。1 行で入る。
不明: 商用条件、Cookie の有無、データの保存場所、スクリプトの大きさ。採用するなら、アカウントを作る前にこの 4 点を規約とプライバシーポリシーで確認する。

### 候補から外した理由
- Plausible、Fathom、Tinylytics、Simple Analytics（有料側）: 無料で使えない。Simple Analytics の Free はバッジ表示が必須で、商用可かどうかも未確認。
- Counter.dev: sessionStorage を使うため「端末に何も残さない」とは言えない。公式も Cookie 同意の要否は不明と書いている。
- Cloudflare Web Analytics: 無料で端末側の保存もしない有力候補。ただしプロジェクトの方針（Cloudflare は今は使わない）と合わない。方針を変えるなら 2 番手に上がる。

## ③ 日本の「外部送信規律」の結論

### 結論（1 行）
個人が運営する無料の画像変換ツールは、おそらく対象外（推測）。ただし総務省が個別のツールについて答えた資料は見つからなかったので、断定はしない。念のため、画面に短い説明を載せておくのが安全。

### 根拠（事実。出典は総務省の外部送信規律 FAQ とパンフレット）
- 根拠条文は電気通信事業法第 27 条の 12（2023 年 6 月 16 日施行）。利用者の端末から外部へ情報を送らせるタグなどを配る事業者が、事前に通知・公表する義務を負う。
- FAQ 問 1-7: Cookie を使っていなくても、端末から外部へ情報を送るよう指令するプログラムを送る行為なら対象になる。
- FAQ 問 1-8: 対象は「電気通信事業を営む者」で、「利用者の利益に及ぼす影響が少なくない電気通信役務」を提供する者。電気通信事業を営んでいなければ、外部送信があっても対象外。
- FAQ 問 1-9: 「影響が少なくない電気通信役務」は 4 種類に限られる。(1) 利用者間のメッセージ媒介、(2) SNS・電子掲示板・動画共有・オンラインモール等、(3) オンライン検索、(4) ニュース配信・気象情報・動画配信・地図等の各種情報のオンライン提供。
- FAQ 問 1-11: 利用者が少なくても、役務の種類で決まる（利用者数は関係しない）。
- FAQ 問 1-12・問 2-12: 本来の事業の手段としてサイトを使っているだけの場合や、自分の情報発信のために運営しているページは、電気通信事業に当たらず対象外。
- パンフレット（総務省 000862755.pdf）: 「企業・個人等が自己の情報発信のために運営しているホームページ・個人ブログ」は対象外と図示されているように読める。ただしこの PDF は文字化けして読み取りづらく、図の文言は復元した読みで、確実ではない。同じ趣旨は FAQ の問 1-12・問 2-12 でも確認できる。
- 「無料かどうか」を直接扱う Q&A、個人運営者を直接扱う Q&A は見つからなかった。

### 当てはめ（推測）
- このツールは、メッセージ媒介・SNS・検索・ニュース等の情報提供のいずれにも当たらず、画像は端末内で処理して送信しない。4 種類のどれにも当たらない可能性が高い。
- ただし (4) の「各種情報のオンライン提供」の範囲が広く、ツール型のサイトが入るかどうかを示した公式の例は確認できなかった。将来、ブログ記事や使い方の解説を載せて「情報提供」の性格が強まると、判断が変わり得る。
- 不安なら、総務省の外部送信規律の問い合わせ先に聞く方法がある（問い合わせ先は総務省の外部送信規律のページに載っている）。

### 対象だった場合に必要なこと（事実。FAQ 問 3・4・5）
通知か公表をする。公表は、情報の外部送信を指令するページ、またはそこから容易に行けるページに、次を載せる。
1. 送信される情報の内容（例: 閲覧したページの URL、閲覧した日時）
2. 送信先の氏名または名称
3. 送信先と自分における利用目的
4. オプトアウト（送信・利用の停止）の方法がある場合は、その案内（FAQ 問 5。ある場合の話）

書き方の決まり: 日本語、専門用語を避ける、拡大しなくても読める大きさ。利用目的は、送信先の公開ページへのリンクで示してもよい（日本語以外のリンク先ならリンクだけでは不可。リンク先の概要も添える）。

### 個人情報保護法との関係（一言）
今回確認していない（個人情報保護委員会の FAQ は開けなかったため、不明）。推測としては、アクセス解析の数字だけを見るなら、特定の個人を識別する情報は集めない前提で、個人情報の取り扱いが問題になる場面は小さい。ただし、サービス側が IP アドレスを一時的に処理している点（GoatCounter はメモリ上のみ）はプライバシー説明に書いておくと誠実。

### 画面に載せる文の案（念のための短い説明。送信先は採用した計測サービスに置き換える）
置き場所: フッターのリンクから行ける「プライバシーについて」ページ、または画面の下部。

> このサイトで使う画像は、お使いの端末の中だけで処理し、サイトの外へは送りません。
> 利用状況を知るため、アクセス解析サービス「GoatCounter」（運営: GoatCounter の運営者）を使っています。閲覧したページのアドレス、閲覧した日時、参照元のサイト、ブラウザの種類、画面の幅、おおよその地域、言語が、このサービスに送られます。Cookie は使わず、端末に何も保存しません。IP アドレスなどから作る識別用の番号は、最大 8 時間だけ記憶され、個人を特定するためには使いません。
> 目的は、ツールの改善に役立てるための、利用者数の集計です。詳しくは同サービスのプライバシーのページ（https://www.goatcounter.com/help/privacy）をご覧ください。

注意: 上の文は GoatCounter の公式説明（プライバシーのページ）に合わせて書いた。採用するサービスを変えたら、送信される情報と保存の説明を、そのサービスの公式説明に合わせて書き直す。

## ④ 計測しないで反応を見る方法（短く）

- GitHub のリポジトリの Traffic（Insights の Traffic）: リポジトリへの閲覧・クローンと参照元が見られる。ただし push 権限のある人だけ、保存は過去 14 日だけ。見られるのはリポジトリのページへの訪問で、公開した Pages のツールの利用数ではない（Pages の閲覧数は含まれないと推測。公式に明記されていたわけではなく、未確認）。
- Issue・Discussions: 「使ってみた」「困った」を書いてもらう。画面に Issue へのリンクを置く。
- スター数・フォーク数、寄付リンクのクリック（寄付サービス側の数字）。
- ブログやフォーラムでの紹介の数、検索で自分のサービス名を調べたときの出方。
- 画面に 1 行のアンケートリンク（Google フォーム等）を置く。
- 事実として、GitHub Pages は商取引・商用 SaaS の用途に使えない（GitHub Docs の「primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS)」）。有料化を考えるときはホスティングを変える前提。

## ⑤ 出典一覧（確認日はすべて 2026-11-04）

- GoatCounter 規約: https://www.goatcounter.com/terms
- GoatCounter プライバシー: https://www.goatcounter.com/help/privacy
- GoatCounter ヘルプ: https://www.goatcounter.com/help
- GoatCounter トップ: https://www.goatcounter.com/
- Umami 料金: https://umami.is/pricing
- Umami プライバシー: https://umami.is/privacy
- Umami トラッカー設定: https://docs.umami.is/docs/tracker-configuration
- Umami Cloud: https://docs.umami.is/docs/cloud
- Plausible トップ（料金・EU）: https://plausible.io/
- Plausible データポリシー: https://plausible.io/data-policy
- Plausible スクリプトの大きさ: https://plausible.io/lightweight-web-analytics
- Plausible スクリプト: https://plausible.io/docs/plausible-script
- Simple Analytics 料金: https://www.simpleanalytics.com/pricing
- Simple Analytics スクリプト: https://docs.simpleanalytics.com/script
- Counter.dev: https://counter.dev/ と https://github.com/ihucos/counter.dev
- Tinylytics 料金: https://tinylytics.app/pricing
- Fathom 料金: https://usefathom.com/pricing
- Fathom トップ: https://usefathom.com/
- Cloudflare Web Analytics: https://www.cloudflare.com/web-analytics/
- Cloudflare Web Analytics FAQ: https://developers.cloudflare.com/web-analytics/faq/
- Cloudflare Web Analytics 設定: https://developers.cloudflare.com/web-analytics/get-started/
- 総務省 外部送信規律: https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu.html
- 総務省 外部送信規律 FAQ: https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu_00002.html
- 総務省 外部送信規律 パンフレット: https://www.soumu.go.jp/main_content/000862755.pdf
- GitHub Docs（Traffic）: https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository
- GitHub Docs（Pages の制限）: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- 参考にしたが公式ではないもの（結論の根拠には使っていない）: 総務省会議資料に載った MyDataJapan の意見書 https://www.soumu.go.jp/main_content/000832491.pdf（意見であり総務省の見解ではない）

## 不明点・確認できなかったこと
1. Umami Cloud の商用条件、Cookie、保存場所、スクリプトの大きさ
2. Simple Analytics の Free の商用可否、データの保存場所
3. Counter.dev、Tinylytics、Fathom の商用・保存場所・スクリプトの大きさ（有料側は商用問題なし）
4. 日本語対応（どのサービスも管理画面の対応言語を確認できていない）
5. Cloudflare Web Analytics の無料の規約・サイト数の上限・データ保存場所
6. 外部送信規律: ツール型の無料サイトが第 4 号に入るかの公式の例、パンフレットの文字化けした部分
7. 個人情報保護法との関係の公式見解
