"""Score how 'hot' each company is from its signals (the triage step).

Score = sum over signals of (type weight x recency factor). Recent, high-value
signals (funding, leadership) push a company over the hot threshold.
"""
from __future__ import annotations

from .config import SIGNAL_WEIGHTS, settings
from .signals import Signal


def recency_factor(days: int) -> float:
    # 1.0 today -> ~0.5 at 45 days -> ~0.25 at 90 days
    return max(0.2, 1.0 - days / 120.0)


def score_signals(signals: list[Signal]) -> float:
    return round(sum(SIGNAL_WEIGHTS.get(s.type, 0.5) * recency_factor(s.recency_days) for s in signals), 2)


def is_hot(score: float) -> bool:
    return score >= settings.hot_threshold


def top_signal(signals: list[Signal]) -> Signal | None:
    if not signals:
        return None
    return max(signals, key=lambda s: SIGNAL_WEIGHTS.get(s.type, 0.5) * recency_factor(s.recency_days))
