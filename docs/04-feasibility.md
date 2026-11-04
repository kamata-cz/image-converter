# 4 実現性の検証（2026-11-04）

要件定義書（`03-requirements.md`）の 6「技術と規約の前提」を、小さな試作（`spike/`）で 3 つのブラウザの部品（エンジン）について実測した結果。

- 測った環境: macOS 27.2、Apple M1 Max（10 コア、メモリ 64GB）。Playwright 1.57 でヘッドレス（画面を出さない）起動
  - Chromium 145.0.7632.6（Chrome・Edge と同じエンジン。headless shell 版）
  - Firefox 144.0.2（Playwright 用のビルド）
  - WebKit 26.0（Safari と同じエンジン。Playwright 用のビルドで、本物の Safari とは細部が違う → ⑤）
- 試験用の写真: ページ内で作った 4032×3024 の合成写真 20 枚（ぼかした図形・細かい線・ノイズ入り、JPEG 品質 0.92、2.1〜7.2MB。ノイズの強さを 1 枚ずつ変えて、軽くしにくい写真も混ぜた）。200 枚の試験は同じ 20 枚を 10 回ずつ使い、毎回読み込み直した
- 数値はすべて各条件 1 回だけの実測（生データ: `spike/measured/*.json`）。時間は ±10% 程度ぶれうる。この Mac は速いので、一般的なノート PC では時間が 2〜3 倍になると見込む（推測）
- 用語:
  - **メインスレッド**: 画面の描画とボタン操作を受け持つ処理の流れ。ここで重い処理をすると画面が固まる
  - **Worker（Web Worker）**: 画面とは別の流れで処理を動かす仕組み。**OffscreenCanvas** は Worker の中で使える画像の描画面
  - **画面の止まり**: メインスレッドで 10ms ごとのタイマーを動かし、次に動くまでの最大の間隔を測った。60ms を超えた回数も数えた（60ms ≒ 50ms 以上タイマーが動けなかった）
  - **RSS 増**: ブラウザの全プロセスが使う実メモリ（`ps` の RSS の合計）の、試験中の最大値と開始時の差。大まかな目安
  - **探索回数**: 目標容量に収めるために画質を変えて書き出した回数

---

## ① 4a 技術の確定

