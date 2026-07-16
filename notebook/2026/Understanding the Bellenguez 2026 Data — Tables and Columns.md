---
tags: [popgen, project, reference, data-dictionary]
area: Population Genetics
type: reference
created: 2026-07-13
---
# Understanding the Bellenguez 2026 Data: Tables & Columns

*[[Learning Map|◀ Learning Map]] · Population Genetics · a data dictionary for the supplementary tables you build Step 1 from*

> [!info] What this covers
> The supplement to Bellenguez et al. (2026) is one Excel file with **25 tables**. This note explains what each table is, and walks column-by-column through the three you actually use — **S2** (the locus list), **S3** (locus detail), and **S7** (the three-analysis stats). The allele bookkeeping (REF/ALT vs effect vs risk) is folded into the S2 walkthrough.

## Where the data lives
- **Raw file:** `data/raw/Bellenguez2026_supplementary_tables_MOESM4.xlsx` (immutable; all 25 sheets).
- Positions and alleles throughout are **GRCh38**, with variants written as `chr:pos:REF:ALT`.

## The 25 tables at a glance

| Group | Tables | What they are |
| --- | --- | --- |
| **Core — you use these** | **S2, S3, S7** | The 91+18 loci, their lead variants, per-locus detail, and stats across the three meta-analyses. |
| **Functional / pleiotropy** (Step 8) | S8, S9, S10, S11, S12, S13, S14 | Rare-variant (ADES/ADSP) results, single-cell (microglia) & pathway enrichment, and **PheWAS** (what other traits these loci hit). |
| **Polygenic-score half** (not your pilot) | S15, S16, S17, S18, S19, S20, S21 | The PGS weights and their associations with neuropathology. Skip for the annotation pilot. |
| **Context** | S1, S22 | Sample sizes per study; detailed per-study methods. |
| **Niche / robustness** | S4, S5, S6, S23, S24, S25 | Locus-specific deep dives, discordant variants, adjusted/sensitivity analyses. |

## Table S2 — the locus list (your Step 1 table)
One row per locus: **91 Tier 1 + 18 Tier 2**. This is where the master table comes from.

| Column | What it is | How you use it |
| --- | --- | --- |
| **Locus name** | A label for the locus, usually a nearby gene | A *name*, not proof of the causal gene (see the trap below) |
| **Meta-analysis** | Which analysis the lead is reported from | Uniformly `Main` for all 91 Tier 1 — so it does **not** give you the tiering (use S7) |
| **Tier** | `Tier1` (genuine — your 91) or `Tier2` (18, need validation) | Filter to Tier1 for the pilot |
| **known locus** | `YES` = previously known (replicated), `NO` = novel | The **75 known / 16 new** split |
| **index variant** | The lead SNP as `chr:pos:REF:ALT` on GRCh38 | Your harmonized `variant_id_GRCh38`; REF/ALT come from the map |
| **rsID** | dbSNP identifier | A label only (can be blank in other files — find by coordinate) |
| **chr / position** | GRCh38 coordinate | Redundant with the index variant, but handy |
| **EA/OA** | **Effect allele / other allele** | The OR is measured against the **EA** — and EA is **not** always the ALT |
| **EAF** | Effect-allele frequency in the (European) study sample | Your **European baseline** to compare against 1000G in Step 3 |
| **OR** | Odds ratio (95% CI) for the EA | `>1` → EA raises risk; `<1` → protective → used to derive the risk allele |
| **P** | Two-sided raw p-value | Significance of the association |
| **I2 / Het P** | Heterogeneity across the contributing studies | QC; flag a locus if I2 is very high |

> [!tip] The four allele roles (folded in from allele conventions)
> **REF / ALT** come from the *map* (GRCh38) — REF is just the letter printed at that position, arbitrary re: biology. **EA / OA** come from the *paper's reporting choice* — an OR relative to one allele is simply the reciprocal (`1/OR`) relative to the other, so "effect allele" is a framing choice, not a fact. The **risk allele** is the biological one you *derive*: EA if `OR > 1`, otherwise OA. Example — **APOE** `chr19:44908684:T:C`, EA = C, OR = 3.0 → risk allele **C** (EA = ALT here). Counter-example — **AGRN** `chr1:1080437:G:A`, EA = G = **REF**, OR = 0.96 → risk allele **A**. Never assume EA = ALT.

> [!tip] Heterogeneity: reading I2 and Het P
> This GWAS is a **meta-analysis** — a mash-up of dozens of independent studies (different labs, countries, hospitals). I2 and Het P ask one thing: *do those studies actually agree?* If the US, UK, and Swedish cohorts all saw the same risk for a variant, the signal is trustworthy; if they clash, the averaged OR can be an illusion.
> - **I2** (0–100) — the share of the variation that reflects *real disagreement* between studies rather than random noise. **I2 ≈ 0** = every cohort saw roughly the same OR (clean). **I2 > 50** = high disagreement (e.g., one cohort sees doubled risk, another none, another protective), so the averaged OR is masking a chaotic dataset.
> - **Het P** — a p-value testing whether that disagreement is statistically real. **High Het P** (e.g., 0.60) = studies mostly aligned, differences are just noise. **Low Het P** (< 0.05) = studies fundamentally clash.
> **As QC:** a locus with **high I2 and low Het P** has an unreliable average OR — flag it and lean less on its effect size (and its ΔAF interpretation).

