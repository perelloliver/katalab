from pydantic import BaseModel, Field

class Technology(BaseModel):
    name: str = Field(description="Name of the technology")
    internal_usage_preferences: str | None = Field(description="Preferences for use - i.e we use Rust but only for backend optimisations, uv and poetry are allowed but uv preferred. If no specific usage preferences are given, leave blank.")
    use_cases: list[str] | None = Field(description="Use cases for the technology - i.e we use Weaviate for vector databases for RAG applications")

class Stack(BaseModel):
    languages: list[Technology] | None = Field(description="Programming languages used e.g Rust, Go, Python, etc.")
    package_managers: list[Technology] | None = Field(description="Package managers used i.e uv, npm, pip, conda")
    libraries: list[Technology] | None = Field(description="Libraries used i.e React, PyTorch, etc.")
    frameworks: list[Technology] | None = Field(description="Frameworks used i.e Django, Flask, etc.")
    agent_frameworks: list[Technology] | None = Field(description="Agent frameworks used i.e LangChain, PydanticAI, etc.")
    cloud: list[Technology] | None = Field(description="Cloud providers used i.e AWS, GCP, Azure, etc.")
    devops: list[Technology] | None = Field(description="Devops tools used i.e Docker, Kubernetes, etc.")
    monitoring: list[Technology] | None = Field(description="Monitoring tools used i.e Prometheus, Grafana, etc.")
    databases: list[Technology] | None = Field(description="Databases used i.e PostgreSQL, MongoDB, Weaviate, etc.")
    storage: list[Technology] | None = Field(description="Storage solutions used i.e S3.")
    containerisation: list[Technology] | None = Field(description="Containerisation solutions used i.e Docker, Kubernetes, etc.")
    machine_learning: list[Technology] | None = Field(description="Machine learning models used e.g XGBoost, ARIMA, etc.")
    llms: list[Technology] | None = Field(description="LLMs used i.e OpenAI, Anthropic, etc.")

class RoleInformation(BaseModel):
    title: str = Field(description="Title of the role")
    stack: Stack = Field(description="Stack of technologies used")
    industry: str = Field(description="Industry the role is in, for example 'Biotechnology'")
    dev_philosophy: str = Field(description="Development philosophy, for example 'We use a modern, agile development approach with regular code reviews and pair programming.'")
    extra_preferences: str = Field(description="Additional development preferences, for example 'We use jinja templates for prompting.'")