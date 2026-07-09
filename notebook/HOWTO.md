# How to keep this lab notebook

**What it is.** A chronological, dated, append-only record of what you did, why,
and what you found. The computational equivalent of a bench notebook. It is a
*diary* — distinct from the `README.md`, which is a *map* of the current state.

## Daily routine
1. Copy `TEMPLATE.md` to a new file named for today: `2026-07-13.md`.
2. Fill it in as you work — don't wait until the end of the day.
3. Never rewrite past entries. If you were wrong, add a new entry correcting it.
4. Link outputs (figures/tables) by their path in `results/` rather than pasting.

## Why this format
Six months from now a reviewer (or you) will ask "why did you exclude that locus?"
or "which window size did you use here?" The answer should be findable in one place,
with the reasoning intact.

## Industry-standard references
- Noble WS (2009), *A Quick Guide to Organizing Computational Biology Projects*,
  PLoS Computational Biology — the canonical layout; recommends a dated lab notebook.
- Wilson et al. (2017), *Good Enough Practices in Scientific Computing*, PLoS Comp Biol.

## Alternatives (ask your PI what the lab standard is)
- **This markdown log** — versioned in git alongside the code. Great default.
- **Jupyter notebooks** — best for *exploratory* analysis where code + output + notes
  live together; keep these in `scripts/` or a `notebooks/` folder and still write a
  short daily summary here.
- **Electronic Lab Notebook (ELN)** — Benchling, LabArchives, OneNote, Obsidian.
  Some labs mandate one for compliance/IP. If so, mirror key decisions here too.
