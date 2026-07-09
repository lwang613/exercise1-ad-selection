#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# 00_get_1000g.sh  —  Access 1000 Genomes 30x high-coverage data (GRCh38)
#
# 1000 Genomes is OPEN: no dbGaP, no application. This script does NOT bulk-
# download whole chromosomes by default. It STREAMS only the small genomic
# windows you care about (the pilot loci) straight from the EBI mirror using
# tabix remote access — fast, and a few MB instead of tens of GB.
#
# Requires: bcftools + tabix  (from environment.yml:  conda activate exercise1)
# ---------------------------------------------------------------------------
set -euo pipefail

# Base location of the 3,202-sample phased high-coverage call set (Byrska-Bishop 2022, GRCh38)
BASE="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20201028_3202_phased"
FILE_TPL="CCDG_14151_B01_GRM_WGS_2020-08-05_chrN.filtered.shapeit2-duohmm-phased.vcf.gz"

OUTDIR="data/raw/1000g"
mkdir -p "$OUTDIR"

# --- 1. Sample -> population panel (needed to compute per-population frequencies) ---
PANEL_URL="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/20130606_g1k_3202_samples_ped_population.txt"
if [ ! -f "$OUTDIR/samples_ped_population.txt" ]; then
  echo ">> Fetching sample->population panel"
  curl -fSL "$PANEL_URL" -o "$OUTDIR/samples_ped_population.txt"
fi

# --- 2. Detect contig naming (chr19 vs 19) once, from a header ---
url_for_chr () { local n="$1"; echo "$BASE/${FILE_TPL/chrN/chr$n}"; }
CHR=19
if bcftools view -h "$(url_for_chr 19)" 2>/dev/null | grep -q "ID=chr19"; then
  PREFIX="chr"; else PREFIX="";
fi
echo ">> Contig naming detected: '${PREFIX}19'"

# --- 3. Stream each region listed in the regions file into its own small VCF ---
# regions.tsv columns (tab-separated):  name  chrom  start  end   (GRCh38, 1-based)
REGIONS="${1:-refs/pilot_regions.tsv}"
echo ">> Using regions file: $REGIONS"

while IFS=$'\t' read -r name chrom start end; do
  [[ "$name" =~ ^#.*$ || -z "$name" ]] && continue
  region="${PREFIX}${chrom}:${start}-${end}"
  out="$OUTDIR/${name}.${PREFIX}${chrom}_${start}_${end}.vcf.gz"
  echo ">> $name  ->  $region"
  bcftools view -r "$region" "$(url_for_chr "$chrom")" -Oz -o "$out"
  bcftools index -t "$out"
done < "$REGIONS"

echo ">> Done. Region VCFs are in $OUTDIR/"
echo ">> Tip: for genome-wide work later, download a whole chromosome instead:"
echo "   curl -fSLO $BASE/${FILE_TPL/chrN/chr19}"
