# Sebastian

**Sebastian** is a deterministic, safety-first AI agent runtime written in Python. Unlike typical ReAct chatbots which blindly trust LLM-generated code and tool calls, Sebastian decouples *intent* from *execution*. 

An LLM is used purely as a parsing layer to produce structured intents and arguments. The core system deterministically routes these intents through a strict pipeline of context compilation, static planning, execution, verification, and automated recovery. It implements a fully functional permission kernel, sandboxed execution, and an evidence-grounded response generator.

## Architecture

The LLM is NOT the final execution authority. The pipeline works as follows:

User -> Intent (LLM) -> Context Compiler -> Planner -> ActionExecutor -> ToolExecutor (Applies Permissions & Safety) -> Verification -> Checkpoint -> Response Generator -> User

## Built-in Tools
- read_file
- list_directory
- write_file
- create_directory
- move_file
- run_command
- run_python
- git_status
- git_diff
- git_log

## Configuration
Set up your .env file:
\\\ash
GROQ_API_KEY=your_groq_key
\\\`n
## Running the Demo
\\\ash
python demo.py
\\\`n
## Running Tests
\\\ash
pytest tests/ -m "not real_groq"
\\\`n
## Known Limitations (V1)
- Single turn execution (no multi-step LLM feedback loops yet)
- Keyword-based static planner

## V2 Direction
Future versions will introduce LLM-driven planning with strict sub-agent isolation and multi-turn capabilities.
