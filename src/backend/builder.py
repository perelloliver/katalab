from src.backend.agent import KataAgent
from src.backend.summarisation.role import summarise_role_information
from src.backend.models import RoleInformation
import os
import zipfile

class KataBuilder:
    def __init__(self, docs: list[str], agent_llm: str = "gemini-2.5-flash", output_dir: str = "downloads", n_tasks: int = 5):
        self.summarised_data = self._parse_data(docs)
        self.agent = KataAgent(model_name=agent_llm, n_tasks=n_tasks)
        self.output_dir = output_dir
        self.repo: dict[str, str] | None = None

    def _parse_data(self, docs: list[str]) -> RoleInformation:
        return summarise_role_information(docs)

    def _plan_repo(self, feedback: str | None = None):
        return self.agent.plan(role_information=self.summarised_data, feedback=feedback)

    def _build_repo(self):
        self.repo = {}
        generator = self.agent.run(role_information=self.summarised_data)
        
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

if __name__ == "__main__":
    from src.backend.utils import read_documents_from_directory
    builder = KataBuilder(docs=read_documents_from_directory("case-studies/nebula_junior_dev/company"))
    print(builder._plan_repo().model_dump_json(indent=2))