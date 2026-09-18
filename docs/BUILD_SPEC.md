# Build spec: Which ICS advisories matter to a pipeline operator?

**Status:** Author-verified 2026-09-18. See `docs/VERIFY_CHECKLIST.md` for the sign-off record.

## Target

Ikwuogu, O. F., et al. *Which ICS advisories matter to a pipeline operator? Exploitation
likelihood, patch availability, and compensating controls across CISA advisories, 2010 to
2026.* IEEE Texas Power and Energy Conference (TPEC 2027), College Station, TX, Feb 7–9,
2027. IEEE Xplore. 6-page limit including figures, tables, references. Submission deadline:
not yet announced by the conference as of this build (confirmed via TPEC 2027 CFP listing,
2026-09-16) — will be tracked and flagged once published.

## The question

Of the CISA ICS advisories issued 2010–2026, which ones meaningfully affect pipeline-sector
operators specifically — based on (1) real-world exploitation likelihood, (2) patch
availability, and (3) compensating-control coverage — and how much does restricting the
lens to "pipeline-relevant" change the prioritization picture versus treating all ICS
advisories as equally relevant to a pipeline operator?

## Data sources

| Source | Role | Vintage | License |
|---|---|---|---|
| ICS Advisory Project (via `ong-ot-dataset-pipeline` v1.1, reused) | CISA ICS advisories, cleaned, 27,944 CVE–advisory rows, 2010–2026 | fetched 2026-09-12 | ODbL v1.0, attribution required |
| CISA KEV catalog | known_exploited flag | joined 2026-09-12; 360/27,944 matched (1.29%) | US gov, public domain |
| FIRST.org / empiricalsecurity.com EPSS | exploit-probability score + percentile | joined 2026-09-12; 99.43% match rate | public |
| CISA Vulnrichment (ADP/CNA enrichment) | remediation/workaround text for patch-availability inference | joined 2026-09-12; text present for 14.92% of rows | public |
| MITRE ATT&CK for ICS | named-actor/malware association | joined 2026-09-12; 100/27,944 matched (0.36%) — narrow by construction | public |
| TSA Pipeline-2021-02F crosswalk (`crosswalk-lookup` project, verified 2026-09-16) | compensating-control coverage across NIST 800-82 Rev.3, NIST 800-53 Rev.5, IEC 62443, CIS Controls v8, NIST CSF 2.0 | verified/signed-off | Code MIT; crosswalk CC BY 4.0 except IEC 62443 / CIS Controls v8 cells (own licenses) |
| CISA CPG 2.0 compensating controls (already joined into the v1.1 dataset) | secondary/generic compensating-control measure | 2 controls only, 16.81% of rows have ≥1 applicable control | — |
| PHMSA pipeline incident data (hazardous liquid accidents; gas distribution and gas transmission/gathering incidents, Jan 2010–present) | optional real-world context/motivation, not causal linkage to specific CVEs | downloaded, not yet processed | public (PHMSA) |

**Decision (confirmed with author, 2026-09-16): reuse the existing v1.1 draft as the
dataset of record for this paper rather than re-fetching.** The local device's shell bridge
that would be needed to re-fetch from cisa.gov / first.org / mitre.org is currently down
(a tracked Windows-update issue since 2026-09-08), so re-fetching is not possible from this
session regardless. The dataset is explicitly disclosed as a **draft** in every downstream
document — see Limitations.

## Unit of analysis

One row = one CVE × ICS advisory pairing (27,944 rows in the reused v1.1 dataset).

## Pipeline-sector scope (new classification layer built for this paper)

**Decision (confirmed with author): combine both signals.**

1. **Sector signal** — `Critical_Infrastructure_Sector` field, already present in the raw
   ICS Advisory Project data (semicolon-delimited, multi-valued). Matched case-insensitively
   for `Energy` OR `oil` OR `pipeline` substrings (catches the literal `"oil and gas"` /
   `"Oil and Gas"` tag present on 272 rows, plus the broader `Energy` tag on 9,424 rows). This
   is empirical: confirmed by direct inspection of the v1.1 CSV (2026-09-16), not assumed.
