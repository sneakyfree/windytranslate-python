"""Guard for the whole-suite rule (Boss, 2026-10-28; ruling 07:26Z): the unittest suite runs on
every pull request, and no workflow that runs tests or a suite gate carries a paths /
paths-ignore filter. Each workflow is PARSED (block and flow forms), never regex-matched.
A filter is allowed only for a workflow listed in EXCEPTIONS with its reason; none here.
Needs PyYAML (the 'test' extra); CI installs it."""
import pathlib
import unittest

import yaml

WORKFLOWS = pathlib.Path(__file__).resolve().parent.parent / ".github" / "workflows"
EXCEPTIONS = {}  # {"file.yml": "reason"}


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


if __name__ == "__main__":
    unittest.main()
