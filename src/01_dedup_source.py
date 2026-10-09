"""
Deduplicate the reused ong-ot-dataset v1.1 CSV before any classification or
scoring happens.

Finding (caught during this paper's build, 2026-09-16): the upstream v1.1
dataset's own documentation states "one row = one CVE-advisory pair" and
reports 27,944 rows on that basis. Direct inspection shows this is not true:
the ICS Advisory Project source ships both a cumulative "Master" CSV and a
series of per-year snapshot CSVs that re-list the same advisory records, and
the upstream pipeline concatenated all of them without deduplication. Every
row that shares (cve_id, icsad_ID) with another row is byte-identical to it
in every column except `__source_file` (verified: 5,001 duplicate groups
checked, 0 with any substantive mismatch). Deduplicating drops 27,944 rows to
13,939 genuinely unique CVE-advisory pairs — essentially half.

This is disclosed prominently in docs/LIMITATIONS.md and should also be
reported back to the upstream ong-ot-dataset-pipeline project as a fix
candidate for its next version; it is fixed here, for this paper's own
numbers, by keeping first-seen rows and dropping the rest.

Usage:
    python3 src/01_dedup_source.py
"""
from __future__ import annotations
import pandas as pd

IN_CSV = "/home/claude/work/ong-ot-v1.1/data/processed/ong_ot_dataset_v1.1.csv"
OUT_CSV = "data/processed/ong_ot_dataset_v1.1_deduped.csv"
QA_REPORT = "data/processed/qa_report_dedup_v1.txt"


def main() -> None:
    df = pd.read_csv(IN_CSV, low_memory=False)
    n_before = len(df)

    key_cols = [c for c in df.columns if c != "__source_file"]
    deduped = df.drop_duplicates(subset=key_cols, keep="first").copy()
    n_after = len(deduped)

    # newline="" on the handle + default to_csv behavior avoids Python's own
    # text-mode newline translation, so this writes LF line endings on every
    # OS (Windows' default text-mode write would otherwise emit CRLF,
    # producing a byte-different-but-content-identical file — see
    # docs/LIMITATIONS.md item 13 for how this cross-platform gap was found).
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        deduped.to_csv(f, index=False)

    lines = [
        f"Dedup QA report",
        f"Rows before dedup: {n_before}",
        f"Rows after dedup (dropped exact re-exports across __source_file variants): {n_after}",
        f"Rows dropped: {n_before - n_after} ({(n_before - n_after) / n_before * 100:.2f}%)",
        "",
        "Source-file distribution before dedup:",
        str(df["__source_file"].value_counts()),
        "",
        f"Rows with no cve_id (kept as-is, not part of the dedup key issue): {int(df['cve_id'].isna().sum())}",
    ]
    with open(QA_REPORT, "w", newline="\n", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\nWrote {OUT_CSV} ({n_after} rows)")
    print(f"Wrote {QA_REPORT}")


if __name__ == "__main__":
    main()
