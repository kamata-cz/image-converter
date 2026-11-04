# ライセンスと公開先の調査（Claude 担当）

確認日: 2026-11-04。料金・上限は確認時点の値。法的な判断ではなく、公式ページの記述の整理である。契約・権利関係の最終判断は弁護士など専門家への確認が望ましい。
記号: 〔事実〕は公式ページの記述、〔推測〕は調査者の解釈。

## ① ライセンスの比較

前提: 現在のリポジトリに LICENSE ファイルは無い。公開リポジトリで、配信物（ブラウザに届く JavaScript）は誰でも読める。

| 型 | 他人のコピー・競合サービス | 自分が後から有料版を作るとき | 公開リポジトリのままでよいか |
|---|---|---|---|
| MIT | 〔事実〕商用利用・配布・改変が許される。条件は「著作権表示と許諾表示を含める」のみ（choosealicense.com / OSI） | 〔事実〕すでに公開した版は MIT のまま残る。〔推測〕以後の新しいコードを非公開にしたり別ライセンスにすることは、著作権者本人なら通常可能と読める（過去に公開した版の取り消しは想定されていない） | 可。公開のまま使う型 |
| Apache-2.0 | 〔事実〕商用利用・配布・改変・特許利用が許される。条件は、ライセンスの写しの添付、変更の明示、帰属表示の保持。商標の使用は許されない（choosealicense.com） | MIT と同様の構図。〔事実〕貢献者から特許の許諾が明示される | 可 |
| ライセンス無し（All rights reserved 相当） | 〔事実〕choosealicense.com は「ライセンスが無い作品は既定で著作権者の排他的権利の下にあり、他人が使用・改変・共有する許可は一般に無い」と説明。GitHub で公開しても広い再利用の権利は与えられない、とも書く。ただし GitHub の利用規約には、公開リポジトリを閲覧・フォークできる旨の定めが別にある（今回は規約本文を開いていない: 不明） | 制約が最も少ない（誰にも許諾していないため） | 可。ただし他人が合法的に再利用できる範囲が曖昧になる〔推測〕 |
| PolyForm Noncommercial 1.0.0 | 〔事実〕許される目的は非商用のみ（個人の研究・趣味、慈善・教育・公的機関など）。配布時は条項（または URL）と「Required Notice:」行を添える。〔推測〕競合サービスの商用運営は許諾の対象外と読める | 〔事実〕条文は著作権者自身には及ばないため、有料版の提供は通常の著作権者の立場でできると読める〔推測〕 | 可（ソース公開型）。OSI 承認のオープンソースではない〔推測。PolyForm は OSI 承認ではないと一般に説明される。今回は公式で直接確認していない〕 |
| Business Source License 1.1（BSL） | 〔事実〕Additional Use Grant で許す本番利用の範囲を著作権者が決める。「None」も可。変更日（最長でその版の初回公開から 4 年）に、指定した Change License（GPL v2 以降またはその互換）へ切り替わる（MariaDB の BSL 1.1 本文） | 変更日まで制限を維持できる。ただし変更日後はその版が GPL 系になる | 可。〔事実〕BSL は OSI のオープンソースではない（切り替え後にオープンソース化） |

実効性についての材料（〔推測〕を含む）
- ブラウザで動くツールは、配信される JavaScript（ビルド後、難読化しても）を誰でもダウンロードできる。ライセンスは、コピーを技術的に防ぐのではなく、コピーした相手に許諾が無いことを示す法的な根拠になる。実際の取り締まりの手間は個人には大きい。
- 競合に真似されにくい要素は、ライセンスよりも、サービスの運営（ドメイン、サポート、更新、ブランド）側にある〔推測〕。
- 有料化の候補（1 回 200 枚超と設定保存の買い切り）は、クライアント側で動くため、制限の判定も配信されるコード内に入る。ライセンスの種類に関わらず、判定を回避する改造は技術的に可能〔推測〕。ライセンスキーを検証する別サーバーが要るかどうかは本調査の範囲外。

初版を無料公開して将来有料化を考える個人への選択肢（推奨なし）

| 選択肢 | 長所 | 短所 |
|---|---|---|
| MIT | 信頼されやすく、貢献を受けやすい。依存と同じ型で表示の管理が一本化できる | 競合が同じコードで有料・広告サービスを出しても、ライセンス上は止められない |
| Apache-2.0 | 特許の許諾が明示される。依存に Apache-2.0 の @jsquash/webp を使う場合と型が揃う | 帰属表示・変更の明示など条件が MIT より多い。結論は MIT と同様に競合の自由 |
| ライセンス無し | 追加の許諾を与えない。後からどの型にも切り替えやすい | 他人が使ってよいか不明のため、貢献・再利用が実質止まる。「オープン」な印象は出ない |
| PolyForm Noncommercial | 見せるが商用は許さない意思を明確にできる | 型が新しく、法的な解釈の実績や GitHub 上の表示（ライセンス判別）が限られる可能性がある（不明）。貢献を受ける際の取り決めが別途必要になりうる〔推測〕 |
| BSL 1.1 | 変更日まで商用の競合を制限しつつソースを公開できる | 変更日後は GPL 系になる。個人の小さなツールには複雑〔推測〕 |
| 初版は MIT、有料版の新機能は別リポジトリ・非公開 | 公開部分は広く使われ、有料部分は手元に置ける | 公開済みの版は MIT のまま残る。2 つのコードの管理が増える |

