# Limitations

Numbered, specific, written before the manuscript draft — read this before treating
any number in this project as a finished, defensible metric.

1. **The reused upstream dataset contained undocumented duplicate rows; this
   build deduplicates them, but the fix has not been pushed upstream.** The
   `ong-ot-dataset-pipeline` v1.1 draft's own manifest claims "one row = one
   CVE-advisory pair" and reports 27,944 rows. Direct inspection (2026-09-16)
   found this false: the ICS Advisory Project source ships both a cumulative
   "Master" CSV and per-year snapshot CSVs that re-list the same advisory
   records, and the upstream pipeline concatenated all of them without
   deduplication. 14,005 of 27,944 rows (50.12%) were exact re-exports —
   identical in every column except which source file they came from. This
   paper's own pipeline (`src/01_dedup_source.py`) removes them, leaving
   13,939 genuinely unique rows, which is the basis for every number in this
   project. **This has not been fixed in the upstream `ong-ot-dataset-pipeline`
   / ONG-OT Vulnerability Explorer projects themselves** — their own published
   row counts and percentages remain on the pre-dedup, ~2x-inflated basis
   until that is done separately.

2. **This project did not build the underlying vulnerability data.** All KEV/
   EPSS/Vulnrichment/ATT&CK-ICS joining happens in the reused upstream
   `ong-ot-dataset-pipeline` v1.1 draft (built 2026-09-12). Any error in that
   join is inherited here unchanged (beyond the dedup fix above). The upstream
   pipeline's own QA report is preserved at `data/raw/upstream_qa_report.txt`.

3. **The pipeline-relevance taxonomy is a new judgment call, not a
   ready-made standard.** `pipeline_relevant` combines a sector-tag signal
   (empirically confirmed: `Critical_Infrastructure_Sector` carries a literal
   `"oil and gas"` value on some rows) with an expanded vendor/product
   taxonomy built for this paper. Of the pipeline-relevant subset, 98.88% is
   classified only at `tier2_ot_general_energy` — a vendor-level match
   (Siemens, GE, Rockwell Automation, Emerson, ABB, etc.) that is plausible
   but not confirmed pipeline-specific; only 1.12% (`tier1_pipeline_core`) is a
   named pipeline SCADA/flow-computer product line (Experion PKS, Totalflow,
   ROC/FloBoss, etc.). An earlier draft of this taxonomy classified whole
   vendors as "pipeline_core," which incorrectly caught a Siemens *Spectrum
   Power 7* row — an electric-grid SCADA product, not pipeline — before being
   corrected. **The tier2 vendor list is the single largest open judgment call
   in this paper and needs the author's own direct review before submission**
   (this paper is sole-authored as of 2026-09-18; an earlier draft had
   flagged this as a co-author review item — see `AUTHORS.json`).

4. **Patch-availability determination is text-matching, not verification.**
   `no_patch_available` scans CISA Vulnrichment CNA remediation text for
   phrases like "end-of-life" or "will not fix." The large majority of rows
   have no remediation text captured at all (coded `no_patch_basis =
   no_remediation_text_captured`), which is treated as `no_patch_available =
   False` — i.e., **absence of evidence is coded the same as "patch exists,"
   which is weaker than it looks.** Only 1 of 3,734 pipeline-relevant rows is
   flagged `no_patch_available = True` on this basis; this should be read as
   "text-matching found almost no explicit no-patch language," not "patches
   exist for virtually all pipeline-relevant advisories." Concretely: this
   count is a **lower bound on the true number of no-patch cases, not an
   estimate of it** — the true count can only be equal to or higher than 1,
   never lower, since the method can miss real no-patch cases but cannot
   manufacture false ones.

