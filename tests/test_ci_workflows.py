"""Guard for the whole-suite rule (Boss, 2026-10-28; ruling 07:26Z): the unittest suite runs on
every pull request, and no workflow that runs tests or a suite gate carries a paths /
paths-ignore filter. Each workflow is PARSED (block and flow forms), never regex-matched.
A filter is allowed only for a workflow listed in EXCEPTIONS with its reason; none here.
Needs PyYAML (the 'test' extra); CI installs it."""
import pathlib
import re
import unittest

import yaml

WORKFLOWS = pathlib.Path(__file__).resolve().parent.parent / ".github" / "workflows"
EXCEPTIONS = {}  # {"file.yml": "reason"}

# Live-host jobs rule (Boss, 2026-10-28 07:36Z): a job that can reach a live host or publish a
# public download must be `if: false` or sit in a workflow_dispatch-only workflow.
KNOWN_LIVE = ["release.yml:publish"]  # PyPI publish: manual only
LIVE = [re.compile(p) for p in (
    r"\b(ssh|scp|rsync|sshpass)\b", r"\bwrangler\b", r"\bpages\s+deploy\b",
    r"\b(docker[ -])?compose\b[^\n]*\bup\b", r"\baws\s+s3\s+(cp|sync|mv|rm)\b",
    r"\bgh\s+release\s+(create|upload)\b", r"uploads\.github\.com", r"\btwine\s+upload\b",
    r"\b(uv|poetry)\s+publish\b", r"\bnpm\s+publish\b", r"\bfastlane\b", r"\baltool\b")]
LIVE_ACTIONS = [re.compile(p, re.I) for p in (
    r"ssh-action", r"cloudflare/(wrangler-action|pages-action)", r"pypa/gh-action-pypi-publish",
    r"upload-google-play", r"app-store", r"scp-action", r"rsync", r"s3-sync")]


def is_off(v):
    return v is False or (isinstance(v, str) and re.fullmatch(r"\s*(\$\{\{\s*)?false(\s*\}\})?\s*", v) is not None)


def live_jobs(doc):
    trig = list(triggers(doc))
    manual_only = bool(trig) and all(t == "workflow_dispatch" for t in trig)
    out = []
    for name, job in (doc.get("jobs") or {}).items():
        steps = job.get("steps") or []
        if any((s.get("run") and any(r.search(s["run"]) for r in LIVE)) or
               (s.get("uses") and any(r.search(s["uses"]) for r in LIVE_ACTIONS)) for s in steps):
            out.append({"job": name, "manual_only": manual_only, "off": is_off(job.get("if"))})
    return out


def all_live():
    return [dict(j, id=f"{p.name}:{j['job']}") for p in sorted(WORKFLOWS.glob("*.y*ml"))
            for j in live_jobs(yaml.safe_load(p.read_text()))]


def triggers(doc):
    on = doc.get("on", doc.get(True))  # PyYAML (YAML 1.1) loads the key `on` as True
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return {t: None for t in on}
    return on if isinstance(on, dict) else {}


def load(name):
    return yaml.safe_load((WORKFLOWS / name).read_text())


class CiWorkflowsTest(unittest.TestCase):
    def test_no_path_filters(self):
        files = sorted(p.name for p in WORKFLOWS.glob("*.y*ml"))
        self.assertTrue(files, "no workflow files found")
        for f in files:
            if f in EXCEPTIONS:
                continue
            filtered = [t for t, cfg in triggers(load(f)).items()
                        if isinstance(cfg, dict) and ("paths" in cfg or "paths-ignore" in cfg)]
            self.assertEqual(filtered, [], f"{f} filters {filtered} by path")

    def test_parser_sees_flow_form(self):
        doc = yaml.safe_load("on: { pull_request: { paths: ['src/**'] } }")
        self.assertIn("paths", triggers(doc)["pull_request"])

    def test_suite_runs_on_pull_request(self):
        doc = load("test.yml")
        self.assertIn("pull_request", triggers(doc))
        runs = "\n".join(s.get("run", "") for j in doc["jobs"].values() for s in j.get("steps", []))
        self.assertIn("unittest discover -s tests", runs)

    def test_live_host_jobs_are_manual_or_off(self):
        for j in all_live():
            self.assertTrue(j["manual_only"] or j["off"], f"{j['id']} can publish without a person")

    def test_sight_known_live_jobs(self):
        self.assertEqual(sorted(j["id"] for j in all_live()), sorted(KNOWN_LIVE))

    def test_sight_fixtures_and_negatives(self):
        wf = lambda on, step, **extra: {"on": on, "jobs": {"j": dict({"runs-on": "x", "steps": [step]}, **extra)}}
        pub = {"uses": "pypa/gh-action-pypi-publish@release/v1"}
        self.assertFalse(live_jobs(wf({"push": {"tags": ["v*"]}}, pub))[0]["manual_only"])
        self.assertEqual(len(live_jobs(wf("pull_request", {"run": "twine upload dist/*"}))), 1)
        self.assertEqual(len(live_jobs(wf({"schedule": [{"cron": "0 0 * * *"}]}, {"run": "rsync -a d/ h:/s"}))), 1)
        self.assertTrue(live_jobs(wf("workflow_dispatch", pub))[0]["manual_only"])
        self.assertTrue(live_jobs(wf({"push": None}, pub, **{"if": False}))[0]["off"])
        self.assertTrue(live_jobs(wf({"push": None}, pub, **{"if": "${{ false }}"}))[0]["off"])
        self.assertEqual(live_jobs(wf("pull_request", {"run": "python -m unittest"})), [])
        self.assertEqual(live_jobs(wf("pull_request", {"run": "uv build"})), [])
        # YAML 1.1 parses the key `on` as True: the parser path must handle it
        self.assertFalse(live_jobs(yaml.safe_load("on: {push: {tags: ['v*']}}\njobs: {p: {runs-on: x, steps: [{uses: pypa/gh-action-pypi-publish@v1}]}}"))[0]["manual_only"])


if __name__ == "__main__":
    unittest.main()
