# Publish guide — TPEC 2027 submission

**Last checked:** 2026-09-18 (TPEC organizers' own site + the TPEC 2026
precedent, same organizing department). **Nothing in this guide can be
executed yet** — TPEC 2027's call for papers has not been published. This
document exists so that when it is published, the remaining steps are
already laid out.

## The short answer: how does the paper get an IEEE Xplore DOI?

Not directly, and not by anything either the author or this build process
can do unilaterally. The DOI is the last link in a chain that runs entirely
through the conference and IEEE, in this order:

1. **Peer review acceptance.** The paper is submitted to TPEC 2027 (via
   EasyChair, going by the TPEC 2026 precedent) and accepted by the technical
   program committee.
2. **Camera-ready revision.** The accepted paper is revised into IEEE's
   official conference template (Word or LaTeX, US Letter, page-limited —
   6 pages including figures/tables/refs for TPEC 2026) and validated through
   **IEEE PDF eXpress**, a compliance tool tied to a conference-specific ID
   issued by IEEE per event (TPEC 2026's was `67884X`; TPEC 2027's does not
   exist yet because the conference hasn't been set up in IEEE's system).
3. **Copyright transfer.** The author executes an IEEE copyright transfer
   form through the conference's own submission portal at camera-ready time.
   This is a personal, author-signed action — not something that can be done
   on the author's behalf.
4. **In-person presentation.** Per TPEC's own CFP language (TPEC 2026:
   "Papers must be presented in person at the conference to be submitted for
   inclusion into IEEE Xplore"), an author must physically present the paper
   at the conference (College Station, TX, Feb 7–9, 2027) for it to be
   eligible for Xplore at all. A paper that is accepted but not presented is
   typically dropped from the proceedings submitted to IEEE.
5. **Committee compiles proceedings.** After the conference, the TPEC
   organizing committee — not individual authors — bundles all presented,
   copyright-cleared papers into the proceedings package and submits it to
   IEEE.
6. **IEEE reviews and publishes.** IEEE checks the package against its own
   scope/quality criteria and, once cleared, publishes it to Xplore —
   typically **about six weeks after the conference ends**, per IEEE's own
   Author Center guidance. The DOI is assigned at this point, by IEEE, not
   before.

So the DOI is a downstream consequence of being accepted, revised to
camera-ready spec, copyright-cleared, and physically presented — not
something that attaches to a paper on submission, and not something this
project's build process (or any automated tooling) can produce or shortcut.

## What is confirmed NOT yet available (checked 2026-09-18)

- `tpec.engr.tamu.edu/submissions.html` — the conference's own official
  site — still only covers TPEC 2026; no TPEC 2027 page, deadline,
  EasyChair portal, IEEE template link, or PDF eXpress conference ID exists
  there yet.
- A third-party CFP aggregator (allconferencecfpalerts.com) does list a
  "2027 IEEE Texas Power and Energy Conference" entry with dates Feb 7–9,
  2027, IEEE format, 6-page limit, and submission deadline "to be
  announced" — but this is not the organizing committee's own site, it
  gave an inconsistent secondary deadline reference elsewhere on the page,
  and it provided no working submission portal link. Treat it as an early
  signal, not a confirmed CFP, until the official TAMU site or an
  EasyChair link corroborates it.
- The TPEC 2026 cycle (same organizing department, same venue pattern) is
  the only reliable precedent for what TPEC 2027's requirements will likely
  look like: EasyChair submission, IEEE Word/LaTeX template, 6-page limit,
  PDF eXpress validation, copyright transfer via the portal, in-person
  presentation requirement.

## What can legitimately be prepared right now

- Clear `docs/VERIFY_CHECKLIST.md` — this is the actual blocking step and is
  entirely independent of TPEC's publication schedule. A paper that isn't
  verified isn't ready regardless of when the CFP drops.
- Keep the manuscript's content (methods, results, figures, numbers all
  traced to `data/processed/stats.json`) stable and citable, so that once the
  real IEEE template is available, converting the content into it is a
  formatting pass, not a rewrite.
- Monitor `tpec.engr.tamu.edu` and EasyChair for the TPEC 2027 CFP
  announcement. Once it appears: fill in the submission deadline, IEEE
  template link, and PDF eXpress conference ID in this document, then work
  through steps 1–4 above.

## Explicitly out of scope for this build process

Per this project's own build rules, nothing here submits to TPEC, executes a
copyright transfer, or represents the paper as ready for a personal
attestation the author has not made. Those are the author's actions alone,
and only once `docs/VERIFY_CHECKLIST.md` is fully signed off and TPEC 2027's
actual requirements are published.
