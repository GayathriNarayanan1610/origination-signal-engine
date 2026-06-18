"""Orchestration: targets -> signals -> triage -> ranked digest + draft email."""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass

from . import llm
from .signals import get_signals
from .triage import is_hot, score_signals, top_signal


@dataclass
class CompanyResult:
    company: str
    score: float
    hot: bool
    rationale: str
    signals: list[dict]
    top_signal: str | None


def load_targets(path: str) -> list[str]:
    with open(path, newline="", encoding="utf-8") as fh:
        return [row["company"] for row in csv.DictReader(fh) if row.get("company")]


def analyse(company: str) -> CompanyResult:
    signals = get_signals(company)
    score = score_signals(signals)
    top = top_signal(signals)
    return CompanyResult(
        company=company, score=score, hot=is_hot(score),
        rationale=llm.rationale(company, signals, top),
        signals=[asdict(s) for s in signals],
        top_signal=top.headline if top else None,
    )


def build_digest(path: str) -> dict:
    results = sorted((analyse(c) for c in load_targets(path)), key=lambda r: r.score, reverse=True)
    hot = [r for r in results if r.hot]
    draft = None
    if hot:
        top_company = hot[0]
        top_sig = top_signal(get_signals(top_company.company))
        draft = {"company": top_company.company, "email": llm.draft_email(top_company.company, top_sig)}
    return {
        "generated": len(results),
        "hot_count": len(hot),
        "ranked": [asdict(r) for r in results],
        "draft_outreach": draft,
    }
