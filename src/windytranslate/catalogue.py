"""The model catalogue (standard library only)."""
from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

MANIFEST_URL = "https://windytranslate.com/models.json"
USER_AGENT = "windytranslate-python/0.1.0"
_cache: dict = {}


@dataclass(frozen=True)
class Model:
    id: str
    repo: str
    task: str
    name: str
    licence: str
    licence_status: str
    attribution: str
    notice: str
    library: Optional[str] = None
    src_langs: tuple = ()
    tgt_langs: tuple = ()
    multi_target: bool = False
    subfolder: Optional[str] = None
    score: Optional[dict] = None
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @property
    def page(self) -> str:
        return f"https://windytranslate.com/models/{self.id}"

    @property
    def chrf(self) -> Optional[float]:
        return (self.score or {}).get("chrf")

    @property
    def licence_clear(self) -> bool:
        """False when the catalogue flags the licence (under review, differs from upstream...)."""
        return self.licence_status in ("matches-upstream", "", None)

    @classmethod
    def from_json(cls, m: dict) -> "Model":
        return cls(
            id=m["id"], repo=m["repo"], task=m.get("task", ""), name=m.get("name", ""),
            licence=m.get("licence", ""), licence_status=m.get("licenceStatus") or "",
            attribution=m.get("attribution", ""), notice=m.get("notice") or m.get("attribution", ""),
            library=m.get("library"),
            src_langs=tuple(m.get("srcLangs") or ([m["src"]] if m.get("src") else [])),
            tgt_langs=tuple(m.get("tgtLangs") or ([m["tgt"]] if m.get("tgt") else [])),
            multi_target=bool(m.get("multiTarget")), subfolder=m.get("subfolder"),
            score=m.get("score") or None, raw=m,
        )


def catalogue(url: str = MANIFEST_URL, data: Optional[dict] = None, refresh: bool = False) -> list:
    """All models. Pass `data` (the parsed models.json) to work offline."""
    if data is None:
        if refresh or url not in _cache:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                _cache[url] = json.load(r)
        data = _cache[url]
    return [Model.from_json(m) for m in data["models"]]


def candidates(src: str, tgt: str, models: Optional[list] = None, library: Optional[str] = None) -> list:
    """Translation models covering src -> tgt, best measured chrF++ first; unscored last."""
    src, tgt = src.lower(), tgt.lower()
    models = catalogue() if models is None else models
    hits = [m for m in models if m.task == "translation" and src in m.src_langs and tgt in m.tgt_langs
            and (library is None or m.library == library)]
    return sorted(hits, key=lambda m: (m.chrf is None, -(m.chrf or 0.0), m.multi_target))


def find(src: str, tgt: str, models: Optional[list] = None, library: Optional[str] = None) -> Model:
    """The best model for src -> tgt. Raises LookupError if none exists."""
    found = candidates(src, tgt, models, library)
    if not found:
        raise LookupError(f"no model for {src} -> {tgt}; browse https://windytranslate.com/languages")
    return found[0]
