from typing import Optional
from src.backend.agent import KataAgent
from src.backend.summariser import Summariser
from src.backend.models import CompanyInfo
import os
import zipfile
import io

class KataBuilder:
    def __init__(self, docs: list[str], model_name: str = "gemini-3-pro-preview", output_dir: str = "downloads"):
        self.summariser = Summariser(model_name=model_name)
        self.agent = KataAgent(model_name=model_name)
        self.docs = docs
        self.output_dir = output_dir
        self.data: CompanyInfo | None = None
        self.repo: dict[str, str] | None = None

    def _parse_data(self) -> CompanyInfo:
        self.data = self.summariser.run(self.docs)
        return self.data

    def _plan_repo(self, feedback: str | None = None):
        if not self.data:
            raise ValueError("Data not parsed yet. Call _parse_data() first.")
        return self.agent.plan(data=self.data, feedback=feedback)

    def _build_repo(self):
        if not self.data:
            raise ValueError("Data not parsed yet.")
        self.repo = self.agent.run(data=self.data)
        return self.repo

    def _output_repo(self) -> str:
        """
        Saves the repo as a .zip file and returns the path to the zip file.
        """
        if not self.repo:
            raise ValueError("Repo not built yet.")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Create zip in memory first or directly write
        zip_filename = f"kata_repo.zip"
        zip_path = os.path.join(self.output_dir, zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, content in self.repo.items():
                zipf.writestr(file_path, content)
        
        return zip_path
    
    def run_pipeline(self):
        """
        Run the full pipeline non-interactively (for testing or batch)
        """
        self._parse_data()
        self._plan_repo()
        self._build_repo()
        return self._output_repo()
