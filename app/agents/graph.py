from langgraph.graph import StateGraph, END
from app.agents.state import OutreachState
from app.agents.nodes.score_fit import score_fit_node

graph = StateGraph(OutreachState)
graph.add_node("score_fit", score_fit_node)
graph.set_entry_point("score_fit")
graph.add_edge("score_fit", END)

app_graph = graph.compile()