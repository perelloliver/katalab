from src.backend.client import google_client
from src.backend.models import CompanyInfo, EmployeeInfo, KataPlan, Plan, TaskImplementation
from google.genai import types
import json

from pydantic import create_model, Field

class KataAgent:
    def __init__(self, model_name: str = "gemini-3-pro-preview", n_tasks: int = 3):
        self.client = google_client
        self.model_name = model_name
        self.n_tasks = n_tasks
        self.latest_plan: KataPlan | None = None

    def plan(self, company_data: CompanyInfo, employee_data: EmployeeInfo, feedback: str | None = None) -> KataPlan:
        prompt = f"""
        You are an expert technical interviewer and coding kata designer.
        Design a coding kata (a set of EXACTLY {self.n_tasks} tasks) tailored to the candidate based on:

        Company Context:
        {company_data.model_dump_json(indent=2)}

        Candidate Profile:
        {employee_data.model_dump_json(indent=2)}

        Feedback from previous iteration (if any):
        {feedback or "None"}

        Tailor the kata to match the candidate's:
        - Experience level: {employee_data.level}
        - Years of experience: {employee_data.experience_yrs}
        - Learning style: {employee_data.likely_learning_style}
        - Technical stack: {employee_data.stack}

        The kata should simulate real-world scenarios relevant to the company's product and tech stack,
        while being appropriately challenging for the candidate's level.
        Each task must be a logical step in building a feature or solving a problem.

        IMPORTANT: The output must contain exactly {self.n_tasks} tasks. No more, no less.

        Output a structured KataPlan.
        """

        # Dynamic model to enforce n_tasks
        DynamicKataPlan = create_model(
            'DynamicKataPlan',
            title=(str, Field(description="Title of the Kata Repository")),
            description=(str, Field(description="Overview of what this Kata aims to teach/assess")),
            tasks=(list[Plan], Field(min_length=self.n_tasks, max_length=self.n_tasks, description=f"List of exactly {self.n_tasks} tasks"))
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DynamicKataPlan,
            ),
        )
        
        if not response.parsed:
             raise ValueError("Failed to parse the response into KataPlan.")

        # Convert back to standard KataPlan for type consistency if needed, 
        # but the structure is identical so we can just cast or return
        self.latest_plan = KataPlan(**response.parsed.model_dump())
        return self.latest_plan

    def run(self, company_data: CompanyInfo, employee_data: EmployeeInfo):
        if not self.latest_plan:
            raise ValueError("No plan found. Please run plan() first.")

        # README.md for the root
        root_readme = f"# {self.latest_plan.title}\n\n{self.latest_plan.description}\n\n## Tasks\n\n" + \
                      "\n".join([f"- {task.name}: {task.description}" for task in self.latest_plan.tasks])
        
        yield {"type": "log", "message": "Generated root README.md"}
        yield {"type": "file", "path": "README.md", "content": root_readme}

        for i, task in enumerate(self.latest_plan.tasks):
            yield {"type": "log", "message": f"[{i+1}/{len(self.latest_plan.tasks)}] designing task: {task.name}..."}
            
            # Step 1: Generate README and Task Design
            readme_prompt = f"""
            Design a specific, short coding task for this Kata.

            Task Info:
            Name: {task.name}
            Description: {task.description}
            
            Company Context:
            {company_data.model_dump_json(indent=2)}
            
            Candidate Profile:
            {employee_data.model_dump_json(indent=2)}
            
            Tailor the task explanation and difficulty to the candidate's level ({employee_data.level})
            and learning style ({employee_data.likely_learning_style}).
            
            Output a detailed README.md file content that explains the task to the candidate.
            The task should involve fixing or implementing a specific feature.
            """
            
            try:
                readme_response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[readme_prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="text/plain"
                    )
                )
                
                readme_content = readme_response.text
                folder_name = task.id
                readme_path = f"{folder_name}/README.md"
                yield {"type": "file", "path": readme_path, "content": readme_content}
                
                yield {"type": "log", "message": f"[{i+1}/{len(self.latest_plan.tasks)}] generating code for: {task.name}..."}

                # Step 2: Generate Implementation based on the README
                impl_prompt = f"""
                Based on the following README for a coding task, generate the necessary code files.
                
                README Content:
                {readme_content}
                
                Requirements:
                1. Create a skeleton code file (e.g. `main.py`, `service.js` etc) that contains signatures or incorrect code for the candidate to fix, as described in the README.
                2. Create a `tests/` folder with valid test files (e.g. `tests/test_task.py`) that will verify the correct solution.
                
                Return a JSON object with the list of files (excluding README.md).
                """

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[impl_prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json", 
                        response_schema=TaskImplementation,
                        safety_settings=[
                            types.SafetySetting(
                                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                                threshold="BLOCK_NONE"
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_HATE_SPEECH",
                                threshold="BLOCK_NONE"
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_HARASSMENT",
                                threshold="BLOCK_NONE"
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                threshold="BLOCK_NONE"
                            ),
                        ]
                    ),
                )
                
                if response.parsed:
                    task_impl = response.parsed
                    for file_obj in task_impl.files:
                        file_path = f"{folder_name}/{file_obj.filename}"
                        yield {"type": "file", "path": file_path, "content": file_obj.content}
                else:
                    msg = f"Failed to generate code for task {task.name}. Response: {response}"
                    print(msg)
                    yield {"type": "log", "message": f"Error: {msg}"}

            except Exception as e:
                msg = f"Exception for task {task.name}. Error: {e}"
                print(msg)
                import traceback
                traceback.print_exc()
                yield {"type": "log", "message": f"Error: {msg}"}
