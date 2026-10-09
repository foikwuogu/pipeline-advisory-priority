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

## Update — 2026-10-08: the situation has changed, and may be urgent

Rechecked today. The official TAMU TPEC homepage (`tpec.engr.tamu.edu/`) now
shows a "TPEC 2027 Begins in..." countdown, a published Call-for-Papers
banner image, and text stating "Paper submissions for TPEC 2027 are now
open." **However, the site is in an inconsistent, mid-transition state**:
the "LEARN MORE & SUBMIT" and "Call For Papers" links on that homepage both
resolve to `submissions.html` and `call-for-papers.html`, and those two
pages still serve **TPEC 2026** content when checked directly (2026
deadline, 2026 PDF eXpress ID `67884X`, no 2027 EasyChair link). So the
homepage banner has been updated but the actual submission mechanics
pages have not — there is no confirmed, working TPEC-2027-specific
submission portal, template link, or PDF eXpress ID yet, despite the
banner's claim.

A separate, TAMU-affiliated source — `epg.engr.tamu.edu/upcoming-events/`
(the Electric Power & Power Electronics Group's own events page, not the
TPEC site itself) — states: **"Full paper submission deadline: Sunday,
November 1, 2026" and explicitly calls this "FINAL and will not be
extended."** That page also says conference dates are still "to be
determined" (not confirmed as Feb 7–9, 2027, despite that date appearing
elsewhere, including the target citation this project started from), lists
the venue as the Memorial Student Center at Texas A&M University, and
names the IEEE Industry Applications Society as this cycle's sponsor, with
possible invited publication in *IEEE Transactions on Industry
Applications* or *IEEE Industry Applications Magazine* for presented
papers.

**This November 1, 2026 date, if real, is about 3.5 weeks from today.**
I was not able to independently confirm it against the TPEC site's own
submission pages (which are still stale), and a third-party CFP aggregator
checked the same day shows internally inconsistent deadline text of its
own ("2026-11-01" in one spot, "To Be Announced" in another). A real CFP
flyer image now exists on the TPEC homepage
(`tpec.engr.tamu.edu/uploads/1/4/2/3/142355208/tpec-2027-call-for-papers-web-150dpi-2_orig.png`)
that likely has the authoritative wording, but it's an image — the tools
available to this project can fetch the page but cannot read text out of
an image file at a URL. **The author should open that flyer directly in a
browser** to get the confirmed deadline, format, and portal link, rather
than relying on any of the secondhand sources above.

**Bottom line:** treat November 1, 2026 as a real possibility that needs
the author's own direct confirmation, not a settled fact — and given how
little time that would leave, confirming it is now the single highest-
priority open item in `docs/VERIFY_CHECKLIST.md`'s TPEC-2027 line.

## What is confirmed NOT yet available (checked 2026-09-18, partially superseded above)

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
