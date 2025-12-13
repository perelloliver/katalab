from src.models import RoleInformation
from google.genai import types
from src.backend.client import google_client
from src.backend.utils import get_logger

logger = get_logger(__name__)

def summarise_role_information(documents: list[str]):
    logger.info(f"Starting role information summarisation with {len(documents)} documents")
    
    # Combine documents into a single context.
    combined_text = "\n\n---DOCUMENT SEPARATOR---\n\n".join(documents)
    
    prompt = f"""
You are analyzing a collection of documents that describe an engineering role. Your task is to extract comprehensive, structured information about this role.

Please carefully extract the following information:

1. **Role Title**: The official title or designation for this position.

2. **Technology Stack**: Identify all technologies mentioned, categorized by type:
   - Programming languages (e.g., Python, Rust, Go, TypeScript)
   - Package managers (e.g., uv, npm, pip, conda)
   - Libraries and frameworks (e.g., React, PyTorch, Django, Flask)
   - Agent frameworks (e.g., LangChain, PydanticAI, CrewAI)
   - Cloud providers and services (e.g., AWS, GCP, Azure)
   - DevOps tools (e.g., Docker, Kubernetes, CI/CD pipelines)
   - Monitoring and observability tools (e.g., Prometheus, Grafana, DataDog)
   - Databases (e.g., PostgreSQL, MongoDB, Weaviate, Redis)
   - Storage solutions (e.g., S3, Cloud Storage)
   - Containerisation technologies (e.g., Docker, Kubernetes)
   - Machine learning models and frameworks (e.g., XGBoost, scikit-learn, ARIMA)
   - LLMs and AI services (e.g., OpenAI, Anthropic, Gemini)
   
   For each technology, note any specific preferences or use cases mentioned.

3. **Industry**: The industry sector this role operates in (e.g., biotechnology, fintech, e-commerce).

4. **Development Philosophy**: The team's approach to software development, including methodologies, practices, and values (e.g., agile, test-driven development, code review practices).

5. **Additional Preferences**: Any other relevant development preferences, coding standards, or technical approaches mentioned.

Please be thorough but concise. If specific information isn't mentioned in the documents, omit that field rather than guessing.

{combined_text}
    """
    
    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RoleInformation,
        ),
    )
    
    if not response.parsed:
            logger.error(f"Error generating response. Response content: {response}")
            raise ValueError(f"Error generating response. Output: {response}")
            
    logger.info("Successfully extracted role information")
    return response.parsed
