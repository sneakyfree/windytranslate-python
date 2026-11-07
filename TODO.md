# TODO: windytranslate (Python client)

Owner of every line: the Windy Translate team unless a line names someone else.
Read this first at every session start and turnover. A promise or date that names this team goes in here the same day. Line standard: `- [ ] what · OWNER · ADDED · DUE · STATUS · SOURCE`; done lines `- [x] what · OWNER · ADDED · DONE · PROOF` move to Done.
Items leave only into Done (shipped and tested) or by a recorded owner decision saying why.

**WE ARE LIVE. NOT A SANDBOX.** (owner's standing rule, 2026-11-06). Build and ship for real. What does not change: don't break what's live (every change has a way back), say only what's true, and every production release has an owner's go.
The owner's gates before any big marketing push, in order: (1) the owner and a few friends use everything and call it solid; (2) record-keeping works end to end (ledger, signed documents, support email, sign-up); (3) an attorney reviews the legal documents; (4) every credential is renewed; (5) then the marketing spend.

## Now

Honest state (2026-11-07): version 0.1.0 is on PyPI (published 2026-10-01; its source matches main). It lists open models from the windytranslate.com catalogue and runs them locally. No release is planned right now. Publishing is manual only (release.yml, run by hand from a v* tag).

- [ ] Catch-up TODO PR merged to main (the we-are-live line, the gates, the line standard) · OWNER Windy Translate · ADDED 2026-11-06 · DUE 2026-11-07 · STATUS waiting on a reader + the owner's stamp · SOURCE this PR (#4)
- [ ] Delete the merged branch docs/todo-compress-20261104 (#3) after checking tip = merged PR head · OWNER Windy Translate · ADDED 2026-11-07 · DUE 2026-11-08 · STATUS now · SOURCE Branches table below

## Waiting on

- [ ] A public "Windy Translate" tile in the Windy Fly apps (badge: developer) linking to windytranslate.com, the developer side that this package belongs to; nothing changes here for it; done when the tile is live · OWNER the Windy Fly app teams · ADDED 2026-11-06 · DUE none · STATUS waiting on the app teams · SOURCE owner decision 2026-11-06

## Later

- [ ] A client for a hosted Windy Translate API; the hosted developer API does not exist yet · OWNER Windy Translate · ADDED 2026-11-04 · DUE none · STATUS later · SOURCE TODO.md 2026-11-04

## Branches

Checked 2026-11-07. Besides `main`:

| Branch | PR | Owner | Verdict | Why |
|---|---|---|---|---|
| docs/todo-compress-20261104 | #3 (merged as 840732a1) | Windy Translate | delete after the tip check | squash-merged |
| (this PR's branch) | this file | Windy Translate | merge, then delete | open PR |

ci/tests-on-every-pr (#1) is gone; its tip is kept by tag archive/ci-tests-on-every-pr-20261104.

## Done (last 30 days)

- [x] TODO.md re-dated · OWNER Windy Translate · ADDED 2026-11-04 · DONE 2026-11-05 · PROOF #3 840732a1
- 2026-11-04: #2 TODO.md + CLAUDE.md line (ad8f926).
- 2026-10-28: #1 tests run on every PR; PyPI release is manual only and refuses unless run from a v* tag; workflow guards parse the YAML.
