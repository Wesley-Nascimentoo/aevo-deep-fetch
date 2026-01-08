import pandas as pd
from typing import List, Dict, Any
import os
from datetime import datetime

class ExcelService:
    """
    Service responsible for generating Excel (.xlsx) files from data lists.
    """

    def create_excel_from_list(self, data: List[Dict[str, Any]], filename_prefix: str = "report") -> str:
        """
        Generates an Excel file from a list of dictionaries.
        
        Args:
            data (List[Dict]): List of data to be written. Keys become headers.
            filename_prefix (str): Prefix for the filename.
            
        Returns:
            str: The path to the generated file.
        """
        if not data:
            print("[ExcelService] Warning: No data provided to generate Excel.")
            return ""

        try:
            # 1. Create DataFrame
            df = pd.DataFrame(data)

            # 2. Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Ensure 'output' directory exists (optional, keeping it simple in root or specific folder)
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            file_path = f"{output_dir}/{filename_prefix}_{timestamp}.xlsx"

            # 3. Save to Excel
            # index=False removes the generic row numbers (0, 1, 2...)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            print(f"[ExcelService] Excel file created successfully: {file_path}")
            return file_path

        except Exception as e:
            print(f"[ExcelService] Failed to create Excel: {e}")
            raise e

excel_service = ExcelService()