5. **The TSA-outcome mapping is a new, author-mapped judgment call with a
   specific, disclosed limitation: it is deliberately held constant across
   rows.** No ready-made crosswalk exists from an individual CVE/advisory to a
   TSA Pipeline-2021-02 outcome group. This paper's mapping assigns four
   baseline outcomes (Network Segmentation, Access Control, Patch Management,
   Governance & Risk Management) to every `pipeline_relevant` row uniformly,
   and reports Continuous Monitoring / Incident Response applicability as a
   separate informational flag rather than folding it into the risk-reduction
   term. An earlier version of this scoring counted those two conditional
   outcomes as "coverage" that reduced the priority score — which produced a
   direct contradiction (the most urgent, actively-exploited rows scored as
   fully mitigated, simply because their own urgency triggered more outcome
   matches) and was corrected before this version. The current, corrected
   design still rests on a real assumption: that "a compensating-control
   mapping exists for this outcome" is a reasonable proxy for "this control is
   actually implemented at a given pipeline operator," which is not verified
   and cannot be, from advisory data alone. **Reviewers should expect this
   mapping to be explicitly flagged, in the manuscript itself and not only
   here, as unvalidated and non-operator-specific**: it states what a TSA
   outcome group could plausibly address for a given product class, not
   what any particular pipeline operator has actually deployed, tested, or
   confirmed effective. Treat every `overall_control_reduction` value in
   this paper as a structural, not empirical, coverage estimate.

6. **ATT&CK-for-ICS technique matches are narrow by construction** (0.36% of
   rows) — see upstream limitations; unchanged by this paper's additions.

7. **`Cumulative_CVSS` may mix CVSS versions** (2.0/3.x/4.0) across the
   2010–2026 range; the source does not record which version applies per row.

8. **EPSS and KEV reflect a single point in time** (2026-09-12, upstream
   access date, itself reused without refresh — see decision log). Both
   change daily/regularly; treat any number here as dated to that build, not
   real-time. This paper's decision (confirmed with the author, 2026-09-16)
   was to reuse this draft rather than re-fetch, because the local device's
   shell bridge needed to re-fetch from cisa.gov/first.org/mitre.org was down
   (a tracked Windows-update issue since 2026-09-08) at build time.

9. **The composite `priority_score` is a transparent, documented heuristic,
   not a validated risk model.** It has not been benchmarked against any
   ground-truth outcome (e.g., actual pipeline incidents). PHMSA pipeline
   incident data (hazardous liquid, gas distribution, gas transmission/
   gathering, 2010–present) was downloaded during this build's research phase
   but has NOT been joined to this analysis — PHMSA incidents are
   overwhelmingly physical/mechanical (corrosion, equipment failure), not
   cyber-attributed, so a direct causal linkage to specific CVEs would not be
   defensible. If used at all, it belongs only as separately-presented
   context/motivation, never merged into `priority_score`. **Confirmed by
   author, 2026-09-18: PHMSA data stays context/motivation only and is not
   merged into the quantitative analysis.**

10. **Data licensing.** Rows inherited from the ICS Advisory Project remain
    ODbL v1.0 (share-alike, attribution required). The TSA-crosswalk-derived
    columns inherit that project's licensing (CC BY 4.0, except IEC 62443 /
    CIS Controls v8 cells, which are not reused verbatim here — only outcome
    IDs are referenced). New columns in this project (pipeline tier, TSA
    outcome mapping, priority score) are original to this paper: code MIT,
    derived data CC BY 4.0.

11. **This is a research paper draft, not a compliance or endorsement
    artifact.** Nothing here is TSA, CISA, NIST, or vendor-endorsed guidance,
    and it does not substitute for an operator's own compliance review.

12. **`known_exploited` is joined from CISA's separate KEV catalog, not
    parsed from the advisory's own text, and the two can disagree.** Spot
    checking the top-10 prioritized rows against their CISA advisory pages
    (2026-09-18) found advisories whose own boilerplate reads "No known
    public exploitation... has been reported to CISA at this time" (e.g.
    ICSA-24-165-04, covering CVE-2023-44487 / HTTP-2 Rapid Reset) while this
    paper correctly flags that CVE `known_exploited=True`, because it is
    separately listed in CISA's KEV catalog (added October 2023) — a fact
    the underlying advisory page may not reflect if it predates or wasn't
    updated after the KEV listing. This is not a data error; it is a known
    property of combining two CISA sources that update independently, and
    is worth a sentence in the manuscript so a reviewer checking an advisory
    page directly doesn't read it as a contradiction.
