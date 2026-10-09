"""
Classify each row of the reused ong-ot-dataset v1.1 for pipeline-sector
relevance, using two independent signals:

1. sector_signal: Critical_Infrastructure_Sector contains "Energy", "oil",
   or "pipeline" (case-insensitive substring; the raw field is semicolon-
   delimited and multi-valued, e.g. "Chemical; Energy; oil and gas").
2. pipeline_tier: vendor/product match against
   config/product_class_taxonomy_pipeline.yaml (tier1_pipeline_core /
   tier2_ot_general_energy / excluded / unmapped).

pipeline_relevant = sector_signal AND pipeline_tier in {tier1, tier2}

This is a NEW classification layer for this paper. It does not modify or
depend on the existing ong_product_class column already in the reused
dataset (that column stays as-is, reported alongside for comparison).

Usage:
    python3 src/classify_pipeline_scope.py
"""
from __future__ import annotations
import json
import yaml
import pandas as pd

SRC_CSV = "data/processed/ong_ot_dataset_v1.1_deduped.csv"
TAXONOMY_YAML = "config/product_class_taxonomy_pipeline.yaml"
OUT_CSV = "data/processed/pipeline_scored_v1.csv"
QA_REPORT = "data/processed/qa_report_pipeline_scope_v1.txt"


def load_taxonomy(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sector_signal(sector_text: str) -> bool:
    s = str(sector_text).lower()
    return ("energy" in s) or ("oil" in s) or ("pipeline" in s)


def pipeline_tier(vendor: str, product: str, taxonomy: dict) -> tuple[str, float]:
    vendor_l = str(vendor).strip().lower()
    product_l = str(product).strip().lower()
    combined = vendor_l + " " + product_l

    classes = taxonomy.get("classes", {})

    # Excluded takes precedence: a vendor known to make non-pipeline gear
    # should not be pulled back in by a coincidental product-keyword hit.
    excluded_vendors = [v.lower() for v in classes.get("excluded", {}).get("vendors", [])]
    if any(v in vendor_l for v in excluded_vendors):
        return "excluded", 0.0

    tier1 = classes.get("tier1_pipeline_core", {})
    tier1_vendors = [v.lower() for v in tier1.get("vendors", [])]
    tier1_keywords = [k.lower() for k in tier1.get("product_keywords", [])]
    if any(v in vendor_l for v in tier1_vendors) or any(k in combined for k in tier1_keywords):
        return "tier1_pipeline_core", tier1.get("weight", 0.9)

    tier2 = classes.get("tier2_ot_general_energy", {})
    tier2_vendors = [v.lower() for v in tier2.get("vendors", [])]
    if any(v in vendor_l for v in tier2_vendors):
        return "tier2_ot_general_energy", tier2.get("weight", 0.5)

    return "unmapped", taxonomy.get("unmapped_default_weight", 0.0)


def main() -> None:
    taxonomy = load_taxonomy(TAXONOMY_YAML)
    df = pd.read_csv(SRC_CSV, low_memory=False)

    df["pipeline_sector_signal"] = df["Critical_Infrastructure_Sector"].apply(sector_signal)

    tiers, weights = [], []
    for _, row in df.iterrows():
        t, w = pipeline_tier(row.get("Vendor", ""), row.get("Product", ""), taxonomy)
        tiers.append(t)
        weights.append(w)
    df["pipeline_tier"] = tiers
    df["pipeline_tier_weight"] = weights

    df["pipeline_relevant"] = df["pipeline_sector_signal"] & df["pipeline_tier"].isin(
        ["tier1_pipeline_core", "tier2_ot_general_energy"]
    )

    # newline="" avoids platform-dependent newline translation (Windows'
    # default text-mode write would emit CRLF) — see docs/LIMITATIONS.md
    # item 13.
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        df.to_csv(f, index=False)

    n = len(df)
    lines = []
    lines.append(f"QA report generated for pipeline-scope classification (v1), {n} rows")
    lines.append("")
    lines.append(f"Sector signal (Energy/oil/pipeline substring match): {df['pipeline_sector_signal'].sum()} of {n} ({df['pipeline_sector_signal'].mean()*100:.2f}%)")
    lines.append("")
    lines.append("Pipeline tier distribution (all rows, regardless of sector signal):")
    for k, v in df["pipeline_tier"].value_counts().items():
        lines.append(f"  {k}: {v} ({v/n*100:.2f}%)")
    lines.append("")
    lines.append(f"pipeline_relevant = sector_signal AND tier in {{tier1, tier2}}: {df['pipeline_relevant'].sum()} of {n} ({df['pipeline_relevant'].mean()*100:.2f}%)")
    lines.append("")
    lines.append("Pipeline-relevant subset: tier breakdown")
    rel = df[df["pipeline_relevant"]]
    for k, v in rel["pipeline_tier"].value_counts().items():
        lines.append(f"  {k}: {v} ({v/len(rel)*100:.2f}% of relevant subset)")
    lines.append("")
    lines.append("Pipeline-relevant subset: original ong_product_class comparison (existing 6-vendor column)")
    for k, v in rel["ong_product_class"].value_counts().items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("Pipeline-relevant subset: exploitation & patch signals")
    lines.append(f"  known_exploited=True: {rel['known_exploited'].sum()} of {len(rel)} ({rel['known_exploited'].mean()*100:.2f}%)")
    lines.append(f"  no_patch_available=True: {rel['no_patch_available'].sum()} of {len(rel)} ({rel['no_patch_available'].mean()*100:.2f}%)")
    epss_present = rel["epss"].notna()
    lines.append(f"  EPSS present: {epss_present.sum()} of {len(rel)} ({epss_present.mean()*100:.2f}%); mean EPSS among present = {rel.loc[epss_present, 'epss'].mean():.4f}")
    lines.append("")
    lines.append("Named spot checks (pipeline-relevant subset, tier1 only, first 5 by row order):")
    tier1_rel = rel[rel["pipeline_tier"] == "tier1_pipeline_core"].head(5)
    for _, r in tier1_rel.iterrows():
        lines.append(
            f"  cve_id={r.get('cve_id')} | ICS-CERT_Number={r.get('ICS-CERT_Number')} | "
            f"Vendor={r.get('Vendor')} | Product={r.get('Product')} | "
            f"sector={r.get('Critical_Infrastructure_Sector')} | "
            f"known_exploited={r.get('known_exploited')} | no_patch_available={r.get('no_patch_available')}"
        )

    with open(QA_REPORT, "w", newline="\n", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\nWrote {OUT_CSV} ({n} rows)")
    print(f"Wrote {QA_REPORT}")


if __name__ == "__main__":
    main()
