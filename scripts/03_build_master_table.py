#!/usr/bin/env python3
"""Build the frozen pilot master table (v2) from the annotated loci.

Selects the 10 curated pilot loci, assigns a stable locus_id, adds biology/QC
notes, and carries the paper-consistent significance fields (single-variant P +
joint P for all three analyses, plus the no-proxy / no-biobank GWS flags).

Input : results/loci_annotated.csv
Output: results/master_table_v2.csv   (v1 kept as the immutable earlier record)
"""
import csv, pathlib

ANN="results/loci_annotated.csv"
OUT=pathlib.Path("results/master_table_v2.csv")
PILOT=["APOE","BIN1","CLU/PTK2B","ABCA7","TREM2","CR1","MS4A","SORL1","INPP5D","HLA"]
RARE={"TREM2","SORL1","ABCA7"}
EXC={"APOE":"APOE — exceptional effect; analyze separately",
     "HLA":"HLA — complex region / balancing-selection teaching case; analyze separately"}

ann={r["locus_name"]:r for r in csv.DictReader(open(ANN))}
def notes_for(r):
    n=[]
    if r["locus_name"] in RARE: n.append("rare-variant gene — separate lane")
    if r["locus_name"] in EXC: n.append(EXC[r["locus_name"]])
    try:
        if float(r["EAF"])<0.05 or float(r["EAF"])>0.95: n.append("low-frequency lead (EAF<5%)")
    except (ValueError,TypeError): pass
    return "; ".join(n)

FIELDS=["locus_id","locus_name","lead_snp","variant_id_GRCh38","chr","position","ref","alt",
        "effect_allele","other_allele","risk_allele","EAF_eur","OR",
        "P_main","P_noproxy","P_nobiobank","Pjoint_main","Pjoint_noproxy","Pjoint_nobiobank",
        "gws_noproxy","gws_nobiobank","origin","confidence_tier","tier","known_or_novel",
        "candidate_gene","gene_position","consequence","REVEL","I2","Het_P","source_GWAS","notes"]

out=[]
for i,name in enumerate(PILOT, start=1):
    r=ann[name]
    out.append(dict(
        locus_id=f"AD2026_L{i:03d}", locus_name=r["locus_name"], lead_snp=r["rsID"],
        variant_id_GRCh38=r["index_variant"], chr=r["chr"], position=r["position"],
        ref=r["ref"], alt=r["alt"], effect_allele=r["effect_allele"], other_allele=r["other_allele"],
        risk_allele=r["risk_allele"], EAF_eur=r["EAF"], OR=r["OR"],
        P_main=r["P_main"], P_noproxy=r["P_noproxy"], P_nobiobank=r["P_nobiobank"],
        Pjoint_main=r["Pjoint_main"], Pjoint_noproxy=r["Pjoint_noproxy"], Pjoint_nobiobank=r["Pjoint_nobiobank"],
        gws_noproxy=r["gws_noproxy"], gws_nobiobank=r["gws_nobiobank"],
        origin=r["origin"], confidence_tier=r["confidence_tier"], tier=r["tier"],
        known_or_novel=("known" if r["known_locus"]=="YES" else "novel"),
        candidate_gene=r["gene"], gene_position=r["gene_position"], consequence=r["variant_category"],
        REVEL=r["REVEL"], I2=r["I2"], Het_P=r["Het_P"],
        source_GWAS="Bellenguez 2026 (Nat Genet 58:1214-1225)", notes=notes_for(r)))

with OUT.open("w", newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(out)
print(f"Wrote {OUT}  ({len(out)} pilot loci)")
