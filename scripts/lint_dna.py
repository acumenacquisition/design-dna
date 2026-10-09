#!/usr/bin/env python3
"""Lint a Design DNA style folder (dna.json + PROMPT.md) and report its derived status.

  python3 lint_dna.py <style-folder>

Checks the rules the method depends on: counts (3-9 signatures, >=5 bans, 8-12 tests),
weird move present, coverage sums ~100 and matches palette roles, every font has a
fallback, colour names are descriptive not token-style, spacing has no px values,
PROMPT.md under 2KB and in the fixed order, required folder contents present.

Status is DERIVED from reconstruction.passes: UNVERIFIED until at least one
reconstruct-and-diff pass is recorded. Exit 0 = no FAILs (warnings allowed).
"""
import json
import re
import sys
from pathlib import Path

PROMPT_CAP = 2048
TOKEN_NAME = re.compile(r"^[a-z]+[-_]?\d{2,3}$|^(primary|secondary|accent|brand|neutral)[-_ ]?\d*$", re.I)
PROMPT_ORDER = ["reference", "soul", "weird", "signature", "ban", "palette", "archetype", "self-check"]


def main(folder):
    root = Path(folder)
    fails, warns = [], []
    F, W = fails.append, warns.append

    dna_path = root / "dna.json"
    if not dna_path.exists():
        print(f"FAIL  no dna.json in {root}")
        return 1
    try:
        dna = json.loads(dna_path.read_text())
    except json.JSONDecodeError as e:
        print(f"FAIL  dna.json is not valid JSON: {e}")
        return 1

    for key in ["meta", "soul", "palette", "type", "space", "signatures", "weird_move", "bans", "tests", "reconstruction"]:
        if key not in dna:
            F(f"missing top-level key: {key}")

    sig = dna.get("signatures", [])
    if not 3 <= len(sig) <= 9:
        F(f"signatures: {len(sig)} (must be 3-9; to add one, cut one)")
    for s in sig:
        if not s.get("never"):
            W(f"signature '{s.get('move')}' has no 'never'")

    wm = dna.get("weird_move", {})
    if not (wm.get("what") and wm.get("how")):
        F("weird_move missing what/how")

    bans = dna.get("bans", [])
    if len(bans) < 5:
        F(f"bans: {len(bans)} (minimum 5)")
    if len(bans) < len(sig):
        W(f"bans ({len(bans)}) do not outnumber signatures ({len(sig)})")

    tests = dna.get("tests", [])
    if not 8 <= len(tests) <= 12:
        F(f"tests: {len(tests)} (must be 8-12)")
    vague = re.compile(r"\b(feels?|looks? (clean|premium|good|nice)|on[- ]brand|elegant|modern)\b", re.I)
    for t in tests:
        if vague.search(t.get("check", "")):
            F(f"test {t.get('id')} is not binary: '{t.get('check')}'")
        if "auto" not in t:
            W(f"test {t.get('id')} does not say whether it is auto")

    pal = dna.get("palette", {})
    roles = {c.get("role") for c in pal.get("colors", [])}
    for c in pal.get("colors", []):
        if TOKEN_NAME.match(c.get("name", "")):
            F(f"colour name '{c.get('name')}' is token-style; use a descriptive name")
    cov = pal.get("coverage", {})
    if not cov:
        F("palette.coverage missing (the most decisive field)")
    else:
        total = sum(cov.values())
        if not 90 <= total <= 110:
            F(f"coverage sums to {total}, not ~100")
        for r in cov:
            if r not in roles:
                F(f"coverage role '{r}' has no colour in palette.colors")

    for fam in dna.get("type", {}).get("families", []):
        if not fam.get("fallback"):
            F(f"font '{fam.get('family')}' has no fallback")
    if "display_to_body_ratio" not in dna.get("type", {}).get("scale", {}):
        F("type.scale.display_to_body_ratio missing")

    if re.search(r"\d+\s*px", json.dumps(dna.get("space", {}))):
        F("space contains px values; use % of canvas")

    if not dna.get("meta", {}).get("not_copied"):
        W("meta.not_copied is empty: confirm no third-party marks were in the reference")

    # PROMPT.md
    pm = root / "PROMPT.md"
    if not pm.exists():
        F("PROMPT.md missing")
    else:
        text = pm.read_text()
        size = len(text.encode())
        if size > PROMPT_CAP:
            F(f"PROMPT.md is {size} bytes (cap {PROMPT_CAP})")
        low = text.lower()
        pos = [low.find(k) for k in PROMPT_ORDER]
        missing = [k for k, p in zip(PROMPT_ORDER, pos) if p < 0]
        if missing:
            F(f"PROMPT.md missing sections: {', '.join(missing)}")
        else:
            if pos != sorted(pos):
                F("PROMPT.md sections out of order (reference, soul, weird move, signatures, bans, palette/type, archetypes, self-check)")
        if "never return output with a failing test" not in low:
            F("PROMPT.md does not end with the self-check instruction")

    for sub in ["reference", "example"]:
        d = root / sub
        if not d.is_dir() or not any(p for p in d.iterdir() if not p.name.startswith(".")):
            F(f"{sub}/ is empty")
    if not (root / "tools" / "check.py").exists():
        F("tools/check.py missing")

    # derived status
    rec = dna.get("reconstruction", {})
    passes = rec.get("passes", 0)
    if not rec.get("attempted") or passes < 1:
        status = "UNVERIFIED (no reconstruct-and-diff pass recorded)"
    elif rec.get("stranger_test") == "pass":
        status = f"VERIFIED ({passes} pass(es), stranger test passed)"
    else:
        status = f"IN PROGRESS ({passes} pass(es), stranger test {rec.get('stranger_test', 'not_run')})"
    unc = rec.get("uncertain", [])

    print(f"style: {dna.get('meta', {}).get('name', root.name)}")
    print(f"status: {status}")
    print(f"gaps folded back: {len(rec.get('gaps_found', []))}  |  uncertain: {len(unc)}")
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    print("OK: lint clean" if not fails else f"{len(fails)} FAIL(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
