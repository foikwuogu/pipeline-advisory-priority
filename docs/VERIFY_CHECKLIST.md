# Verification checklist

Nothing in this project is published, submitted, or presented as finished
until every item below is checked by the author in their own hand. This is
not a formality — the artifact carries the author's name into a permanent
IEEE Xplore record. (This paper is sole-authored as of 2026-09-18; items
below that once named specific co-authors have been updated accordingly.)

## Mechanical checks (run before the human checks)

- [x] `python3 src/01_dedup_source.py && python3 src/02_classify_pipeline_scope.py && python3 src/03_score_prioritization.py` reproduces `data/processed/stats.json` exactly. **Verified 2026-09-18** — reran all three scripts, byte-for-byte diff against the prior `stats.json` was empty.
- [x] No `DRAFT`, `[VERIFY]`, or placeholder-bracket text remains anywhere in `manuscript/` or `docs/` (see `scripts/publish_gate.py`). **Verified 2026-09-18** — rescanned after sign-off; the manuscript's DRAFT stamp and every remaining `[VERIFY]` marker in `docs/BUILD_SPEC.md`, `docs/CODEBOOK.md`, and `docs/LIMITATIONS.md` were resolved to reflect the author's confirmed decisions. The only remaining string match is the literal filename `TPEC2027_manuscript_DRAFT.docx`, which is not placeholder content.

## Independently checked, 2026-09-18 (factual, not a judgment call)

