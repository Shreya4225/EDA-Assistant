# src/agents/langgraph_workflow.py

from langgraph.graph import StateGraph
from src.agents.response_generator import handle_user_query
from src.agents.chat_memory import ChatMemory

memory = ChatMemory()

class ChatState(dict):
    user_input: str


def chatbot_node(state: ChatState):
    user_text = state["user_input"]

    response_text, chart_path = handle_user_query(user_text)

    memory.add_message("user", user_text)
    memory.add_message("assistant", response_text)

    return {
        "response_text": response_text,
        "chart_path": chart_path
    }

graph = StateGraph(ChatState)
graph.add_node("chat_node", chatbot_node)
graph.set_entry_point("chat_node")
chatbot = graph.compile()
