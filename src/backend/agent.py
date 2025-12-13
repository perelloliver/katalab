from src.backend.google_client import google_client
from src.backend.models import RoleInformation, Plan, Repo, TaskImplementation
from google.genai import types


class KataAgent:
    def __init__(self, model_name: str = "gemini-3-pro-preview", n_tasks: int = 3, role_information: RoleInformation | None = None):
        self.client = google_client
        self.model_name = model_name
        self.n_tasks = n_tasks
        self.role_information = role_information
        self.latest_plan: Plan | None = None

    def plan(self, feedback: str | None = None) -> Plan:
        prompt = f"""
        You are a senior software engineer, technical interviewer and technical trainer.
        You are designing a coding kata of length {self.n_tasks} tasks, tailored to the role information below.
        Your plan will be passed to the engineering team.
        Consider the most salient elements of the role that a new engineer would need to know in order to make their first successful contributions.
        The engineering team will give you feedback, take this on board with each iteration.

        Key contextual information about the role:
        {role_information.model_dump_json(indent=2)}

        Feedback from previous iteration (if any):
        {feedback or "None"}

        IMPORTANT: The output must contain exactly {self.n_tasks} tasks. No more, no less.

        Output a structured KataPlan.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Plan
            )
        )

        if response.parsed:
            self.latest_plan = response.parsed
            return response.parsed
        else:
            raise ValueError(f"Failed to parse response: {response}")
        
    def create_repo(self) -> Repo:
        if not self.latest_plan:
            self.latest_plan = self.plan()
        
        # functionize create_task - run an LLM call to create a task implementation
        # run this async for each task in self.latest_plan
        # generate a readme and compile these into a Repo