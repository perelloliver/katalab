from typing import Optional
from pydantic import BaseModel, Field
from typing import Literal

class ProductOrClient(BaseModel):
    name: str
    type: Literal["product", "client"]
    description: Optional[str] = Field("A description of the work done for this client, or a product description.")
    resources: Optional[list[str]] = Field("A list of relevant resources for this client or product, e.g. a URL to a website or github repository.")

class Team(BaseModel):
    name: str = Field("The name of the team")
    products: Optional[list[ProductOrClient]] = Field("The products this team is responsible for")
    clients: Optional[list[ProductOrClient]]
    size: int = Field("The number of people in the team")
    context: Optional[str] = Field("A description of the context of the team, e.g. the company culture, or the team's role in the company. For example, the R&D team is responsible for pushing the company forward with new ideas and technologies.")
    tools_used: Optional[list[str]] = Field("A list of tools used by the team, e.g. a list of programming languages, development tools, frameworks, libraries, hardware, cloud services, etc.")
    philosophy: Optional[list[str]] = Field("A list of values and principles that guide the team's work, e.g. agile development, test driven, no vibe coding, trust and safety oriented, review culture, etc.")

class Role(BaseModel):
    title: str = Field(description="The job title")
    stack: list[str]
    requirements: str
    team: Optional[Team] = Field(description="The team this role is situated in.")

class CompanyInfo(BaseModel):
    roles: list[Role]
    teams: list[Team]
    clients: Optional[list[ProductOrClient]]
    products: Optional[list[ProductOrClient]]
    philosophy: str = Field(description="The engineering philosophy or mission statement at company level. For example, we are building the future of artificial intelligence in banking using human-centred design.")