# Publishing this package to GitHub and Zenodo

This is separate from — and doesn't wait on — the TPEC 2027 conference
submission. GitHub and Zenodo are self-serve: you own both accounts, nothing
requires a third party's approval, and neither commits you to anything
about the paper's eventual peer review. This is exactly the kind of publish
step `docs/PUBLISH_GUIDE.md` calls out as available now versus TPEC 2027's
own timeline, which is still not published.

Status as of 2026-09-18: `docs/VERIFY_CHECKLIST.md` is signed off, the
placeholder/DRAFT text is cleared, and `scripts/publish_gate.py` passes.
The repository has already been initialized and committed on your computer
at `Project\pipeline-advisory-priority` (one commit so far). What's left is
entirely steps only you can do, because they need your own GitHub and
Zenodo login — nothing here can be done on your behalf without your
credentials, and it shouldn't be.

## Part 1 — Push to GitHub

1. **Create an empty repository on GitHub** (github.com → the "+" menu →
   "New repository"). Suggested name: `pipeline-advisory-priority`. Leave
   it empty — no README, no license, no .gitignore — since this repo
   already has all of those; adding them on GitHub's side would conflict
   with the first push.
2. **Choose public or private.** Public is normal for this kind of
   reproducibility package and is what lets Zenodo mint a DOI from it for
   free; private repos need a paid Zenodo-for-GitHub tier for the same
   thing. If you're not sure, public is the standard choice here.
3. **Copy the repository's URL** GitHub shows you right after creation —
   it looks like `https://github.com/<your-username>/pipeline-advisory-priority.git`.
4. Tell me that URL (or just your GitHub username, if the repo name above
   is right) and I'll run the two remaining commands on your computer:
   ```
   git remote add origin <that URL>
   git push -u origin main
   ```
   The push is the one step that needs your own authentication — GitHub
   will prompt you (browser sign-in or a credential-manager popup on
   Windows) the first time, since this is your account, not something I
   can authenticate as. That's expected and correct.

Once that succeeds, the repository is live at
`https://github.com/<your-username>/pipeline-advisory-priority`.

## Part 2 — Connect Zenodo and mint a DOI

Zenodo's GitHub integration auto-archives a snapshot of your repo every
time you create a GitHub "Release," and mints a permanent DOI for each one.
This is the standard way researchers get a citable DOI for a GitHub repo
without touching Zenodo's upload UI directly.

1. Go to **zenodo.org** and log in — the easiest way is "Log in with
   GitHub," which also handles the permission Zenodo needs to watch your
   repos.
2. Go to **Settings → GitHub** (under your account menu).
3. Find `pipeline-advisory-priority` in the list and **toggle it on**. If
   it doesn't appear, click "Sync now" — Zenodo only lists repos it's
   already aware of, and a fresh push sometimes needs a manual sync.
4. Back on GitHub, go to your repo's **Releases** page and **"Create a new
   release."**
   - Tag: `v1.0.0` (or `v0.1.0` if you'd rather signal this is still a
     pre-submission draft snapshot — either is fine, Zenodo doesn't care
     which scheme you use).
   - Title: something like "v1.0.0 — TPEC 2027 submission draft."
   - Description: can just point back to the paper title and note this is
     the reproducibility package, not the manuscript's camera-ready form.
   - Click **"Publish release."**
5. Zenodo picks this up automatically (usually within a minute or two),
   archives that exact snapshot, and assigns it a DOI. You'll see it appear
   under your Zenodo "Uploads."

## Part 3 — Fold the DOI back into the package

Once Zenodo gives you the DOI (it looks like `10.5281/zenodo.XXXXXXX`), send
it to me and I'll update, in one pass:

- `CITATION.cff` — replace `"[to be filled in on Zenodo publish]"` with the
  real DOI.
- `README.md` — add a DOI badge/line near the top.
- The project's `claude/build-status.md` doc, so the record stays current.

The `repository-code` field in `CITATION.cff` (currently
`"[to be filled in on GitHub publish]"`) can be filled in as soon as you
have the GitHub URL from Part 1 — no need to wait for the DOI for that one.

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