## ② 依存の著作権表示の義務と載せ方

〔事実〕
- MIT: 「The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.」（OSI の MIT 本文）。
- Apache-2.0 第 4 条（apache.org の本文）: (a) ライセンスの写しを受け手に渡す。(b) 変更したファイルに変更した旨を明記する。(c) 配布する派生物のソース形式で、著作権・特許・商標・帰属の表示を保持する。(d) Work に NOTICE ファイルが付属する場合、配布する派生物に、その帰属表示の読める写しを、(i) 派生物と一緒に配布する NOTICE ファイル、(ii) 派生物と一緒に配布するソースまたは文書、(iii) 派生物が生成する画面で第三者の表示が通常出る場所、のいずれかに含める。NOTICE の内容は情報提供のためだけで、ライセンスを変更しない。

載せ方の候補（〔推測〕。いずれも法的な十分性の保証ではない）
1. ビルド時に依存のライセンス文を集めて、配信物に `THIRD-PARTY-NOTICES.txt`（同じオリジンで配る）として含め、画面のフッターから「オープンソースライセンス」リンクで開けるようにする。
2. Vite は依存のコードを 1 つの JS にまとめるため、ミニファイ時にコメントが落ちる。そのため、ファイルの先頭コメントに頼らず、1. のようにライセンス文を別ファイルで出すのが確実と考えられる。自動生成するプラグインやツールがあるが、今回は個別に検証していない（不明）。
3. 自分のコードに MIT／Apache-2.0 を付けるなら、リポジトリ直下に LICENSE を置き、Apache-2.0 の依存に NOTICE があれば、その内容も一覧に含める。
4. fflate（MIT）、@jsquash/webp（Apache-2.0。WASM を含む）の各 LICENSE と、NOTICE の有無はインストール後に node_modules 内で確認する必要がある（今回は未確認: 不明）。

## ③ 公開先の比較

商用の意味は「将来、有料機能（決済）や広告を入れる」場合。サイトに決済ページ自体を置くか、外部の決済サービスへリンクするだけかで規約の読み方が変わりうる〔推測〕。

| 公開先 | 無料で商用可か（規約の引用） | 帯域・ビルドの上限 | 独自ドメイン | 今の GitHub Actions からの移行の手間 |
|---|---|---|---|---|
| GitHub Pages | 不可寄り。GitHub 追加製品規約: 「GitHub Pages is not intended for or allowed to be used as a free web hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS).」 | 公開サイト 1 GB 以内、デプロイは 10 分でタイムアウト（GitHub Docs の Pages 上限）。規約には「may not be appropriate for some high-bandwidth uses」との記述。別の取得結果ではソフトな上限が 100 GB/月・ビルド 10 回/時（独自の Actions には適用されない）とされたが、Docs の最終的な本文での再確認はできていない（要確認） | 可〔GitHub Pages の機能。今回は個別ページを開いていない: 不明〕 | 現状のまま |
| Cloudflare Pages / Workers（無料） | 規約（cloudflare.com/terms）に、無料プランの商用利用を禁じる条文は今回見つからなかった。無料サービス部分では「We will have no liability for any harm or damage arising out of or in connection with any Free Services.」（2.6）と、無料サービスの対象のウェブでクレジットカード情報の処理・収集をしないこと（2.2.1(h)）が書かれている。商用可否は明示されていない（不明） | Pages 無料: ビルド 500 回/月、1 ファイル 25 MiB、2 万ファイル、独自ドメイン 100 個/プロジェクト。静的アセットのリクエストは無料・無制限（「On both free and paid plans, requests to static assets are free and unlimited.」）。Workers 無料は 1 日 10 万リクエストの上限があるが、静的アセットが数えられるかは Workers の上限ページに記載なし | 可（上記） | Wrangler か Git 連携で新規プロジェクトを作る。GitHub Actions から wrangler で配るか、リポジトリ連携に切り替える。比較的小さい作業〔推測〕 |
| Netlify（Free） | 利用規約ページには商用・広告の明示的な制限は見つからなかった。サービスの条件は別の Self-Serve Subscription Agreement と Acceptable Use Policy にあるが、今回は未取得（不明） | 月 300 クレジットのハードリミット、自動チャージなし。目安: 帯域 1 GB＝20 クレジット（約 15 GB）、本番デプロイ 1 回＝15 クレジット（約 20 回）、1 万リクエスト＝2 クレジット（約 150 万）。プレビュー・失敗デプロイは計測されない。上限到達時の挙動は未取得（不明） | 可（SSL つき。個数は記載なし） | Netlify 連携か CLI。リポジトリに `netlify.toml` が残っている。軽い作業〔推測〕 |
| Vercel（Hobby） | 不可。「Hobby teams are restricted to non-commercial personal use only. All commercial usage of the platform requires either a Pro or Enterprise plan.」商用の定義に「Any method of requesting or processing payment from visitors of the site」「The inclusion of advertisements, including but not limited to online advertising platforms like Google AdSense」を含む。「Asking for Donations does not fall under commercial usage.」（寄付は商用に当たらない） | Hobby の目安: Fast Data Transfer 最初の 100 GB など（Fair Use Guidelines） | 今回は未取得（不明） | Vercel 連携。Vite の静的サイトなので軽い〔推測〕 |