## Table S3 — per-locus detail (main analysis)
Deeper information on each locus in the **main** meta-analysis, plus the conditional analyses that reveal *independent secondary signals* inside a locus. Columns come in blocks:

| Block | Key columns | What it gives you |
| --- | --- | --- |
| **Locus** | Locus number, Locus name, Tier, **chr / start / end**, known locus (+ name) | The **locus boundaries** (the window around the signal) |
| **Index variant** | index variant, rsID, position, lead variant, **Gene**, Gene position, **variant category**, **REVEL score** | The *mapped* gene (≠ locus name!), what kind of variant it is (intronic, missense, `outside_gene`…), and REVEL (missense deleteriousness, 0–1) |
| **Main results** | EA/OA, EAF, OR, P, I2, P het, **N cases, N controls, Effective sample size** | Full association stats + how much data backed this locus |
| **Conditional analyses** | GWS secondary signal, GCTA stepwise / joint / strict conditional OR & P, best tag, best tag r², exact conditional OR/P (uncond vs cond) | Whether the locus holds **more than one independent signal**, and whether the lead survives conditioning |

Use S3 for **functional annotation** (Gene, variant category, REVEL → Step 8) and to spot loci with **secondary signals**.

## Table S7 — the three-analysis stats (read it in full)

This is your **tiering source**, and it is the densest table in the file — so here is how to read it without getting lost.

### Why it exists
S7 runs every index variant through **three parallel meta-analyses** that differ only in *how a "case" is defined*, so you can watch a signal survive (or not) as the phenotype gets stricter:

- **Main** — everyone: clinically diagnosed + family-history "proxy" cases + large biobanks.
- **No-proxy** — the same, but with the **proxy cases removed**.
- **No-biobank** — the biobanks removed entirely, leaving **only clinically diagnosed AD** (the strictest definition).

### How the header is built (two rows)
S7 has a **two-row header**: a top **banner** row of merged group titles, and a **sub-header** row beneath. Read them together — e.g. *"No-biobank meta-analysis" → "P"*. Each data row is **one index variant**, and a locus with secondary signals gets more than one row, so S7 holds ~197 rows for the ~109 loci.

### Every column, group by group

**① Identity**

| Column | Meaning |
| --- | --- |
| Locus name | The locus label (a name, not necessarily the gene). |
| Index variant | The lead SNP as `chr:pos:REF:ALT` (GRCh38). |

**② "Meta-analysis identifying the index variant"** — did each analysis *independently discover* this variant as genome-wide significant?

| Column                       | Meaning                                                                                                                                |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| main / no-proxy / no-biobank | `YES` = this analysis found it on its own; `NA` = it did not (even if the variant still has stats in the blocks below).                |
| tag variant                  | A proxy SNP substituted if the exact variant was not available in an analysis (usually bc of technology advancements). Done through LD |
| signal summary               | Plain-English list of where it was found, e.g. `main + no-proxy`.                                                                      |

**③ Index variant / locus characteristics** (the annotation, same idea as S3)