| 区分 | 候補 | 採否 | 理由（実測） | 決定的な欠点 | 乗り換える条件 |
|---|---|---|---|---|---|
| 処理の場所 | **Worker＋OffscreenCanvas**（4 並列） | **採用** | 200 枚で画面の止まりが Chromium 最大 15ms・WebKit 16ms。並列で速くなる（Chromium 178s→47s） | Firefox では Worker でも 1 枚ごとに最大 176ms 止まる（原因は読み込み。下の「読み込み」の行） | — |
| 処理の場所 | メインスレッドだけ | 不採用 | Chromium だけは止まらない（最大 42ms） | Firefox で最大 367ms・WebKit で最大 300ms 止まり、200 枚の間ずっと続く（60ms 超が 175 回・206 回） | — |
| 読み込み | createImageBitmap（Worker 内） | **採用（基本）** | 3 エンジンとも EXIF の向きを自動で直す。壊れたファイルは 0〜2ms で例外になり捕まえられる | Firefox では Worker 内でも画面が止まる（20 枚で最大 126ms、60ms 超 16 回） | — |
| 読み込み | ImageDecoder（WebCodecs、Worker 内） | **条件付き採用（Firefox だけ）** | Firefox で画面の止まりが最大 26ms・60ms 超 0 回に下がった。向き 6・8 も正しく出た | WebKit には無い。Chromium は向きを `rotation` で返すので描き方が違う | Firefox の止まりが気にならなければ入れない（実装を単純にする） |
| ZIP | **fflate の Zip（ストリーム、無圧縮 ZipPassThrough）** | **採用** | 500MB を 1.7〜2.2s。3 エンジンとも保存でき、`unzip -t` で壊れなし、フォルダ構成どおり。日本語名に UTF-8 の印が付く | ZIP64 を書けない（ソースに読み取り用しか無い）ので、ZIP 1 つは 4GB・65,535 件まで | 1 回の ZIP が 4GB か 65,535 件を超える使い方が要るとき → client-zip |
| ZIP | fflate の zipSync | 不採用 | 速さは同じ（1.6〜2.3s） | 全部をメモリに読むので、500MB で RSS 増 1.5〜2.1GB、JS ヒープ 404MB（Chromium） | — |
| ZIP | client-zip 2.5 | 予備 | ZIP64 に対応。Chromium・Firefox では RSS 増が少ない（575MB・507MB） | WebKit で RSS 増 2,668MB と最も多い。Firefox で 4.5s と遅い | 上の fflate の乗り換え条件 |
| フォルダ読み込み | **`<input webkitdirectory>`** | **採用（主）** | 3 エンジンとも 3 階層下まで相対パスつきで読めた | Playwright の WebKit では隠しファイル（`.DS_Store`）が来なかった（件数がエンジンで違いうる） | — |
| フォルダ読み込み | **ドロップ（webkitGetAsEntry で再帰）** | **採用（補助）** | Chromium で実際のドロップを再現し、13 件・250 件とも全部読めた | Firefox・WebKit は自動化できず未測定（⑤で手動確認） | 手動確認で読めなければ、そのブラウザでは「フォルダを選ぶ」ボタンへ案内 |
| フォルダ読み込み | showDirectoryPicker | 不採用 | — | Chromium だけ（Firefox・WebKit は無いことを確認） | — |

---

## ② 測定結果

判定: **できる**＝3 エンジンで問題なし／**条件付き**＝条件や工夫が要る／**できない**。

### 1. フォルダ選択（webkitdirectory）— 判定: できる

| 前提 | 方法 | Chromium | Firefox | WebKit |
|---|---|---|---|---|
| 3 階層・画像と画像以外が混ざったフォルダを読める | `spike/make_fixtures.py` で作った `tree/`（画像 8・画像以外 5〔txt・md・mov・.DS_Store〕、最も深いのは `tree/2026-10/kyoto/day1/`）を Playwright の setInputFiles で渡す | 13 件すべて、相対パスあり | 13 件すべて、相対パスあり | **12 件**（`.DS_Store` が来ない。Playwright の渡し方によるのか WebKit 自体かは S2 で確認）、相対パスあり |
| ファイルの種類（MIME）が取れる | `file.type` | 取れる（.heic は image/heic） | **すべて空文字**（Playwright 経由。本物の画面からは未確認） | 取れる |

- 結論: 画像かどうかは `file.type` ではなく**拡張子で判定**する。隠しファイル（名前が `.` で始まる）は**どのブラウザでも数えない**と決めれば、「対象外 n 件」がエンジンで食い違わない

### 2. フォルダのドロップ — 判定: 条件付き（Chromium はできる、Firefox・WebKit は手動確認待ち）

| 前提 | 方法 | Chromium | Firefox | WebKit |
|---|---|---|---|---|
| ドロップしたフォルダの中身を再帰的に読める | Chromium の開発者向け命令（CDP の Input.dispatchDragEvent）で本物のドロップを再現。`webkitGetAsEntry()` → `readEntries()` を空になるまで繰り返す | `tree/` 13 件すべて、相対パスあり（5ms） | 未測定（Playwright で再現する手段が無い） | 未測定（同左） |
| 1 フォルダ 250 件でも全部読める | 250 件のフォルダをドロップ | 250 件。`readEntries` は 3 回に分かれて返った（1 回 100 件まで） | 未測定 | 未測定 |

- 注意: `readEntries` を 1 回だけ呼ぶ書き方だと 100 件で切れる。**空の配列が返るまで繰り返す**こと（試作 `spike/lib.js` の `readAllEntries`）

