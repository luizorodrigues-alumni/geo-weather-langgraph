from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph.state import RunnableConfig
from graph import build_graph
import threading
from prompts import SYSTEM_PROMPT


def main() -> None:
    # Config from RunnableConfig
    config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

    # Build the graph
    graph = build_graph()

    # Initial message
    system_message = SystemMessage(SYSTEM_PROMPT)
    initial_human_message = HumanMessage("Ola!")
    result = graph.invoke({"messages": [system_message, initial_human_message]}, config=config)

    print("\n--- GEO-WEATHER ---\n")
    print("Bem-vindo ao assistente de clima e localização! (Digite 'q', 'quit', 'exit' para sair)")
    while True:
        user_input = input("Pergunte sobre uma uma localização ou a temperatura de um local: ")
        if user_input.lower() in ['q', 'quit', 'exit', '/q']:
            print("Bye 👋")
            break
        result = graph.invoke({"messages": [HumanMessage(user_input)]}, config=config)

        print("\n--- AI ---\n")
        print(result["messages"][-1].content)

    # Formating result['messages'] for better readability and learning
    print("\n\n--- Full Conversation ---")
    for i, message in enumerate(result["messages"]):
        print(f"\n--- Message {i+1} ---")
        print(f"Type: {type(message).__name__}")
        print(f"Content: {message.content}")
        if hasattr(message, "tool_calls"):
            print(f"Tool Calls: {message.tool_calls}")


if __name__ == "__main__":
    main()