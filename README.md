# Which ICS advisories matter to a pipeline operator?

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22822467.svg)](https://doi.org/10.5281/zenodo.22822467)

**Status: Author-verified 2026-09-18.** TPEC 2027's own call for papers is
not yet published (see `docs/PUBLISH_GUIDE.md`), so this package is not yet
submitted anywhere. See `docs/VERIFY_CHECKLIST.md` for the full sign-off
record.

Reproducibility package for a manuscript prepared for the IEEE Texas Power and
Energy Conference (TPEC 2027), College Station, TX, Feb 7–9, 2027. Not yet
submitted — TPEC 2027's own call for papers isn't published yet.

> Ikwuogu, O. F. *Which ICS advisories matter to a pipeline operator?
> Exploitation likelihood, patch availability, and compensating controls
> across CISA advisories, 2010 to 2026.* IEEE Texas Power and Energy
> Conference (TPEC 2027). [IEEE Xplore DOI pending]

**Archived release:** [Zenodo v.1.0, DOI: 10.5281/zenodo.22822467](https://doi.org/10.5281/zenodo.22822467).

## What this project does

Reuses an existing, already-built CISA ICS advisory dataset (2010–2026, joined
with CISA KEV, FIRST.org EPSS, CISA Vulnrichment, and MITRE ATT&CK-for-ICS —
see "Data sources" below) and adds three new layers on top of it:

1. **A pipeline-sector relevance filter** (`pipeline_relevant`), combining a
   Critical-Infrastructure-Sector tag already in the raw data with a new,
   expanded vendor/product taxonomy built for this paper.
2. **A TSA Pipeline-2021-02 compensating-control mapping**, connecting each
   pipeline-relevant advisory to the TSA Security Directive's six outcome
   groups (via a second reused project, the TSA `crosswalk-lookup`), alongside
   the dataset's existing generic CISA CPG 2.0 mapping.
3. **A composite, fully transparent prioritization score** combining
   exploitation likelihood (KEV + EPSS), patch availability, and compensating-
   control coverage.

**A real data-quality bug was found and fixed during this build**: the reused
upstream dataset's 27,944-row count included ~50% exact duplicate rows (the
same advisory record re-exported across a cumulative "Master" file and
per-year snapshot files). This project deduplicates before any analysis; see
`docs/LIMITATIONS.md` item 1.

## Repository layout

```
config/     product_class_taxonomy_pipeline.yaml, tsa_outcome_mapping.yaml
data/raw/   reused source excerpts (upstream QA/provenance, TSA crosswalk)
data/processed/   deduplicated dataset, scored dataset, QA reports, stats.json
src/        01_dedup_source.py, 02_classify_pipeline_scope.py, 03_score_prioritization.py, 04_build_stats.py
figures/    fig1_advisories_by_year.png, fig2_priority_tiers.png
docs/       BUILD_SPEC.md, CODEBOOK.md, LIMITATIONS.md, VERIFY_CHECKLIST.md, NEXT_STEPS.md
manuscript/ the IEEE TPEC 2027 submission draft (.docx)
```

## Reproducing the numbers

`src/01_dedup_source.py` reads from an upstream raw export that lives in a
separate, unpublished sibling project (`ong-ot-dataset-pipeline`) and is
**not included in this repository** — running that script alone will fail
on a fresh clone. What *is* fully reproducible from what's checked in here
is everything downstream of deduplication:

```bash
pip install pandas pyyaml
python3 src/02_classify_pipeline_scope.py   # reads the committed data/processed/ong_ot_dataset_v1.1_deduped.csv
python3 src/03_score_prioritization.py
python3 src/04_build_stats.py               # writes data/processed/stats.json
```

`src/01_dedup_source.py` is included for transparency — it documents exactly
how the 27,944-row upstream export was deduplicated to the 13,939-row file
committed at `data/processed/ong_ot_dataset_v1.1_deduped.csv` (see
`docs/LIMITATIONS.md` item 1) — but it is not runnable standalone from this
repo alone. `scripts/publish_gate.py` checks reproducibility from the
deduplicated CSV forward (02 → 03 → 04), for the same reason.

Each script writes its own QA report to `data/processed/`. Every number quoted
in the manuscript is sourced from `data/processed/stats.json`, written by
`src/04_build_stats.py` (added 2026-10-08 — see `docs/LIMITATIONS.md` item 13
for why that file previously had no generating script at all, and what that
cost).

## Data sources

See `docs/BUILD_SPEC.md` for the full table with vintages and licenses:
ICS Advisory Project (ODbL v1.0), CISA KEV, FIRST.org EPSS, CISA Vulnrichment,
MITRE ATT&CK-for-ICS, and the TSA Pipeline-2021-02 crosswalk (from the
companion `crosswalk-lookup` project, code MIT / data CC BY 4.0).

## Author

Sole author: Friday Ogochukwu Ikwuogu (ORCID 0009-0009-2222-1318),
Independent Researcher, Odessa, Texas, USA. See `AUTHORS.json`.

## License

Code: MIT (`LICENSE`). Data: CC BY 4.0, except columns inherited from the ICS
Advisory Project, which remain ODbL v1.0 (share-alike, attribution required to
the ICS Advisory Project and this repository).
