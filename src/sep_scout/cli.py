from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from .agent import extract_candidates
from .config import load_config
from .search import search_public_web
from .sheets import append_new_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Find public-web SEP prospects at Cal Poly SLO")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write-sheet", action="store_true")
    args = parser.parse_args()
    load_dotenv()
    config = load_config(args.config)
    results: list[dict[str, str]] = []
    per_query = max(1, int(__import__("os").getenv("SEARCH_RESULTS_PER_QUERY", "10")))
    for query in config["queries"]:
        results.extend(search_public_web(query, limit=per_query))
    candidates = extract_candidates(results[: args.limit * 4], config)[: args.limit]
    Path("data").mkdir(exist_ok=True)
    Path("data/latest_candidates.json").write_text(json.dumps([c.to_dict() for c in candidates], indent=2, ensure_ascii=False))
    if args.write_sheet and not args.dry_run:
        print(f"Appended {append_new_candidates(candidates)} new candidates to Google Sheets.")
    for candidate in candidates:
        print(f"{candidate.score:>3} | {candidate.name} | {candidate.cutoff_status} | {candidate.source_url}")


if __name__ == "__main__":
    main()