補足: 初版は寄付リンクのみのため、〔事実〕Vercel は寄付を商用に含めないと明記している。GitHub Pages の「商取引」の範囲に寄付リンクが入るかは規約の文面からは明確でない（不明）。

## ④ 独自ドメインの費用の目安

| 事業者 | .com | .jp | .app | 出典・注意 |
|---|---|---|---|---|
| Cloudflare Registrar | 公式は「Registration, transfer, and renewal prices are always at or below what registries and ICANN charge us.」。金額の表は取得できず（不明）。第三者サイトでは年約 10 ドル前後とする記述が複数あるが、サイトにより差があり未確認 | 対応 TLD 一覧（tld-policies）に .jp は無い | 対応（Google Registry）。金額は不明 | 公式ページに金額なし。2 年目以降も原価（at cost） |
| お名前.com | 新規 1 円（1 人 1 個まで）、2 個目以降 750 円（税込）。更新額は取得できず（不明） | 新規 1 円（1 人 1 個まで）、ローマ字 .jp の 2 個目以降 1,060 円（税込）。更新額は不明 | 公式の料金ページに記載なし | 新規受付停止の告知がページ上部にあった。更新料は「登録時期により異なる」と記載 |
| バリュードメイン | 登録 790 円（2 個目以降 1,390 円）、更新 2,283 円（税込・税抜の表記なし。「2026.11.30まで」の注記） | 登録 1,485 円、更新 3,889 円 | 掲載なし | 期間限定価格の可能性 |
| Porkbun（第三者の集計 tld-list.com 経由。公式ページは 403 で開けず） | 11.81 ドル（登録・更新同額） | 不明（.jp は未掲載） | 初年度 8.75 ドル、更新 14.93 ドル | 第三者サイト。事業者の特定が不確実なため目安 |

補足: 日本向けのサービスなら .com を想定するのが無難か、.jp が必要かは別途の判断材料。.jp は Cloudflare では扱えない（取得は他社になる）。

## ⑤ 出典一覧（すべて確認日 2026-11-04）

- https://choosealicense.com/licenses/ （MIT・Apache-2.0 の許可・条件）
- https://choosealicense.com/no-permission/ （ライセンス無しの扱い）
- https://opensource.org/license/mit （MIT の条文）
- https://www.apache.org/licenses/LICENSE-2.0.txt （第 4 条）
- https://polyformproject.org/licenses/noncommercial/1.0.0 （PolyForm Noncommercial）
- https://mariadb.com/bsl11/ （BSL 1.1）
- https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features （GitHub Pages の禁止用途）
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits （1 GB・10 分）
- https://developers.cloudflare.com/pages/platform/limits/ （Pages 無料の上限）
- https://developers.cloudflare.com/pages/functions/pricing/ （静的アセット無制限）
- https://developers.cloudflare.com/workers/platform/limits/ 、https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/
- https://www.cloudflare.com/terms/ （無料サービス条項）
- https://www.cloudflare.com/products/registrar/ 、https://www.cloudflare.com/tld-policies/
- https://www.netlify.com/pricing/ 、https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/ 、https://www.netlify.com/legal/terms-of-use/
- https://vercel.com/docs/limits/fair-use-guidelines （Hobby と商用）
- https://www.onamae.com/domain/ 、https://www.onamae.com/service/d-price/
- https://www.value-domain.com/
- https://tld-list.com/tld/com （第三者の集計）

## 不明点（未確認の項目）
1. GitHub Pages の帯域・独自ドメインの個別ページ未確認、寄付リンクが商取引に当たるかの文言
2. Cloudflare の商用可否の明示文（無料プラン）が規約に見つからない点、Registrar の金額
3. Netlify の Self-Serve Subscription Agreement と AUP の商用・広告の扱い、上限到達時の挙動
4. Vercel の独自ドメインの扱い（Hobby）
5. PolyForm が OSI 非承認である点の公式確認、GitHub でのライセンス表示
6. お名前.com の更新料金、.app の金額、Porkbun 公式の料金
7. fflate・@jsquash/webp の NOTICE の有無とライセンス文
