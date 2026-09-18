# Codebook — `data/processed/pipeline_prioritized_v1.csv`

13,939 rows after deduplication (see `docs/LIMITATIONS.md` item 1). One row = one
CVE × ICS-advisory pairing.

## Columns inherited unchanged from the reused ong-ot-dataset v1.1

| Column | Type | Definition |
|---|---|---|
| `icsad_ID` | int | Internal ICS Advisory Project record ID. |
| `Original_Release_Date`, `Last_Updated` | date | Advisory publication/update dates. |
| `Year` | int | Advisory year, 2010–2026. |
| `ICS-CERT_Number` | string | CISA advisory number (e.g. `ICSA-24-165-04`). |
| `ICS-CERT_Advisory_Title` | string | Advisory title. |
| `Vendor`, `Product`, `Products_Affected` | string | As published by CISA. |
| `cve_id` | string | CVE identifier; blank for 29 rows (advisories issued without an assigned CVE). |
| `Cumulative_CVSS`, `CVSS_Severity`, `CWE_Number` | mixed | As published; may mix CVSS 2.0/3.x/4.0 across the 2010–2026 range (see LIMITATIONS item 6). |
| `Critical_Infrastructure_Sector` | string | Semicolon-delimited, multi-valued (e.g. `"Chemical; Energy; oil and gas"`). |
| `Product_Distribution`, `Company_Headquarters`, `License` | string | As published. |
| `known_exploited` | bool | CISA KEV catalog membership, joined on `cve_id`. |
| `epss`, `percentile` | float [0,1] | FIRST.org EPSS exploit-probability score and percentile. |
| `vulnrichment_*` | mixed | CISA Vulnrichment (ADP/CNA) enrichment fields. |
| `ong_product_class`, `ong_product_weight` | string/float | The upstream dataset's original 6-vendor product taxonomy (kept for comparison; NOT the taxonomy this paper's analysis uses). |
| `no_patch_available`, `no_patch_basis` | bool/string | Text-match-based patch-availability flag and its basis (see LIMITATIONS item 4). |
| `cpg2_applicable_controls`, `cpg2_combined_risk_reduction` | string/float | CISA CPG 2.0 compensating-control mapping (generic, 2 controls total). |
| `attack_ics_matched_entity`, `attack_ics_entity_type`, `attack_ics_technique_ids`, `attack_ics_matched_token` | string | MITRE ATT&CK-for-ICS named-actor/malware association (narrow; see LIMITATIONS item 5). |

## Columns new to this paper

| Column | Type | Definition |
|---|---|---|
| `pipeline_sector_signal` | bool | `Critical_Infrastructure_Sector` contains "Energy", "oil", or "pipeline" (case-insensitive). |
| `pipeline_tier` | string | `tier1_pipeline_core` (named pipeline SCADA/flow-computer product line), `tier2_ot_general_energy` (vendor-level OT match, not pipeline-exclusive), `excluded` (vendor makes non-OT-relevant equipment), or `unmapped`. See `config/product_class_taxonomy_pipeline.yaml`. |
| `pipeline_tier_weight` | float | 0.9 / 0.5 / 0.0 per tier. |
| `pipeline_relevant` | bool | `pipeline_sector_signal AND pipeline_tier in {tier1, tier2}`. This is the paper's scope filter. |
| `tsa_outcome_coverage_fraction` | float | 4/6 for every `pipeline_relevant` row (the four baseline TSA outcomes — Network Segmentation, Access Control, Patch Management, Governance & Risk Management), 0 otherwise. Deliberately constant per row; see `docs/LIMITATIONS.md` item 3 for why. |
| `tsa_baseline_outcomes` | string | Comma-separated list of the baseline outcome IDs (same 4 for every relevant row). |
| `tsa_response_flags` | string | TSA-3 (Continuous Monitoring) if `known_exploited` or `epss >= 0.10`; TSA-6 (Assessment & Incident Response) if `known_exploited`. Informational only — not part of the priority-score calculation. |
| `exploitation_score` | float [0,1] | 1.0 if `known_exploited`, else `epss` (0 if EPSS missing). |
| `raw_urgency` | float [0,1] | `exploitation_score` + 0.2 if `no_patch_available`, capped at 1.0. |
| `overall_control_reduction` | float [0,1] | `1 - (1 - cpg2_combined_risk_reduction) * (1 - tsa_outcome_coverage_fraction)` — CPG 2.0 and TSA-outcome coverage stacked multiplicatively. |
| `priority_score` | float [0,1] | `raw_urgency * (1 - overall_control_reduction)`. Higher = more urgent for a pipeline operator's attention. |

## Config files (this paper's new judgment calls, confirmed by author 2026-09-18)

- `config/product_class_taxonomy_pipeline.yaml` — the tier1/tier2/excluded vendor and product-line lists.
- `config/tsa_outcome_mapping.yaml` — the baseline/conditional TSA outcome assignment and the EPSS high-threshold (0.10).
