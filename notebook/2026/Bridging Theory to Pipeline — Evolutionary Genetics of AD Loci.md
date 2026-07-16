---
tags: [popgen, project, synthesis]
area: Population Genetics
type: synthesis
created: 2026-07-13
---
# Bridging Theory to Pipeline: Evolutionary Genetics of AD Loci

*[[Learning Map|◀ Learning Map]] · Population Genetics · connects [[Vitti et al "Detecting Natural Selection in Genetic Data"]] to the Exercise 1 pilot*

## I. The Core Philosophy: The Pleiotropy Reframe

Standard evolutionary tests scan the genome for traits that provided a direct survival advantage. Alzheimer's Disease (AD) is the worst-case scenario for these tests because it is **late-onset** (acting after reproductive age) and **polygenic** (spread across hundreds of tiny variants).

To make this project work, you must rely on the **hypothesis-generating / pleiotropy reframe**:

* You are **not** asking: *"Was Alzheimer's selected for?"*
* You are asking the sideways question: *"Do these predefined AD loci happen to sit in regions that evolution shaped for an earlier-life reason (e.g., immunity, lipid metabolism, vascular biology)?"*

This reframe dodges the late-onset and polygenic problems entirely, allowing you to use these tools to annotate disease loci rather than testing the disease itself.

---

## II. The Dataset: Origin of the 91 Loci

The 91 loci come from a massive consensus meta-analysis of genome-wide association studies (GWAS) for Alzheimer's Disease and Related Dementias (ADRD), published in *Nature Genetics* (Bellenguez et al., 2026; 58:1214–1225). It pooled European-ancestry GWAS across the major consortia — including the European Alzheimer & Dementia Biobank (EADB), the International Genomics of Alzheimer's Project (IGAP), and the Psychiatric Genomics Consortium (PGC-ALZ) — led by Céline Bellenguez and Jean-Charles Lambert.

To reach the statistical power needed to confidently isolate these signals, the researchers pooled a staggering cohort of **128,681 cases** (including family-history "proxy" cases) and **849,833 controls**.

The final list of **91 Tier 1 loci** divides into two groups:

* **75 known loci:** risk regions already identified by earlier, smaller milestone studies.
* **16 new loci:** signals reaching genome-wide significance in European-ancestry samples for the first time in this analysis (including genes like PTPRC, MGAT5, FAM193B, and LILRB1/LILRB4).

The paper also flags a separate set of **18 Tier 2 loci** (15 of them new) that require further external validation.

### Why this origin matters for your pipeline

* **The European Ancestry Trap:** this entire mega-dataset was explicitly mapped using individuals of European ancestry. This is the exact origin of the **ascertainment bias** your project has to handle — the reason you cannot blindly trust a European "tag" SNP and must rigorously test for **LD portability** in other ancestral groups.
* **The "Proxy Case" Noise:** to reach nearly a million total participants, the study leaned heavily on biobanks (like the UK Biobank and FinnGen) that used "dementia by proxy" — including healthy participants who simply reported a parent or sibling with dementia, rather than only clinical AD diagnoses. This expanded the data but introduced broader, non-specific dementia risk loci. Tellingly, only **56 of the 91** loci stayed genome-wide significant once the analysis was restricted to clinically diagnosed AD (dropping the proxy/biobank cases) — direct evidence that proxy definitions pad the list, and exactly why **Phase A starts by tiering these 91 loci into strict clinical-AD vs. proxy groups.**

Ultimately, this consensus dataset is the definitive, bleeding-edge map of common-variant AD genetics — the perfect predefined set in which to look for historical evolutionary footprints.

