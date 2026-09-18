#!/usr/bin/env python3
"""
Pre-publish gate for this reproducibility package.

Run this before pushing to GitHub or creating a Zenodo-triggering release.
It does NOT replace the human judgment calls in docs/VERIFY_CHECKLIST.md —
it only catches mechanical regressions (a placeholder that crept back in,
a script that no longer reproduces stats.json). Exits non-zero on failure
so it can be used as a CI check or a pre-push hook.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories scanned for leftover placeholder text. The manuscript's own
# filename (TPEC2027_manuscript_DRAFT.docx) is a name, not content, and is
# deliberately not flagged here.
SCAN_DIRS = ["manuscript", "docs"]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bDRAFT\b"),
    re.compile(r"\[VERIFY\]"),
]
# Files whose content is allowed to mention these words because they are
# describing the check itself, not leaving a real placeholder behind.
ALLOWLIST = {
    "docs/VERIFY_CHECKLIST.md",
    "scripts/publish_gate.py",
    "docs/GITHUB_ZENODO_GUIDE.md",
}


def scan_placeholders() -> list[str]:
    problems = []
    for d in SCAN_DIRS:
        for path in (ROOT / d).rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in ALLOWLIST:
                continue
            if path.suffix in {".png", ".jpg", ".jpeg", ".pdf", ".docx"}:
                continue  # binary; DRAFT stamp inside the docx itself is checked separately if needed
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            for pat in PLACEHOLDER_PATTERNS:
                if pat.search(text):
                    problems.append(f"{rel}: matches {pat.pattern}")
    return problems


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def check_reproducibility() -> list[str]:
    problems = []
    stats_path = ROOT / "data" / "processed" / "stats.json"
    if not stats_path.exists():
        return [f"{stats_path} does not exist"]
    before_hash = sha256_of(stats_path)
    before_text = stats_path.read_text()

    # src/01_dedup_source.py is deliberately excluded from this automated
    # check: it reads from an upstream raw export that lives in a separate,
    # unpublished sibling project (ong-ot-dataset-pipeline) and is not
    # checked into this repo (see README.md "Reproducing the numbers" for
    # why, and what IS fully reproducible: everything from the deduplicated
    # CSV forward, which is a committed file in this repo).
    scripts = [
        "src/02_classify_pipeline_scope.py",
        "src/03_score_prioritization.py",
    ]
    for s in scripts:
        result = subprocess.run(
            [sys.executable, s], cwd=ROOT, capture_output=True, text=True
        )
        if result.returncode != 0:
            problems.append(f"{s} failed:\n{result.stderr[-2000:]}")
            return problems  # no point diffing if a script errored

    after_hash = sha256_of(stats_path)
    if before_hash != after_hash:
        after_text = stats_path.read_text()
        problems.append(
            "data/processed/stats.json changed after rerunning the pipeline "
            "scripts — the paper's numbers are not currently reproducible "
            "from the checked-in source. Diff the two versions before publishing."
        )
        # Restore the original so a failed gate run doesn't leave the repo dirty.
        stats_path.write_text(before_text)
    return problems


def check_verify_checklist_signed() -> list[str]:
    checklist = ROOT / "docs" / "VERIFY_CHECKLIST.md"
    if not checklist.exists():
        return ["docs/VERIFY_CHECKLIST.md is missing"]
    text = checklist.read_text()
    unchecked = re.findall(r"^- \[ \] \*\*(.+?)\*\*", text, re.MULTILINE)
    # The TPEC 2027 deadline item is allowed to stay unchecked — it's an
    # external fact, not something the author can sign off on.
    blocking_unchecked = [u for u in unchecked if "TPEC 2027" not in u]
    problems = []
    if blocking_unchecked:
        problems.append(
            "Unchecked judgment-call items remain in docs/VERIFY_CHECKLIST.md: "
            + "; ".join(blocking_unchecked)
        )
    if "Signed:" not in text or "Date:" not in text:
        problems.append("Sign-off block missing from docs/VERIFY_CHECKLIST.md")
    elif re.search(r"Signed: _+\s", text):
        problems.append("Sign-off block present but not actually filled in (still blank underscores)")
    return problems


def main() -> int:
    all_problems = []
    all_problems += [f"[placeholder] {p}" for p in scan_placeholders()]
    all_problems += [f"[checklist] {p}" for p in check_verify_checklist_signed()]
    all_problems += [f"[reproducibility] {p}" for p in check_reproducibility()]

    if all_problems:
        print("PUBLISH GATE: FAIL\n")
        for p in all_problems:
            print(f"  - {p}")
        print(f"\n{len(all_problems)} problem(s) found. Fix before publishing.")
        return 1

    print("PUBLISH GATE: PASS")
    print("  - No placeholder text found.")
    print("  - docs/VERIFY_CHECKLIST.md is signed and has no blocking unchecked items.")
    print("  - data/processed/stats.json reproduces exactly from the committed")
    print("    deduplicated CSV via src/02 and src/03 (src/01 needs an external,")
    print("    unpublished upstream file — see README.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
