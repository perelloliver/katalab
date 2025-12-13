import json
import os
from src.backend.models import CompanyInfo, KataPlan
from src.backend.builder import KataBuilder

SESSION_FILE = "sessions.json"

class SessionManager:
    def __init__(self):
        self.sessions: dict[str, KataBuilder] = {}
        self._load_sessions()

    def _load_sessions(self):
        if not os.path.exists(SESSION_FILE):
            return

        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                
            for session_id, session_data in data.items():
                # Re-hydrate builder
                builder = KataBuilder(docs=[], output_dir=session_data["output_dir"])
                if session_data.get("company_info"):
                    builder.data = CompanyInfo(**session_data["company_info"])
                if session_data.get("plan"):
                    builder.agent.latest_plan = KataPlan(**session_data["plan"])
                
                self.sessions[session_id] = builder
        except Exception as e:
            print(f"Failed to load sessions: {e}")
            # Start fresh if corrupted
            self.sessions = {}

    def save_session(self, session_id: str, builder: KataBuilder):
        self.sessions[session_id] = builder
        self._persist()

    def get_session(self, session_id: str) -> KataBuilder | None:
        return self.sessions.get(session_id)
    
    def _persist(self):
        data = {}
        for session_id, builder in self.sessions.items():
            data[session_id] = {
                "output_dir": builder.output_dir,
                "company_info": builder.data.model_dump() if builder.data else None,
                "plan": builder.agent.latest_plan.model_dump() if builder.agent.latest_plan else None
            }
            
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=2)

session_manager = SessionManager()
