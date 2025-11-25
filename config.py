import os
from pathlib import Path

class Config:
    """Configuration settings for AskFileAI"""
    
    OLLAMA_BASE_URL = "http://localhost:11434"
    LLM_MODEL = "qwen2.5:7b"  # Change to your installed model
    EMBEDDING_MODEL = "nomic-embed-text"
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    CHROMA_DB_DIR = "./data/chroma_db"
    COLLECTION_NAME = "file_documents"
    
    TOP_K_RESULTS = 4
    
    Path(CHROMA_DB_DIR).mkdir(parents=True, exist_ok=True)


