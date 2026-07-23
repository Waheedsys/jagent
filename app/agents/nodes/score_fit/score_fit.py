
from app.core.llm_client import get_llm_client
from app.agents.nodes.score_fit.score_prompt import SCORING_PROMPT
from app.agents.nodes.score_fit.score_schema import compute_overall, FitEvaluation
def make_score_fit_node(model_name: str = "claude-sonnet-4-6"):
    """
    Returns a node function `score_fit_node(state) -> dict` for use in your
    StateGraph. Assumes state has `resume: str` and `job_description: str`,
    and writes `fit_evaluation: FitEvaluation` back into state.
 
    Wire it in like:
        graph.add_node("score_fit", make_score_fit_node())
        graph.add_conditional_edges(
            "score_fit",
            lambda state: "tailor_cv" if state["fit_evaluation"].recommend_apply else "log_and_skip",
        )
    """
    llm = get_llm_client("gpt-oss:20b-cloud", "ollama_cloud")
    structured_llm = llm.with_structured_output(FitEvaluation,method="json_mode")
    chain = SCORING_PROMPT | structured_llm
 
    def score_fit_node(state: dict) -> dict:
        raw_eval: FitEvaluation = chain.invoke(
            {
                "resume": state["resume_summary"],
                "job_description": state["job_description"],
            }
        )
        print("BEFORE compute_overall:", raw_eval.overall, raw_eval.grade)
        evaluated = compute_overall(raw_eval)
        print("AFTER compute_overall:", evaluated.overall, evaluated.grade)
        return {"fit_evaluation": evaluated}
 
    return score_fit_node