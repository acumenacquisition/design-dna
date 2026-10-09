#!/usr/bin/env python3
"""Colour coverage for Design DNA.

Two modes:
  --sample IMAGE            dominant colours of a reference + % of canvas each covers (Step 1)
  --dna DNA_JSON IMAGE      map every pixel to the nearest palette colour in dna.json and
                            compare per-role coverage with palette.coverage (+/- tolerance)

Deterministic, local, free. Needs Pillow. Exit code 0 = pass (or sample), 1 = coverage fail.
Also imported by each style skill's tools/check.py (copied in as _coverage.py).
"""
import argparse
import json
import sys

from PIL import Image

MAX_SIDE = 400          # downscale for speed; coverage is a proportion so this is safe
OFF_PALETTE_DIST = 60   # weighted RGB distance beyond which a pixel matches no palette colour


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dist(a, b):
    # "redmean" weighted RGB distance: cheap, closer to perception than plain Euclidean
    rm = (a[0] + b[0]) / 2
    dr, dg, db = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return ((2 + rm / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rm) / 256) * db * db) ** 0.5


def _load(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    return img


def sample(path, n=8):
    img = _load(path)
    q = img.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    out = []
    for c, idx in counts:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        out.append({"hex": "#%02X%02X%02X" % (r, g, b), "pct": round(100 * c / total, 1)})
    return out


def measure(dna, path):
    """Return {role: pct, '_off_palette': pct} for the image against dna palette."""
    colours = [(c["role"], _hex_to_rgb(c["hex"])) for c in dna["palette"]["colors"]]
    img = _load(path)
    counts = {}
    for n, px in img.getcolors(maxcolors=img.width * img.height):
        best_role, best_d = None, None
        for role, rgb in colours:
            d = _dist(px, rgb)
            if best_d is None or d < best_d:
                best_role, best_d = role, d
        key = best_role if best_d <= OFF_PALETTE_DIST else "_off_palette"
        counts[key] = counts.get(key, 0) + n
    total = sum(counts.values())
    return {k: round(100 * v / total, 1) for k, v in counts.items()}


def check(dna, path):
    """Yield (id, passed, detail) for each coverage role."""
    got = measure(dna, path)
    target = dna["palette"].get("coverage", {})
    tol_cfg = dna["palette"].get("coverage_tolerance_pct", 5)
    results = []
    for role, want in target.items():
        # per-role override if a dict; otherwise small roles get a proportional tolerance
        # (a 1% accent at +/-5 would let a 6% accent pass, which is a different design)
        if isinstance(tol_cfg, dict):
            tol = tol_cfg.get(role, 5)
        else:
            tol = min(tol_cfg, max(1.0, want * 0.5))
        have = got.get(role, 0.0)
        results.append((f"coverage:{role}", abs(have - want) <= tol,
                        f"{have}% vs target {want}% (+/-{tol})"))
    cap = dna["palette"].get("max_off_palette_pct")
    if cap is not None:
        off = got.get("_off_palette", 0.0)
        results.append(("coverage:off_palette", off <= cap, f"{off}% off-palette vs cap {cap}%"))
    return results, got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--dna")
    ap.add_argument("-n", type=int, default=8)
    a = ap.parse_args()
    if a.sample or not a.dna:
        for row in sample(a.image, a.n):
            print(f"{row['hex']}  {row['pct']:>5}%")
        return 0
    dna = json.load(open(a.dna))
    results, got = check(dna, a.image)
    print("measured:", json.dumps(got))
    ok = True
    for tid, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'}  {tid}  {detail}")
        ok &= passed
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
