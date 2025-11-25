import os
from src.file_loaders.pdf_loader import PDFLoader
from src.file_loaders.docx_loader import DOCXLoader
from src.file_loaders.text_loader import TextLoader
from src.file_loaders.csv_loader import CSVLoader
from src.file_loaders.excel_loader import ExcelLoader
from src.file_loaders.image_loader import ImageLoader
from src.file_loaders.base_loader import BaseFileLoader
import os
from src.file_loaders.base_loader import BaseFileLoader
import os

class FileLoaderFactory:
    """Factory to get appropriate file loader based on extension"""
    
    LOADERS = {
        '.pdf': PDFLoader,
        '.docx': DOCXLoader,
        '.doc': DOCXLoader,
        '.txt': TextLoader,
        '.md': TextLoader,
        '.csv': CSVLoader,
        '.xlsx': ExcelLoader,
        '.xls': ExcelLoader,
        '.py': TextLoader,
        '.cpp': TextLoader,
        '.java': TextLoader,
        '.js': TextLoader,
        '.html': TextLoader,
        '.css': TextLoader,
        '.json': TextLoader,
        '.xml': TextLoader,
        '.png': ImageLoader,
        '.jpg': ImageLoader,
        '.jpeg': ImageLoader,
        '.bmp': ImageLoader,
    }
    
    @classmethod
    def get_loader(cls, file_path: str) -> BaseFileLoader:
        """Return appropriate loader for file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        loader_class = cls.LOADERS.get(ext)
        
        if loader_class is None:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return loader_class()


