import pytest
import json
from app.response.generator import ResponseGenerator
from app.response.models import FinalResponse
from app.llm.gateway import ModelResponse
from app.orchestrator import TaskReport
from app.execution.models import ExecutionReport, ActionOutcome
from app.models.tool_result import ToolResult, ToolResultStatus
from app.verification.models import VerificationResult, VerificationStatus

class FakeResponseGateway:
    def __init__(self, response_text):
        self.response_text = response_text
    def generate(self, messages, response_format=None):
        return ModelResponse(content=self.response_text)

def test_successful_read_file_summary():
    gateway = FakeResponseGateway('{\"status\": \"success\", \"answer\": \"The file was read successfully.\"}')
    generator = ResponseGenerator(gateway)
    
    report = TaskReport(
        task_id='1', success=True, goal='Read file', plan_goal='Read file',
        execution=ExecutionReport(task_id='1', success=True, actions_completed=1, actions_failed=0, actions_total=1, outcomes=[
            ActionOutcome(action_id='1', tool_name='read_file', tool_result=ToolResult(status=ToolResultStatus.SUCCESS, data='File content', error=None), verification=VerificationResult(status=VerificationStatus.PASS, method='test', reason='ok'), recovery_attempts=0)
        ], cancelled=False, reason='done')
    )
    
    response = generator.generate('Read file', report)
    assert response.status == 'success'
    assert response.answer == 'The file was read successfully.'

def test_missing_information():
    gateway = FakeResponseGateway('{\"status\": \"missing_information\", \"answer\": \"I need a filename.\"}')
    generator = ResponseGenerator(gateway)
    
    report = TaskReport(
        task_id='1', success=False, goal='Read file', plan_goal='Pending Information',
        execution=ExecutionReport(task_id='1', success=False, actions_completed=0, actions_failed=0, actions_total=0, reason='Missing information'),
        missing_information=['Filename']
    )
    
    response = generator.generate('Read file', report)
    assert response.status == 'missing_information'
    assert response.answer == 'I need a filename.'

