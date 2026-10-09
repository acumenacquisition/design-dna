# Design DNA (a Claude skill)

Turn designs you love into a style Claude follows every time, so your visuals stay consistent.

Design DNA studies one finished piece you love, writes down
the rules that make the look work (ratios, colours and how much of each, what's never allowed), tests them, and saves
the result as its own Claude skill. From then on, ask for a visual "in my style" and it follows the rules.

## Install

**Claude Code:** paste this into Claude Code:

> Install the Design DNA skill from https://github.com/acumenacquisition/design-dna into my Claude skills folder (~/.claude/skills/design-dna), then confirm it's available.

**Claude app (claude.ai or desktop):** download `design-dna.zip` from the latest release (Releases, on the right of this
page), then go to Customize > Skills > + > Create skill > Upload a skill and upload it. Code execution must be on
(Settings > Capabilities).

## Use

Start with `SKILL.md`. In short: collect designs you like, tell Claude what you like and don't, have it mock up a few
options and refine one until you love it, then run design-dna on that one design and name your style. It saves your
style as its own skill (`style-<name>`).

## Credit

The Design DNA method is by **Jack Roberts**: [Design DNA: one beautiful design into a permanent skill](https://app.notion.com/p/Design-DNA-One-beautiful-design-into-a-permanent-skill-3bee8d6bd1378159ab0ee0b9a88f44f8).
Jack also made [SlopMonster](https://github.com/ItsssssJack/SlopMonster). This repo adapts his write-up into an installable
skill and is maintained by Acumen so the install link stays stable. It is not affiliated with or endorsed by Jack Roberts;
all credit for the method is his.
