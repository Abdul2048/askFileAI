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


#import pandas as pd
#import chardet
#from src.file_loaders.base_loader import BaseFileLoader
#import os
#
#class CSVLoader(BaseFileLoader):
#    """Load CSV files with encoding auto-detection"""
#
#    def load(self, file_path: str) -> str:
#        try:
#            # ---- 1. Detect encoding ----
#            with open(file_path, "rb") as f:
#                rawdata = f.read()
#                result = chardet.detect(rawdata)
#                encoding = result["encoding"] or "utf-8"
#
#            # ---- 2. Load CSV with detected encoding ----
#            df = pd.read_csv(file_path, encoding=encoding, engine="python")
#
#            # ---- 3. Build readable text output ----
#            text = f"CSV File: {os.path.basename(file_path)}\n\n"
#            text += f"Detected Encoding: {encoding}\n\n"
#            text += f"Columns: {', '.join(df.columns.tolist())}\n\n"
#            text += f"Row count: {len(df)}\n\n"
#            text += "Data preview:\n"
#            text += df.to_string(index=False)
#
#            return text
#
#        except Exception as e:
#            raise Exception(f"Error loading CSV: {str(e)}")
#