"""CLI: print the daily origination digest.  python -m app.run"""
from __future__ import annotations

from .config import settings
from .engine import build_digest


def main() -> None:
    digest = build_digest(settings.targets_csv)
    print(f"\n=== Origination Digest — {digest['hot_count']} hot of {digest['generated']} targets ===\n")
    for r in digest["ranked"]:
        flag = "HOT " if r["hot"] else "    "
        print(f"  {flag}[{r['score']:5.2f}] {r['company']:24s} {r['rationale']}")
    if digest["draft_outreach"]:
        print(f"\n--- Draft outreach to {digest['draft_outreach']['company']} ---\n")
        print(digest["draft_outreach"]["email"])
    print()


if __name__ == "__main__":
    main()
