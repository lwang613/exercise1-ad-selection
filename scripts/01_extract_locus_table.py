#!/usr/bin/env python3
"""Extract Supplementary Table S2 (lead variants of the Tier 1/2 loci) from the
Bellenguez 2026 consensus meta-analysis supplement into a clean CSV.

**Activating your virtual environment temporarily updates your system's `PATH` so that whether you explicitly type `python` or rely on the `env` shebang, your computer knows to use your project's isolated tools instead of the global defaults.**

Input : data/raw/Bellenguez2026_supplementary_tables_MOESM4.xlsx  (immutable raw)
Output: data/processed/bellenguez2026_lead_variants_TableS2.csv
"""
import csv, openpyxl, pathlib

RAW = pathlib.Path("data/raw/Bellenguez2026_supplementary_tables_MOESM4.xlsx")
OUT = pathlib.Path("data/processed/bellenguez2026_lead_variants_TableS2.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

wb = openpyxl.load_workbook(RAW, read_only=True, data_only=True)
ws = wb["Table S2"]
rows = list(ws.iter_rows(values_only=True))

# find the header row (the one that starts with "Locus name")
hdr_i = next(i for i, r in enumerate(rows) if r and str(r[0]).strip() == "Locus name")
header = [str(c).strip() for c in rows[hdr_i] if c is not None]
ncol = len(header)

data = [r[:ncol] for r in rows[hdr_i + 1:] if any(c is not None for c in r[:ncol])]

with OUT.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(header)
    w.writerows(data)

tier1 = sum(1 for r in data if str(r[2]).strip() == "Tier1")
tier2 = sum(1 for r in data if str(r[2]).strip() == "Tier2")
print(f"Wrote {OUT}  ({len(data)} rows: {tier1} Tier1, {tier2} Tier2)")