| Column | Meaning |
| --- | --- |
| Tier / known locus | Tier1 or Tier2; previously known (`YES`) or novel (`NO`). |
| rsID / chr / position | Identity plus GRCh38 coordinate. |
| **Gene** | The *mapped* gene — **can differ from Locus name** (AGRN's variant maps to `RNF223`). |
| Gene position | `in_gene` or `outside_gene` (intergenic). |
| variant category | Consequence: `missense_variant`, `3_prime_UTR_variant`, intronic, … (`NA` if intergenic). |
| REVEL score | Deleteriousness of a *missense* variant (0–1); `NA` otherwise. |
| EA/OA | Effect allele / other allele. |

**④ Main meta-analysis**

| Column | Meaning |
| --- | --- |
| lead variant | `YES` if this is the locus's lead SNP in the main analysis. |
| GWS secondary signal | `YES` if this row is a *secondary* independent signal inside the locus. |
| start locus / end locus | The locus **window boundaries** (GRCh38) in the main analysis. |
| EAF / OR / P | Single-variant stats (frequency, odds ratio, raw p-value). |
| I2 / Het P | Heterogeneity across the contributing studies (see the S2 heterogeneity callout). |
| OR joint / P joint | Stats from the **joint analysis** across loci (conditioning on the other signals). |
| in joint main/no-proxy · P joint main/no-proxy | Whether it stays significant in a joint model combining the main + no-proxy data. |
| in joint main/no-biobank · P joint main/no-biobank | The same cross-check against the no-biobank data. |

**⑤ No-proxy meta-analysis** — the same core stats, recomputed with proxy cases removed:

| Column | Meaning |
| --- | --- |
| lead variant · start/end locus | Lead status and window in this analysis (`NA` if not the lead here). |
| EAF / OR / **P** / I2 / Het P | Single-variant stats without proxy cases. |
| OR joint / P joint | Joint-analysis stats. |

**⑥ No-biobank meta-analysis** — the identical set of columns, recomputed in **clinically diagnosed AD only**. The **`P`** column in this block is your tiering column.

**⑦ Comments** — free-text notes.

### Reading a row — three real examples

> [!example] The same three loci across all three analyses
> - **APOE** — identified in **all three** (YES/YES/YES). Watch the OR *strengthen* as the phenotype gets cleaner: **3.0 (main) → 3.07 (no-proxy) → 3.23 (no-biobank)**, because proxy cases *dilute* a real effect. No-biobank P = 0 → rock-solid **Clinical AD**.
> - **AGRN** — identified in **main only** (YES/NA/NA). It still *has* stats in the other blocks (no-proxy P = 7×10⁻⁷, no-biobank P = 5.7×10⁻⁵), but neither clears 5×10⁻⁸ → **proxy/biobank-dependent** → Origin = **Proxy**. (And its mapped Gene is `RNF223`, not AGRN.)
> - **ADAMTS4** — identified in **main + no-proxy** (YES/YES/NA). It survives removing *proxy* cases (no-proxy P = 5×10⁻⁹, GWS) but **not** removing all *biobank* data (no-biobank P = 1.9×10⁻⁷, not GWS). A clean reminder that "no-proxy" and "no-biobank" strip out *different* things.

### How to actually use it
- **Origin tier (your Step 1 column):** label a locus **Clinical AD** if its **No-biobank single-variant P < 5×10⁻⁸**, otherwise **Proxy**. This reproduces the paper's **56 of 91**. (The paper's strict definition also counts a variant as GWS via a significant *joint* P; the single-variant P is the simplest handle, and what we have been using.)
- **Don't confuse** the ②-block `YES/NA` "identified in" flags with "has a p-value there" — *every* variant carries stats in all three blocks; identification means it reached GWS on its own.
- **One locus can span multiple rows** (secondary signals). To get exactly one row per locus, filter to Main `lead variant = YES`.
- **Candidate gene** comes from the `Gene` column, never the `Locus name`.

## How these map to your master table

| Master-table field | Source |
| --- | --- |
| `locus_id` / locus name | S2 `Locus name` (+ S3 `Locus number`) |
| `lead_snp` (rsID) | S2 `rsID` |
| `variant_id_GRCh38` (`chr:pos:REF:ALT`) | S2 `index variant` |
| `effect_allele` / `other_allele` | S2 `EA/OA` |
| `EAF_europe` | S2 `EAF` |
| `OR`, `p_value` | S2 `OR`, `P` |
| `AD_risk_allele` | **derived** from EA + OR direction |
| `known_or_novel` | S2 `known locus` |
| `tier` | S2 `Tier` |
| `clinical_AD_robust` (Origin) | S7 `No-biobank P < 5e-8` |
| `candidate_gene` | S3/S7 `Gene` (≠ locus name) |
| `consequence` | S3/S7 `variant category`, `REVEL score` |

> [!warning] Two traps this data will spring on you
> 1. **Locus name ≠ causal gene.** The "Locus name" is a label; the *mapped* `Gene` (S3/S7) can differ — the **AGRN** locus's index variant actually maps to **RNF223 / `outside_gene`**. Keep `locus name` and `candidate gene` as separate fields.
> 2. **Effect allele ≠ ALT.** Read EA/OA per variant and derive the risk allele from the OR — **AGRN** reports EA = REF. Assuming EA = ALT silently flips the locus and inverts every downstream frequency.

**Key terms:** Tier 1 / Tier 2 · known vs novel locus · index variant (`chr:pos:REF:ALT`) · REF / ALT · effect allele (EA) / other allele (OA) · risk allele · EAF · OR · main / no-proxy / no-biobank meta-analysis · locus name vs mapped gene · variant category · REVEL score · conditional (secondary) signal · heterogeneity (I2, Het P)

> [!question] Check yourself
> 1. Which table gives you the clinical-vs-proxy tiering, and what threshold defines "robust in clinically diagnosed AD"?
> 2. For `chr1:1080437:G:A`, EA/OA = `G/A`, OR = 0.96 — name REF, ALT, EA, and the risk allele.
> 3. Why must "Locus name" and "candidate gene" be separate columns in your master table?
> 4. A locus has I2 = 70 and Het P = 0.01 — what does that say about its OR, and how should it affect your confidence?

## Links
- [[Bridging Theory to Pipeline — Evolutionary Genetics of AD Loci]] — Steps 1–2 build directly on these tables
- [[Working with 1000 Genomes — bcftools, VCFs, and the Data Stack]] — where REF/ALT/genotypes live in the VCF
- [[Learning Map]]
