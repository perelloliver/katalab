import os
from typing import List
from google import genai
from google.genai import types
from src.models import CompanyInfo

class InformationExtractionPipeline:
    def __init__(self, api_key: str | None = None, model_name: str = "gemini-3-pro-preview"):
        """
        Initialize the pipeline with Gemini client.
        
        Args:
            api_key: The Google Cloud API key. If None, it will be read from GOOGLE_API_KEY env var.
            model_name: The Gemini model to use.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be provided or set in the environment.")
            
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def process_documents(self, documents: List[str]) -> CompanyInfo:
        """
        Process a list of text documents and extract structured company information.
        
        Args:
            documents: A list of strings, where each string is the content of a document.
            
        Returns:
            CompanyInfo: The extracted structured data.
        """
        
        # Combine documents into a single context for now, or we could handle them iteratively.
        # For a "set of documents" usually implies disjointed info that needs aggregation.
        # A large context window allow us to dump them all in.
        
        combined_text = "\n\n--- DOCUMENT SEPARATOR ---\n\n".join(documents)
        
        prompt = """
        You are an expert information extraction system.
        Your task is to analyze the provided text documents and extract information to populate the CompanyInfo schema.
        
        Extract all relevant details about roles, teams, products, clients, and company philosophy.
        Ensure that the output strictly adheres to the provided JSON schema.
        If a field is optional and information is not found, omit it or set it to null/empty as appropriate for the type.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt, combined_text],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CompanyInfo,
            ),
        )
        
        if not response.parsed:
             raise ValueError("Failed to parse the response into the CompanyInfo model.")
             
        return response.parsed
