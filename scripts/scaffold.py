#!/usr/bin/env python3
"""Scaffold a new style skill folder from the Design DNA templates.

  python3 scaffold.py <slug> [--dest DIR] [--name "Human Name"] [--reference FILE ...]

Creates <dest>/style-<slug>/ with SKILL.md, PROMPT.md, dna.json, reference/, example/,
tools/check.py (+ tools/_coverage.py). Copies any --reference files into reference/.
Never overwrites an existing folder.
"""
import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / "assets" / "templates"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--dest", default=str(Path.home() / ".claude" / "skills"))
    ap.add_argument("--name")
    ap.add_argument("--reference", nargs="*", default=[])
    a = ap.parse_args()

    slug = re.sub(r"[^a-z0-9-]+", "-", a.slug.lower()).strip("-")
    name = a.name or slug.replace("-", " ").title()
    out = Path(a.dest) / f"style-{slug}"
    if out.exists():
        print(f"refusing: {out} already exists")
        return 1

    (out / "reference").mkdir(parents=True)
    (out / "example").mkdir()
    (out / "tools").mkdir()

    subs = {"{{SLUG}}": slug, "{{NAME}}": name, "{{DATE}}": datetime.date.today().isoformat()}

    def render(src, dst):
        text = (TPL / src).read_text()
        for k, v in subs.items():
            text = text.replace(k, v)
        (out / dst).write_text(text)

    render("SKILL.template.md", "SKILL.md")
    render("PROMPT.template.md", "PROMPT.md")
    render("dna.template.json", "dna.json")
    render("check.template.py", "tools/check.py")
    shutil.copy(HERE / "coverage.py", out / "tools" / "_coverage.py")

    refs = []
    for r in a.reference:
        p = Path(r).expanduser()
        shutil.copy(p, out / "reference" / p.name)
        refs.append(f"reference/{p.name}")
    if refs:
        dna = json.loads((out / "dna.json").read_text())
        dna["meta"]["source"] = refs
        (out / "dna.json").write_text(json.dumps(dna, indent=2) + "\n")

    print(f"scaffolded {out}")
    print("next: fill dna.json, compile PROMPT.md, write tools/check.py tests, then lint:")
    print(f"  python3 {HERE / 'lint_dna.py'} '{out}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
