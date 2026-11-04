#!/usr/bin/env python3
"""段階 6 の見本 app.html を組み立てる（外部読み込みなしの単一 HTML）。
使い方: python3 -I docs/mock/build_app.py
材料: app.src.html（骨組み）、app.css、app.js、octicons-extra.html（このページで足したアイコン）、
      ~/.claude/skills/github-primer-artifact/assets/ の primer-base.css と octicons-symbols.html
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = pathlib.Path.home() / ".claude/skills/github-primer-artifact/assets"


def symbols(text: str) -> str:
    """<symbol> 要素だけを取り出す（id の重複は先勝ち）。"""
    seen, out = set(), []
    for m in re.finditer(r'<symbol\b[^>]*\bid="([^"]+)"[\s\S]*?</symbol>', text):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(0))
    return out


def main() -> None:
    src = (HERE / "app.src.html").read_text(encoding="utf-8")
    syms = symbols((ASSETS / "octicons-symbols.html").read_text(encoding="utf-8")) + symbols(
        (HERE / "octicons-extra.html").read_text(encoding="utf-8"))
    icons = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">' + "".join(syms) + "</svg>"
    out = (src.replace("{{PRIMER_BASE}}", (ASSETS / "primer-base.css").read_text(encoding="utf-8"))
              .replace("{{PAGE_CSS}}", (HERE / "app.css").read_text(encoding="utf-8"))
              .replace("{{ICONS}}", icons)
              .replace("{{PAGE_JS}}", (HERE / "app.js").read_text(encoding="utf-8")))
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        raise SystemExit(f"置き場所が残っています: {left}")
    (HERE / "app.html").write_text(out, encoding="utf-8")
    # Artifact 公開用: 公開時に doctype・html・head・body が付くので、中身だけにする
    title = re.search(r"<title>.*?</title>", out).group(0)
    style = re.search(r"<style>[\s\S]*?</style>", out).group(0)
    body = re.search(r"<body>([\s\S]*)</body>", out).group(1)
    pub = title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + style + "\n" + body
    (HERE / "app.publish.html").write_text(pub, encoding="utf-8")
    print(f"app.html {len(out.encode('utf-8')):,} バイト、公開用 app.publish.html {len(pub.encode('utf-8')):,} バイト、アイコン {len(syms)} 個")


if __name__ == "__main__":
    main()
