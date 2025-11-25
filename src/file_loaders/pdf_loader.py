import PyPDF2
from src.file_loaders.base_loader import BaseFileLoader
import os

class PDFLoader(BaseFileLoader):
    """Load PDF files"""
    
    def load(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n[Page {page_num + 1}]\n{page_text}"
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
        return text


