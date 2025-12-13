from typing import List, Type, TypeVar, Generic
from google.genai import types
from pydantic import BaseModel
from src.backend.client import google_client

T = TypeVar("T", bound=BaseModel)

class InformationExtractionPipeline(Generic[T]):
    def __init__(self, output_format: Type[T], llm: str = "gemini-3-pro-preview"):
        """
        Initialize the pipeline with Gemini client.
        
        Args:
            output_format: The Pydantic model class to use for structured output.
            model_name: The Gemini model to use.
        """
        self.output_format = output_format
        self.client = google_client
        self.llm = llm

    def process_documents(self, documents: List[str]) -> T:
        """
        Process a list of text documents and extract structured information based on the model.
        
        Args:
            documents: A list of strings, where each string is the content of a document.
            
        Returns:
            T: The extracted structured data.
        """
        
        # Combine documents into a single context.
        combined_text = "\n\n--- DOCUMENT SEPARATOR ---\n\n".join(documents)
        
        prompt = f"""
        You are an expert information extraction system.
        Your task is to analyze the provided text documents and extract information to populate the {self.output_format.__name__} schema.
        
        Extract all relevant details.
        Ensure that the output strictly adheres to the provided JSON schema.
        If a field is optional and information is not found, omit it or set it to null/empty as appropriate for the type.
        """
        
        response = self.client.models.generate_content(
            model=self.llm,
            contents=[prompt, combined_text],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=self.output_format,
            ),
        )
        
        if not response.parsed:
             raise ValueError(f"Failed to parse the response into the {self.output_format.__name__} model.")
             
        return response.parsed
