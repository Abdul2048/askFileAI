
from docx import Document
from src.file_loaders.base_loader import BaseFileLoader
import os

class DOCXLoader(BaseFileLoader):
    """Load Word documents"""
    
    def load(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error loading DOCX: {str(e)}")


