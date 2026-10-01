"""Windy Translate: find, license-check and run Windstorm Labs' open models.

    >>> import windytranslate as wt
    >>> m = wt.find("en", "de")          # best measured English -> German model
    >>> m.repo, m.licence, m.score
    >>> print(m.notice)                  # attribution to ship with your product
    >>> wt.translate("Where is the station?", "en", "de")   # needs: pip install "windytranslate[local]"

The catalogue is https://windytranslate.com/models.json (fetched once per
process, or pass your own copy). Scores are a FLORES-200 screening; a model
with no score is "not yet scored", never "good".
"""
from .catalogue import Model, catalogue, candidates, find
from .local import translate

__all__ = ["Model", "catalogue", "candidates", "find", "translate"]
__version__ = "0.1.0"
