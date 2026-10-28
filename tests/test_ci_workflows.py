"""Guard for the whole-suite rule (Boss, 2026-10-28): the unittest suite runs on every pull
request, and no workflow uses a paths / paths-ignore filter that could skip it."""
import pathlib
import re
import unittest

WORKFLOWS = pathlib.Path(__file__).resolve().parent.parent / ".github" / "workflows"
FILTER = re.compile(r"^\s*(paths|paths-ignore)\s*:", re.M)


class CiWorkflowsTest(unittest.TestCase):
    def test_no_path_filters(self):
        files = sorted(WORKFLOWS.glob("*.y*ml"))
        self.assertTrue(files, "no workflow files found")
        for f in files:
            text = "\n".join(l for l in f.read_text().splitlines() if not l.lstrip().startswith("#"))
            self.assertIsNone(FILTER.search(text), f"{f.name} has a path filter")

    def test_suite_runs_on_pull_request(self):
        s = (WORKFLOWS / "test.yml").read_text()
        self.assertRegex(s, r"(?m)^\s*pull_request:\s*$")
        self.assertIn("unittest discover -s tests", s)


if __name__ == "__main__":
    unittest.main()
