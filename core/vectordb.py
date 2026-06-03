import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "video_transcripts"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_embedding():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_vectorstore(transcript: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(transcript)

    documents = [Document(page_content=chunk) for chunk in chunks]

    embedding = get_embedding()
    vectorstore = Chroma.from_documents(documents, embedding, collection_name=COLLECTION_NAME, persist_directory=CHROMA_DIR)
    return vectorstore

def load_vectorstore():
    embedding = get_embedding()
    vectorstore = Chroma(collection_name=COLLECTION_NAME, embedding_function=embedding, persist_directory=CHROMA_DIR)
    return vectorstore


def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5}, fetch_k=10)
