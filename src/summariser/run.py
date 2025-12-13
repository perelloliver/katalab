import os
from dotenv import load_dotenv
from src.summariser.pipeline import InformationExtractionPipeline
from src.models import CompanyInfo

def main():
    load_dotenv()
    print("Initializing Gemini Pipeline...")
    
    # Check for API Key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        print("Please set it with: export GOOGLE_API_KEY='your_api_key'")
        return

    pipeline = InformationExtractionPipeline()
    
    # Example documents
    documents = [
        """
        Katalab is an engineering company focused on building the future of AI in banking.
        Our philosophy is centered around human-centred design and we believe in trust and safety.
        
        We have a Research Team (R&D) that explores new technologies. They use Python and PyTorch.
        The team is small, about 5 people.
        """
        ,
        """
        We also have a Product Team focused on our client 'NeoBank'. 
        They are building a fraud detection system.
        
        Role: Senior Engineer
        Stack: Rust, Python, AWS
        Requirements: 5+ years experience, extensive knowledge of distributed systems.
        Team: Product Team
        """
    ]
    
    print("Processing documents...")
    try:
        result: CompanyInfo = pipeline.process_documents(documents)
        print("\n--- Extracted Information ---\n")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
