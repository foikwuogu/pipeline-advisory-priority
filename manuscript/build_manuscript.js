const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, ImageRun,
  BorderStyle, PageOrientation, convertInchesToTwip
} = require("docx");

// ---------- US Letter, IEEE-ish two-column body ----------
const PAGE_W = 12240, PAGE_H = 15840; // DXA, US Letter
const MARGIN = 1080; // 0.75in

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: opts.after ?? 120, line: 260 },
    children: [new TextRun({ text, size: 18, font: "Times New Roman", bold: !!opts.bold, italics: !!opts.italics })],
  });
}

function heading(text, num) {
  return new Paragraph({
    spacing: { before: 200, after: 100 },
    alignment: AlignmentType.LEFT,
    children: [new TextRun({ text: `${num}. ${text}`.toUpperCase(), bold: true, size: 18, font: "Times New Roman" })],
  });
}

function subheading(text) {
  return new Paragraph({
    spacing: { before: 140, after: 80 },
    children: [new TextRun({ text, bold: true, italics: true, size: 18, font: "Times New Roman" })],
  });
}

function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 160 },
    children: [new TextRun({ text, size: 16, font: "Times New Roman" })],
  });
}

function refItem(num, text) {
  return new Paragraph({
    spacing: { after: 80, line: 240 },
    indent: { left: 260, hanging: 260 },
    children: [new TextRun({ text: `[${num}] ${text}`, size: 16, font: "Times New Roman" })],
  });
}

const titlePara = new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 160 },
  children: [new TextRun({
    text: "Which ICS Advisories Matter to a Pipeline Operator? Exploitation Likelihood, Patch Availability, and Compensating Controls Across CISA Advisories, 2010–2026",
    bold: true, size: 28, font: "Times New Roman",
  })],
});

const authorsPara = new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 40 },
  children: [new TextRun({
    text: "Ogochukwu Friday Ikwuogu",
    size: 20, font: "Times New Roman",
  })],
});
const authorsPara2 = new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: "Independent Researcher, Odessa, Texas, USA — Friday.ikwuogu@gmail.com — ORCID 0009-0009-2222-1318", size: 16, font: "Times New Roman", italics: true })],
});

const abstractHeading = new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({ text: "Abstract—", bold: true, italics: true, size: 18, font: "Times New Roman" })],
});

const abstractText = "CISA has published ICS security advisories at an accelerating rate: this study finds 13,939 unique CVE–advisory pairs between 2010 and 2026 after removing an undocumented duplication in a reused upstream dataset (which had reported 27,944 rows, roughly double the true count). Pipeline operators cannot treat all of these as equally relevant. We define a pipeline-sector relevance filter combining a Critical-Infrastructure-Sector tag already present in the source data with an expanded, empirically-derived vendor and product-line taxonomy, and identify 3,734 pipeline-relevant rows (26.8% of the deduplicated set). We compute a transparent composite prioritization score from CISA Known Exploited Vulnerabilities (KEV) status, FIRST.org Exploit Prediction Scoring System (EPSS) values, patch-availability signals, and compensating-control coverage under both the CISA Cross-Sector Cybersecurity Performance Goals (CPG) 2.0 and the TSA Pipeline-2021-02 Security Directive's six outcome groups. Restricting the lens to pipeline-relevant equipment shifts the risk picture measurably: the pipeline-relevant subset skews toward lower priority scores than the full advisory population (74.5% low-tier vs. 60.9%), while still surfacing a specific, actionable set of actively-exploited advisories concentrated in a small number of vendors. We report this result together with the specific taxonomy, mapping, and data-quality decisions behind it, so a pipeline operator or auditor can audit — and challenge — every judgment call.";

const indexTerms = new Paragraph({
  spacing: { after: 200 },
  children: [
    new TextRun({ text: "Index Terms—", bold: true, italics: true, size: 18, font: "Times New Roman" }),
    new TextRun({ text: "ICS advisories, pipeline cybersecurity, vulnerability prioritization, EPSS, KEV, TSA Security Directive, compensating controls, operational technology.", size: 18, font: "Times New Roman" }),
  ],
});

