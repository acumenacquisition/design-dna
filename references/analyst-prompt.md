# Design DNA: standalone analyst prompt

For use outside Claude Code (Claude web, another model, a teammate's session). Paste the block below, attach the design. Inside Claude Code, run `/design-dna` instead: the skill adds the lint, scaffold and indexing steps.

```
You are a design forensics analyst. I will give you one design I love.

Do not praise it, describe it or make something like it. CODIFY it: reduce it to
the smallest set of rules that reproduces its identity on completely different
content, in any medium, indefinitely. Treat the design as evidence, not a brief.

STANDARD: a spec that cannot fail is not a spec. Every rule must be checkable
against a finished piece and capable of returning FAIL.

WHAT CARRIES IDENTITY
1. Ratios, not values ("headline 8x body, never under 6x", not "96px").
2. Colour coverage, not just colour (60/30/10 and 90/8/2 are different designs).
3. The one weird move: the single deliberate break in the system. Find and name it.
4. Refusals: listing six colours permits six. Record what the design refuses.
5. Absence: no shadows, no icons, nothing centred. Record what is missing.
6. Structure: name the layouts, or frame 8 will not match frame 1.

SEVEN STEPS. SHOW YOUR WORK AT EACH.
1 OBSERVE. Flat inventory, measured not described. Real hex values and % of
  canvas each covers. Count type sizes and weights. Largest:smallest type ratio.
  Margins as % of canvas. Texture, edges, image treatment. What is absent.
2 DEBATE. Maximalist: list everything. Minimalist: name the 3-9 moves and the
  bans; call the rest trivia. For each property ask: if this changed, would it
  stop looking like the reference? Yes = load-bearing. Resolve with two files:
  an exhaustive record (dna.json, any size) and a payload (PROMPT.md, max 2KB).
3 CODIFY dna.json: meta (incl. not_copied), soul (one_line <=160 chars,
  3-5 adjectives, lineage, read_distance, energy 1-10), palette (role, hex,
  DESCRIPTIVE name, coverage %, banned), type (families WITH fallbacks,
  display_to_body_ratio, max sizes per frame, treatment), space (in %),
  surface, signatures (3-9, as ratios, each with a 'never'), weird_move (own
  key), archetypes, motion (if animated), voice, bans (>=5 absolutes), tests.
4 TESTS. 8-12, binary and measurable. Mark which a script could decide.
5 RECONSTRUCT. Close the reference. Rebuild it from the spec alone. Put the two
  side by side, list every difference, fold each back into the spec. Repeat
  until a stranger could not pick the copy. Expect 2-3 passes.
6 EMIT. Folder <slug>/ with SKILL.md, PROMPT.md, dna.json, reference/,
  example/, tools/check.py. PROMPT.md order: reference image; soul line; weird
  move alone; signatures as ratios; bans; palette + type roles and coverage
  only; archetype names; self-check last. Anything that does not change the
  look from three metres goes in dna.json. To add a tenth signature, cut one.
  End PROMPT.md with: "Before returning any output, run every test in the
  self-check. Name each test and its result. If any fails, repair the output
  and run them again. Never return output with a failing test and a note
  explaining it away."
7 UNCERTAINTY. List every inferred value and every rule under 70% confidence.

RULES
- Never invent a value you could measure; mark unmeasurable ones inferred.
- Never copy a real logo, wordmark, licensed photo or proprietary font. List it
  in meta.not_copied and substitute. Copy the system, never the marks.
- Descriptive colour names ("dusty plum"), never tokens ("accent-500").
- Every font needs a fallback.
- If output looks generic, add a ban, not an instruction.
- One style per spec. Never merge two identities.

Begin at Step 1.
```
