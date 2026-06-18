from app.signals import Signal
from app.triage import recency_factor, score_signals, is_hot, top_signal


def test_recency_decays():
    assert recency_factor(0) > recency_factor(45) > recency_factor(90)


def test_funding_outranks_news():
    funding = [Signal("funding_round", "Raised Series B", 5)]
    news = [Signal("news_mention", "Mentioned in press", 5)]
    assert score_signals(funding) > score_signals(news)


def test_top_signal_picks_strongest():
    sigs = [Signal("news_mention", "press", 2), Signal("funding_round", "Series A", 2)]
    assert top_signal(sigs).type == "funding_round"


def test_is_hot_threshold():
    hot = [Signal("funding_round", "x", 1), Signal("leadership_change", "y", 1)]
    assert is_hot(score_signals(hot))
