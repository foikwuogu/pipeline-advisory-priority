"""
Compute the composite prioritization score for every row, using:
  - exploitation_score: known_exploited (KEV) as 1.0, else the row's EPSS
    score (0 if EPSS missing).
  - raw_urgency: exploitation_score, +0.2 if no_patch_available (capped at 1.0).
  - tsa_outcome coverage: baseline outcomes always counted for pipeline-relevant
    rows; TSA-3/TSA-6 counted only under their stated conditions
    (config/tsa_outcome_mapping.yaml).
  - overall_control_reduction: CPG 2.0 reduction and TSA-outcome coverage
    fraction stacked multiplicatively (same stacking convention as the
    existing cpg2_combined_risk_reduction column).
  - priority_score = raw_urgency * (1 - overall_control_reduction).

Higher priority_score = more urgent for a pipeline operator's attention
(more likely to be exploited and/or unpatched, less covered by known
compensating controls).

Usage:
    python3 src/score_prioritization.py
"""
from __future__ import annotations
import yaml
import pandas as pd

IN_CSV = "data/processed/pipeline_scored_v1.csv"
MAPPING_YAML = "config/tsa_outcome_mapping.yaml"
OUT_CSV = "data/processed/pipeline_prioritized_v1.csv"
QA_REPORT = "data/processed/qa_report_prioritization_v1.txt"


def load_mapping(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def response_flags_for_row(row: pd.Series, mapping: dict) -> list[str]:
    """TSA-3 / TSA-6: informational response-posture flags, NOT fed into the
    risk-reduction term (see note below on why they were removed from
    scoring: counting them as 'coverage' created a perverse cancellation
    where the most urgent, actively-exploited rows scored as fully
    mitigated, simply because their own urgency triggered more outcome
    matches. These are reported as a separate column instead."""
    threshold = mapping.get("epss_high_threshold", 0.10)
    known_exploited = bool(row.get("known_exploited", False))
    epss = row.get("epss")
    epss_val = float(epss) if pd.notna(epss) else 0.0

    flags = []
    for cond in mapping.get("conditional_outcomes", []):
        cid = cond["id"]
        if cid == "TSA-3" and (known_exploited or epss_val >= threshold):
            flags.append(cid)
        elif cid == "TSA-6" and known_exploited:
            flags.append(cid)
    return flags


def main() -> None:
    mapping = load_mapping(MAPPING_YAML)
    df = pd.read_csv(IN_CSV, low_memory=False)

    # tsa_outcome_coverage_fraction feeds the risk-reduction term below and is
    # deliberately held CONSTANT across all pipeline-relevant rows (the four
    # baseline outcomes only, 4/6). It represents "the fraction of the TSA's
    # six outcome groups for which a documented compensating-control mapping
    # exists that is applicable to pipeline OT equipment in general" — a
    # property of the CONTROL FRAMEWORK's coverage, not of any individual
    # vulnerability's severity. TSA-3/TSA-6 are reported separately as
    # response-posture flags and are NOT part of this fraction (see
    # response_flags_for_row docstring for why).
    baseline_n = len(mapping.get("baseline_outcomes", []))
    df["tsa_outcome_coverage_fraction"] = df["pipeline_relevant"].astype(float) * (baseline_n / 6.0)
    df["tsa_baseline_outcomes"] = df["pipeline_relevant"].apply(
        lambda rel: ",".join(mapping.get("baseline_outcomes", [])) if rel else ""
    )

    response_flags_list = [
        response_flags_for_row(row, mapping) if row.get("pipeline_relevant") else []
        for _, row in df.iterrows()
    ]
    df["tsa_response_flags"] = [",".join(f) for f in response_flags_list]

    exploitation_score = df["known_exploited"].astype(bool).astype(float)
    epss_filled = df["epss"].fillna(0.0)
    exploitation_score = exploitation_score.where(df["known_exploited"].astype(bool), epss_filled)
    df["exploitation_score"] = exploitation_score

    no_patch_bonus = df["no_patch_available"].astype(bool).astype(float) * 0.2
    df["raw_urgency"] = (df["exploitation_score"] + no_patch_bonus).clip(upper=1.0)

    cpg2 = df["cpg2_combined_risk_reduction"].fillna(0.0)
    tsa_cov = df["tsa_outcome_coverage_fraction"].fillna(0.0)
    df["overall_control_reduction"] = 1 - (1 - cpg2) * (1 - tsa_cov)

    df["priority_score"] = (df["raw_urgency"] * (1 - df["overall_control_reduction"])).round(6)

    df.to_csv(OUT_CSV, index=False)

    n = len(df)
    rel = df[df["pipeline_relevant"]]
    lines = []
    lines.append(f"QA report generated for prioritization scoring (v1), {n} total rows, {len(rel)} pipeline-relevant rows")
    lines.append("")
    lines.append("priority_score distribution, full dataset:")
    lines.append(str(df["priority_score"].describe()))
    lines.append("")
    lines.append("priority_score distribution, pipeline-relevant subset:")
    lines.append(str(rel["priority_score"].describe()))
    lines.append("")
    lines.append("Range check priority_score in [0,1]:")
    lines.append(f"  violations: {((df['priority_score'] < 0) | (df['priority_score'] > 1)).sum()}")
    lines.append("")
    lines.append("Top 15 pipeline-relevant advisories by priority_score:")
    top = rel.sort_values("priority_score", ascending=False).head(15)
    for _, r in top.iterrows():
        lines.append(
            f"  score={r['priority_score']:.3f} | cve_id={r.get('cve_id')} | "
            f"{r.get('ICS-CERT_Number')} | {r.get('Vendor')} / {r.get('Product')} | "
            f"tier={r.get('pipeline_tier')} | KEV={r.get('known_exploited')} | "
            f"EPSS={r.get('epss')} | no_patch={r.get('no_patch_available')} | "
            f"tsa_outcomes={r.get('tsa_baseline_outcomes')} + response:{r.get('tsa_response_flags')} | cpg2_reduction={r.get('cpg2_combined_risk_reduction')}"
        )
    lines.append("")
    lines.append("Bottom 5 pipeline-relevant advisories by priority_score (best-covered / lowest urgency):")
    bottom = rel.sort_values("priority_score", ascending=True).head(5)
    for _, r in bottom.iterrows():
        lines.append(
            f"  score={r['priority_score']:.3f} | cve_id={r.get('cve_id')} | "
            f"{r.get('ICS-CERT_Number')} | {r.get('Vendor')} / {r.get('Product')} | "
            f"tsa_outcomes={r.get('tsa_baseline_outcomes')} + response:{r.get('tsa_response_flags')} | cpg2_reduction={r.get('cpg2_combined_risk_reduction')}"
        )

    with open(QA_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\nWrote {OUT_CSV} ({n} rows)")
    print(f"Wrote {QA_REPORT}")


if __name__ == "__main__":
    main()