> [!info] Further context
> [Genetic Factors in Exceptional Brain Aging](https://www.youtube.com/watch?v=XazM6haWpDg) discusses how variations in key AD risk genes such as APOE affect long-term cognitive health and resilience in "super agers."

---

## III. The Reference Panel: The 1000 Genomes Project

If the 91 loci are the specific "street addresses" of Alzheimer's risk in the genome, the **1000 Genomes Project (1000G)** is the global map you use to investigate who lives at those addresses and what the neighbourhood looks like.

### What it is
Completed in 2015, 1000G was an international effort to sequence the genomes of over 2,500 seemingly healthy individuals from 26 populations, grouped into five **super-populations**:

* **AFR** — African
* **EUR** — European
* **EAS** — East Asian
* **SAS** — South Asian
* **AMR** — Admixed American (populations in the Americas with mixed Indigenous, European, and African ancestry)

Crucially, it provides **phased data** (you know which variants sit together on the same physical chromosome) for millions of genetic variants across a genuinely diverse global sample.

### How 1000G relates to your 91 loci
Because the 91 AD loci were discovered almost entirely in European participants, you know almost nothing about their evolutionary history or how they behave in the rest of humanity. 1000G is the **reference panel** you project those loci onto to run the tests: its per-population allele frequencies feed the ΔAF / differentiation check (e.g., a variant at 20% in EUR but 0% in AFR and EAS is an immediate flag), its **phased haplotypes** power the LD-portability check, and the browsers built on top of it — the **1000 Genomes Selection Browser** and **PopHumanScan** — supply precomputed selection statistics (iHS, FST, Tajima's D) you look up by coordinate. *(The step-by-step mechanics live in §VIII; here the point is simply where the data comes from.)*

In short: **the 91 loci are your hypotheses, and 1000G is the environment you test them in.** You project the European-discovered disease loci onto the 1000G global background to see whether they carry the historical scars of natural selection.

---

## IV. The Reference Genome: The Coordinate Template (and Its Blind Spots)

Everything above is expressed against one shared coordinate system — the **human reference genome** (currently **GRCh38**). It is worth knowing what it actually is, because its limits are yet another source of the ascertainment bias your pipeline fights.

* **What it is:** a universal coordinate grid used as a baseline template. This works because all humans share about **99.9%** of the same DNA sequence, so one grid can locate everyone's variants.
* **Whose DNA it is:** a patchwork quilt. Roughly **70%** of the map comes from a single anonymous man from New York (sample code **RP11**), with the remaining ~30% stitched in from a handful of other volunteers from the late 1990s.
* **It is not "normal" or "perfect":** it is just a baseline. It actually contains known disease mutations, simply because the original volunteers happened to be carriers.
* **The major flaw — missing diversity:** if a population carries a unique chunk of DNA that was not present in the original volunteers, it simply **does not exist on the map**, and standard software ignores it — a massive, structural source of **ascertainment bias**, now baked into the map itself.
* **The modern fix — the Pangenome:** rather than a single flat map, scientists are building the **Human Pangenome** — a graph-like ("3D") reference showing branching genetic paths for different global ancestries.
* **Current status (Summer 2026):** the Pangenome is hitting a major stable completion milestone (**Release 3**), featuring over **350** telomere-to-telomere genomes that represent true global diversity.

> [!warning] Why this matters for you
> Your loci and your 1000G data are all expressed in **GRCh38** coordinates, so a European-biased reference is one more reason a signal (or its absence) can be an artifact rather than biology. It is the same **ascertainment** confounder your LD-portability checks target — only here it is built into the map. Until pangenome-based analysis is standard, treat the reference itself as part of the ascertainment problem.

---

## V. Biological Realities: Why to Expect a "Quiet" Result

Before running a single test, you must emotionally and intellectually internalize that **a clean, well-controlled negative is a highly likely and completely valid outcome.**

* **Standing Variation & Soft Sweeps:** Human immune and metabolic adaptations frequently act on pre-existing genetic variation (soft sweeps). Most standard statistical methods are either completely blind (SFS methods) or only weakly sensitive (LD methods) to soft sweeps. A faint or absent signal does not necessarily mean no selection occurred.
* **Polygenicity:** Because AD is polygenic, coordinated selection across many genes is practically invisible to single-locus statistics.
* **The Takeaway:** You should expect mostly weak or null results. Your protocol dictates that a clean negative beats an over-interpreted positive.

---

## VI. The Three Statistical Families

Your toolkit is strictly focused on **microevolution** (within-species, recent human variation).

1. **Site Frequency Spectrum (SFS):** Includes Tajima's D, Fay & Wu's H, and CLR. These catch *older, completed sweeps*.
2. **Linkage Disequilibrium (LD) / Haplotypes:** Includes iHS, XP-EHH, and EHH. These catch *recent, incomplete sweeps*—the exact timescale where human immune and lipid adaptations likely occurred. LD portability is a central pillar of your analysis.
3. **Population Differentiation:** Includes FST, ΔAF, XP-CLR, and PBS. Because AD loci were discovered in European cohorts, looking at cross-population frequency differences is your first diagnostic step.

> [!note] Note on Macroevolution
> Deep-time, cross-species tests (like Ka/Ks) mostly sit this out. The only exception is **constraint/purifying selection** (e.g., gnomAD LoF-intolerance), which you will use *only* for rare-variant genes (TREM2, SORL1, ABCA7). Never mix constraint signals with recent sweep evidence.

---

## VII. The Three Confounders & Your Defenses

Every signal is guilty until it survives these three filters.

### 1. Demography (The Biggest Threat)
The out-of-Africa bottleneck, genetic drift, and founder effects create cross-population differences that look identical to local adaptation.

* **Your Defense:** ΔAF is a descriptive flag, *not* proof of selection. You must use **matched-background/null controls** to compare your loci against a realistic demographic model. This is what makes the project "reviewer-proof."

### 2. Ascertainment Bias (Equipment Blind Spots)
Your data is skewed: GWAS discovery was European, SNP arrays use known variants, and reference panels are biased.

* **Your Defense:** Prioritize **LD portability**. You must determine if the signal is at the actual causal variant or if it is just a European tag. Never trust a label (rsID); always map to the exact genomic coordinate (chr:pos:REF:ALT).
* **How portability discriminates (Step 4):** you check the *neighbourhood* of each locus across the global 1000G map. If the lead SNP is highly portable across all ancestries, there is a good chance you are looking at the true, causal mutation. If the signal vanishes outside Europe, it is just a "European tag" — an ascertainment artifact. Identifying these tags is what stops you from making false evolutionary claims about global populations based on European blind spots.

### 3. Relaxed Constraint vs. Adaptation
A fast-changing gene could signify recent positive adaptation, or it could just mean the gene is no longer functionally vital (relaxed constraint).

* **Your Defense:** For rare-variant genes, high constraint equals *purifying selection* (functional importance). You must rely on functional context to resolve the direction of selection.

---

## VIII. The Systematic Pipeline

This 10-step pipeline operationalizes the concepts above. You build the foundation, read the signals, subtract the confounders, and finally grade the evidence. Each step gives the concept, then — under *At the keyboard* — the literal actions you take.

### Phase A: Get the Unit Right (The Foundation)
*Mostly organizing your spreadsheet so the tools don't break later.*

* **Step 1. Locus Set & Phenotype Tiering:** Select your loci (10 for the pilot, 91 total) and tier them by clinical AD vs. proxy/ADRD. *Controls for proxy ascertainment and encodes your hypothesis-generating reframe.*
    * *At the keyboard:* open the spreadsheet of 91 variants, add an **"Origin"** column, label each variant "Clinical AD" (real patients) or "Proxy" (family-history biobanks) from the source paper, then filter down to your 10 pilot variants.
* **Step 2. Strict Harmonization:** Lock everything to `chr:pos:REF:ALT` on GRCh38. *This is your first defense against data-artifact ascertainment (rsID, build, and strand errors).*
    * *At the keyboard:* for each pilot variant, drop the rsID; in a genome browser (Ensembl, UCSC, or dbSNP) set the build to **GRCh38**, find the exact coordinate, and record it as `chr:pos:REF:ALT` (e.g., `19:44908684:T:C`).
    * *Allele gotcha:* the reported **effect allele is not always the ALT** (in Table S2, AGRN's EA is the REF) — read the EA/OA column explicitly and derive the risk allele from the OR direction. See [[Understanding the Bellenguez 2026 Data — Tables and Columns]].

### Phase B: Read the Footprints
*Querying online databases and filling your spreadsheet with raw numbers.*

* **Step 3. Allele Frequency & ΔAF:** Read the per-super-population differentiation. *This utilizes the Differentiation family. Remember: this is just a descriptive flag, as demography looms large here.*
    * *At the keyboard:* plug the 10 coordinates into the 1000 Genomes database, record the % carrying the variant in EUR, AFR, and EAS, subtract to get ΔAF, and highlight any big gap (e.g., 20% in EUR vs 0% in AFR).
* **Step 4. Ancestry-Specific LD & Portability:** Check proxies across ancestries to see if the lead SNP is just a European tag. *This utilizes the LD family and acts as your Ascertainment defense.*
    * *At the keyboard:* in a tool like **LDlink**, inspect the DNA "neighbourhood" around each variant — does it travel with the same neighbouring mutations in African genomes as in European ones? If the correlation breaks down in non-Europeans, flag it as a **"European Tag"** (low portability).
* **Step 5. Precomputed Selection Statistics:** Read the footprints across all three families simultaneously (Tajima's D, iHS, FST, etc.) in specific genomic windows. *This acts as your composite test. Expect faint signals due to soft sweeps and polygenicity.*
    * *At the keyboard:* log into a precomputed database like **PopHumanScan**, paste the 10 coordinates, and copy the **Tajima's D, iHS, and FST** scores for the ~50 kb window around each variant into your master spreadsheet.

### Phase C: Subtract the Confounders (The Decisive Phase)
*Running statistics to decide whether the Phase B numbers are actually special or just noise.*

* **Step 6. Positive Controls & Matched-Null Background:** Use positive controls (e.g., LCT, EDAR) to prove the pipeline works. Then, compare your AD loci against demography-matched control regions. *This fixes the "outlier fallacy" and defeats the Demography confounder.*
    * *At the keyboard:* first run the **LCT** (lactase) gene through Steps 1–5 to confirm your tools light up on a known sweep; then use a script to draw hundreds of "dummy" coordinates with the same background mutation rate, and cross off any AD locus whose score isn't significantly above the dummy average.
* **Step 7. Sensitivity Analyses:** Vary your window sizes, ancestry groupings, and MAF bins. Drop extreme outliers like APOE or HLA. *This proves robustness and ensures you haven't cherry-picked your data.*
    * *At the keyboard:* rerun Step 5 while deliberately changing the settings — switch the window from 50 kb to 100 kb, drop APOE — and cross off any locus whose signal disappears when you do.

### Phase D: Interpret and Grade
*Stepping back from the raw data, putting on your biologist hat, and writing up the results.*

* **Step 8. Functional / Disease-Biology Annotation:** Propose the linked earlier-life trait (immunity, lipids) to fulfill the pleiotropy reframe. Separate the rare-variant constraint story from the common-variant sweep story.
    * *At the keyboard:* for the survivors, look each gene up in a biology database (e.g., **GeneCards**) to see what it does; if one sits by a cholesterol gene, write "Hypothesis: this region was selected for early-life lipid metabolism."
* **Step 9. Evidence Grading:** Run the data through your graded matrix (signal + robustness + LD + functional plausibility) and subtract penalties for red flags (single-window signals, non-portability). *This enforces the "convergent evidence / guilty-until-proven" rule.*
    * *At the keyboard:* build a literal scorecard — award points for convergence (e.g., high iHS **and** high FST), deduct points for a "European Tag" flag (Step 4) or a "Proxy" tier (Step 1).
* **Step 10. Ranked Hypotheses:** Output your ranked list using highly careful language (e.g., "compatible with selection on a linked trait," never "adaptive").
    * *At the keyboard:* write the report, rank the 10 loci high-to-low, give cautious conclusions for high scorers ("Locus X shows convergent evidence compatible with selection on a linked immune trait"), and report low scorers as likely demographic artifacts.

---

## IX. Pipeline Summary at a Glance

| Step | Action | Conceptual Embodiment | Confounder Controlled For |
| --- | --- | --- | --- |
| **1** | Tier 91/10 loci (clinical vs proxy) | Hypothesis-generating / Reframe | Proxy ascertainment; over-claiming |
| **2** | Harmonize (chr:pos:REF:ALT) | Get the unit right | Data-artifacts (rsID, strand, build) |
| **3** | Read Allele Frequencies (ΔAF) | Differentiation family | None yet (flags potential demography) |
| **4** | Test LD & Portability | LD family / Causal vs. Tag | Ascertainment (European lead SNP) |
| **5** | Read Selection Stats in Windows | All 3 families / Composite convergence | Soft sweeps / Polygenicity (expect faint) |
| **6** | Controls + Matched Nulls | The outlier-fallacy fix | **Demography** (The critical defense) |
| **7** | Sensitivity Analyses | Robustness testing | Cherry-picking |
| **8** | Functional Annotation | Pleiotropy reframe / Direction | Relaxed constraint / Nearest-gene bias |
| **9** | Evidence Grading | Convergent evidence | Over-interpretation |
| **10** | Ranked Report | Hypothesis-generating output | Over-claiming |

---

## X. Daily Operating Rules

1. **Demand Convergence:** A lone extreme iHS or high FST is a lead, never a verdict.
2. **Separate the Lanes:** Keep common-variant sweeps and rare-variant constraint completely separated.
3. **Quarantine APOE:** Treat it as a massive exception and analyze it apart so it doesn't distort your baseline intuition.
4. **Embrace the Negative:** Your job is to rule out demography and ascertainment. Given the biology, a rigorous list of "no global enrichment, but a few interesting loci" is the most defensible result you can produce.

## Links
- [[Vitti et al "Detecting Natural Selection in Genetic Data"]] — the theory behind this bridge
- [[Learning Map]]
