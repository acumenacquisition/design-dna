# Design DNA: method notes

Background for `SKILL.md`. Read when a style is drifting, or when someone asks why the rules are shaped the way they are.

## Why the payload is capped at 2KB

- **Rule count vs compliance.** The more instructions a model gets, the smaller the share it follows, and the drop is steady. A 200-rule spec is a lottery over which rules survive, and you do not choose the winners.
- **Lost in the middle.** Material in the middle of a long context is recovered markedly worse (reported gaps of 30%+) than material at the start or end. A great rule on line 147 of 400 is in the dead zone. That is why PROMPT.md has a fixed order and the weird move sits near the top, the self-check at the bottom.
- **Style resists words.** Strong style-transfer work sends content through text and style through an image, because fine-grained style is hard to describe.
- **The image is nearly free.** Image conditioning runs on its own pathway and does not compete for the attention the words are fighting over. Attach the reference every time.

## Why a ban beats an instruction

- **Image models:** a negative prompt is not advice. The sampler computes one prediction with the prompt and one with the negative, then steps away from the negative. It works on its own channel rather than competing with the rest of the prompt.
- **Any model:** a positive instruction ("use an asymmetric layout") is one vote against the training average. A ban ("never centre the hero") removes the average from the options. One ban can close a whole region: "never more than one accent colour" kills every multi-accent palette.
- **Checkable:** "is the hero centred?" has an answer. "does it feel editorial?" does not.

## Why maximalist vs minimalist is not a compromise

Exhaustive design systems (Material, Tailwind, W3C design tokens) are exhaustive because compilers and humans read them, and a compiler does not sample. A model does. So the exhaustive record and the lean payload are two different documents for two different readers. Keep both; compile one from the other; never paste the big one.

## Why Step 5 (reconstruct and diff) is the whole game

A spec that has never rebuilt its own source is untested. The rebuild exposes the rules you were sure were obvious. Doing the rebuild in a fresh-context subagent matters for the same reason fresh-eyed reviewers do: the context that wrote the spec silently fills its gaps from memory of the image.

## When it goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| Matches every value, still looks generic | Moves missing, or too many | Cut to 3-9 signatures, written as ratios |
| Drifts back to the stock AI look | Too few bans | Bans should outnumber positive style rules |
| Frame 1 and frame 8 do not match | No named layouts | Add archetypes |
| The accent reads as a theme | No coverage % | Add coverage per role |
| Works on a slide, breaks on a carousel | Pixel values in spacing | Convert to % of canvas |
| Obeys different rules each run | PROMPT.md over the cap | Cut to 2KB |
| Best rule keeps being ignored | Buried in the middle | Move it to the top or bottom |
| Fine but forgettable | No weird move | Find the one break in the system |
| Spec feels complete, output is wrong | Step 5 skipped | Rebuild the original from the spec and diff |

## Good vs bad tests

Good (binary, measurable): accent under 8% of canvas; max 3 type sizes per frame; largest-to-smallest type above 6:1; smallest type at least 28px at 1080px wide; weird move present exactly once; body measure under 65 characters; squint from three metres and the mass sits where it sits in the reference.

Bad: "feels premium", "looks clean", "on brand". If two people could disagree, it is not a test.