- [x] **Top-10 prioritized advisories, existence and vendor/product match.**
  All 5 unique `ICS-CERT_Number`s behind the top-10 rows resolve to real,
  matching CISA advisory pages: ICSA-24-165-04 (Siemens ST7 ScadaConnect),
  ICSA-25-203-04 (Schneider Electric EcoStruxure Power Operation, Update A),
  ICSA-17-208-04 and ICSA-18-184-01 (Rockwell Automation Allen-Bradley
  Stratix/ArmorStratix/5950), ICSA-26-218-01 (ABB Ability Zenon — confirmed
  by search result title match; CISA's page itself returned a 403 to direct
  fetch, so its CVE list wasn't independently re-checked). Where advisory
  text was readable, CVE IDs matched too (e.g. CVE-2023-44487 and
  CVE-2023-5217 both appear on their respective advisory pages). **This
  covers existence/vendor/product/CVE-membership — it does not replace your
  own read of each advisory's substance**, which the checklist item below
  still asks for.
- [x] **EPSS 0.10 threshold, checked against FIRST.org's own guidance.**
  FIRST.org does not prescribe a fixed numeric cutoff; it recommends a
  percentile-based approach tailored to an organization's own vulnerability
  distribution, and notes historically that a CVSS-Critical-equivalent
  effort level lines up with roughly the 90th percentile (~0.04), a lower
  bar than this paper's 0.10. This doesn't make 0.10 wrong, but it means the
  manuscript should describe 0.10 as an author-chosen operating point, not
  cite it as a FIRST.org-endorsed cutoff — the checklist item below still
  needs your own sign-off on the choice itself.
- [x] **`known_exploited` vs. advisory text nuance found during the spot
  check** — logged as `docs/LIMITATIONS.md` item 12. Some advisories'
  boilerplate ("no known public exploitation... reported to CISA") predates
  or wasn't updated after the CVE's later KEV listing; the dataset's
  `known_exploited` flag is correctly sourced from the separate KEV catalog,
  not this boilerplate, but it's worth a sentence in the manuscript so a
  reviewer checking an advisory page directly doesn't read it as a
  contradiction.

## Judgment calls requiring the author's own sign-off

- [x] **Pipeline vendor/product taxonomy** (`config/product_class_taxonomy_pipeline.yaml`).
  **Confirmed by author, 2026-09-18**: reviewed both tiers as described in
  `docs/LIMITATIONS.md` item 3 — the sector-tag signal, the tier2
  vendor-level match (plausible, not pipeline-specific), and tier1 as the
  only defensible named-product-line list — and confirmed the write-up is
  accurate as-is. The author did not request any vendor/product additions
  or removals; this closes the taxonomy's *documentation* as accurate. It
  does not itself constitute a fresh line-by-line audit of every vendor
  entry — flag here if that separate audit is still wanted before
  submission.
- [x] **EPSS high-exploitation threshold** (`config/tsa_outcome_mapping.yaml`,
  `epss_high_threshold: 0.10`). **Confirmed by author, 2026-09-18**: keep
  0.10, framed explicitly as author-chosen, not FIRST.org-endorsed. The
  manuscript's Methods (Section II.C) now states this explicitly, cites
  FIRST.org's own no-universal-cutoff guidance [3] and NIST CSWP 41's
  precedent for 0.1 as a practical screening cutoff [11], and clarifies the
  threshold affects only the TSA-3/TSA-6 informational flags, not
  `priority_score` itself. `config/tsa_outcome_mapping.yaml`'s comment
  updated to match.
- [x] **Product-class → TSA-outcome mapping** (baseline outcomes TSA-1/2/4/5
  applied uniformly; TSA-3/6 as response flags). **Confirmed by author,
  2026-09-18**: reviewed `docs/LIMITATIONS.md` item 5 and confirmed the
  reasoning (author-defined, held constant, the earlier circularity bug
  real) reflects their own judgment — and asked that the manuscript and
  this file both state more explicitly that the mapping is unvalidated and
  non-operator-specific. Both documents updated accordingly.
- [x] **Composite prioritization-score formula** (`raw_urgency * (1 -
  overall_control_reduction)`, in `src/03_score_prioritization.py`).
  **Signed off by author, 2026-09-18** as part of the general "verified and
  sign off" attestation below — this specific item was not discussed
  line-by-line with the weighting broken out (KEV=1.0, EPSS continuous,
  +0.2 no-patch bonus, multiplicative stacking). Flag this item specifically
  if you want to revisit the weighting before submission.
- [x] **Top-10 prioritized advisories, substantive read.**
  **Signed off by author, 2026-09-18** as part of the general attestation
  below. The existence/vendor/product/CVE-membership check was independently
  done earlier; the substantive read of each advisory's full text against
  how it's characterized in the manuscript was not walked through item by
  item here — flag this specifically if you want to revisit it.
- [x] **PHMSA incident data decision.** **Confirmed by author, 2026-09-18**:
  PHMSA data stays context/motivation only, never merged into
  `priority_score` — matches the default assumption already coded here.
- [x] **Duplicate-row fix.** **Signed off by author, 2026-09-18** as part of
  the general attestation below. Whether/when to push the same fix into the
  upstream `ong-ot-dataset-pipeline` project remains a separate, undecided
  follow-up (see `docs/NEXT_STEPS.md` item 2) — that's a decision about a
  different project, not a blocker on this one.
- [ ] **TPEC 2027 submission deadline.** Deliberately left unchecked — this
  is not something the author can sign off on, since it is an external fact
  that hasn't happened yet, not a judgment call. Rechecked 2026-09-18: still
  not on the official conference site (`tpec.engr.tamu.edu` only covers
  TPEC 2026); a third-party CFP aggregator lists Feb 7–9, 2027 but is
  unconfirmed. This box gets checked only when TPEC 2027's real CFP is
  published and its requirements are read against this package.

## Sign-off

**Signed: Friday Ogochukwu Ikwuogu — Date: 2026-09-18**

The author confirmed "verified and sign off" on 2026-09-18, covering every
item above except the TPEC 2027 submission deadline (not sign-off-able —
see that item's note). This closes the verification gate for this package's
current content. It does not freeze the paper: if TPEC 2027's eventual peer
review, or the author's own further reading, surfaces something that needs
to change, that's a normal revision, not a failure of this process — the
gate exists so nothing ships *unreviewed*, not so nothing is ever revised.
