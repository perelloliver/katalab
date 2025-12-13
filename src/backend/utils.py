import os
import logging
import sys

def get_logger(name: str = "katalab", level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: The name of the logger (typically __name__)
        level: The logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: The configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handler if it hasn't been added already
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        # Format: Time | Level | Path:Line - Message
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Prevent propagation to avoid duplicate logs if root logger is configured
        logger.propagate = False

    return logger

def read_documents_from_directory(directory_path: str) -> list[str]:
    """
    Reads all file contents from a directory and returns them as a list of strings.
    
    Args:
        directory_path: Path to the directory containing documents.
        
    Returns:
        List[str]: list of document contents.
    """
    documents = []
    if not os.path.exists(directory_path):
        logger.warning(f"Directory {directory_path} does not exist.")
        return documents

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    documents.append(f.read())
            except Exception as e:
                logger.warning(f"Skipping file {filename}: {e}")
                
    return documents
