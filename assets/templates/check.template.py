#!/usr/bin/env python3
"""Automated tests for the {{NAME}} style.

  python3 tools/check.py <render.png> [more renders...]

Runs every test in ../dna.json marked "auto": true. Colour coverage is built in;
add a function to CHECKS for each other auto test id (keyed by the test's "id").
An auto test with no implementation counts as a FAIL, so the spec and the checker
cannot quietly drift apart. Exit 0 = all pass, 1 = any fail.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _coverage  # noqa: E402

DNA = json.loads((Path(__file__).parent.parent / "dna.json").read_text())


def coverage(image):
    results, _ = _coverage.check(DNA, image)
    return all(p for _, p, _ in results), "; ".join(f"{t} {d}" for t, p, d in results)


# test id -> fn(image_path) -> (passed: bool, detail: str)
CHECKS = {
    # "t1-accent-under-8pct": lambda img: coverage(img),
}


def main(images):
    ok = True
    auto = [t for t in DNA.get("tests", []) if t.get("auto")]
    for img in images:
        print(f"== {img}")
        passed, detail = coverage(img)
        print(f"{'PASS' if passed else 'FAIL'}  palette-coverage  {detail}")
        ok &= passed
        for t in auto:
            fn = CHECKS.get(t["id"])
            if fn is None:
                print(f"FAIL  {t['id']}  NOT IMPLEMENTED in tools/check.py ({t['check']})")
                ok = False
                continue
            passed, detail = fn(img)
            print(f"{'PASS' if passed else 'FAIL'}  {t['id']}  {detail}")
            ok &= passed
    manual = [t for t in DNA.get("tests", []) if not t.get("auto")]
    if manual:
        print(f"-- {len(manual)} manual test(s) still to run from the PROMPT.md self-check")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
