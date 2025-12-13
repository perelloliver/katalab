from typing import Optional
from pydantic import BaseModel, Field
from typing import Literal

class ProductOrClient(BaseModel):
    name: str
    type: Literal["product", "client"]
    description: Optional[str] = Field(description="A description of the work done for this client, or a product description.")
    resources: Optional[list[str]] = Field(description="A list of relevant resources for this client or product, e.g. a URL to a website or github repository.")

class Team(BaseModel):
    name: str = Field(description="The name of the team")
    products: Optional[list[ProductOrClient]] = Field(default=None, description="The products this team is responsible for")
    clients: Optional[list[ProductOrClient]] = None
    size: int = Field(description="The number of people in the team")
    context: Optional[str] = Field(description="A description of the context of the team, e.g. the company culture, or the team's role in the company. For example, the R&D team is responsible for pushing the company forward with new ideas and technologies.")
    tools_used: Optional[list[str]] = Field(description="A list of tools used by the team, e.g. a list of programming languages, development tools, frameworks, libraries, hardware, cloud services, etc.")
    philosophy: Optional[list[str]] = Field(description="A list of values and principles that guide the team's work, e.g. agile development, test driven, no vibe coding, trust and safety oriented, review culture, etc.")

class Role(BaseModel):
    title: str = Field(description="The job title")
    stack: list[str] = Field(max_length=10, description="List of technologies in the tech stack")
    requirements: str
    team: Optional[Team] = Field(default=None, description="The team this role is situated in.")

class CompanyInfo(BaseModel):
    roles: list[Role]
    teams: list[Team]
    clients: Optional[list[ProductOrClient]] = None
    products: Optional[list[ProductOrClient]] = None
    philosophy: str = Field(description="The engineering philosophy or mission statement at company level. For example, we are building the future of artificial intelligence in banking using human-centred design.")

class EmployeeInfo(BaseModel):
	name: str
	stack: list[str]
	experience_yrs: int
	level: Literal["junior", "mid", "senior"]
	likely_learning_style: str

class Plan(BaseModel):
    id: str = Field(description="Unique identifier for the task, snake_case")
    name: str = Field(description="Human readable name of the task")
    description: str = Field(description="Detailed description of the task")
    files: list[str] = Field(description="List of files that will be created for this task")

class KataPlan(BaseModel):
    title: str = Field(description="Title of the Kata Repository")
    description: str = Field(description="Overview of what this Kata aims to teach/assess")
    tasks: list[Plan]

class FileContent(BaseModel):
    filename: str = Field(description="Name of the file, e.g. main.py")
    content: str = Field(description="Content of the file")

class TaskImplementation(BaseModel):
    files: list[FileContent]