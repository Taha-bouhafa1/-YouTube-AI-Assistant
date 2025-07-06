from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import OpenAI
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
embeddings=OpenAIEmbeddings()

def create_vect_db_from_ytb_url(video_url) -> FAISS:
    loader=YoutubeLoader.from_youtube_url(video_url,
    add_video_info=False,
    transcript_format=TranscriptFormat.TEXT
                                          )

    docs=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    docs=text_splitter.split_documents(docs)

    db=FAISS.from_documents(docs,embeddings)

    return db

def response_from_query(db,question,k=4):
    docs=db.similarity_search(question,k=k)
    docs_page_content=" ".join([d.page_content for d in docs])

    llm=OpenAI(temperature=0)
    prompt=PromptTemplate(input_variable=["question",docs],
                          template ="""
    You are an intelligent and helpful assistant specialized in answering questions about YouTube videos.
    
    Use only the transcript provided below to answer the question. If the answer is not in the transcript, respond with "I don't know."
    
    Transcript:
    {docs}
    
    Question:
    {question}
    
    Answer with clear, detailed, and factual information based strictly on the transcript.

    """
    )
    chain=LLMChain(llm=llm,prompt=prompt)
    response=chain.run(question=question,docs=docs_page_content)

    return response