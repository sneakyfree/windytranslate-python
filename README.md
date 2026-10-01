# windytranslate

Find, license-check and run [Windstorm Labs](https://windstormlabs.com)' open
translation and speech models: 1,660 translation pair models, 3 multilingual
models and 66 speech-to-text models, each with its measured score, licence
and attribution. Catalogue: **[windytranslate.com](https://windytranslate.com)**.

```bash
pip install windytranslate            # catalogue client: standard library only
pip install "windytranslate[local]"   # + local translation with transformers
```

```python
import windytranslate as wt

m = wt.find("en", "de")       # best measured English -> German model
print(m.repo, m.licence, m.chrf, m.page)
print(m.notice)               # attribution text to ship with your product

print(wt.translate("Where is the train station? The museum opens at ten.", "en", "de"))
```

```bash
windytranslate find en sw --all
windytranslate find en fr --notice
windytranslate translate en fr "Where is the train station?"
```

- **Scores** are a FLORES-200 screening (48 sentences per pair), published for
  every scored pair including weak ones. A model with no score is "not yet
  scored", never "good". Method: [windytranslate.com/evaluation](https://windytranslate.com/evaluation).
- **Licences** belong to each model (usually Apache-2.0 or CC-BY-4.0, from
  OPUS-MT by Helsinki-NLP). CC-BY requires attribution; `m.notice` gives it.
  `m.licence_clear` is False when the catalogue flags the licence (e.g. under
  review). See [windytranslate.com/licensing](https://windytranslate.com/licensing).
- Text is translated sentence by sentence: small pair models drop or invent
  sentences when a paragraph is one input.
- Everything runs on your machine after the model download. No key, no account.

This package's code is Apache-2.0. Hosted API: early access, free in beta,
[windytranslate.com/api](https://windytranslate.com/api). Examples and a
Docker self-host server: [windytranslate-examples](https://github.com/sneakyfree/windytranslate-examples).
