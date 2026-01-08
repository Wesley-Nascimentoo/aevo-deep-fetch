import os
import logging

# Configure basic logging if not already configured globally
logger = logging.getLogger(__name__)

class FileService:
    """
    Service responsible for file system operations like deletion and verification.
    """

    def delete_file(self, file_path: str) -> bool:
        """
        Deletes a file from the filesystem if it exists.
        
        Args:
            file_path (str): The absolute or relative path to the file.
            
        Returns:
            bool: True if deleted or didn't exist, False if error occurred.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[FileService] File deleted: {file_path}")
                return True
            else:
                print(f"[FileService] File not found (nothing to delete): {file_path}")
                return True
        except Exception as e:
            print(f"[FileService] Error deleting file {file_path}: {e}")
            return False

file_service = FileService()