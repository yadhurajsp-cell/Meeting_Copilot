from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda , RunnablePassthrough
import os
from core.vectordb import load_vectorstore, get_retriever , create_vectorstore

def getllm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

def formatdocs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_rag(transcript: str):
    vectorstore = create_vectorstore(transcript)
    retriever = get_retriever(vectorstore)
    llm = getllm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions based on video transcripts.context is provided as {context}."),
        ("human", "Answer the following Question:\n{question}")
    ])
    rag_chain = (
        {
            "context": retriever | RunnableLambda(formatdocs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def load_rag():
    vectorstore = load_vectorstore()
    retriever = get_retriever(vectorstore)
    llm = getllm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions based on video transcripts.context is provided as {context}."),
        ("human", "Answer the following Question:\n{question}")
    ])
    rag_chain = (
        {
            "context": retriever | RunnableLambda(formatdocs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def ask_question(rag_chain, question: str) -> str:
    print(f"Asking question: {question}")
    return rag_chain.invoke(question)

    