function img(path, widthPx, heightPx) {
  return new ImageRun({ type: "png", data: fs.readFileSync(path), transformation: { width: widthPx, height: heightPx } });
}

function statsTableRow(cells, opts = {}) {
  return new TableRow({
    children: cells.map((c, i) => new TableCell({
      width: { size: opts.widths ? opts.widths[i] : 1600, type: WidthType.DXA },
      shading: opts.header ? { type: ShadingType.CLEAR, fill: "D9E6F5" } : undefined,
      children: [new Paragraph({
        children: [new TextRun({ text: String(c), size: 13, font: "Times New Roman", bold: !!opts.header })],
      })],
    })),
  });
}

// Column width in a 2-column US-Letter section with 0.75in margins and
// 360-DXA gutter is 4860 DXA (~3.375in) — tables/images MUST fit inside
// that, not the full page width, or they overflow into the other column.
const COL_WIDTH = 4680;

const topAdvisories = [
  ["ICSA-24-165-04", "Siemens", "ST7 ScadaConnect", "Y", "1.00", "0.333"],
  ["ICSA-25-203-04", "Schneider Elec.", "EcoStruxure PO", "Y", "1.00", "0.333"],
  ["ICSA-15-344-01B", "Advantech", "EKI", "Y", "1.00", "0.333"],
  ["ICSA-14-105-03B", "Siemens", "Ind. Products OpenSSL", "Y", "1.00", "0.333"],
  ["ICSA-14-135-02", "Schneider Elec.", "Wonderware OpenSSL", "Y", "1.00", "0.333"],
  ["ICSA-22-256-01", "Hitachi Energy", "TXpert Hub CoreTec 4", "Y", "1.00", "0.333"],
  ["ICSA-18-184-01", "Rockwell Auto.", "Stratix 5950", "Y", "1.00", "0.333"],
  ["ICSA-21-077-03", "Hitachi/ABB", "eSOMS Telerik", "Y", "1.00", "0.333"],
];

const table1Widths = [980, 900, 1300, 300, 550, 650];
const table1 = new Table({
  width: { size: COL_WIDTH, type: WidthType.DXA },
  columnWidths: table1Widths,
  rows: [
    statsTableRow(["ICS-CERT #", "Vendor", "Product", "KEV", "EPSS", "Score"], { header: true, widths: table1Widths }),
    ...topAdvisories.map(r => statsTableRow(r, { widths: table1Widths })),
  ],
});

const table2Widths = [2400, 1140, 1140];
const table2 = new Table({
  width: { size: COL_WIDTH, type: WidthType.DXA },
  columnWidths: table2Widths,
  rows: [
    statsTableRow(["Metric", "Full", "Pipeline"], { header: true, widths: table2Widths }),
    statsTableRow(["Known-exploited (KEV)", "1.29%", "1.69%"], { widths: table2Widths }),
    statsTableRow(["No-patch-available flag", "0.97%", "0.03%"], { widths: table2Widths }),
    statsTableRow(["EPSS score present", "99.43%", "99.44%"], { widths: table2Widths }),
    statsTableRow(["≥ 1 CPG 2.0 control", "16.81%", "16.81%†"], { widths: table2Widths }),
    statsTableRow(["Mean priority score", "0.044", "0.022"], { widths: table2Widths }),
    statsTableRow(["Median priority score", "0.006", "0.004"], { widths: table2Widths }),
  ],
});

