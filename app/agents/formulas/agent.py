from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from agents.formulas.state import AgentState
from agents.formulas.formulas_agent import start_agent, generate_formula, organiza_atributos
from agents.formulas.tools import tools

# Define a new graph
workflow = StateGraph(AgentState)

workflow.add_node("start", start_agent)
retrieve = ToolNode(tools)
workflow.add_node("tools", retrieve)
workflow.add_node("organiza", organiza_atributos)
workflow.add_node("generate", generate_formula)
workflow.set_entry_point("start")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "start",
    # Assess agent decision
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "tools",
        END: END,
    },
)

workflow.add_edge("start", END)
workflow.add_edge("tools", "organiza")
workflow.add_edge("organiza", "generate")
workflow.add_edge("generate", END)

# Compile
graph = workflow.compile()

print(graph.get_graph().print_ascii())
