from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "drone_safety_manual.txt"
)

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

sections = [
    section.strip()
    for section in text.split("\n\n")
    if section.strip()
]

documents = [
    Document(
        page_content=section,
        metadata={"source": "drone_safety_manual.txt"}
    )
    for section in sections
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "chroma_db"
    ),
    embedding_function=embeddings
)

vectorstore.add_documents(documents)

print("Drone Safety Manual added to RAG successfully!")
print("Sections added:", len(documents))