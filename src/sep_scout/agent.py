from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI

from .models import Candidate
from .scoring import score_candidate


EXTRACTION_PROMPT = """
You are the SEP Candidate Scout for Sigma Eta Pi at Cal Poly SLO.
Extract only candidates and evidence present in the supplied public search results.
Do not infer protected traits or private contact details. Do not invent graduation years.
A class-of-2029 or later signal qualifies; otherwise use Needs verification.
Look for future-entrepreneur signals including builders, operators, domain experts,
connectors/storytellers, high-impact niches, and early work from high school or community projects.
Return JSON with a top-level `candidates` array. Each item must contain:
name, grad_signal, major_area, public_signal, fit_angle, cutoff_status,
source_type, source_url, roles, evidence.
"""


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def extract_candidates(results: list[dict[str, str]], config: dict[str, Any]) -> list[Candidate]:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for candidate extraction")
    client = OpenAI(api_key=key)
    payload = json.dumps({"school": config["school"], "results": results}, ensure_ascii=False)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": payload},
        ],
    )
    data = json.loads(response.choices[0].message.content or "{}")
    candidates: list[Candidate] = []
    for raw in data.get("candidates", []):
        candidate = Candidate(
            name=str(raw.get("name", "")).strip(),
            grad_signal=str(raw.get("grad_signal", "")).strip(),
            major_area=str(raw.get("major_area", "")).strip(),
            public_signal=str(raw.get("public_signal", "")).strip(),
            fit_angle=str(raw.get("fit_angle", "")).strip(),
            cutoff_status=str(raw.get("cutoff_status", "Needs verification")).strip(),
            source_type=str(raw.get("source_type", "Public web")).strip(),
            source_url=str(raw.get("source_url", "")).strip(),
            roles=[str(x) for x in raw.get("roles", [])],
            evidence=[str(x) for x in raw.get("evidence", [])],
        )
        if candidate.name:
            candidates.append(score_candidate(candidate, config))
    return dedupe_candidates(candidates)


def dedupe_candidates(candidates: list[Candidate]) -> list[Candidate]:
    merged: dict[str, Candidate] = {}
    for candidate in candidates:
        key = _normalize(candidate.name)
        current = merged.get(key)
        if not current or candidate.score > current.score:
            merged[key] = candidate
    return sorted(merged.values(), key=lambda x: (-x.score, x.name.lower()))