2. **Product-class signal** — an **expanded** vendor/product taxonomy
   (`config/product_class_taxonomy_pipeline.yaml`), built empirically from the vendor
   frequency table among Energy/oil-and-gas-tagged rows in the actual dataset (Siemens,
   Hitachi Energy, Schneider Electric, Advantech, Rockwell Automation, ABB, Moxa, GE, Emerson,
   Yokogawa, Honeywell, etc. — the existing 6-vendor taxonomy left most of these unclassified)
   plus known pipeline-specific SCADA/RTU/flow-computer product lines (Totalflow, ROC/FloBoss/
   ControlWave, SCADAPack, Experion PKS, OASyS) layered on top as a higher-confidence tier.

   `pipeline_relevant = sector_signal AND product_class_signal != "unmapped"`, reported
   alongside `energy_or_oilgas_tagged` (sector signal alone) and the full 27,944-row set, per
   the coverage-handling decision below.

## Compensating controls

**Decision (confirmed with author): use both, cross-referenced.** CPG 2.0 stays as the
generic, already-joined measure. A new mapping (`config/tsa_outcome_mapping.yaml`) assigns
each `ong_product_class` (plc / rtu / scada / ong_product_line) to the TSA Pipeline-2021-02
outcome group(s) whose controls are most directly applicable (e.g., PLC/RTU/SCADA → Network
Segmentation + Access Control baseline; `no_patch_available=True` rows additionally flagged
against the Patch Management outcome). This mapping is a **new judgment call**, flagged
`source_type = author-mapped` exactly like the existing crosswalk's own author-mapped cells,
and goes on the verification checklist for the author's sign-off — it is not sourced from a
ready-made CVE-to-TSA-outcome crosswalk (none exists).

## Coverage handling

**Decision (confirmed with author): full dataset as the headline analysis, with the
sector+product-mapped subset reported as a sensitivity/robustness check.** The v1.1 draft's
real limitations are disclosed prominently rather than hidden: 83.2% of all rows have no
mapped product class; patch-availability judgments rest on remediation text present for only
14.92% of rows (the rest are coded "no remediation text captured," not "confirmed patched").

## Measures

- **Exploitation likelihood**: `known_exploited` (KEV boolean) OR `epss ≥ threshold`. The
  threshold (0.10) is author-chosen, not FIRST.org-mandated — confirmed by the author
  2026-09-18; see `docs/VERIFY_CHECKLIST.md` and `config/tsa_outcome_mapping.yaml`.
- **Patch availability**: `no_patch_available` (existing boolean, text-match based) — reported
  with its basis breakdown (`no_patch_basis`) so "no text captured" is never conflated with
  "confirmed patched."
- **Compensating-control coverage**: `cpg2_combined_risk_reduction` (existing, CPG 2.0) and a
  new TSA-outcome coverage count/flag per row.
- **Composite prioritization score**: a transparent, documented function of the three measures
  above, computed only after the individual measures are built and QA'd — not before.

## Outputs

- `data/processed/pipeline_scored_v1.csv` — full 27,944-row table with new scope/score columns.
- `data/processed/qa_report_v1.txt` — row counts, match rates, sanity checks, named spot checks.
- `figures/` — built under the `dataviz` skill once the scoring step is QA'd.
- `docs/` — README, CODEBOOK, LIMITATIONS, VERIFY_CHECKLIST, PUBLISH_GUIDE, CITATION.cff.
- Manuscript: IEEE two-column conference paper, 6-page limit, built with the `docx` skill
  against an IEEE conference template.

## Verification points (author sign-off required before publish)

1. The expanded pipeline vendor/product taxonomy (`config/product_class_taxonomy_pipeline.yaml`).
2. The EPSS threshold used for "high exploitation likelihood."
3. The new product-class → TSA-outcome mapping (author-mapped, not from a ready crosswalk).
4. The composite prioritization-score formula and its weights.
5. A hand spot-check of a sample of top-prioritized advisories against the original CISA text.
6. Whether/how to incorporate PHMSA incident data (currently downloaded, not yet processed;
   default plan is context/motivation only, not causal linkage to specific CVEs — confirm or
   veto).

## License

Code: MIT. New derived data: CC BY 4.0, except columns inherited from the ICS Advisory
Project (ODbL v1.0, share-alike, attribution required) and any IEC 62443 / CIS Controls v8
cells reused from the Crosswalk Lookup project (their own licenses) — consistent with the
sibling projects.