### 3. 目標容量の自動調整（20 枚、長辺 1600px、1 枚 300KB 以下）— 判定: 条件付き（WebKit〔Safari〕は WebP を作れない）

探し方: 画質 0.9 で書き出し → 超えたら 0.1 で書き出し（これでも超えたら「目標超過」）→ 0.1〜0.9 の間を半分ずつ絞る。合計 7 回まで。Worker 1 つで 1 枚ずつ処理。

| 条件 | Chromium | Firefox | WebKit |
|---|---|---|---|
| WebP・300KB | 1 枚 平均 896ms（遅い 5% は 1,253ms 以上）、探索 平均 5.5 回・最大 7 回、届かず 0 件、平均 253KB | 平均 1,110ms（同 1,355ms）、探索 平均 6.4 回・最大 7 回、届かず 0 件、平均 283KB | **作れない**（WebP を指定しても PNG が返る） |
| JPEG・300KB | 平均 149ms（同 179ms）、探索 平均 6.1 回、届かず 0 件、平均 279KB | 平均 111ms（同 126ms）、探索 平均 7 回、届かず 0 件、平均 286KB | 平均 230ms（同 262ms）、探索 平均 7 回、届かず 0 件、平均 286KB |
| WebP・300KB・早めに止める（目標の 90〜100% に入ったら止める） | 平均 796ms（11% 減）、探索 平均 4.9 回 | 平均 894ms（19% 減）、探索 平均 5.1 回 | — |
| JPEG・300KB・早めに止める | 平均 143ms、探索 平均 5.7 回 | 平均 101ms、探索 平均 5.75 回 | 平均 216ms、探索 平均 6.05 回 |
| 厳しめ: WebP・100KB | 平均 930ms、届かず 0 件 | 平均 826ms、**届かず 6 件**（画質 0.1 でも 103〜160KB） | — |
| 厳しめ: JPEG・100KB | 平均 141ms、届かず 0 件 | 平均 105ms、届かず 0 件 | 平均 215ms、届かず 0 件 |

- 1 枚の時間のほとんどは書き出し（WebP は 1 回あたり約 150〜160ms〔Chromium 830ms÷5.5 回、Firefox 1,039ms÷6.4 回〕× 最大 7 回）。読み込みは 1 枚 63〜97ms
- 「目標超過（最小 nKB）」の表示に要る値（画質 0.1 での大きさ）は、探索の 2 回目で必ず得られる
- 同じ画質でも、エンジンによって WebP の大きさが違う（Firefox の方が大きい）。100KB のような厳しい目標では、エンジンによって届く・届かないが変わる

### 4. 200 枚の処理 — 判定: 条件付き（Worker が必須。Firefox は読み込みの工夫で止まりを減らせる）

形式: Chromium・Firefox は WebP、WebKit は WebP を作れないので JPEG。同じ条件で比べるため、Chromium・Firefox の JPEG も測った。

| 条件 | Chromium | Firefox | WebKit |
|---|---|---|---|
| メインスレッド（WebP） | 合計 178.3s、止まり最大 42ms・60ms 超 0 回、RSS 増 323MB | 合計 226.7s、**止まり最大 367ms・60ms 超 175 回**、RSS 増 207MB | — |
| Worker 1（WebP） | 合計 178.1s、最大 15ms・0 回、RSS 増 180MB | 合計 224.0s、**最大 176ms・155 回**、RSS 増 80MB | — |
| Worker 4（WebP） | **合計 46.8s**（1 枚あたり 234ms）、最大 15ms・0 回、RSS 増 334MB | **合計 105.5s**（527ms）、**最大 176ms・151 回**、RSS 増 279MB | — |
| メインスレッド（JPEG） | 合計 35.0s、最大 54ms・0 回、RSS 増 370MB | 合計 21.9s、最大 100ms・163 回、RSS 増 619MB | 合計 48.7s、**最大 300ms・206 回**、RSS 増 349MB |
| Worker 1（JPEG） | 合計 32.3s、最大 18ms・0 回、RSS 増 150MB | 合計 22.5s、最大 111ms・158 回、RSS 増 165MB | 合計 47.7s、最大 183ms・1 回、RSS 増 708MB |
| Worker 4（JPEG） | **合計 8.3s**、最大 24ms・0 回、RSS 増 312MB | **合計 14.8s**、最大 397ms・69 回、RSS 増 439MB | **合計 20.0s**、最大 16ms・0 回、RSS 増 1,017MB |
| 200 枚の出力をそのまま ZIP（fflate ストリーム） | 200 件・49.5MB を 187ms、保存できた | 55.3MB を 253ms、保存できた | 55.9MB を 237ms、保存できた |

