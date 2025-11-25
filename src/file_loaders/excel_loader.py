from src.file_loaders.base_loader import BaseFileLoader
import os
import pandas as pd
class ExcelLoader(BaseFileLoader):
    """Load Excel files"""
    
    def load(self, file_path: str) -> str:
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            text = f"Excel File: {os.path.basename(file_path)}\n\n"
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text += f"\n--- Sheet: {sheet_name} ---\n"
                text += f"Columns: {', '.join(df.columns.tolist())}\n"
                text += f"Row count: {len(df)}\n\n"
                text += df.to_string(index=False)
                text += "\n\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error loading Excel: {str(e)}")


