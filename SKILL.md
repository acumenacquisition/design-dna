---
name: design-dna
description: >-
  Turns a look you love (one finished piece, or a mood board plus a design
  brief: a landing page, poster, carousel, deck, infographic, motion piece,
  email template, anything visual) into a permanent, reusable style skill, so the
  look can be reproduced on new content in any format without drifting back
  to generic AI output. It measures the reference, separates load-bearing
  moves from trivia, writes a full record (dna.json) plus a sub-2KB prompt
  payload (PROMPT.md), writes pass/fail tests, then rebuilds the original
  from the spec alone and folds every gap back in before emitting a new
  skill folder. Use whenever the user says "/design-dna", "codify this
  design", "turn this into a skill", "capture this style", "make this look
  repeatable", "extract the design DNA", "lock in this look", or has made one
  visual they love and wants more of it. Not for generating a design from
  nothing, and never for merging two styles into one.
---

# Design DNA

**The idea:** a design loop finds one beautiful thing. Design DNA turns that one thing into a skill, so the look becomes a command instead of a memory. The subject is the *system*, not the format: the same process codifies a website, a poster, a carousel, a deck or a motion piece, and the resulting skill can output any of them.

**Why it matters:** every rule left unwritten gets guessed, and a model guesses the average of everything it has seen. That average is the generic AI look. Drift is just unwritten rules.

Credit: packaged by Acumen; adapted from the "Design DNA" method (Notion write-up, 2026). Reasoning, research notes and the troubleshooting table: `references/method-notes.md`. A standalone paste-anywhere version of the analyst brief: `references/analyst-prompt.md`. Field-by-field schema: `references/design-dna.schema.json`.

Works best **downstream of one piece you love**: make (or find) the winner first, then let design-dna make it permanent. Starting from a mood board and a design brief works too; run it again on your first visual you love, because a real example carries a look far better than a description.

## Inputs (ask together, then wait)

1. **The reference.** A file (PNG, PDF, HTML, video frames) or a URL. Push for the actual file, not a description. If it is a live site, screenshot it at the sizes it will be used.
2. **A name.** Short, descriptive (e.g. "plum editorial", "brand carousel v2"). Becomes the slug.
3. **Where it will be used.** Formats it must drive (carousel 1080x1350, slide 1920x1080, landing page, etc). Sets `read_distance` and the archetypes.
4. **Anything that must not be copied.** Third-party logos, licensed photos, proprietary fonts. Assume any real brand mark is excluded unless it is your own or your client's.

If the reference is a client's asset, the output belongs under that client's scope; say so and confirm before writing.

## The six things that carry a look (read before Step 1)

1. **Ratios, not values.** "Headline 8x body, never under 6x" is the style. "96px" is not.
2. **Coverage, not just colour.** The same palette at 60/30/10 and 90/8/2 is two designs. Record share of canvas.
3. **The one weird move.** The single deliberate break in the system. Highest-information element, first thing lost in a copy.
4. **Refusals.** Listing six colours permits six. If the reference uses one accent on 3%, the content is a refusal.
5. **Absence.** No shadows, no icons, nothing centred. Record what is missing as carefully as what is present.
6. **Named layouts.** Without archetypes, output #8 will not sit beside output #1.

## The core decision: two files, compiled not pasted

| | `dna.json` (the record) | `PROMPT.md` (the payload) |
|---|---|---|
| Read by | You, build tools, check scripts | The model |
| Size | As big as needed | **Hard cap 2KB** |
| Holds | Every measured value | Reference image, soul line, weird move, 3-9 moves, bans, roles + coverage, archetype names, self-check |
| Rule | Never goes into a prompt | Never ships without the reference image |

The cap is real: compliance falls as rule count rises, and rules in the middle of a long document are recovered far worse than those at either end. Style resists words; the reference image carries it on a separate channel almost for free. **Always attach the reference image.**

## Run it in seven steps. Show the work at each.

### Step 1: Observe (no interpretation)
Flat inventory of literal observations. Sample real hex values (use `scripts/coverage.py --sample` on an image to get the dominant colours and their share). Count type sizes, weights, accent uses. Measure largest-to-smallest type ratio. Margins and gutters as **% of canvas**. Texture, grain, edges, image treatment. List what is absent. Mark anything estimated rather than measured as `inferred`.

### Step 2: Debate it
Run two honest positions, then adjudicate:
- **Maximalist:** anything unwritten will be improvised; list every property.
- **Minimalist:** a copy can match every value and still look generic; name the 3-9 moves and the bans that carry identity, and attack the maximalist list as trivia.
- **Adjudicate** each property with one question: *if this value changed, would the output stop looking like the reference?* Yes = load-bearing (goes to PROMPT.md). No = trivia (dna.json only).

