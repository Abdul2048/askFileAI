import pandas as pd
from src.file_loaders.base_loader import BaseFileLoader
import os

class CSVLoader(BaseFileLoader):
    """Load CSV files"""
    
    def load(self, file_path: str) -> str:
        try:
            df = pd.read_csv(file_path)
            text = f"CSV File: {os.path.basename(file_path)}\n\n"
            text += f"Columns: {', '.join(df.columns.tolist())}\n\n"
            text += f"Row count: {len(df)}\n\n"
            text += "Data preview:\n"
            text += df.to_string(index=False)
            return text
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")


