import os
import argparse
from dotenv import load_dotenv
from src.backend.summariser.pipeline import InformationExtractionPipeline
from src.backend.models import CompanyInfo
from src.backend.summariser.utils import read_documents_from_directory

def main():
    load_dotenv()
    print("Initializing Gemini Pipeline...")
    
    # Check for API Key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        print("Please set it with: export GOOGLE_API_KEY='your_api_key'")
        return

    parser = argparse.ArgumentParser(description="Run Information Extraction Pipeline")
    parser.add_argument("directory", nargs="?", default="case-study/company", help="Directory containing documents to process")
    args = parser.parse_args()

    pipeline = InformationExtractionPipeline(output_format=CompanyInfo)
    
    print(f"Reading documents from {args.directory}...")
    documents = read_documents_from_directory(args.directory)
    
    if not documents:
        print("No documents found to process.")
        return

    print(f"Found {len(documents)} documents. Processing...")
    
    try:
        result = pipeline.process_documents(documents)
        print("\n--- Extracted Information ---\n")
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
