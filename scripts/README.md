# scripts/

All analysis code lives here. Naming convention: number scripts in run order so the
pipeline is self-documenting.

```
01_build_master_table.py     # extract + harmonize the 91 loci
02_allele_frequencies.py     # 1000G risk-allele AF per super-population, dAF
03_ld_portability.py         # LD proxies across EUR/AFR/EAS/SAS/AMR
04_selection_annotation.py   # precomputed selection stats in windows
05_matched_null.py           # matched-background enrichment
```

Each script reads from `data/` and writes to `data/processed/` or `results/`.
Nothing here should require manual editing of inputs — raw data stays immutable.
