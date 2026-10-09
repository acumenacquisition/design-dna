---
name: style-{{SLUG}}
description: >-
  Produces new work in the "{{NAME}}" visual style (codified with design-dna on
  {{DATE}}) on any content and in any format it supports: REPLACE WITH the
  formats (carousel, slide, landing page, poster...) and the look in one line.
  Use whenever the user asks for something "in the {{NAME}} style", "like the
  {{NAME}} one", or names this style for a new piece. Not for other styles:
  one skill per style, never blended.
---

# {{NAME}}

REPLACE WITH soul.one_line.

## How to use

1. Load `PROMPT.md` into the generating context. Attach every file in `reference/` and `example/`. Never load `dna.json` into a prompt; it is the record, not the payload.
2. Pick the archetype(s) from `PROMPT.md` that fit the content. Keep to each archetype's content budget.
3. Generate and render (screenshot, PNG export or frame grab).
4. Run the checks: `python3 tools/check.py <render.png>` for the automated tests, then the manual self-check in `PROMPT.md`. Repair and re-run until everything passes. Never return an output with a failing test and a note explaining it away.

## Source and status

- Reference: `reference/`. Canonical proof: `example/`.
- Full record: `dna.json` (status in its `reconstruction` block; run design-dna's `lint_dna.py` on this folder to see it).
- Not copied: see `dna.json` `meta.not_copied`.
- To change the style, edit `dna.json` first, recompile `PROMPT.md`, re-run a reconstruct-and-diff pass. For a genuinely different look, make a new style skill rather than stretching this one.