- 200 枚すべて「完了」（3 エンジンとも失敗 0）
- JS ヒープ（Chromium だけ測れる）は全条件で 3MB 以下。画像のデータは JS の外（ブラウザ内部）に置かれる
- **Firefox の止まりの原因**（20 枚で Worker の中の各段階だけを動かして切り分けた）:

| Worker 内の処理 | Chromium 止まり最大 | Firefox 止まり最大（60ms 超の回数） | WebKit 止まり最大 |
|---|---|---|---|
| createImageBitmap(File) だけ | 13ms | **126ms（16 回）** | 13ms |
| ArrayBuffer に読んでから createImageBitmap | 13ms | 111ms（17 回） | 13ms |
| createImageBitmap で縮小しながら読む | 13ms | 162ms（20 回） | 13ms |
| ImageDecoder（WebCodecs） | 34ms | **26ms（0 回）** | 無い |
| WebP の書き出しだけ | 13ms | 14ms（0 回） | 13ms |
| JPEG の書き出しだけ | 13ms | 14ms（0 回） | 14ms |

  → Firefox は Worker の中でも、createImageBitmap の読み込みがメインスレッドを止める。ImageDecoder なら止まらない。ImageDecoder の向きの扱いも確かめた: Firefox は回転済みの 200×400 を返し、Chromium は 400×200 と `rotation: 90`（向き 8 は 270）を返して描くときに回る。どちらも描いた結果は正しい向き

- メモリ: 20 枚（Chromium・Worker 1・WebP）の RSS 増 152MB と、200 枚の 180MB がほぼ同じ。**メモリは枚数にほぼ比例せず、同時に処理する枚数（Worker の数）と出力の合計（1 枚 約 0.25〜0.28MB）で決まる**。最大は WebKit の Worker 4 で RSS 増 1,017MB

### 5. ZIP（合計約 500MB）— 判定: できる

200 ファイル × 2.5MB（中身は乱数＝圧縮済みの画像と同じく縮まない）、無圧縮。フォルダは `2026-01/trip0/day0/IMG_0000.webp` の形（3 階層）。各方式ごとに新しいタブで測った。

| 方式 | Chromium | Firefox | WebKit |
|---|---|---|---|
| fflate Zip（ストリーム） | 1.7s、RSS 増 639MB、JS ヒープ最大 100MB | 2.2s、RSS 増 1,600MB | 1.8s、RSS 増 868MB |
| client-zip | 1.7s、RSS 増 575MB、JS ヒープ最大 67MB | 4.5s、RSS 増 507MB | 1.9s、RSS 増 2,668MB |
| fflate zipSync | 1.6s、**RSS 増 1,513MB、JS ヒープ最大 404MB** | 2.3s、**RSS 増 2,089MB** | 1.7s、**RSS 増 1,502MB** |

