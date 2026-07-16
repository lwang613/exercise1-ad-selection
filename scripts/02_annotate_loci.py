#!/usr/bin/env python3
"""Annotate every Bellenguez-2026 locus by joining Table S2 (lead variants) with
Table S7 (main / no-proxy / no-biobank results), following the PAPER's definitions.

A LOCUS is 'genome-wide significant in a meta-analysis' if ANY of its signals
(lead or secondary) is identified there — reproducing the paper's counts
(75/91 in no-proxy, 56/91 in no-biobank). We therefore aggregate S7's
"Meta-analysis identifying the index variant" (YES/NA) flags per locus.

Per lead we also carry the single-variant P and the joint P for all three
analyses, so the authoritative fields are on record.

Origin           = "Clinical AD" if the locus is GWS in no-biobank, else "Proxy".
confidence_tier  = A_clinical_robust / B_noproxy_robust / C_main_only.

Input : data/processed/bellenguez2026_lead_variants_TableS2.csv
        data/raw/Bellenguez2026_supplementary_tables_MOESM4.xlsx (sheet Table S7)
Output: results/loci_annotated.csv
"""
import csv, pathlib, openpyxl
from collections import defaultdict

RAW="data/raw/Bellenguez2026_supplementary_tables_MOESM4.xlsx"
S2 ="data/processed/bellenguez2026_lead_variants_TableS2.csv"
OUT=pathlib.Path("results/loci_annotated.csv"); OUT.parent.mkdir(exist_ok=True)

def parse_p(v):
    if v is None: return None
    s=str(v).strip().replace("<","").strip()
    if s in ("","NA","nan"): return None
    try: return float(s)
    except ValueError: return None
def parse_or(v):
    if v is None: return None
    tok=str(v).strip().split("(")[0].split()
    try: return float(tok[0])
    except (ValueError,IndexError): return None
def yes(v): return str(v).strip().upper()=="YES"

wb=openpyxl.load_workbook(RAW, read_only=True, data_only=True)
s7=list(wb["Table S7"].iter_rows(values_only=True))
grp=[];last=None
for g in s7[2]:
    if g not in (None,""): last=g
    grp.append(last)
sub=s7[3]
def col(gs,se):
    for i,(g,s) in enumerate(zip(grp,sub)):
        if g and gs in str(g) and str(s).strip()==se: return i
    raise KeyError(f"{gs}/{se}")
C=dict(name=0, idx=1,
    id_np=col("identifying","no-proxy"), id_nb=col("identifying","no-biobank"),
    gene=col("characteristic","Gene"), gpos=col("characteristic","Gene position"),
    vcat=col("characteristic","variant category"), revel=col("characteristic","REVEL score"),
    p_main=col("Main meta-analysis","P"), p_np=col("No-proxy","P"), p_nb=col("No-biobank","P"),
    pj_main=col("Main meta-analysis","P joint"), pj_np=col("No-proxy","P joint"), pj_nb=col("No-biobank","P joint"))

by_variant={}
by_locus=defaultdict(lambda: {"gws_np":False,"gws_nb":False})
for r in s7[4:]:
    if r[C["idx"]] is None: continue
    d={k:r[v] for k,v in C.items()}
    by_variant[str(r[C["idx"]])]=d
    L=by_locus[str(r[C["name"]])]
    if yes(d["id_np"]): L["gws_np"]=True     # locus GWS in no-proxy  if ANY signal is
    if yes(d["id_nb"]): L["gws_nb"]=True      # locus GWS in no-biobank if ANY signal is

out, unmatched = [], []
for r in csv.DictReader(open(S2)):
    idx=r["index variant"]; chrom,pos,ref,alt=idx.split(":")
    ea,oa=(r["EA/OA"].split("/")+[""])[:2]
    orv=parse_or(r["OR"]); risk=(ea if orv and orv>1 else oa) if orv is not None else ""
    d=by_variant.get(idx)
    if d is None: unmatched.append(idx)
    locus=by_locus[str(d["name"])] if d else {"gws_np":False,"gws_nb":False}
    gws_nb, gws_np = locus["gws_nb"], locus["gws_np"]
    tier="A_clinical_robust" if gws_nb else ("B_noproxy_robust" if gws_np else "C_main_only")
    g=lambda k: d[k] if d else None
    out.append(dict(
        locus_name=r["Locus name"], tier=r["Tier"], known_locus=r["known locus"],
        index_variant=idx, rsID=r["rsID"], chr=chrom.replace("chr",""), position=pos,
        ref=ref, alt=alt, effect_allele=ea, other_allele=oa, EAF=r["EAF"], OR=orv, risk_allele=risk,
        gws_noproxy=("YES" if gws_np else "NA"), gws_nobiobank=("YES" if gws_nb else "NA"),
        origin=("Clinical AD" if gws_nb else "Proxy"), confidence_tier=tier,
        P_main=parse_p(g("p_main")), P_noproxy=parse_p(g("p_np")), P_nobiobank=parse_p(g("p_nb")),
        Pjoint_main=parse_p(g("pj_main")), Pjoint_noproxy=parse_p(g("pj_np")), Pjoint_nobiobank=parse_p(g("pj_nb")),
        gene=g("gene"), gene_position=g("gpos"), variant_category=g("vcat"), REVEL=g("revel"),
        I2=r["I2"], Het_P=r["Het P"]))

with OUT.open("w", newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
from collections import Counter
t1=[x for x in out if x["tier"]=="Tier1"]
print(f"Wrote {OUT}  ({len(out)} loci; {len(t1)} Tier1)")
print("unmatched:", unmatched or "none")
print("Tier1 GWS no-proxy (paper 75):", sum(x['gws_noproxy']=='YES' for x in t1))
print("Tier1 GWS no-biobank / Clinical AD (paper 56):", sum(x['gws_nobiobank']=='YES' for x in t1))
print("confidence:", dict(Counter(x["confidence_tier"] for x in t1)))
