"""Local translation with transformers (pip install "windytranslate[local]")."""
from __future__ import annotations

import re
from typing import Optional

from .catalogue import find


def sentences(text: str) -> list:
    """Split on sentence-ending punctuation: small pair models drop or invent
    sentences when given a whole paragraph as one input."""
    # Latin-style ends need whitespace after them; CJK full-width ends don't.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|(?<=[。！？])\s*", text.strip()) if s.strip()]


_loaded: dict = {}


def translate(text: str, src: str, tgt: str, repo: Optional[str] = None, num_beams: int = 4) -> str:
    """Translate locally with the best transformers model for src -> tgt (or `repo`).
    Line breaks are kept; each line is translated sentence by sentence."""
    try:
        from transformers import MarianMTModel, MarianTokenizer
    except ImportError as e:  # pragma: no cover
        raise ImportError('local translation needs: pip install "windytranslate[local]"') from e
    if repo is None:
        m = find(src, tgt, library="transformers")
        if m.multi_target:
            raise ValueError(f"{m.repo} is multi-target; pass repo= and see {m.page}")
        repo, sub = m.repo, m.subfolder
    else:
        sub = None
    key = (repo, sub)
    if key not in _loaded:
        kw = {"subfolder": sub} if sub else {}
        _loaded[key] = (MarianTokenizer.from_pretrained(repo, **kw), MarianMTModel.from_pretrained(repo, **kw))
    tok, model = _loaded[key]
    out_lines = []
    for line in text.split("\n"):
        parts = sentences(line)
        if not parts:
            out_lines.append(line)
            continue
        batch = tok(parts, return_tensors="pt", padding=True)
        gen = model.generate(**batch, num_beams=num_beams, max_new_tokens=256)
        out_lines.append(" ".join(tok.batch_decode(gen, skip_special_tokens=True)))
    return "\n".join(out_lines)
