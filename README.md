# SEP Candidate Scout

A GitHub-based research agent for finding promising Sigma Eta Pi prospects at Cal Poly SLO.

It searches public web sources, extracts evidence about future-entrepreneur signals, applies the December 2028+ graduation cutoff, ranks candidates using a version-controlled preference profile, deduplicates against an existing Google Sheet, and can append approved-format rows to the `Web Prospects` tab.

## What it is

This is an agent workflow, not model training. GitHub stores the code, prompts, configuration, and history. At runtime it uses an LLM plus public search results and public pages.

The preference profile currently prioritizes:

- concrete products and prototypes, when available
- strong operators who recruit, organize, sell, fundraise, or execute
- high-impact domain work in areas such as climate, health, biotech, aerospace, robotics, AI safety, education, sustainability, and accessibility
- builder mindset shown through competitions, research, high-school ventures, community projects, or independent work
- cross-functional potential across technical, product, business, and storytelling roles

## Safety and source policy

- Public pages only. Do not bypass logins, paywalls, robots controls, or access restrictions.
- LinkedIn is an optional discovery source; the agent does not log in or scrape private pages.
- Store public professional/project links, not private contact details.
- The agent drafts research rows only. It does not send outreach.
- Graduation and fit claims must retain a source URL and evidence note.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Required for a live run:

- `OPENAI_API_KEY` — candidate extraction and evidence normalization
- `SERPAPI_API_KEY` — public web search

Optional Google Sheets writeback:

- `GOOGLE_SERVICE_ACCOUNT_JSON` — service-account JSON as one environment variable
- `SEP_SPREADSHEET_ID` — the target spreadsheet ID
- `SEP_SHEET_NAME` — defaults to `Web Prospects`

Share the target Google Sheet with the service-account email as an editor before enabling writeback.

## Run

Preview candidates without changing Google Sheets:

```bash
python -m sep_scout --dry-run --limit 20
```

Append new candidates to the configured sheet:

```bash
python -m sep_scout --write-sheet --limit 20
```

The run writes a local `data/latest_candidates.json` artifact and prints a concise summary. The GitHub Action uses the same command and stores the JSON artifact for review.

## GitHub Actions

The workflow can be started manually or scheduled weekly. Add these repository secrets:

- `OPENAI_API_KEY`
- `SERPAPI_API_KEY`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `SEP_SPREADSHEET_ID`

The action is intentionally review-friendly: it appends only candidates not already present by normalized name and leaves the existing `Sheet1` untouched.
