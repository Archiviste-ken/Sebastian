import os
from pathlib import Path
from app.orchestrator import Sebastian
from app.llm.groq import GroqModelGateway
from tests.test_orchestrator import FakeGateway
from app.security.permissions import PermissionLevel

def main():
    workspace = Path.cwd()
    print("Setting up Sebastian for an end-to-end task...")
    
    # Use real gateway if key is available, else use FakeGateway
    if "GROQ_API_KEY" in os.environ:
        print("Using REAL GroqModelGateway...")
        gateway = GroqModelGateway(model="llama3-8b-8192")
    else:
        print("Using FakeGateway (no API key found)...")
        gateway = FakeGateway(workspace=workspace)
        
    permissions = {
        "read_file": PermissionLevel.AUTONOMOUS,
        "write_file": PermissionLevel.AUTONOMOUS,
        "list_directory": PermissionLevel.AUTONOMOUS,
    }
    
    agent = Sebastian(workspace=workspace, gateway=gateway, permissions=permissions)
    
    # Create a test file
    test_file = workspace / "test.txt"
    test_file.write_text("This is an end-to-end test.")
    
    try:
        report = agent.run("Read test.txt")
        print("\n=== TASK REPORT ===")
        print(f"Success: {report.success}")
        print(f"Goal: {report.goal}")
        print(f"Plan Goal: {report.plan_goal}")
        print(f"Actions Completed: {report.execution.actions_completed}")
        
        print("\n=== AUDIT LOG ===")
        for event in report.audit_events:
            print(f"- Tool: {event.tool_name}, Success: {event.success}, Msg: {event.message[:50]}")
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    main()
