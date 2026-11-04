# TODO: windytranslate (Python client)

Owner of every line: the Windy Translate team unless a line names someone else.
Read this first at every session start and turnover. Add every promise here the same turn.
Items leave only into Done (shipped and tested) or by a recorded owner decision saying why.

## Now

Honest state (2026-11-04): version 0.1.0 is on PyPI (published 2026-10-01; its source matches main). It lists open models from the windytranslate.com catalogue and runs them locally. No release is planned right now. Publishing is manual only (release.yml, run by hand from a v* tag).

- Nothing scheduled this week.

## Waiting on

- Nothing.

## Later

- A client for a hosted Windy Translate API. Why later: the hosted developer API does not exist yet.

## Branches

Checked 2026-11-04. Besides `main`, only the branch of this open PR:

| Branch | PR | Owner | Verdict | Why |
|---|---|---|---|---|
| docs/todo-compress-20261104 | #3 (this file) | Windy Translate | merge, then delete | open PR |

## Done (last 30 days)

- 2026-11-04: ci/tests-on-every-pr (#1) DELETED after re-checking tip = merged PR head = archive tag; tag archive/ci-tests-on-every-pr-20261104 keeps the tip.
- 2026-11-04: #2 TODO.md; archive tag pushed for ci/tests-on-every-pr.
- 2026-10-28: #1 tests run on every PR; PyPI release is manual only and refuses unless run from a v* tag; workflow guards parse the YAML.