- すべての方式・エンジンで、Blob にして `<a download>` で保存でき、保存されたファイルの大きさが一致し、200 件・フォルダ構成どおり・`unzip -t` で壊れなし
- 画面の止まりは最大 38ms（WebKit の client-zip）。ZIP を作る間も画面は固まらない
- 日本語のフォルダ名（`2026-10/京都旅行/写真 1.webp`）: fflate（両方式）・client-zip とも UTF-8 の印（一般フラグの 11 ビット目）が付いた（Node で同じライブラリを動かして確認）
- 注意: Blob を作った直後に URL を消す（revokeObjectURL）と保存に失敗しうるので、試作では 2 分後に消した

### 6. EXIF の向き — 判定: できる（直し方は ④）

向き 1・6・8（6 はビッグエンディアンとリトルエンディアンの 2 種）の JPEG を作った（正しく回すと「左上 赤・右上 緑・左下 青・右下 白」の縦長 200×400 になる）。

| 読み方 | Chromium | Firefox | WebKit |
|---|---|---|---|
| createImageBitmap（既定） | 向き 6・8 とも 200×400 で正しい | 同左 | 同左 |
| createImageBitmap（`imageOrientation: 'none'`） | **それでも回転する**（200×400） | 同左 | 同左 |
| `<img>` | 正しい | 正しい | 正しい |
| 既存コードの回転処理に正しい向きの値を渡す | **400×200 で誤り（二重回転）** | 同左 | 同左 |
| 既存コードの EXIF 読み取り（`getExifOrientation` をそのまま移植） | **例外（RangeError）** | 同左 | 同左 |
| 直し方（既定で読み、手動で回さない）で書き出して読み直す | 200×400 で正しい | 同左 | 同左 |

- 既存の `getExifOrientation` は位置の計算を誤っていて、EXIF のある JPEG では範囲外を読んで例外になる。元のコードは `onload` の中に try/catch が無いので、**Promise が終わらず、変換が止まったままになる**（試作では try/catch を足して例外の中身を記録した）
- 読み取りを直しても、既存の回転処理を重ねると二重回転になる

### 7. 追加の確認 — 判定: できる（HEIC は WebKit だけ読める）

| 項目 | Chromium | Firefox | WebKit |
|---|---|---|---|
| 透過 PNG → JPEG、塗りなし（透明の部分の色） | 黒（0,0,0） | 黒 | 黒 |
| 先に白で塗ってから描く | 白（255,255,255） | 白 | 白 |
| OffscreenCanvas でも同じ | 同上 | 同上 | 同上 |
| HEIC（macOS の sips で作成）を読む | 1ms で例外（InvalidStateError）。Worker でも「読めない形式」にできた | 1ms で例外。同左 | **読めた**（200×400）。処理も完了 |
| 中身が壊れた .jpg・0 バイトの .jpg | 0〜1ms で例外。捕まえられる | 同左 | 同左 |

### 測定の副産物（形式の対応）

| 書き出し | Chromium | Firefox | WebKit |
|---|---|---|---|
| WebP（toBlob・convertToBlob） | できる | できる | **できない（PNG が返る）** |
| AVIF（convertToBlob） | できない（PNG） | できない（PNG） | image/avif が返った（Playwright の WebKit。本物の Safari は未確認） |

- 対応していない形式を指定するとエラーにならず PNG が返るので、**書き出した後に `blob.type` を必ず確かめる**

---

## ③ 1 回に扱う枚数の上限の提案

**提案: 1 回 500 枚まで（501 枚目からは「次の回に分けてください」と出す）。ZIP は 1 つ 500MB を超えたら分ける。**

根拠（すべて上の実測から）:

