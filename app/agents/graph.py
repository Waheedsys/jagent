from langgraph.graph import StateGraph, END
from app.agents.state import OutreachState
from app.agents.nodes.score_fit import score_fit_node
from app.agents.nodes.find_contact import find_contact_node

def route_after_score(state: OutreachState):
    if state["fit_score"] is not None and state["fit_score"] > 0.7:
        return "good"
    return "bad"

graph = StateGraph(OutreachState)
graph.add_node("find_contact", find_contact_node)
graph.add_node("score_fit", score_fit_node)
graph.set_entry_point("score_fit")
graph.add_conditional_edges(
   "score_fit",
    route_after_score,
    {
        "good": "find_contact",
        "bad": END,
    },
)
graph.add_edge("find_contact", END)

app_graph = graph.compile()