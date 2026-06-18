"""LLM layer: a one-line investment rationale + a draft outreach email.

`mock` is deterministic (no creds). `azure` calls Azure OpenAI. Same interface.
"""
from __future__ import annotations

from .config import settings
from .signals import Signal


def _mock_rationale(company: str, signals: list[Signal], top: Signal | None) -> str:
    if not top:
        return f"No notable triggers for {company} right now."
    return (f"{company} is worth a look: {top.headline.lower()} "
            f"({top.recency_days}d ago), plus {len(signals)} active signal(s).")


def _mock_email(company: str, top: Signal | None) -> str:
    hook = top.headline.lower() if top else "your recent momentum"
    return (f"Subject: Congratulations on the recent news, {company}\n\n"
            f"Hi <name>,\n\nI noticed {hook}. We invest in European B2B software "
            f"businesses at exactly {company}'s stage and would love to compare notes "
            f"on your roadmap. Open to a short call next week?\n\nBest,\n<you>")


def _azure(messages):  # pragma: no cover - requires creds
    from langchain_openai import AzureChatOpenAI

    llm = AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint, api_key=settings.azure_openai_api_key,
        azure_deployment=settings.azure_deployment, api_version=settings.azure_api_version,
        temperature=0.3,
    )
    return llm.invoke(messages).content


def rationale(company: str, signals: list[Signal], top: Signal | None) -> str:
    if settings.llm_mode == "azure":  # pragma: no cover
        ctx = "; ".join(s.headline for s in signals) or "no signals"
        return _azure([("system", "One sentence, why a B2B-software PE investor should look now. No fluff."),
                       ("user", f"Company: {company}. Signals: {ctx}.")])
    return _mock_rationale(company, signals, top)


def draft_email(company: str, top: Signal | None) -> str:
    if settings.llm_mode == "azure":  # pragma: no cover
        hook = top.headline if top else "recent momentum"
        return _azure([("system", "Write a short, warm, non-salesy outreach email (<120 words) with a subject line."),
                       ("user", f"Company: {company}. Hook: {hook}.")])
    return _mock_email(company, top)
