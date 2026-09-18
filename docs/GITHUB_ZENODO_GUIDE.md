# Publishing this package to GitHub and Zenodo

This is separate from — and doesn't wait on — the TPEC 2027 conference
submission. GitHub and Zenodo are self-serve: you own both accounts, nothing
requires a third party's approval, and neither commits you to anything
about the paper's eventual peer review. This is exactly the kind of publish
step `docs/PUBLISH_GUIDE.md` calls out as available now versus TPEC 2027's
own timeline, which is still not published.

## Published release

The public source repository is
[`foikwuogu/pipeline-advisory-priority`](https://github.com/foikwuogu/pipeline-advisory-priority),
with a web results view at
[`foikwuogu.github.io/pipeline-advisory-priority`](https://foikwuogu.github.io/pipeline-advisory-priority/).

Zenodo archived the first public release as **v.1.0** on 2026-09-18. The
version-specific DOI is [10.5281/zenodo.22822467](https://doi.org/10.5281/zenodo.22822467).
This DOI and the source repository URL are recorded in `CITATION.cff` and
the README.

For a later release, create a new GitHub release and allow Zenodo to archive
the resulting immutable snapshot. Zenodo will mint a distinct version DOI;
the concept DOI remains the appropriate citation for the latest version.

## What this does and doesn't do for TPEC 2027

This DOI is for the **reproducibility package** (data, code, docs, this
manuscript draft) — a normal, encouraged practice that many venues actually
ask authors to link to in the paper itself (a "data and code availability"
statement). It is a different, separate thing from the **IEEE Xplore DOI**
the published *paper* would eventually get after TPEC 2027 accepts it,
you present it, and the conference committee submits proceedings to IEEE
(the full mechanics are in `docs/PUBLISH_GUIDE.md`). Once you have this
Zenodo DOI, it's worth adding a one-line "Data and code availability"
statement to the manuscript citing it — that's a genuine, professional
touch reviewers like to see, and I can add it once you have the DOI.
