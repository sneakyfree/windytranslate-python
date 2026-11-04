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

| Branch | PR | Last commit | Owner | Verdict | Why |
|---|---|---|---|---|---|
| ci/tests-on-every-pr | #1 (merged as ce627cb0) | c87371e1, 2026-10-28 | Windy Translate | superseded: tag archive/ci-tests-on-every-pr-20261104, then delete | squash-merged; its tip equals the merged PR head (checked 2026-11-04) |

## Done (last 30 days)

- 2026-10-28: #1 tests run on every PR; PyPI release is manual only and refuses unless run from a v* tag; workflow guards parse the YAML.
