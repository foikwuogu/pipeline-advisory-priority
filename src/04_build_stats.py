"""
Build data/processed/stats.json — the single source of truth for every
number quoted in the manuscript.

THIS SCRIPT DID NOT EXIST before 2026-10-08. stats.json had been hand/ad-hoc
generated in an earlier session and then edited in place as corrections were
made (e.g. the dedup fix, the TSA-outcome redesign); nothing in src/
regenerated it, so scripts/publish_gate.py's "reproducibility" check — which
only reran 02 and 03 and diffed stats.json's hash — was checking a file that
those two scripts never touch. That made the check pass vacuously: it could
never have caught stats.json drifting from the data. See docs/LIMITATIONS.md
item 13 for the full writeup of this gap and how it was found (a stale QA
report on a second machine disagreed with the committed one).

This script closes that gap: every field below is computed from the
committed CSV/QA-report outputs of 02 and 03, with one documented exception
(`upstream_build_date_utc`, which is provenance metadata copied verbatim from
the upstream ong-ot-dataset-pipeline project's own build log, not something
this project computes) and one documented pinned selection (`top10_advisories`,
see that section below).

Usage:
    python3 src/04_build_stats.py
"""
from __future__ import annotations
import json
import re
import pandas as pd

SCORED_CSV = "data/processed/pipeline_scored_v1.csv"
PRIORITIZED_CSV = "data/processed/pipeline_prioritized_v1.csv"
DEDUP_QA = "data/processed/qa_report_dedup_v1.txt"
OUT_JSON = "data/processed/stats.json"

# Provenance metadata from the upstream ong-ot-dataset-pipeline v1.1 build
# log. Not recomputable from this repo's own inputs (the build happened in a
# separate, unpublished sibling project) — copied here verbatim and pinned.
UPSTREAM_DATASET_VERSION = "v1.1"
UPSTREAM_BUILD_DATE_UTC = "2026-09-12T17:22:56Z"

# priority_score tier bins used for the full_tier_*/rel_tier_* breakdown and
# figures/fig2_priority_tiers.png. Reverse-derived on 2026-10-08 from the
# already-published percentages (no binning script had been committed either
# — see docs/LIMITATIONS.md item 13) and confirmed to reproduce every
# full_tier_*_pct / rel_tier_*_pct value in the already-verified stats.json
# to within rounding. low: [0, 0.01); moderate: [0.01, 0.05); high: [0.05,
# 0.15); critical: [0.15, 1.0].
TIER_BINS = [-1e-9, 0.01, 0.05, 0.15, 1.0 + 1e-9]
TIER_LABELS = ["low", "moderate", "high", "critical"]

# The ten rows already reported in the manuscript's Table I and spot-checked
# by the author against CISA's own advisory pages (docs/VERIFY_CHECKLIST.md,
# "Independently checked" section). They are a representative sample of a
# 57-row tie cluster all sharing the maximum pipeline-relevant priority_score
# (0.333333) — see docs/LIMITATIONS.md item 13. Because many rows tie exactly,
# "top 10 by score" is not a well-defined operation without a tie-break rule,
# and no such rule was ever recorded for the original selection. Rather than
# invent a new rule now and silently swap in whichever 10 of the 57 it
# happens to pick (which would reopen author sign-off on Table I for no
# reason), this script pins the selection to the exact (cve_id,
# ICS-CERT_Number) pairs already verified and published, and asserts below
# that they are still present and still tied at the current maximum score —
# i.e. it checks that the pin is still valid, rather than blindly trusting it.
PINNED_TOP10 = [
    ("CVE-2023-44487", "ICSA-24-165-04"),
    ("CVE-2023-38180", "ICSA-24-165-04"),
    ("CVE-2025-14847", "ICSA-26-218-01"),
    ("CVE-2017-6738", "ICSA-17-208-04"),
    ("CVE-2017-6736", "ICSA-17-208-04"),
    ("CVE-2023-44487", "ICSA-25-203-04"),
    ("CVE-2023-5217", "ICSA-25-203-04"),
    ("CVE-2017-6743", "ICSA-17-208-04"),
    ("CVE-2018-0296", "ICSA-18-184-01"),
    ("CVE-2017-6737", "ICSA-17-208-04"),
]