const body2Col = [
  heading("Introduction", "I"),
  p("The Cybersecurity and Infrastructure Security Agency (CISA) has published thousands of Industrial Control Systems (ICS) advisories since 2010, and the annual rate has grown sharply in recent years. A pipeline operator monitoring this feed faces a volume problem before a technical one: most advisories describe equipment the operator does not run, in sectors the operator is not part of, with exploitation and patch status that are rarely spelled out plainly. This paper asks a narrow, practical question — of the CISA ICS advisories issued 2010–2026, which ones meaningfully affect a pipeline-sector operator specifically, and how does restricting the lens to pipeline-relevant equipment change the prioritization picture?"),
  p("Our contribution is threefold. First, we identify and correct a data-quality defect in a reused, previously-published advisory dataset: an undocumented duplication that inflated its reported row count by roughly a factor of two. Second, we build and disclose a pipeline-sector relevance taxonomy on top of the corrected data, combining a Critical-Infrastructure-Sector tag already present in the source with an expanded vendor/product-line classification, and we show why a naïve vendor-level taxonomy over-claims precision. Third, we compute a transparent, fully-documented composite prioritization score from exploitation likelihood, patch availability, and compensating-control coverage under two independent control frameworks — CISA's CPG 2.0 and the TSA Pipeline-2021-02 Security Directive — and show that pipeline-relevant equipment does not simply inherit the risk profile of the broader ICS advisory population."),

  heading("Data and Methods", "II"),
  subheading("A. Reused dataset and a duplication defect"),
  p("We reuse an existing pipeline (the ong-ot-dataset-pipeline project, v1.1, built 2026-09-12) that joins CISA ICS advisories from the ICS Advisory Project [1] with the CISA Known Exploited Vulnerabilities (KEV) catalog [2], FIRST.org's Exploit Prediction Scoring System (EPSS) [3], CISA Vulnrichment CNA/ADP enrichment [4], and MITRE ATT&CK for ICS [5], on cve_id. Its own manifest reports 27,944 rows on the premise that one row equals one CVE–advisory pair. Direct inspection contradicts this: the ICS Advisory Project source ships both a cumulative export and a series of per-year snapshot exports that re-list the same records, and the upstream join concatenated all of them without deduplication. We find 14,005 of 27,944 rows (50.1%) are exact re-exports, identical in every field except which source file they came from. We deduplicate on all fields except that source-file identifier, leaving 13,939 unique CVE–advisory pairs, and every number in this paper is computed on that corrected basis."),

  subheading("B. Pipeline-sector relevance"),
  p("We define pipeline_relevant as the conjunction of two independent signals. The sector signal is a case-insensitive match for “Energy”, “oil”, or “pipeline” against the Critical_Infrastructure_Sector field, which we found to carry a literal “oil and gas” tag on a subset of rows, in addition to the broader “Energy” tag. The product-class signal is a new taxonomy with two confidence tiers: tier1 (pipeline_core) matches only named pipeline SCADA/RTU/flow-computer product lines (e.g., Totalflow, ROC/FloBoss, SCADAPack, Experion PKS); tier2 (ot_general_energy) matches at the vendor level (e.g., Siemens, Emerson, ABB, Rockwell Automation) and is disclosed as plausible but not pipeline-exclusive. An earlier version of this taxonomy classified vendors at tier1, which incorrectly captured a Siemens electric-grid SCADA product as “pipeline core”; we corrected this before reporting results, and it is documented as a caught error rather than removed silently. Of the 3,734 pipeline-relevant rows, 98.9% rest on the tier2 vendor-level signal, which we flag as the largest open judgment call in this study."),

  subheading("C. Compensating controls and prioritization score"),
  p("Each pipeline-relevant row is checked against two independent compensating-control frameworks: the dataset's existing CISA CPG 2.0 mapping (generic, product-class based), and a new mapping we build to the TSA Pipeline-2021-02 Security Directive's six outcome groups — Network Segmentation, Access Control, Continuous Monitoring, Patch Management, Governance & Risk Management, and Assessment & Incident Response — via a companion crosswalk project that maps those outcomes to NIST SP 800-82, NIST SP 800-53, IEC 62443, CIS Controls v8, and NIST CSF 2.0 [6]–[10]. Four outcomes (Network Segmentation, Access Control, Patch Management, Governance & Risk Management) are treated as a constant baseline for every pipeline-relevant row; Continuous Monitoring and Incident Response are reported separately as response-posture flags rather than folded into the control-coverage term. We made this choice after an earlier design counted all six outcomes as risk-reducing coverage, which produced a self-defeating result: the most urgent, actively-exploited advisories scored as fully mitigated, simply because their own urgency triggered more outcome matches. Removing that circularity is, to our knowledge, an underappreciated pitfall for any TSA/NIST-outcome-based scoring scheme and is worth flagging for other researchers building similar models."),
  p("The Continuous Monitoring flag (TSA-3) triggers when known_exploited is true or EPSS ≥ 0.10; the Incident Response flag (TSA-6) triggers when known_exploited is true. This 0.10 EPSS cutoff is an author-chosen operating point, not a value FIRST.org endorses: FIRST.org's own guidance recommends tuning a threshold to an organization's own vulnerability distribution rather than adopting a universal cutoff, and its cited historical reference point for a CVSS-Critical-equivalent effort level (≈10th percentile from the top, ≈0.04) is lower than the value used here [3]. We retain 0.10 because it falls within the range treated as a practical screening cutoff in published exploitation-likelihood guidance [11], and, critically, because this threshold affects only the two informational response-posture flags above — it has no effect on priority_score, which consumes EPSS as a continuous value rather than a thresholded one."),
  p("The final score is priority = raw_urgency × (1 − overall_control_reduction), where raw_urgency is 1.0 for KEV-listed vulnerabilities (else the EPSS score, plus a 0.2 bonus when no patch is available, capped at 1.0), and overall_control_reduction stacks CPG 2.0 and TSA-outcome coverage multiplicatively, consistent with the stacking convention already used for CPG 2.0 in the reused dataset."),

  heading("Results", "III"),
  p("Fig. 1 shows the year-over-year count of ICS advisories, full population versus the pipeline-relevant subset, on the corrected (deduplicated) basis. Both series grow over the period, with the pipeline-relevant subset tracking a roughly proportional but consistently smaller share — it does not disproportionately grow or shrink relative to the whole."),
  new Paragraph({ children: [img("../figures/fig1_advisories_by_year.png", 300, 229)], alignment: AlignmentType.CENTER, spacing: { before: 120 } }),
  caption("Fig. 1. CISA ICS advisories by year, 2010–2026, deduplicated."),
  p("Table I lists the eight distinct pipeline-relevant advisories tied at the highest observed priority score (0.333), all KEV-listed with EPSS at or near 1.0, concentrated in six vendors. Table II summarizes headline coverage statistics for the full deduplicated set (n=13,939) versus the pipeline-relevant subset (n=3,734)."),
  caption("TABLE I. Highest-Priority Pipeline-Relevant Advisories"),
  table1,
  new Paragraph({ text: "", spacing: { after: 160 } }),
  caption("TABLE II. Coverage Summary, Full (n=13,939) vs. Pipeline-Relevant (n=3,734)"),
  table2,
  p("† CPG 2.0 coverage is unchanged by the pipeline filter because it is computed on the same product-class column for both subsets; see Section IV.", { after: 160 }),
  p("Fig. 2 bins every row's priority score into four tiers. The pipeline-relevant subset is more concentrated in the lowest tier than the full population (74.5% vs. 60.9%) and correspondingly lighter in the moderate and critical tiers."),
  new Paragraph({ children: [img("../figures/fig2_priority_tiers.png", 300, 229)], alignment: AlignmentType.CENTER, spacing: { before: 120 } }),
  caption("Fig. 2. Prioritization-score tier distribution, full vs. pipeline-relevant."),

  heading("Discussion and Limitations", "IV"),
  p("The headline finding — that pipeline-relevant equipment skews toward lower priority scores than the broader ICS advisory population — is counter-intuitive if one expects sector-specific filtering to concentrate risk. We think this reflects two things rather than an absence of real risk: (1) the tier2 vendor-level signal that carries 98.9% of the pipeline-relevant subset is a broad industrial-automation match, diluted by advisories for those same vendors' non-pipeline product lines, which this taxonomy cannot yet separate out; and (2) EPSS and KEV coverage for narrowly pipeline-specific product lines (tier1, 0.5% of the full dataset) is itself thin. Both point toward the same next step: a higher-precision taxonomy, ideally validated against a real pipeline operator's asset inventory rather than vendor name alone."),
  p("This study inherits every limitation of its reused upstream data — patch-availability inference is text-matching against remediation fields present for only 14.9% of rows, and ATT&CK-for-ICS technique matches cover 0.36% of rows — in addition to the new judgment calls disclosed in Section II: the tier2 vendor list, the EPSS high-exploitation threshold (0.10), and the product-class-to-TSA-outcome assignment. Two of these deserve explicit emphasis rather than a passing mention. First, because absence of remediation text defaults to “patch available,” the reported no-patch count is a lower bound on the true number of no-patch cases, not an estimate of it. Second, the TSA-outcome coverage term is a structural, not empirical, proxy: it states what an outcome group could plausibly address for a product class, not what any specific pipeline operator has implemented, tested, or confirmed effective, and it is not validated against operator-reported control data. None of these are hidden; all are flagged in the project's verification checklist for the authors' own sign-off before submission, and none should be read as settled by this draft alone."),

  heading("Conclusion and Future Work", "V"),
  p("Restricting a CISA ICS advisory feed to pipeline-relevant equipment is possible using signals already present in public advisory data, but it requires disclosing exactly how “relevant” is defined — a vendor-level match is not the same claim as a confirmed pipeline product line, and conflating the two overstates precision. Once defined transparently, the resulting subset tells a genuinely different, and in this case less alarming, story than the undifferentiated advisory feed, while still surfacing a small, concentrated, and actionable set of actively-exploited advisories. Future work should validate the taxonomy against a real operator asset inventory, benchmark the composite score against reported incident data rather than advisory metadata alone, and re-run this analysis once the upstream duplication defect identified here is corrected at the source."),

  heading("Acknowledgment", "Acknowledgment".length ? "" : ""),
];

