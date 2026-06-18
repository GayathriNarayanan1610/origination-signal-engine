"""Signal source (tool: fetch external triggers about a company).

`mock` generates deterministic, plausible signals so the engine runs offline.
`api` is where you'd wire a real news/firmographic API (httpx + auth + retry).
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass

from .config import SIGNAL_WEIGHTS, settings

_TYPES = list(SIGNAL_WEIGHTS.keys())

_TEMPLATES = {
    "funding_round": "Raised a new funding round (Series {x})",
    "leadership_change": "Appointed a new {role}",
    "acquisition": "Acquired a smaller competitor",
    "hiring_spike": "Open roles up ~{x}% quarter-on-quarter",
    "product_launch": "Launched a new product line",
    "news_mention": "Featured in trade press on {topic}",
}


@dataclass
class Signal:
    type: str
    headline: str
    recency_days: int  # smaller = more recent = more relevant


def _mock_signals(company: str) -> list[Signal]:
    seed = int(hashlib.md5(company.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    out: list[Signal] = []
    for stype in _TYPES:
        if rng.random() < 0.45:  # not every signal fires for every company
            tmpl = _TEMPLATES[stype]
            headline = tmpl.format(
                x=rng.choice(["A", "B", "C"]) if stype == "funding_round" else rng.randint(20, 80),
                role=rng.choice(["CRO", "CTO", "VP Sales"]),
                topic=rng.choice(["AI adoption", "market expansion", "compliance"]),
            )
            out.append(Signal(type=stype, headline=headline, recency_days=rng.randint(1, 90)))
    return out


def get_signals(company: str) -> list[Signal]:
    if settings.signal_source == "api":  # pragma: no cover - seam for a real source
        raise NotImplementedError("wire a real news/firmographic API here (httpx + auth + retry)")
    return _mock_signals(company)
