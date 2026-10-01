import unittest

import windytranslate as wt
from windytranslate.cli import main

DATA = {"models": [
    {"id": "translate-en-de", "repo": "WindyTranslate/translate-en-de", "task": "translation", "name": "English to German",
     "src": "en", "tgt": "de", "licence": "CC-BY-4.0", "licenceStatus": "matches-upstream", "attribution": "Based on OPUS-MT",
     "notice": "NOTICE en-de", "library": "transformers", "score": {"chrf": 63.05, "band": "Excellent", "benchmark": "FLORES-200 dev"}},
    {"id": "translate-en-gem", "repo": "WindyTranslate/translate-en-gem", "task": "translation", "name": "English to Germanic",
     "srcLangs": ["en"], "tgtLangs": ["de", "nl"], "multiTarget": True, "licence": "Apache-2.0", "licenceStatus": "matches-upstream",
     "attribution": "x", "library": "transformers", "score": {"chrf": 55.0, "band": "Good"}},
    {"id": "translate-en-sw", "repo": "WindyTranslate/translate-en-sw", "task": "translation", "name": "English to Swahili",
     "src": "en", "tgt": "sw", "licence": "Apache-2.0", "licenceStatus": "", "attribution": "y", "library": "transformers", "score": None},
    {"id": "translate-hplt-en-sw", "repo": "WindyTranslate/translate-windy-hplt-en-sw", "task": "translation", "name": "x",
     "src": "en", "tgt": "sw", "licence": "CC-BY-4.0", "licenceStatus": "under-review", "attribution": "z", "library": "ctranslate2", "score": None},
    {"id": "listen-windy-core", "repo": "WindyWord/listen-windy-core", "task": "speech-recognition", "name": "ASR",
     "licence": "Apache-2.0", "licenceStatus": "matches-upstream", "attribution": "w"},
]}


class Catalogue(unittest.TestCase):
    def setUp(self):
        self.models = wt.catalogue(data=DATA)

    def test_best_scored_first_then_single_target(self):
        best = wt.find("en", "de", self.models)
        self.assertEqual(best.repo, "WindyTranslate/translate-en-de")
        self.assertEqual([m.id for m in wt.candidates("EN", "DE", self.models)], ["translate-en-de", "translate-en-gem"])

    def test_unscored_is_never_promoted_and_library_filter(self):
        self.assertIsNone(wt.find("en", "sw", self.models).chrf)
        self.assertEqual(wt.find("en", "sw", self.models, library="ctranslate2").library, "ctranslate2")

    def test_licence_flags_and_notice(self):
        m = wt.find("en", "de", self.models)
        self.assertTrue(m.licence_clear)
        self.assertEqual(m.notice, "NOTICE en-de")
        self.assertEqual(m.page, "https://windytranslate.com/models/translate-en-de")
        flagged = wt.find("en", "sw", self.models, library="ctranslate2")
        self.assertFalse(flagged.licence_clear)

    def test_missing_pair_raises(self):
        with self.assertRaises(LookupError):
            wt.find("en", "xx", self.models)

    def test_speech_models_are_not_translation_candidates(self):
        self.assertTrue(all(m.task == "translation" for m in wt.candidates("en", "de", self.models)))

    def test_sentence_split(self):
        from windytranslate.local import sentences
        self.assertEqual(sentences("Hi there. Where is it? 駅はどこ？はい。"), ["Hi there.", "Where is it?", "駅はどこ？", "はい。"])


if __name__ == "__main__":
    unittest.main()
