#!/usr/bin/env python3
"""Print Markdown tables from results-<browser>.json. Usage: python3 -I summarize.py <data_dir>"""
import json
import os
import sys

D = sys.argv[1]
BROWSERS = ["chromium", "firefox", "webkit"]
R = {}
for b in BROWSERS:
    for name in (f"results-{b}.json", f"{b}.json"):  # scratch data dir or spike/measured
        p = os.path.join(D, name)
        if os.path.exists(p):
            R[b] = json.load(open(p))
            break


def g(d, *ks, default="未測定"):
    for k in ks:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def row(label, fn):
    cells = []
    for b in BROWSERS:
        try:
            cells.append(str(fn(R[b])) if b in R else "未測定")
        except Exception as e:  # noqa: BLE001
            cells.append(f"未測定（{type(e).__name__}）")
    print(f"| {label} | " + " | ".join(cells) + " |")


print("| 項目 | " + " | ".join(f"{b} {R.get(b, {}).get('version', '')}" for b in BROWSERS) + " |")
print("|---|" + "---|" * len(BROWSERS))
row("toBlob webp→", lambda r: r["caps"]["toBlob"]["image/webp"])
row("convertToBlob webp→", lambda r: r["caps"]["convertToBlob"]["image/webp"])
row("convertToBlob avif→", lambda r: r["caps"]["convertToBlob"]["image/avif"])
row("longtask / performance.memory", lambda r: f'{r["caps"]["longtask"]} / {r["caps"]["performanceMemory"]}')
row("getAsFileSystemHandle / showDirectoryPicker", lambda r: f'{r["caps"]["getAsFileSystemHandle"]} / {r["caps"]["showDirectoryPicker"]}')
f = lambda r: r["folder"]
row("1 webkitdirectory 全件/画像/対象外/最大深さ/相対パス", lambda r: (f(r)["total"], f(r)["images"], f(r)["excluded"], f(r)["maxDepth"], f(r)["allHaveRelativePath"]) if "total" in f(r) else f(r))
row("1 .heic の file.type", lambda r: [x["type"] or "(空)" for x in f(r)["rows"] if x["path"].endswith(".heic")][0])
row("2 ドロップ tree", lambda r: (lambda d: (d["total"], d["images"], d["excluded"], d["maxDepth"]) if isinstance(d, dict) and d.get("ok") else d)(r["drop"].get("tree", r["drop"])))
row("2 ドロップ 250 件（readEntries 回数）", lambda r: (lambda d: (d["total"], d["stats"]["maxBatchesPerDir"]) if isinstance(d, dict) and d.get("ok") else "-")(r["drop"].get("bulk250", {})))

for key in ["webp_300", "jpeg_300", "webp_300_stop90", "jpeg_300_stop90", "webp_100", "jpeg_100"]:
    def fit(r, key=key):
        v = r["fit20"][key]
        if "error" in v:
            return "エラー " + v["error"][:80]
        if v["actualTypes"] != [v["mime"]]:
            return f'{v["mime"]} 不可（{",".join(v["actualTypes"])}）'
        return (f'平均 {v["perImageMs"]["mean"]}ms・p95 {v["perImageMs"]["p95"]}ms・探索 平均 {v["attempts"]["mean"]} 回/最大 {v["attempts"]["max"]}・'
                f'超過 {v["statuses"].get("over", 0)} 件 {v["overMinKB"]}・平均 {v["outKB"]["mean"]}KB')
    row(f"3 20 枚 {key}", fit)

for cfg in ["main", "worker1", "worker4"]:
    def b200(r, cfg=cfg):
        v = r["batch200"][cfg]
        if "error" in v:
            return "エラー " + v["error"][:80]
        m = v["monitor"]
        lt = m["longtasks"]
        lt_s = f'長いタスク {lt["count"]} 回・最大 {lt["maxMs"]}ms' if isinstance(lt, dict) else "longtask 非対応"
        heap = m["heapMB"]
        heap_s = f'・JS ヒープ最大 {heap["peak"]}MB' if isinstance(heap, dict) else ""
        rss = v.get("rssMB")
        rss_s = f'・RSS 増 {rss["delta"]}MB（最大 {rss["peak"]}MB）' if isinstance(rss, dict) else ""
        return (f'{v["mime"]} 合計 {v["totalMs"]/1000:.1f}s（{v["throughputMsPerImage"]}ms/枚）・最大の間隔 {m["maxGapMs"]}ms・'
                f'60ms 超 {m["gapsOver60ms"]} 回・{lt_s}{heap_s}{rss_s}・状態 {v["statuses"]}')
    row(f"4 200 枚 {cfg}", b200)
row("4 200 枚の出力を ZIP（stream）", lambda r: (lambda z: f'{z["entries"]} 件・{z["zipBytes"]/2**20:.1f}MB・{z["buildMs"]}ms・保存 {z["savedBytes"]==z["zipBytes"]}')(r["batch200"]["worker4_zipOutputs"]))

for kind in ["zipStream", "clientZip", "zipSync"]:
    def zp(r, kind=kind):
        v = r["zip"][kind]
        if "error" in v:
            return "失敗 " + v["error"][:100]
        m = v["monitor"]
        heap = m["heapMB"]
        heap_s = f'・JS ヒープ最大 {heap["peak"]}MB' if isinstance(heap, dict) else ""
        rss = v.get("rssMB")
        rss_s = f'・RSS 増 {rss["delta"]}MB' if isinstance(rss, dict) else ""
        return (f'{v["zipBytes"]/2**20:.0f}MB を {v["buildMs"]/1000:.1f}s・最大の間隔 {m["maxGapMs"]}ms{heap_s}{rss_s}・'
                f'保存 {v["savedBytes"]==v["zipBytes"]}・{v["entries"]} 件・構成 {v["dirsPreserved"]}・unzip -t {v["unzipTest"]}')
    row(f"5 ZIP 500MB {kind}", zp)


def ex(r, fname, key):
    rows = {x["file"]: x for x in r["exif"]}
    v = rows[fname][key]
    if isinstance(v, dict):
        return f'{v["w"]}x{v["h"]} {"正立" if v["upright"] else "誤り"}'
    return str(v)[:60]


for fname in ["orient6.jpg", "orient8.jpg"]:
    for key in ["cibDefault", "cibNone", "imgElement", "legacyRotateWithCorrectValue", "fixPipelineOutput"]:
        row(f"6 {fname} {key}", lambda r, fname=fname, key=key: ex(r, fname, key))
row("6 旧パーサ（orient6.jpg）", lambda r: ex(r, "orient6.jpg", "legacyParser"))
row("7 透過→JPEG 塗りなし/白塗り（透明部の画素）", lambda r: f'{r["transparent"]["canvas_noFill"]["transparentArea"]} / {r["transparent"]["canvas_whiteFill"]["transparentArea"]}')
row("7 透過→JPEG Offscreen 塗りなし/白塗り", lambda r: f'{r["transparent"]["offscreen_noFill"]["transparentArea"]} / {r["transparent"]["offscreen_whiteFill"]["transparentArea"]}')
for fname in ["sample.heic", "broken.jpg", "empty.jpg"]:
    row(f"7 {fname}", lambda r, fname=fname: (lambda x: f'{x["createImageBitmap"][:70]}（{x["ms"]}ms）・worker: {x["workerStatus"][:30]}')({y["file"]: y for y in r["unreadable"]}[fname]))
