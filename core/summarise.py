from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda , RunnablePassthrough

import os

def getllm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

def split_transcript(transcript: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(transcript)


def summarise(transcript: str) -> str:
    llm = getllm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarises video transcripts."),
        ("human", "Summarise the following transcript:\n{transcript}")
    ])
    map_chain = prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)
    chunk_summaries = [map_chain.invoke({"transcript": chunk}) for chunk in chunks]
    combined_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a expert  assistant that combines partial summaries into a concise summary."),
        ("human" , "{text}")])
    
    combined_chain = combined_prompt | llm | StrOutputParser()

    return combined_chain.invoke({"text": "\n\n".join(chunk_summaries)})

def generate_title(transcript: str) -> str:
    llm = getllm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative assistant that generates video titles."),
        ("human", "Generate a catchy title for a video with the following transcript:\n{transcript}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"transcript": transcript})
    
