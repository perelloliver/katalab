from src.backend.agent import KataAgent
from src.backend.summariser import Summariser, EmployeeInfoExtractor
from src.backend.models import CompanyInfo, EmployeeInfo
import os
import zipfile

class KataBuilder:
    def __init__(self, docs: list[str], summariser_llm: str = "gemini-2.5-flash", agent_llm: str = "gemini-2.5-flash", output_dir: str = "downloads", n_tasks: int = 1):
        self.summariser = Summariser(model_name=summariser_llm)
        self.agent = KataAgent(model_name=agent_llm, n_tasks=n_tasks)
        self.docs = docs
        self.output_dir = output_dir
        self.data: CompanyInfo | None = None
        self.repo: dict[str, str] | None = None

    def _parse_data(self) -> CompanyInfo:
        self.data = self.summariser.run(self.docs)
        return self.data

    def _plan_repo(self, feedback: str | None = None):
        if not self.data:
            raise ValueError("Company data not parsed yet. Call _parse_data() first.")
        return self.agent.plan(company_data=self.data, feedback=feedback)

    def _build_repo(self):
        if not self.data:
            raise ValueError("Company data not parsed yet.")
        
        self.repo = {}
        generator = self.agent.run(company_data=self.data)
        
        for event in generator:
            if event["type"] == "file":
                self.repo[event["path"]] = event["content"]
            yield event

    def _output_repo(self) -> str:
        """
        Saves the repo as a .zip file and returns the path to the zip file.
        """
        if not self.repo:
            raise ValueError("Repo not built yet.")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Create zip in memory first or directly write
        zip_filename = "kata_repo.zip"
        zip_path = os.path.join(self.output_dir, zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, content in self.repo.items():
                zipf.writestr(file_path, content)
        
        return zip_path