// fix heading for Acknowledgment (no numbering)
body2Col[body2Col.length - 1] = new Paragraph({
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text: "ACKNOWLEDGMENT", bold: true, size: 18, font: "Times New Roman" })],
});
body2Col.push(p("The authors thank the ICS Advisory Project, CISA, FIRST.org, MITRE, and TSA for maintaining the open data and public directive text this analysis builds on."));

body2Col.push(new Paragraph({
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text: "REFERENCES", bold: true, size: 18, font: "Times New Roman" })],
}));
const refs = [
  "ICS Advisory Project, “ICS-Advisory-Project,” GitHub repository, ODbL v1.0. [Online]. Available: https://github.com/icsadvprj/ICS-Advisory-Project",
  "Cybersecurity and Infrastructure Security Agency, “Known Exploited Vulnerabilities Catalog.” [Online]. Available: https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
  "FIRST.org, “Exploit Prediction Scoring System (EPSS).” [Online]. Available: https://www.first.org/epss/",
  "CISA, “Vulnrichment,” GitHub repository. [Online]. Available: https://github.com/cisagov/vulnrichment",
  "MITRE, “ATT&CK for ICS.” [Online]. Available: https://attack.mitre.org/matrices/ics/",
  "National Institute of Standards and Technology, “Guide to Operational Technology (OT) Security,” NIST SP 800-82 Rev. 3, 2023.",
  "National Institute of Standards and Technology, “Security and Privacy Controls for Information Systems and Organizations,” NIST SP 800-53 Rev. 5, 2020.",
  "International Electrotechnical Commission, “IEC 62443 series — Industrial communication networks – Network and system security.”",
  "Center for Internet Security, “CIS Controls v8.” [Online]. Available: https://www.cisecurity.org/controls",
  "Transportation Security Administration, “Security Directive Pipeline-2021-02F,” 2022.",
  "National Institute of Standards and Technology, “Likely Exploited Vulnerabilities,” NIST CSWP 41, 2025.",
];
refs.forEach((r, i) => body2Col.push(refItem(i + 1, r)));

const doc = new Document({
  styles: { default: { document: { run: { font: "Times New Roman", size: 18 } } } },
  sections: [
    {
      properties: {
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } },
      },
      children: [titlePara, authorsPara, authorsPara2, abstractHeading, p(abstractText), indexTerms],
    },
    {
      properties: {
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } },
        column: { count: 2, space: 360 },
      },
      children: body2Col,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("TPEC2027_manuscript_DRAFT.docx", buf);
  console.log("wrote TPEC2027_manuscript_DRAFT.docx");
});
