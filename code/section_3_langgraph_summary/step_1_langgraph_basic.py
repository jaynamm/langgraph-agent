from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END


class State(BaseModel):
    text: str


def node(state: State) -> State:
    return {"text": "반가워!"}


builder = StateGraph(State)
builder.add_node("node", node)
builder.add_edge(START, "node")
builder.add_edge("node", END)

graph = builder.compile()

print(graph.get_graph().draw_mermaid())

answer = graph.invoke({"text": "안녕?"})

print(answer["text"])
