from src.file_loaders.base_loader import BaseFileLoader
import os

class TextLoader(BaseFileLoader):
    """Load plain text files"""
    
    def load(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error loading text file: {str(e)}")