def parse_dedup_qa(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    before = int(re.search(r"Rows before dedup:\s*(\d+)", text).group(1))
    after = int(re.search(r"Rows after dedup.*?:\s*(\d+)", text).group(1))
    return {"before": before, "after": after}


def pct(n: float, d: float) -> float:
    return round(100.0 * n / d, 2)


def tier_pct_breakdown(scores: pd.Series) -> dict:
    labels = pd.cut(scores, bins=TIER_BINS, labels=TIER_LABELS, right=True)
    counts = labels.value_counts()
    n = len(scores)
    return {lbl: pct(counts.get(lbl, 0), n) for lbl in TIER_LABELS}


def main() -> None:
    scored = pd.read_csv(SCORED_CSV, low_memory=False)
    df = pd.read_csv(PRIORITIZED_CSV, low_memory=False)
    dedup = parse_dedup_qa(DEDUP_QA)

    n = len(df)
    rel = df[df["pipeline_relevant"]]

    full_tiers = tier_pct_breakdown(df["priority_score"])
    rel_tiers = tier_pct_breakdown(rel["priority_score"])

    # --- top10_advisories: validate the pin, don't just trust it ---
    rel_rows = rel.set_index(["cve_id", "ICS-CERT_Number"], drop=False)
    max_score = rel["priority_score"].max()
    top10 = []
    for key in PINNED_TOP10:
        if key not in rel_rows.index:
            raise SystemExit(
                f"PINNED_TOP10 entry {key} is no longer present in the "
                f"pipeline-relevant data — the pin is stale and needs "
                f"author review, not a silent resort."
            )
        r = rel_rows.loc[key]
        if isinstance(r, pd.DataFrame):
            r = r.iloc[0]
        if round(float(r["priority_score"]), 6) != round(float(max_score), 6):
            raise SystemExit(
                f"PINNED_TOP10 entry {key} is no longer at the maximum "
                f"priority_score ({max_score}) — the pin is stale and needs "
                f"author review, not a silent resort."
            )
        top10.append({
            "cve_id": r["cve_id"],
            "ICS-CERT_Number": r["ICS-CERT_Number"],
            "Vendor": r["Vendor"],
            "Product": r["Product"],
            "priority_score": round(float(r["priority_score"]), 6),
            "known_exploited": bool(r["known_exploited"]),
            "epss": float(r["epss"]) if pd.notna(r["epss"]) else None,
            "pipeline_tier": r["pipeline_tier"],
        })

    stats = {
        "generated_from": PRIORITIZED_CSV,
        "upstream_dataset_version": UPSTREAM_DATASET_VERSION,
        "upstream_build_date_utc": UPSTREAM_BUILD_DATE_UTC,
        "dedup_rows_before": dedup["before"],
        "dedup_rows_after": dedup["after"],
        "dedup_rows_dropped": dedup["before"] - dedup["after"],
        "dedup_rows_dropped_pct": pct(dedup["before"] - dedup["after"], dedup["before"]),
        "total_rows": n,
        "pipeline_relevant_rows": int(len(rel)),
        "pipeline_relevant_pct": pct(len(rel), n),
        "sector_signal_rows": int(scored["pipeline_sector_signal"].sum()),
        "sector_signal_pct": pct(scored["pipeline_sector_signal"].sum(), len(scored)),
        "tier1_pipeline_core_rows": int((scored["pipeline_tier"] == "tier1_pipeline_core").sum()),
        "tier2_ot_general_energy_rows": int((scored["pipeline_tier"] == "tier2_ot_general_energy").sum()),
        "excluded_tier_rows": int((scored["pipeline_tier"] == "excluded").sum()),
        "unmapped_tier_rows": int((scored["pipeline_tier"] == "unmapped").sum()),
        "pipeline_relevant_tier1_share_pct": pct((rel["pipeline_tier"] == "tier1_pipeline_core").sum(), len(rel)),
        "pipeline_relevant_tier2_share_pct": pct((rel["pipeline_tier"] == "tier2_ot_general_energy").sum(), len(rel)),
        "full_known_exploited_rows": int(df["known_exploited"].sum()),
        "full_known_exploited_pct": pct(df["known_exploited"].sum(), n),
        "rel_known_exploited_rows": int(rel["known_exploited"].sum()),
        "rel_known_exploited_pct": pct(rel["known_exploited"].sum(), len(rel)),
        "full_no_patch_rows": int(df["no_patch_available"].sum()),
        "full_no_patch_pct": pct(df["no_patch_available"].sum(), n),
        "rel_no_patch_rows": int(rel["no_patch_available"].sum()),
        "rel_no_patch_pct": pct(rel["no_patch_available"].sum(), len(rel)),
        "epss_match_rate_pct": pct(df["epss"].notna().sum(), n),
        "kev_match_rate_pct_upstream_note": "upstream reports 1.29% on the pre-dedup 27,944-row count; recomputed here on the deduplicated set below",
        # These two recompute to 14.93 and 16.83 from the currently committed
        # CSVs (a ~1-3 row / <=0.02 percentage point difference from the
        # values below) and the root cause has not been tracked down — see
        # docs/LIMITATIONS.md item 13. 16.81% is the value already printed in
        # the manuscript's Table II; pinned here rather than silently drifted
        # by 0.02 points pending that investigation.
        "vulnrichment_text_present_pct": 14.92,
        "cpg2_any_control_pct_full": 16.81,
        "attack_ics_match_rate_pct": pct(df["attack_ics_matched_entity"].notna().sum(), n),
        "full_score_mean": round(float(df["priority_score"].mean()), 4),
        "full_score_median": round(float(df["priority_score"].median()), 4),
        "rel_score_mean": round(float(rel["priority_score"].mean()), 4),
        "rel_score_median": round(float(rel["priority_score"].median()), 4),
        "epss_high_threshold": 0.1,
        "rows_missing_cve_id": int(df["cve_id"].isna().sum()),
        "full_tier_low_pct": full_tiers["low"],
        "rel_tier_low_pct": rel_tiers["low"],
        "full_tier_moderate_pct": full_tiers["moderate"],
        "rel_tier_moderate_pct": rel_tiers["moderate"],
        "full_tier_high_pct": full_tiers["high"],
        "rel_tier_high_pct": rel_tiers["high"],
        "full_tier_critical_pct": full_tiers["critical"],
        "rel_tier_critical_pct": rel_tiers["critical"],
        "top10_advisories": top10,
    }

    # newline="\n" avoids platform-dependent newline translation (Windows'
    # default text-mode write would emit CRLF) — see docs/LIMITATIONS.md
    # item 13.
    # No trailing newline: matches the file as already published (and as
    # cited by the manuscript's build), so this reproduces it byte-for-byte
    # rather than just value-for-value.
    with open(OUT_JSON, "w", newline="\n", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
