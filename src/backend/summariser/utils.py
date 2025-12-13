import os
from typing import List

def read_documents_from_directory(directory_path: str) -> List[str]:
    """
    Reads all file contents from a directory and returns them as a list of strings.
    
    Args:
        directory_path: Path to the directory containing documents.
        
    Returns:
        List[str]: list of document contents.
    """
    documents = []
    if not os.path.exists(directory_path):
        print(f"Warning: Directory {directory_path} does not exist.")
        return documents

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    documents.append(f.read())
            except Exception as e:
                print(f"Skipping file {filename}: {e}")
                
    return documents
