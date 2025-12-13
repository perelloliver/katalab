from src.backend.client import google_client
from src.backend.models import RoleInformation, Plan, KataTask
from google.genai import types

from pydantic import create_model, Field

class KataAgent:
    def __init__(self, model_name: str = "gemini-3-pro-preview", n_tasks: int = 3):
        self.client = google_client
        self.model_name = model_name
        self.n_tasks = n_tasks
        self.latest_plan: Plan | None = None

    def plan(self, role_information: RoleInformation, feedback: str | None = None) -> Plan:
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

        return response.parsed if response.parsed else raise ValueError(f"Failed to parse response: {response}")