import ollama
from typing import List

class OllamaEmbeddings:
    """Generate embeddings using Ollama"""
    
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.client = ollama.Client()
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response['embedding']
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        return [self.embed_text(text) for text in texts]


