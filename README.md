# Origination Signal Engine

> Watches a list of target companies, scores their latest signals against the
> investment thesis, and produces a ranked daily digest plus a draft outreach
> email for the hottest name - so origination follow-up is automated, not manual.

## Demo
`python -m app.run` prints the digest; `uvicorn app.main:app` serves `GET /digest`.

## How the team would use it
A morning digest of which targets moved (funding, leadership change, hiring, M&A),
ranked by how strongly the signals fit the thesis, with a ready-to-edit outreach
draft for the top trigger.

## What it does
For each target it fetches signals, scores them by type and recency into a single
"hotness" score, flags the hot ones, writes a one-line rationale, and drafts an
outreach email referencing the strongest signal. The LLM plans the rationale/email;
the scoring/triage is deterministic — the same split as a trustworthy agent.

## How it works
`signals.py` is the tool that fetches triggers (deterministic mock offline; seam for a
real news/firmographic API). `triage.py` scores them. `llm.py` writes the rationale +
email (mock or Azure OpenAI). `engine.py` orchestrates. Reuses the agentic patterns
from the Agentic Integration Service.

## Run it
```bash
pip install -r requirements.txt
python -m app.run        # CLI digest + draft email
pytest -q                # triage logic
```
Set `LLM_MODE=azure` (+ AZURE_* env) for real rationales/emails.

## Built with
Python · FastAPI · (Azure OpenAI in real mode)
