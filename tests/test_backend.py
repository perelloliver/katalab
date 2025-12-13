import pytest
from unittest.mock import MagicMock, patch
from src.backend.builder import KataBuilder
from src.backend.models import CompanyInfo, KataPlan, KataTask, Team, Role, TaskImplementation, FileContent
from src.backend.agent import KataAgent

# Mock Data
MOCK_COMPANY = CompanyInfo(
    roles=[Role(title="Dev", stack=["Python"], requirements="Code")],
    teams=[Team(name="Product", size=5, context="test context", tools_used=[], philosophy=[])],
    philosophy="Move fast"
)

MOCK_PLAN = KataPlan(
    title="Test Kata",
    description="A test kata",
    tasks=[KataTask(id="task_1", name="Task 1", description="Do smth", files=["main.py"])]
)

@pytest.fixture
def mock_summariser():
    with patch("src.backend.builder.Summariser") as MockSummariser:
        instance = MockSummariser.return_value
        instance.run.return_value = MOCK_COMPANY
        yield instance

@pytest.fixture
def mock_agent():
    with patch("src.backend.builder.KataAgent") as MockAgent:
        instance = MockAgent.return_value
        instance.plan.return_value = MOCK_PLAN
        instance.run.return_value = {"task_1/main.py": "print('hello')"}
        yield instance

def test_builder_flow(mock_summariser, mock_agent):
    builder = KataBuilder(docs=["fake doc"])
    
    # Test Parse
    data = builder._parse_data()
    assert data == MOCK_COMPANY
    mock_summariser.run.assert_called_once()
    
    # Test Plan
    plan = builder._plan_repo()
    assert plan == MOCK_PLAN
    mock_agent.plan.assert_called_once_with(data=MOCK_COMPANY, feedback=None)
    
    # Test Build
    repo = builder._build_repo()
    assert "task_1/main.py" in repo
    mock_agent.run.assert_called_once_with(data=MOCK_COMPANY)
    
    # Test Output (mock zipfile or check path)
    with patch("zipfile.ZipFile") as mock_zip:
        out_path = builder._output_repo()
        assert out_path.endswith("kata_repo.zip")

def test_agent_plan():
    # Test Agent logic with mocked client
    with patch("src.backend.agent.google_client") as mock_client:
        mock_response = MagicMock()
        mock_response.parsed = MOCK_PLAN
        mock_client.models.generate_content.return_value = mock_response
        
        agent = KataAgent()
        plan = agent.plan(MOCK_COMPANY)
        
        assert plan == MOCK_PLAN
        assert agent.latest_plan == MOCK_PLAN

def test_agent_run():
    with patch("src.backend.agent.google_client") as mock_client:
        agent = KataAgent()
        agent.latest_plan = MOCK_PLAN
        
        # Mock response for task generation
        mock_response = MagicMock()
        mock_response.parsed = TaskImplementation(files=[FileContent(filename="main.py", content="code")])
        mock_client.models.generate_content.return_value = mock_response
        
        repo = agent.run(MOCK_COMPANY)
        
        # Check keys - agent adds folder prefix
        assert "task_1/main.py" in repo
        assert repo["task_1/main.py"] == "code"
