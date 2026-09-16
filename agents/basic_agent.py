from langchain_ollama import ChatOllama

# Connect to local Llama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# Send question
response = llm.invoke(
    "Explain Artificial Intelligence in simple terms."
)

# Display answer
print(response.content)