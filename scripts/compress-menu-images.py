#!/usr/bin/env python3
"""Kompres poster menu jadi WebP konsisten <= 30 KB dengan kualitas terbaik.

Pakai:
  python scripts/compress-menu-images.py <folder-sumber> [-o /tmp/out30] [--max-kb 30]
  python scripts/compress-menu-images.py --check            # cek ukuran aset terpasang

Strategi: untuk tiap lebar kandidat (dari besar ke kecil) cari kualitas
tertinggi yang masih memenuhi batas ukuran (binary search). Lebar terbesar
yang berhasil dengan kualitas >= MIN_QUALITY dipakai, jadi teks poster tetap
terbaca dan hasilnya selalu konsisten di bawah batas.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from PIL import Image

WIDTHS = [720, 640, 580, 520, 460, 420, 380]
MIN_QUALITY = 25
MAX_QUALITY = 88


def encode(img: Image.Image, width: int, quality: int) -> bytes:
    import io

    w = min(width, img.width)
    h = round(img.height * w / img.width)
    resized = img.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    resized.save(buf, "WEBP", quality=quality, method=6)
    return buf.getvalue()


def best_encoding(path: pathlib.Path, max_bytes: int) -> tuple[bytes, int, int]:
    img = Image.open(path).convert("RGB")
    fallback: tuple[bytes, int, int] | None = None
    for width in WIDTHS:
        lo, hi, best = MIN_QUALITY, MAX_QUALITY, None
        while lo <= hi:
            mid = (lo + hi) // 2
            data = encode(img, width, mid)
            if len(data) <= max_bytes:
                best = (data, width, mid)
                lo = mid + 1
            else:
                hi = mid - 1
        if best:
            return best
        # simpan kandidat terkecil bila tidak ada yang lolos
        fallback = (encode(img, width, MIN_QUALITY), width, MIN_QUALITY)
    assert fallback
    return fallback


def run_compress(src: pathlib.Path, out: pathlib.Path, max_kb: int) -> int:
    max_bytes = max_kb * 1024
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in src.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    if not files:
        print(f"Tidak ada gambar di {src}")
        return 1
    bad = 0
    for f in files:
        data, width, quality = best_encoding(f, max_bytes)
        target = out / (f.stem + ".webp")
        target.write_bytes(data)
        ok = len(data) <= max_bytes
        bad += 0 if ok else 1
        print(
            f"{'OK ' if ok else 'LEBIH'} {target.name:<24} {len(data)/1024:6.1f} KB  "
            f"w={width} q={quality}"
        )
    return 0 if bad == 0 else 1


def run_check(max_kb: int) -> int:
    max_bytes = max_kb * 1024
    root = pathlib.Path(__file__).resolve().parent.parent / "src" / "assets" / "menu"
    pointers = sorted(root.glob("*.asset.json"))
    if not pointers:
        print("Tidak ada pointer gambar.")
        return 1
    bad = 0
    for p in pointers:
        meta = json.loads(p.read_text())
        size = int(meta.get("size", 0))
        ok = 0 < size <= max_bytes
        bad += 0 if ok else 1
        print(f"{'OK ' if ok else 'LEBIH'} {meta['original_filename']:<24} {size/1024:6.1f} KB")
    print(f"\n{len(pointers)} gambar, {bad} melebihi {max_kb} KB")
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", help="folder gambar sumber")
    ap.add_argument("-o", "--out", default="/tmp/out30")
    ap.add_argument("--max-kb", type=int, default=30)
    ap.add_argument("--check", action="store_true", help="cek ukuran aset terpasang")
    args = ap.parse_args()
    if args.check or not args.source:
        return run_check(args.max_kb)
    return run_compress(pathlib.Path(args.source), pathlib.Path(args.out), args.max_kb)


if __name__ == "__main__":
    sys.exit(main())
