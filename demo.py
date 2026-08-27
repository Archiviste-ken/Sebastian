import json
from pathlib import Path

from app.llm.gateway import ModelResponse
from app.orchestrator import Sebastian
from tests.test_orchestrator import FakeGateway

class DemoGateway(FakeGateway):
    def __init__(self, intent_json, arg_json, final_json):
        super().__init__(intent_json=intent_json, arg_json=arg_json, workspace=Path.cwd())
        self.final_json = final_json
    
    def generate(self, messages, response_format=None):
        if response_format is not None:
            schema_name = response_format.get("json_schema", {}).get("name")
            if schema_name == "sebastian_intent":
                return ModelResponse(content=self._intent_json, raw=None)
            elif schema_name == "sebastian_resolved_arguments":
                return ModelResponse(content=self._arg_json, raw=None)
            elif schema_name == "sebastian_final_response":
                return ModelResponse(content=self.final_json, raw=None)
        return ModelResponse(content=self._arg_json, raw=None)

def run_case(name, intent_data, arg_data, final_data, workspace_setup_fn=None):
    print(f"\n=== Case: {name} ===")
    workspace = Path.cwd() / "demo_workspace"
    workspace.mkdir(exist_ok=True)
    if workspace_setup_fn:
        workspace_setup_fn(workspace)
    
    gateway = DemoGateway(json.dumps(intent_data), json.dumps(arg_data), json.dumps(final_data))
    agent = Sebastian(workspace=workspace, gateway=gateway)
    report = agent.run("dummy request")
    
    print(f"Success: {report.success}")
    if report.response:
        print(f"Final Answer [{report.response.status}]: {report.response.answer}")
    print("Audit Events:")
    for event in report.audit_events:
        print(f"  - {event.tool_name}: {event.success}")
    
    # Cleanup
    import shutil
    shutil.rmtree(workspace)

def main():
    print("Sebastian V1 Acceptance Suite")
    
    def setup_readme(w):
        (w / "README.md").write_text("Sebastian is a safe agent.")
        
    run_case(
        "Read README.md",
        {"goal": "Read README.md", "constraints": [], "expected_outcome": "File read", "forbidden_actions": [], "missing_information": [], "required_permissions": ["read_file"], "success_criteria": []},
        {"tool_name": "read_file", "arguments": {"path": "README.md"}},
        {"status": "success", "answer": "Sebastian is a safe agent."},
        setup_readme
    )

    run_case(
        "Missing information",
        {"goal": "Read a file", "constraints": [], "expected_outcome": "File read", "forbidden_actions": [], "missing_information": ["Need file name"], "required_permissions": [], "success_criteria": []},
        {},
        {"status": "missing_information", "answer": "I need a file name."}
    )

if __name__ == "__main__":
    main()
