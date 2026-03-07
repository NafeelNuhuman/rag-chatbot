import os

LLM_MODEL = 'qwen3.5:397b-cloud'
EMBEDDING_MODEL = 'nomic-embed-text'
CHUNK_SIZE = 500 
CHUNK_OVERLAP = 50
NO_OF_CHUNKS = 3
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data')
VECTORSTORE_PATH = os.path.join(BASE_DIR, 'vectorstore')