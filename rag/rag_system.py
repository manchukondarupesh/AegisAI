from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama


# 1. Load document
loader = TextLoader("data/company_info.txt")
documents = loader.load()

print("Document loaded successfully.")


# 2. Split document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embeddings created.")


# 4. Create vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("Vector database created.")


# 5. Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# 6. Local LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# 7. Ask a question
question = "What is the role of the RAG Agent?"


# 8. Retrieve relevant documents
results = retriever.invoke(question)


# 9. Combine retrieved information
context = "\n\n".join(
    document.page_content
    for document in results
)


# 10. Send context to Llama
prompt = f"""
Answer the question using only the information provided below.

Context:
{context}

Question:
{question}

Give a clear and simple answer.
"""

response = llm.invoke(prompt)


# 11. Display final answer
print("\nQuestion:")
print(question)

print("\nFinal Answer:")
print(response.content)