1. 時間: 最も遅い組み合わせ（Firefox・WebP・Worker 4）で 1 枚 527ms。500 枚で約 4.4 分。一般的なノート PC で 2〜3 倍かかるとすると約 9〜13 分（推測）で、待てる長さの上限と考える。200 枚なら同じ条件で約 1.8 分（遅い PC で 3.5〜5 分）
2. メモリ: 枚数にはほぼ比例しない（20 枚 152MB と 200 枚 180MB）。増えるのは出力の分だけで、500 枚 × 約 0.28MB ＝ 約 140MB。最大の RSS 増は WebKit・Worker 4 の 1,017MB で、500 枚でも大きくは変わらない見込み（推測。500 枚そのものは未測定）
3. ZIP: 500 枚 × 300KB ＝ 約 150MB。実測した 500MB の 3 分の 1 以下で、ストリーム方式なら 3 エンジンとも余裕がある。fflate の上限（4GB・65,535 件）にも遠い。500MB で分けるのは、3 エンジンで作れて保存できたことを確かめた大きさがそこまでだから（500MB で RSS 増は最大 1,600MB〔Firefox〕。それより大きい ZIP は未測定）。PNG のように出力が大きい設定で効いてくる
4. Worker の数: `navigator.hardwareConcurrency`（CPU のコア数）から 1 引いた数、ただし最大 4。Chromium は 4 並列で 3.8 倍速くなったが、Firefox は 2.1 倍、WebKit は 2.4 倍にとどまった

- 補足: 無料で 200 枚まで・それ以上は有料にするか（要件 8）は、5 お金の設計で決める。技術の面では 200 枚は十分に安全（最も遅い条件で約 1.8 分）
- 未測定: 4800 万画素（8064×6048）級の大きな写真。1 枚の読み込みに約 195MB 要る計算なので、4 並列だと約 780MB（推測）。大きな写真が多いときは並列数を下げる工夫が要るかもしれない

---

## ④ EXIF の直し方の結論

**手動の回転をやめる。createImageBitmap を既定のまま（`imageOrientation` を指定しない）で読み、ブラウザに回転を任せる。**

- 根拠 1: 3 エンジンとも、既定の createImageBitmap が向き 6・8 を正しく回した。`<img>` も同じ
- 根拠 2: もう一つの案「`imageOrientation: 'none'` で回転させずに読み、自前で回す」は**使えない**。3 エンジンとも `'none'` を指定しても回転した（仕様の変更で、`'none'` は「EXIF を無視する」の意味ではなくなっている〔推測。仕様の該当箇所は今回読んでいない〕）
- 根拠 3: 既存の EXIF 読み取りは例外で止まり、読み取りを直しても回転を重ねると二重回転になる。削るほうが安全で、コードも減る
- 実装でやること: `src/utils/imageProcessor.ts` の `getExifOrientation`・`applyOrientation`・幅と高さの入れ替え（`needsSwap`）を削り、`createImageBitmap(file)` の幅・高さをそのまま使う。Firefox で ImageDecoder を使う場合は、Chromium と違って `rotation` を見ずに描いてよいが、両方に対応させるなら `drawImage(VideoFrame)` に任せる（どちらも描いた結果は正しかった）
- 受け入れの確かめ方: `spike/` の `orient6.jpg`・`orient8.jpg` を変換し、出力が縦長で左上が赤になること。加えて本物の iPhone の縦写真で 1 回（⑤）

---

## ⑤ Chromium 以外で確かめが要ること（手動の手順）

Playwright の WebKit・Firefox は本物の Safari・Firefox と細部が違う。特に WebKit は Playwright 用に作られたもので、Safari のファイル選択の画面・ドラッグ＆ドロップ・HEIC の扱いは同じとは限らない。**公開前に、本物の Safari と Firefox で 1 回ずつ手で確かめる。**

準備（共通、5 分）:

1. ターミナルで `cd ~/orca/image-converter/spike && python3 -m http.server 8765 --bind 127.0.0.1`
2. 試験用のファイルを作る: `python3 -I make_fixtures.py ~/Desktop/spike-data`（`fixtures/` と `tree/` ができる）
3. 確かめるブラウザで `http://127.0.0.1:8765/index.html` を開き、開発者ツールのコンソールを出す（Safari は「設定 → 詳細 → Web 開発者用の機能を表示」をオンにしてから「開発 → JavaScript コンソールを表示」）

