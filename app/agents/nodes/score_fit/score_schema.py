from __future__ import annotations

"""
A-F fit scoring for jagent, ported from career-ops' evaluation approach.
 
Design notes (from career-ops):
- 10 weighted dimensions instead of one scalar fit score.
- role_match and skills_alignment are GATE-PASS dimensions: if either falls
  below the gate threshold, the overall score is capped low regardless of
  how well the other 8 dimensions score. This mirrors "don't apply to
  roles you're clearly not a fit for, even if the comp/culture look great."
- Weighted sum is computed in code, not by the LLM — LLMs are unreliable
  at arithmetic; let the model reason per-dimension and let Python do the math.
- overall < 4.0 -> recommend against applying (career-ops' own threshold).
  Wire this into your graph as a conditional edge so low-fit roles skip
  CV tailoring / contact discovery and just get logged.
 
Drop this file into your jagent package (e.g. jagent/nodes/scoring.py) and
wire `score_fit_node` into your graph where the old scalar-score node was.
"""
 
from typing import Literal
 
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
 
# ---------------------------------------------------------------------------
# 1. Schema
# ---------------------------------------------------------------------------
 
GATE_THRESHOLD = 2.5  # dimension score (1-5) below this fails the gate
RECOMMEND_THRESHOLD = 4.0  # overall score below this -> don't apply
 
 
class DimensionScore(BaseModel):
    score: float = Field(ge=1.0, le=5.0, description="1.0-5.0 rating for this dimension")
    reasoning: str = Field(description="1-2 sentence justification")
 
 
class FitEvaluation(BaseModel):
    # Gate-pass dimensions — checked first, cap the score if either fails
    role_match: DimensionScore
    skills_alignment: DimensionScore
 
    # Remaining 8 weighted dimensions
    seniority_fit: DimensionScore
    comp_alignment: DimensionScore
    location_remote_fit: DimensionScore
    company_stability: DimensionScore
    growth_trajectory: DimensionScore
    culture_signals: DimensionScore
    tech_stack_match: DimensionScore
    mission_alignment: DimensionScore
 
    gaps: list[str] = Field(description="Concrete skill/experience gaps vs the JD")
    summary: str = Field(description="2-3 sentence overall read on this role")
 
    # Filled in by compute_overall(), not the LLM
    gate_passed: bool = Field(default=True)
    overall: float = Field(default=0.0)
    grade: Literal["A", "B", "C", "D", "F"] = Field(default="F")
    recommend_apply: bool = Field(default=False)
 
 
# Weights for the 8 non-gate dimensions. Gate dimensions are pass/fail,
# not part of the weighted sum, once they've passed the gate.
WEIGHTS = {
    "seniority_fit": 0.15,
    "comp_alignment": 0.15,
    "location_remote_fit": 0.10,
    "company_stability": 0.10,
    "growth_trajectory": 0.15,
    "culture_signals": 0.10,
    "tech_stack_match": 0.15,
    "mission_alignment": 0.10,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9
 
 
def compute_overall(ev: FitEvaluation) -> FitEvaluation:
    """Apply gate logic and compute the weighted score + letter grade in code."""
    gate_passed = (
        ev.role_match.score >= GATE_THRESHOLD
        and ev.skills_alignment.score >= GATE_THRESHOLD
    )
 
    weighted = sum(
        getattr(ev, dim).score * weight for dim, weight in WEIGHTS.items()
    )
 
    if not gate_passed:
        # Cap hard: a role/skills mismatch caps the score even if everything
        # else about the job looks great.
        overall = min(weighted, 2.4)
    else:
        overall = weighted
 
    ev.gate_passed = gate_passed
    ev.overall = round(overall, 2)
    ev.grade = _grade(ev.overall)
    ev.recommend_apply = ev.overall >= RECOMMEND_THRESHOLD
    return ev
 
 
def _grade(score: float) -> Literal["A", "B", "C", "D", "F"]:
    if score >= 4.5:
        return "A"
    if score >= 4.0:
        return "B"
    if score >= 3.0:
        return "C"
    if score >= 2.0:
        return "D"
    return "F"
