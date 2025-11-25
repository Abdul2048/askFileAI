from abc import ABC, abstractmethod
from typing import List, Dict
import os

class BaseFileLoader(ABC):
    """Abstract base class for file loaders"""
    
    @abstractmethod
    def load(self, file_path: str) -> str:
        """Load and return text content from file"""
        pass
    
    def get_metadata(self, file_path: str) -> Dict:
        """Return metadata about the file"""
        return {
            "source": file_path,
            "file_name": os.path.basename(file_path)
        }


