from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import calculator
from rag_tool import search_company_documents


# Local LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# Create agent with two tools
agent = create_agent(
    model=llm,
    tools=[
        calculator,
        search_company_documents
    ],
    system_prompt="""
You are AegisAI, an intelligent assistant.

You have two tools:

1. Calculator - use it for mathematical calculations.
2. RAG Search - use it when the user asks about information
contained in company documents.

Choose the appropriate tool when necessary.
"""
)


# Test question
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the role of the RAG Agent?"
            }
        ]
    }
)


# Display final answer
print("\nFinal Answer:")
print(response["messages"][-1].content)