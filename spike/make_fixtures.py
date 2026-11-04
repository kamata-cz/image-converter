#!/usr/bin/env python3
"""Spike fixtures: EXIF orientation JPEGs, transparent PNG, HEIC, and a 3-level mixed folder.

Usage: python3 -I make_fixtures.py <out_dir>
Needs macOS `sips` (PNG -> JPEG / HEIC). No third-party Python packages.
"""
import os
import struct
import subprocess
import sys
import zlib

OUT = os.path.abspath(sys.argv[1])
FIX = os.path.join(OUT, "fixtures")
TREE = os.path.join(OUT, "tree")

# Upright image U: 200 wide x 400 tall, quadrants TL red, TR green, BL blue, BR white.
W, H = 200, 400
COLORS = {"TL": (255, 0, 0), "TR": (0, 255, 0), "BL": (0, 0, 255), "BR": (255, 255, 255)}


def upright():
    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            key = ("T" if y < H // 2 else "B") + ("L" if x < W // 2 else "R")
            row.append(COLORS[key])
        rows.append(row)
    return rows


def rot_cw(img):  # rotate 90 degrees clockwise
    h, w = len(img), len(img[0])
    return [[img[h - 1 - x][y] for x in range(h)] for y in range(w)]


def rot_ccw(img):
    h, w = len(img), len(img[0])
    return [[img[x][w - 1 - y] for x in range(h)] for y in range(w)]


def write_png(path, img, alpha=None):
    h, w = len(img), len(img[0])
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw.extend(img[y][x])
            if alpha is not None:
                raw.append(alpha[y][x])
    color_type = 6 if alpha is not None else 2

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, color_type, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def sips(src, fmt, dst):
    subprocess.run(["sips", "-s", "format", fmt, src, "--out", dst], check=True, capture_output=True)


def exif_app1(orientation, little=False):
    # TIFF header + IFD0 with one entry: 0x0112 Orientation, SHORT, count 1
    if little:
        tiff = b"II" + struct.pack("<HI", 42, 8) + struct.pack("<H", 1)
        tiff += struct.pack("<HHIHH", 0x0112, 3, 1, orientation, 0) + struct.pack("<I", 0)
    else:
        tiff = b"MM" + struct.pack(">HI", 42, 8) + struct.pack(">H", 1)
        tiff += struct.pack(">HHIHH", 0x0112, 3, 1, orientation, 0) + struct.pack(">I", 0)
    payload = b"Exif\x00\x00" + tiff
    return b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload


def strip_app1(jpg):
    """Remove existing APP1 segments (sips may write its own EXIF)."""
    assert jpg[:2] == b"\xff\xd8"
    out, i = bytearray(jpg[:2]), 2
    while i < len(jpg):
        marker = jpg[i:i + 2]
        if marker[0] != 0xFF or marker[1] == 0xDA:
            out.extend(jpg[i:])
            break
        seg_len = struct.unpack(">H", jpg[i + 2:i + 4])[0]
        if marker[1] != 0xE1:
            out.extend(jpg[i:i + 2 + seg_len])
        i += 2 + seg_len
    return bytes(out)


def make_oriented_jpeg(stored_img, orientation, path, little=False):
    tmp_png = path + ".tmp.png"
    tmp_jpg = path + ".tmp.jpg"
    write_png(tmp_png, stored_img)
    sips(tmp_png, "jpeg", tmp_jpg)
    with open(tmp_jpg, "rb") as f:
        jpg = strip_app1(f.read())
    os.remove(tmp_png)
    os.remove(tmp_jpg)
    with open(path, "wb") as f:
        f.write(jpg[:2] + exif_app1(orientation, little) + jpg[2:])


def main():
    os.makedirs(FIX, exist_ok=True)
    u = upright()
    # Orientation 6 = viewer rotates 90 CW to display, so store U rotated 90 CCW.
    make_oriented_jpeg(u, 1, os.path.join(FIX, "orient1.jpg"))
    make_oriented_jpeg(rot_ccw(u), 6, os.path.join(FIX, "orient6.jpg"))
    make_oriented_jpeg(rot_cw(u), 8, os.path.join(FIX, "orient8.jpg"))
    make_oriented_jpeg(rot_ccw(u), 6, os.path.join(FIX, "orient6_le.jpg"), little=True)

    # Transparent PNG 100x100: left half fully transparent, right half opaque red.
    img = [[(255, 0, 0)] * 100 for _ in range(100)]
    alpha = [[0 if x < 50 else 255 for x in range(100)] for _ in range(100)]
    write_png(os.path.join(FIX, "transparent.png"), img, alpha)

    # HEIC via sips, plus a broken "jpg" and an empty file.
    tmp = os.path.join(FIX, "heic_src.png")
    write_png(tmp, u)
    sips(tmp, "heic", os.path.join(FIX, "sample.heic"))
    os.remove(tmp)
    with open(os.path.join(FIX, "broken.jpg"), "wb") as f:
        f.write(b"this is not a jpeg" * 10)
    open(os.path.join(FIX, "empty.jpg"), "wb").close()

    # 3-level folder with images and non-images.
    small = [[(30, 120, 200)] * 64 for _ in range(48)]
    layout = {
        "tree/2026-10/kyoto/day1": ["IMG_0001.jpg", "IMG_0002.JPG", "memo.txt"],
        "tree/2026-10/kyoto/day2": ["IMG_0003.jpeg", "photo.png", "clip.mov"],
        "tree/2026-10": ["cover.png", "notes.md"],
        "tree/2026-11/osaka/night": ["IMG_0100.heic", "IMG_0101.jpg", ".DS_Store"],
        "tree": ["readme.txt", "top.webp"],
    }
    for d, names in layout.items():
        full = os.path.join(OUT, d)
        os.makedirs(full, exist_ok=True)
        for n in names:
            p = os.path.join(full, n)
            ext = n.lower().rsplit(".", 1)[-1]
            if ext == "png":
                write_png(p, small)
            elif ext in ("jpg", "jpeg"):
                write_png(p + ".png", small)
                sips(p + ".png", "jpeg", p)
                os.remove(p + ".png")
            elif ext == "heic":
                write_png(p + ".png", small)
                sips(p + ".png", "heic", p)
                os.remove(p + ".png")
            elif ext == "webp":
                # sips cannot write WebP everywhere; use a tiny valid lossless WebP (1x1).
                with open(p, "wb") as f:
                    f.write(bytes.fromhex(
                        "524946461a000000574542505650384c0d0000002f00000010071011118888fe0700"))
            else:
                with open(p, "wb") as f:
                    f.write(b"not an image\n")
    print("fixtures written to", OUT)


if __name__ == "__main__":
    main()
