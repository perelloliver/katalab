from .pipeline import InformationExtractionPipeline
from src.backend.models import CompanyInfo

class Summariser:
    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        self.pipeline = InformationExtractionPipeline(output_format=CompanyInfo, llm=model_name)

    def run(self, documents: list[str]) -> CompanyInfo:
        return self.pipeline.process_documents(documents)
