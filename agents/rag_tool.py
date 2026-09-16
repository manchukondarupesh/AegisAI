from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
import os

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load ChromaDB
vectorstore = Chroma(
    persist_directory=os.path.join(BASE_DIR, "chroma_db"),
    embedding_function=embeddings
)

# Retrieve relevant documents
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# Local Llama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


@tool
def search_company_documents(question: str) -> str:
    """Search AegisAI company and drone safety documents."""

    documents = retriever.invoke(question)

    if not documents:
        return "No relevant information found."

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are the AegisAI Drone Safety Assistant.

Answer the user's question using ONLY the information
provided in the retrieved documents.

Do not invent information.

Retrieved documents:
{context}

User question:
{question}

Give a clear and concise answer in simple language.
"""

    response = llm.invoke(prompt)

    return response.content