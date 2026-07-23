from langgraph.graph import StateGraph, END
from app.agents.state import OutreachState
from app.agents.nodes.score_fit.score_fit import make_score_fit_node
from app.agents.nodes.find_contact import find_contact_node
from app.agents.nodes.draft_email import draft_email_node
import logging
logger = logging.getLogger("gateway.agent")

graph = StateGraph(OutreachState)

def route_after_score(state: OutreachState) -> str:
    fit = state.get("fit_evaluation")
    if fit is not None and fit.recommend_apply:
        return "good"
    return "bad"

def log_and_skip_node(state: dict) -> dict:
       logger.info(f"Skipping low-fit role: {state.get('fit_evaluation')}")
       return {}

graph.add_node("log_and_skip", log_and_skip_node)
graph.add_edge("log_and_skip", END)

graph.add_conditional_edges(
       "score_fit",
       route_after_score,
       {"good": "find_contact", "bad": "log_and_skip"},
   )


graph.add_node("find_contact", find_contact_node)
graph.add_node("draft_email", draft_email_node)
graph.add_node("score_fit", make_score_fit_node())
graph.set_entry_point("score_fit")
graph.add_conditional_edges(
            "score_fit",
            lambda state: "tailor_cv" if state["fit_evaluation"].recommend_apply else "log_and_skip",
        )
graph.add_edge("find_contact", "draft_email")
graph.add_edge("draft_email", END)

app_graph = graph.compile()