本物の Safari（Mac）で確かめること（6 件）:

| # | 何を | 手順 | 期待する結果（Playwright の WebKit での値） |
|---|---|---|---|
| S1 | WebP・AVIF を書き出せるか | コンソールで `await spike.capabilities()` | toBlob の webp が `image/png`（作れない）。avif は Playwright では `image/avif` だった → 本物の値を記録 |
| S2 | フォルダを選べるか | 「フォルダ選択」で `tree` を選ぶ | 画面下に一覧が出て、total 12（または 13）、images 8、パスが `tree/2026-10/kyoto/day1/...` |
| S3 | フォルダをドロップできるか | Finder から `tree` を点線の枠にドラッグ | 一覧が出て、total・images が S2 と同じ。読めなければ「フォルダを選ぶ」へ案内する作りにする |
| S4 | HEIC を読めるか（本物の iPhone 写真） | iPhone の HEIC 写真を「読めない形式」欄で選び、`await spike.unreadableTest()` | `decoded 幅x高さ` と出る（読めた）。例外なら「読めない形式」 |
| S5 | 縦写真が正しい向きか | `fixtures/orient6.jpg`・`orient8.jpg` と本物の iPhone の縦写真を「EXIF」欄で選び、`await spike.exifTest()` | `cibDefault` と `fixPipelineOutput` が `upright: true`（本物の写真は 200×400 ではないので、幅＜高さ になっていればよい） |
| S6 | 200 枚で画面が固まらないか | 写真を 20 枚以上「写真」欄で選び、`await spike.runBatch({count: 200, mode: 'worker', workers: 4, mime: 'image/jpeg'})`。動いている間に画面をスクロールする | 進み具合（n / 200）が止まらずに増え、スクロールが引っかからない。結果の `monitor.maxGapMs` が 200 未満。アクティビティモニタで Safari のメモリを見て記録 |

本物の Firefox で確かめること（3 件）:

| # | 何を | 手順 | 期待する結果 |
|---|---|---|---|
| F1 | フォルダをドロップできるか | S3 と同じ | 一覧が出て、total 13・images 8 |
| F2 | 本物のファイル選択で種類（MIME）が取れるか | S2 と同じ手順で、出た一覧の `type` を見る | Playwright では全部空だった。空でも拡張子で判定するので動作には響かない（記録だけ） |
| F3 | 200 枚で画面が固まらないか | S6 と同じ（`mime: 'image/webp'`） | Playwright では最大 176ms 止まった。体感で気になるなら ImageDecoder の読み込みを入れる |

自動では確かめていない残り（今回の範囲外）: iPhone・Android の Safari・Chrome（キャンバスの大きさの上限 4096×4096 など）、Windows の Chrome・Edge、性能の低い PC での時間。

---

## ⑥ 要件定義書（03-requirements.md）への修正提案

