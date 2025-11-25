from typing import List, Dict

class TextChunker:
    """Chunk text into smaller pieces for embedding"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split text into overlapping chunks"""
        if not text or not text.strip():
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunk = {
                "text": chunk_text,
                "metadata": metadata or {},
                "start_index": start,
                "end_index": end
            }
            chunks.append(chunk)
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks


