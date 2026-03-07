from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables import RunnablePassthrough
import config
import os

def get_vectorstore():
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    return Chroma(
        collection_name='documents',
        embedding_function=embeddings,
        persist_directory=config.VECTORSTORE_PATH
    )

def index_document(file_path):
    fileName = os.path.basename(file_path)
    vectorstore = get_vectorstore()
    fileExists = vectorstore.get(where={"source":file_path})
    if fileExists['ids']:
        print(f"Document {file_path} already indexed")
        return
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    vectorstore.add_documents(chunks, ids=[f"{fileName}_{i}" for i in range(len(chunks))])

def query(command):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={'k':config.NO_OF_CHUNKS})
    context_formatter = lambda docs: "\n\n".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant. Answer based only on the provided context. If the answer is not in the context, say you don't know."),
                    ("human", "Context: {context}\n\nQuestion: {question}")
                ])
    llm = ChatOllama(model=config.LLM_MODEL)
    chain = {
            "context": retriever | context_formatter,
            "question": RunnablePassthrough()
        } | prompt | llm
    response = chain.invoke(command)
    return response.content
