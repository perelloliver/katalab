from src.backend.google_client import google_client
from src.backend.models import RoleInformation, Plan, Repo, TaskImplementation, KataTask
from google.genai import types


class KataCreator:
    def __init__(self, model_name: str = "gemini-3-pro-preview", n_tasks: int = 3, role_information: RoleInformation):
        if not role_information or not isinstance(role_information, RoleInformation):
            raise ValueError("Role information must be provided")

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
        {self.role_information.model_dump_json(indent=2)}

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
    
    async def _create_task(self, task: KataTask) -> TaskImplementation:
        """
        Create a TaskImplementation for a given KataTask.
        This generates the actual code files needed to implement the task.
        Uses async client for true concurrent execution.
        """
        prompt = f"""
        You are a senior software engineer creating a coding kata task implementation.
        
        Task to implement:
        Name: {task.name}
        Description: {task.description}
        Tech Stack Focus: {', '.join(task.tech_stack)}

        Role Context:
        {self.role_information.model_dump_json(indent=2)}

        Generate a complete, working implementation for this task.
        Create all necessary files with proper code structure, comments, and best practices.
        The code should be production-quality and demonstrate the key concepts for this task.
        
        Include:
        - Main implementation files
        - Configuration files if needed
        - A brief inline comment at the top of each file explaining its purpose
        
        Make the code realistic and educational, suitable for a new engineer learning these technologies.
        """

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TaskImplementation
            )
        )

        if response.parsed:
            return response.parsed
        else:
            raise ValueError(f"Failed to parse response: {response}")
    
    def _generate_readme(self, plan: Plan, task_implementations: list[TaskImplementation]) -> str:
        """Generate a comprehensive README for the kata repository."""
        prompt = f"""
        You are a senior software engineer creating a README for a coding kata repository.
        
        Kata Overview:
        Focus Points: {', '.join(plan.focus_points)}
        Number of Tasks: {len(plan.tasks)}
        
        Tasks:
        {chr(10).join([f"- {task.name}: {task.description}" for task in plan.tasks])}
        
        Role Context:
        {self.role_information.model_dump_json(indent=2) if self.role_information else "No role information provided"}
        
        Create a comprehensive, well-structured README.md that includes:
        1. A compelling title and introduction
        2. Overview of what this kata teaches
        3. Prerequisites and setup instructions
        4. Clear task descriptions in order
        5. Learning objectives for each task
        6. Tips for getting started
        7. Additional resources if relevant
        
        Make it engaging and educational. Use proper markdown formatting.
        The README should motivate learners and provide clear guidance.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="text/plain"
            )
        )
        
        return response.text
    
    async def create_repo(self) -> Repo:
        """
        Create a complete kata repository with all tasks implemented.
        Runs task creation asynchronously for efficiency using Google's async client.
        """
        import asyncio
        
        # Ensure we have a plan
        if not self.latest_plan:
            self.latest_plan = self.plan()
        
        # Create all tasks concurrently using the async client
        task_implementations = await asyncio.gather(
            *[self._create_task(task) for task in self.latest_plan.tasks]
        )
        
        # Generate README
        readme = self._generate_readme(self.latest_plan, task_implementations)
        
        # Compile into Repo
        return Repo(
            readme=readme,
            modules=task_implementations
        )