import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# from langchain.agents import create_agent
# from langchain.agents import AgentExecutor
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from shopping_agent.tools.langchain_tools import (
    search_products_tool,
    get_product_details_tool,
    get_product_rating_tool,
    create_order_tool
)

# Load GROQ key
from dotenv import load_dotenv
import os
load_dotenv()

import os
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found")

# Use Groq LLM
llm = ChatGroq(
    model="qwen/qwen3-32b",  
    temperature=0
)

# Tools
tools = [
    search_products_tool,
    get_product_details_tool,
    get_product_rating_tool,
    create_order_tool
]

# Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful shopping assistant."
    )
)

# Helper function to invoke agent
def ask_shopping_agent(message: str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    return result['messages'][-1].content

# Example Usage
if __name__ == "__main__":
    print("""
    Welcome to the Smart Shopping Agent!
    Type 'exit' to quit.
    """)
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Get response from agent
        print("Agent is thinking...")
        response = ask_shopping_agent(user_input)
        
        # Display agent's response
        print("Agent:", response)
        print("-" * 60)