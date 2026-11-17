from __future__ import annotations

import re

from .models import Candidate


def _year(text: str) -> int | None:
    years = [int(x) for x in re.findall(r"20\d{2}", text)]
    return max(years) if years else None


def score_candidate(candidate: Candidate, config: dict) -> Candidate:
    cutoff = int(config["minimum_grad_year"])
    signal = " ".join([candidate.grad_signal, candidate.public_signal, candidate.fit_angle, *candidate.evidence]).lower()
    grad_year = _year(candidate.grad_signal)
    if grad_year and grad_year >= cutoff:
        candidate.cutoff_status = f"Qualifies — class of {grad_year}"
        score = 25
    else:
        score = 0
        if candidate.cutoff_status == "":
            candidate.cutoff_status = "Needs verification"

    keyword_groups = {
        "build": (20, ["built", "prototype", "shipped", "developed", "project", "software", "hardware"]),
        "founder": (15, ["founder", "startup", "venture", "self-employed", "company"]),
        "operator": (15, ["organized", "recruited", "fundraised", "sponsorship", "president", "lead", "managed", "sales"]),
        "impact": (15, list(map(str.lower, config.get("high_impact_niches", [])))),
        "cross_functional": (10, ["product", "design", "marketing", "pitch", "customer", "community"]),
        "ownership": (15, [
            "founded", "co-founded", "initiated", "started", "launched", "owned",
            "personal contribution", "led development", "ran", "created", "iterated",
            "user feedback", "customer discovery", "validated", "self-directed",
        ]),
    }
    for points, terms in keyword_groups.values():
        if any(term in signal for term in terms):
            score += points
    if candidate.roles:
        score += min(10, 3 * len(candidate.roles))
    candidate.score = min(score, 100)
    return candidate