The resolution is not a compromise: both are right about different documents (see table above).

### Step 3: Codify `dna.json`
Fill every key in `references/design-dna.schema.json` that applies; omit what genuinely does not (e.g. `motion` for static work). Non-negotiables:
- Colour names are **descriptive** ("dusty plum"), never token-style ("accent-500"). Image and video models cannot read tokens.
- Every font family has a **fallback** (silent Arial substitution kills reproductions quietly). Flag licence risk.
- Spacing in **percentages**, so one spec drives a carousel and a slide.
- `signatures`: 3-9, each written as a ratio or relationship, each with a `never`.
- `weird_move` in its own key.
- `bans`: at least 5, absolutes. Aim for bans to outnumber positive style rules.
- `meta.not_copied`: every real mark excluded. Reproduce the system, never the marks.

### Step 4: Write tests that can fail
8-12, binary, measurable. Mark `auto: true` for any a script can decide. Good: "accent covers under 8% of canvas", "max 3 type sizes per frame", "display-to-body ratio above 6:1", "weird move present exactly once", "body measure under 65 characters", "squint test: mass sits in the same places as the reference". Not tests: "feels premium", "looks clean". If two people could disagree, rewrite it.

Validate: `python3 scripts/lint_dna.py <slug-folder>` (checks structure, counts, coverage sums, fallbacks, token-style names, PROMPT.md size and order). Fix every FAIL before Step 5.

### Step 5: Reconstruct and diff (the step nobody does)
Close the reference. Rebuild it **from dna.json + PROMPT.md alone**, ideally in a fresh-context subagent that has never seen the original (only the spec and the original's *content*, not its image). Render the rebuild and put it beside the original. List every difference. Each difference is a field the spec forgot: fold it back, record it in `reconstruction.gaps_found`, increment `reconstruction.passes`, and go again. Expect 2-3 passes. Stop when a stranger could not pick the copy, or when Fabian calls it.

If a render is impossible (no tooling for the medium), say so plainly and mark `reconstruction.attempted: false`. The lint reports the style as **UNVERIFIED** until a pass is recorded; never present it as finished.

### Step 6: Emit the style skill
Scaffold with `python3 scripts/scaffold.py <slug>` (creates `style-<slug>/` in `~/.claude/skills/` from `assets/templates/`; use `--dest` to put it elsewhere), then fill it:

```
style-<slug>/
  SKILL.md         how to use this style (from template; write a real trigger description)
  PROMPT.md        the <2KB payload. THIS goes in a context window.
  dna.json         the full record. NEVER pasted into a prompt.
  reference/       the original, kept forever
  example/         one worked output, the canonical proof (the final Step 5 rebuild is fine)
  tools/check.py   the auto tests; exits non-zero on failure
```

`PROMPT.md` order is fixed, because attention is strongest at the ends:
1. Reference image, attached and named first
2. `soul.one_line`
3. The weird move, alone
4. The 3-9 signatures, as ratios
5. Bans, as absolutes
6. Palette and type: roles and coverage only
7. Archetype names and when to use each
8. The self-check, last, ending with the self-check instruction from the template

If a line would not change the output seen from three metres away, it belongs in dna.json. To add a tenth signature, delete one.

Because it was scaffolded into `~/.claude/skills/`, Claude Code picks it up automatically in new sessions.

### Step 7: Declare uncertainty
List every inferred (not measured) value and every rule under 70% confidence. These are where the style will drift first. Write them into `dna.json` under `reconstruction.uncertain` too, so the next session sees them.

## Rules for the analyst

- Never invent a value that could be measured. If it cannot be measured, say so and mark it inferred.
- Never copy a real logo, wordmark, licensed photo or proprietary typeface. List it in `meta.not_copied` and substitute.
- When output looks generic, **add a ban, not an instruction.** A ban deletes a whole region of options in one line; a positive rule is one weak vote against the training average.
- **One skill per style.** Never merge two identities. The average of two good designs is a bad design.
- Keep the style's `voice` bans consistent with your own copy rules (spelling, punctuation, banned words).

## Status is derived, not remembered

A style skill's state (verified or not, how many passes, open gaps) lives in its own `dna.json` `reconstruction` block. `lint_dna.py` reports it; nobody hand-maintains a status elsewhere. To see where any style stands: `python3 scripts/lint_dna.py <folder>`.

## Using a finished style skill

Load its `PROMPT.md` into the generating context, attach `reference/` and `example/`, generate, then run `tools/check.py` on the render plus the manual self-check. Never return an output with a failing test and a note explaining it away. 
