import pytest
from unittest.mock import MagicMock, patch
from src.backend.builder import KataBuilder
from src.backend.models import CompanyInfo, EmployeeInfo, KataPlan, Plan, Team, Role, TaskImplementation, FileContent
from src.backend.agent import KataAgent

# Mock Data
MOCK_COMPANY = CompanyInfo(
    roles=[Role(title="Dev", stack=["Python"], requirements="Code")],
    teams=[Team(name="Product", size=5, context="test context", tools_used=[], philosophy=[])],
    philosophy="Move fast"
)

MOCK_EMPLOYEE = EmployeeInfo(
    name="John Doe",
    stack=["Python", "FastAPI"],
    experience_yrs=5,
    level="senior",
    likely_learning_style="hands-on practical examples"
)

MOCK_PLAN = KataPlan(
    title="Test Kata",
    description="A test kata",
    tasks=[Plan(id="task_1", name="Task 1", description="Do smth", files=["main.py"])]
)

@pytest.fixture
def mock_summariser():
    with patch("src.backend.builder.Summariser") as MockSummariser:
        instance = MockSummariser.return_value
        instance.run.return_value = MOCK_COMPANY
        yield instance

@pytest.fixture
def mock_employee_extractor():
    with patch("src.backend.builder.EmployeeInfoExtractor") as MockExtractor:
        instance = MockExtractor.return_value
        instance.run.return_value = MOCK_EMPLOYEE
        yield instance

@pytest.fixture
def mock_agent():
    with patch("src.backend.builder.KataAgent") as MockAgent:
        instance = MockAgent.return_value
        instance.plan.return_value = MOCK_PLAN
        # Mock run to return a generator
        def mock_generator(*args, **kwargs):
            yield {"type": "file", "path": "task_1/main.py", "content": "print('hello')"}
        instance.run.side_effect = mock_generator
        yield instance

def test_builder_flow(mock_summariser, mock_employee_extractor, mock_agent):
    builder = KataBuilder(docs=["fake doc"], employee_docs=["fake employee doc"])
    
    # Test Parse Company
    data = builder._parse_data()
    assert data == MOCK_COMPANY
    mock_summariser.run.assert_called_once()
    
    # Test Parse Employee
    employee_data = builder._parse_employee_data()
    assert employee_data == MOCK_EMPLOYEE
    mock_employee_extractor.run.assert_called_once()
    
    # Test Plan
    plan = builder._plan_repo()
    assert plan == MOCK_PLAN
    mock_agent.plan.assert_called_once_with(company_data=MOCK_COMPANY, employee_data=MOCK_EMPLOYEE, feedback=None)
    
    # Test Build - consume generator
    events = list(builder._build_repo())
    assert len(events) > 0
    assert builder.repo["task_1/main.py"] == "print('hello')"
    mock_agent.run.assert_called_once_with(company_data=MOCK_COMPANY, employee_data=MOCK_EMPLOYEE)
    
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
        plan = agent.plan(MOCK_COMPANY, MOCK_EMPLOYEE)
        
        assert plan == MOCK_PLAN
        assert agent.latest_plan == MOCK_PLAN

def test_agent_plan_n_tasks_prompt():
    # Verify n_tasks is in prompt
    with patch("src.backend.agent.google_client") as mock_client:
        mock_response = MagicMock()
        mock_response.parsed = MOCK_PLAN
        mock_client.models.generate_content.return_value = mock_response
        
        tasks_count = 7
        agent = KataAgent(n_tasks=tasks_count)
        agent.plan(MOCK_COMPANY, MOCK_EMPLOYEE)
        
        # Check call args
        call_args = mock_client.models.generate_content.call_args
        assert call_args is not None
        
        # contents arg is the first positional or "contents" kwarg
        # based on agent.py: client.models.generate_content(model=..., contents=[prompt], config=...)
        _, kwargs = call_args
        prompt = kwargs["contents"][0]
        
        assert f"EXACTLY {tasks_count} tasks" in prompt
        assert f"Design a coding kata (a set of EXACTLY {tasks_count} tasks)" in prompt
        
        # Verify schema is passed
        config = kwargs["config"]
        # We can't easily check the dynamic schema class attributes here without inspection, 
        # but we can assume if it runs without error and passes schema it's working.
        assert config.response_schema is not None

def test_agent_run():
    with patch("src.backend.agent.google_client") as mock_client:
        agent = KataAgent()
        agent.latest_plan = MOCK_PLAN
        
        # Mock responses
        # 1. README response
        mock_readme_response = MagicMock()
        mock_readme_response.text = "Mock README content"
        
        # 2. Implementation response
        mock_impl_response = MagicMock()
        mock_impl_response.parsed = TaskImplementation(files=[FileContent(filename="main.py", content="code")])
        
        # Set side_effect for generate_content to return appropriate mock
        mock_client.models.generate_content.side_effect = [mock_readme_response, mock_impl_response]
        
        # Consume generator
        events = list(agent.run(MOCK_COMPANY, MOCK_EMPLOYEE))
        
        # Check that we got file events
        files = {e['path']: e['content'] for e in events if e['type'] == 'file'}
        
        # Check keys - agent adds folder prefix
        assert "README.md" in files # Root readme
        assert "task_1/README.md" in files
        assert "task_1/main.py" in files
        assert files["task_1/main.py"] == "code"
