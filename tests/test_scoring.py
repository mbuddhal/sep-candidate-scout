from sep_scout.models import Candidate
from sep_scout.scoring import score_candidate


CONFIG = {
    "minimum_grad_year": 2029,
    "high_impact_niches": ["robotics", "climate"],
}


def test_later_class_and_builder_signals_score_high():
    candidate = Candidate(
        name="Example",
        grad_signal="2026-2030",
        public_signal="built a robotics prototype and organized a pitch event",
        roles=["Builder", "Operator"],
    )
    scored = score_candidate(candidate, CONFIG)
    assert scored.cutoff_status == "Qualifies — class of 2030"
    assert scored.score >= 70


def test_unknown_grad_year_needs_verification():
    candidate = Candidate(name="Unknown", public_signal="member of a club")
    scored = score_candidate(candidate, CONFIG)
    assert scored.cutoff_status == "Needs verification"