| # | 場所 | 今の書き方 | 修正案 | 理由 |
|---|---|---|---|---|
| 1 | 3 の前文・M2 | PC のブラウザ（Chrome・Edge・Safari・Firefox）で全機能／形式（WebP・JPEG・PNG） | 「Safari では WebP を選べない（JPEG・PNG のみ）。選べない理由を画面に出す」を足す。もう一つの道は WebAssembly の WebP 部品（@jsquash/webp、Apache-2.0、約 0.28MB）を Safari のときだけ読む方法で、これは 5・6 で判断 | WebKit で WebP を指定すると PNG が返った（S1 で本物も確認） |
| 2 | M9 | HEIC は「読めない形式」と表示して止まらない | 「読めないファイル（HEIC を含む）は『読めない形式』と表示して止まらない。読めた場合（Safari の HEIC など）はそのまま処理する」 | WebKit は HEIC を読めた。拡張子で一律に弾くと、Safari の人が使える機能を捨てることになる |
| 3 | M1 | 画像以外は数えずに「対象外 n 件」 | 「画像かどうかは拡張子で判定する。名前が `.` で始まる隠しファイルは対象外の件数にも数えない」 | Firefox（Playwright）は `file.type` が空。Playwright の WebKit は `.DS_Store` が来なかったので件数が食い違う |
| 4 | M4 | 200 枚でも画面が固まらない | 「処理は Worker で行う。画面の止まりは 1 回 200ms 未満（目安）、進み具合が止まらず増える」と測れる形にする | 「固まらない」を確かめる基準が無い。Firefox は Worker でも最大 176ms 止まった |
| 5 | M3 | 探す回数に上限がある | 「探す回数は 1 枚 7 回まで。目標の 90〜100% に入ったら止める」 | 7 回で 300KB の 20 枚はすべて届いた。早めに止めると 11〜19% 速くなった |
| 6 | 6 の表「EXIF の二重回転」の根拠 | Chrome 156 で再現済み（C ⑦） | 「既存の EXIF 読み取りは例外で止まり（変換が終わらない）、読み取りを直しても回転を重ねると二重回転になる（3 エンジンで実測、04 ⑥）」 | 実際の不具合は二重回転の手前で止まることだった |
| 7 | 10 未決事項 | 1 回に扱う枚数の上限: 4 の測定結果で決める | 「技術の上限は 500 枚（04 ③）。無料の範囲（200 枚など）は 5 で決める」 | ③ |
| 8 | M7（補足） | 元と同じフォルダ構成・名前 | 「ZIP の中の名前は Unicode の NFC 形式にそろえる」を足す | macOS のファイル名は濁点が分かれた形（NFD）のことがあり、Windows で解凍すると見た目が崩れることがある（推測。今回は未測定） |

---

## ⑦ 再現のしかた

```bash
cd ~/orca/image-converter/spike
npm install                      # fflate 0.8.2・client-zip 2.5.0・playwright-core 1.57.0（spike/ の中だけ）
DATA=/path/to/spike-data         # リポジトリの外の作業用フォルダ
python3 -I make_fixtures.py "$DATA"   # EXIF の JPEG・透過 PNG・HEIC・3 階層のフォルダ（macOS の sips を使う）

# 1 回目は Chromium で合成写真 20 枚を $DATA/photos/ に作る（約 3.5 分）
node run.mjs --browser chromium --data "$DATA"
node run.mjs --browser firefox  --data "$DATA"
node run.mjs --browser webkit   --data "$DATA"
# 一部だけ: --tests caps,folder,drop,exif,transparent,unreadable,fit20,batch200,diag,zip
# 同じ条件で比べる JPEG の 200 枚: --tests batch200 --batchMime jpeg

python3 -I summarize.py "$DATA"   # 結果の表（Markdown）。spike/measured を渡すと今回の値が出る
```

- 結果は `$DATA/results-<ブラウザ>.json` に追記される。今回の値は `spike/measured/` に写した
- Chromium は `run.mjs` の中で `~/Library/Caches/ms-playwright/chromium_headless_shell-1208/...` を直接指定している
- WebKit・Firefox は `npx playwright@1.57.0 install webkit firefox` で入れる。この Mac では展開の途中で止まったので、curl で取って unzip した（`logs/spike-browser-install_failed.md`）
- 1 つのブラウザの全試験で、Chromium 約 8 分・Firefox 約 11 分・WebKit 約 3 分（写真の生成を除く。`--batchMime jpeg` と `diag` は別に 1〜2 分）
- 試作のファイル: `index.html`（手動確認用の画面）、`lib.js`（試験の本体）、`common.js`（読み込み→縮小→目標容量への書き出し。メインスレッドと Worker で共用）、`worker.js`、`diag-worker.js`（Firefox の止まりの切り分け）、`run.mjs`（Playwright での測定）、`make_fixtures.py`、`summarize.py`
