# 🎩 Sebastian — What Every File Does (Flow of Files)

> **A quick, emojified guide to every file in the project — what it does, why it exists, and how it connects to the rest.**

---

## 🏗️ Project Root Files

### 📄 `pyproject.toml`
> 🔧 **The project's birth certificate**
- 📛 Declares the project name (`sebastian`) and version (`0.1.0`)
- 🐍 Requires Python 3.11+
- 📦 Lists dependencies: `pydantic`, `fastapi`, `sqlalchemy`, `groq`, `python-dotenv`
- 🧪 Dev dependency: `pytest`
- 📂 Tells setuptools where to find packages (`app*`)
- 🏷️ Defines custom pytest marker: `real_groq` for live API tests

### 🔐 `.env`
> 🗝️ **The secret keeper**
- 🤖 Stores `GROQ_API_KEY` — the API key Sebastian uses to talk to the Groq LLM
- 🚫 Git-ignored so secrets never leak to version control

### 🙈 `.gitignore`
> 🧹 **The cleanup crew**
- 🐍 Ignores Python caches (`__pycache__/`, `*.pyc`)
- 🔐 Ignores secrets (`.env`, `*.pem`, `*.key`, credentials)
- 📦 Ignores virtual environments (`.venv/`, `venv/`)
- 🗄️ Ignores databases (`*.db`, `*.sqlite3`)
- 🧪 Ignores test artifacts (`.pytest_cache/`, `coverage/`)
- 🛠️ Ignores IDE files (`.idea/`, `.vscode/`)

### 📖 `README.md`
> 🎩 **Sebastian's introduction to the world**
- 🎯 Explains the vision: "Give Sebastian the outcome. He figures out the work."
- 🔄 Shows the core loop: Intent → Context → Plan → Permission → Execute → Observe → Verify → Recover
- 🛡️ Describes the 3-tier permission model (🟢 Autonomous / 🟡 Approval / 🔴 Blocked)

### 🧠 `Flow.md`
> 📐 **The architect's blueprint** (22KB of pure design documentation)
- 🎯 25 sections covering every design principle
- 🔄 The full system flow from user message to verified outcome
- 🛠️ How tools, permissions, safety, verification, and recovery work
- 🎩 Sebastian's personality: Calm, Competent, Observant, Cautious, Persistent, Honest
- 🌱 The evolution roadmap from V1 (local) → V5 (adaptive automation)

### 🚀 `roadmap.md`
> 🗺️ **The master plan** (22KB)
- 📋 18 phases across 5 versions
- 🧱 Phase 0–1: Foundation + Tool Runtime ✅
- 🧠 Phase 2: LLM Gateway + Intent Engine 🚀 ← **YOU ARE HERE**
- 🔎 Phase 3–11: Context, Planning, Execution, Verification, Recovery
- 🌐 Phase 12–18: Browser, Desktop, Services, Persistence, Learning

### 📊 `versions.md`
> 📜 **The version timeline**
- 🟢 V1 (Phases 0–11): Core Execution Engine
- 🔵 V2 (Phases 12–13): Web + Desktop
- 🟣 V3 (Phases 14–16): Connected Environment
- 🟠 V4 (Phase 17): Persistent Sebastian
- 🔴 V5 (Phase 18): Adaptive Sebastian

### 🗄️ `sebastian.db`
> 💾 **The SQLite database** — stores persisted tasks

---

## ⚙️ `app/config.py` — Configuration Loader

```
📥 .env file
    ↓
🔧 python-dotenv reads GROQ_API_KEY
    ↓
✅ Settings object with validated key
    ↓
❌ RuntimeError if key is missing
```

**What it does:**
- 📍 Finds the project root directory
- 📥 Loads `.env` using `python-dotenv`
- 🔐 Reads `GROQ_API_KEY` from `.env` as the single source of truth
- 💥 Raises `RuntimeError` if the key is empty — prevents running without credentials

---

## 📡 `app/api/` — The HTTP Surface

### 📦 `__init__.py`
> 🏷️ Marks this as the API package — the HTTP surface for Sebastian

### 🚀 `main.py` — FastAPI Entry Point
```
🏗️ App starts → create_tables() runs
    ↓
📡 POST /tasks → creates a new task in the database
📡 GET /tasks/{id} → fetches a task by ID (or 404)
📡 GET /health → returns {"status": "ok"}
```

**What it does:**
- 🏗️ `lifespan()` — ensures DB tables exist on startup
- 🔌 `get_db()` — creates a per-request DB session, closes it after
- 📝 `create_task()` — converts `TaskCreateRequest` → `Task` domain model → saves to DB
- 🔍 `get_task()` — looks up task by ID, returns 404 if not found
- ❤️ `health_check()` — simple liveness probe

### 📋 `schemas.py` — API Request Models
> 📡 **Defines what clients can send**
- 🆔 `TaskCreateRequest.id` — task identifier (min 1 char)
- 🎯 `TaskCreateRequest.goal` — what the user wants (min 1 char)

---

## 🗄️ `app/db/` — The Persistence Layer

### 📦 `__init__.py`
> 🏷️ Marks this as the database package

### 💾 `database.py` — Database Bootstrap
```
🔧 DATABASE_URL = "sqlite:///./sebastian.db"
    ↓
⚙️ create_engine() → SQLAlchemy engine
    ↓
🧵 SessionLocal → session factory
    ↓
🏗️ create_tables() → creates all mapped tables
```

**What it does:**
- 📍 Points to the local SQLite file
- ⚙️ Creates the engine with `check_same_thread=False` (required for SQLite + async)
- 🧵 `SessionLocal` — creates sessions with no auto-flush/commit (explicit control)
- 🏗️ `create_tables()` — runs `Base.metadata.create_all()` to create tables if they don't exist

### 🧱 `models.py` — ORM Models
> 📊 **Translates Python objects into database rows**
- 🏛️ `Base` — the common ancestor for all ORM models
- 📋 `TaskRecord` — maps to the `tasks` table:
  - 🆔 `id` — primary key (string)
  - 🎯 `goal` — what the user wants (string, not null)
  - 🔄 `status` — lifecycle state (string, not null)

### 📂 `repositories/__init__.py` — Task Repository (Main)
> 🧳 **The bridge between business logic and SQLite storage**
- 💾 `create(task)` — converts domain `Task` → `TaskRecord` → saves to DB
- 🔍 `get(task_id)` — finds a `TaskRecord` by ID → converts back to domain `Task`

### 📂 `repositories/task_repository.py` — Task Repository (Duplicate)
> ⚠️ Same as `__init__.py` repository — duplicate file

---

## 🎯 `app/intent/` — Understanding What The User Wants

### 📦 `__init__.py`
> 🏷️ Marks this as the intent package (if exists)

### 📋 `models.py` — The Intent Data Structure
> 📐 **The 7-field blueprint of user intent**

```
👤 "Fix this project and don't delete anything"
                    ↓
🎯 goal:               "Fix this project"
📏 constraints:         ["Don't delete anything"]
🏁 expected_outcome:    "Project works correctly"
🚫 forbidden_actions:   ["Delete files"]
❓ missing_information:  []
🛡️ required_permissions: ["write_file", "run_command"]
✅ success_criteria:    ["All tests pass"]
```

### 🧠 `engine.py` — The Intent Engine
```
👤 User text
    ↓
🧠 IntentEngine.parse()
    ↓
📡 Sends to Groq LLM with strict JSON schema
    ↓
📥 LLM returns structured JSON
    ↓
✅ Validated into Intent model
```

**What it does:**
- 🔧 `_strict_schema()` — builds a JSON schema from the `Intent` Pydantic model, making ALL fields required and removing defaults (forces LLM to fill everything)
- 🧠 `parse(user_request)` — sends a system prompt + user text to the LLM, requiring structured output matching the Intent schema exactly
- 📡 Uses `response_format = {"type": "json_schema", "strict": True}` — Groq's structured output mode
- ✅ Validates the response into an `Intent` object via `model_validate_json()`

---

## 🤖 `app/llm/` — Talking to the AI Model

### 📦 `__init__.py`
> 🏷️ Marks this as the LLM package (if exists)

### 🌉 `gateway.py` — The Model Interface
> 🔌 **Provider-agnostic interface for ANY LLM**
- 📦 `ModelResponse` — wraps the response: `content` (text) + `raw` (full API response)
- 🌉 `ModelGateway` — base class with `generate(messages, response_format)` → raises `NotImplementedError`
- 🔄 Designed so you can swap Groq → OpenAI → Anthropic → Ollama without changing any other code

### 🤖 `groq.py` — Groq Implementation
```
🔑 API key
    ↓
🤖 Groq client initialized
    ↓
📡 generate(messages, response_format)
    ↓
🧠 Groq API processes the request
    ↓
📥 ModelResponse(content=..., raw=...)
```

**What it does:**
- 🏗️ `__init__()` — accepts a `model` name, optional `client`, or `api_key`. Raises `RuntimeError` if no key provided
- 📡 `generate()` — builds the request dict (model + messages + optional response_format), calls `client.chat.completions.create()`
- 🔐 Catches `AuthenticationError` → raises helpful `RuntimeError` with fix instructions
- 📥 Returns `ModelResponse` with the LLM's text content and the raw response object

---

## 📝 `app/models/` — The Domain Vocabulary

> **These are the "nouns" of the system — the objects Sebastian thinks in.**

### 📦 `_init_.py` — Package Exports
> 🎁 Re-exports the key models: `Task`, `TaskStatus`, `Plan`, `can_transition`

### 🧵 `task.py` — Task Lifecycle
```
⏳ PENDING → 🧠 PLANNING → 🛑 WAITING_APPROVAL → ⚙️ EXECUTING
                                                        ↓
                                                   ⏸️ PAUSED
                                                        ↓
                                                   ✅ VERIFYING → 🏁 COMPLETED
                                                        ↓
                                                   🔁 RECOVERING → (back to PLANNING)
                                                        ↓
                                                   ❌ FAILED / 🚫 CANCELLED
```

- 🔄 `TaskStatus` — 10-state enum covering the full lifecycle
- 📋 `Task` — Pydantic model: `id`, `goal`, `status`
- 🗺️ `VALID_TRANSITIONS` — dict mapping each state to its allowed next states
- 🧭 `can_transition()` — checks if a state change is legal

### 🧩 `action.py` — Single Step in a Plan
- 🆔 `id` — unique action identifier
- 🗺️ `plan_id` — which plan this belongs to
- 📝 `description` — what this action does (must not be empty)

### 🗺️ `plan.py` — The Strategy
- 🆔 `id` — unique plan identifier
- 🧵 `task_id` — which task this plan serves
- 📝 `description` — summary of the plan's purpose

### 🧰 `tool_call.py` — Tool Invocation Request
- 🏷️ `tool_name` — which tool to run (e.g., `read_file`)
- 📦 `arguments` — named values for the tool handler (e.g., `{"path": "main.py"}`)

### 🔧 `tool_result.py` — Tool Execution Output
- 🔄 `ToolResultStatus` — enum: `SUCCESS` / `FAILED` / `WAITING_APPROVAL` / `BLOCKED`
- 📊 `ToolResult` — immutable result: `status`, `data`, `error`
- ✅ `.success` property — shortcut for checking `status == SUCCESS`

### 🧾 `audit_event.py` — Audit Record
- 🏷️ `tool_name` — which tool was attempted
- ✅/❌ `success` — whether it worked
- 💬 `message` — human-readable outcome

### 🛡️ `permission.py` — Permission Model
- 🟢 `AUTONOMOUS` — run without asking
- 🟡 `APPROVAL` — ask first
- 🔴 `BLOCKED` — never run
- 📋 `Permission` — maps a tool to its permission level

### 🧭 `checkpoint.py` — State Snapshot
- 🆔 `id` — checkpoint identifier
- 🧵 `task_id` — which task this belongs to
- ⚙️ `action_id` — which action was active (optional)
- 🗂️ `state` — saved progress, flags, partial results
- 🕒 `created_at` — timestamp

### 🧪 `execution_event.py` — Execution Record
- 🆔 `id` — event identifier
- 🔗 `tool_call_id` — which tool call triggered this
- 🏷️ `event_type` — e.g., "tool_started", "tool_completed"
- ✅ `success` — pass or fail
- 🕒 `timestamp` — when it happened
- 📦 `data` — extra metadata (exit codes, outputs)

### ✅ `verification.py` — Evidence-Based Check
- 🆔 `id` — verification identifier
- 🧵 `task_id` — which task is being verified
- ✅ `success` — did it pass?
- 🔎 `method` — how was it verified (e.g., "tests", "diff check")
- 📚 `evidence` — proof (test output, file contents, etc.)

### ⚙️ `config.py` — Settings Model
- 🤖 `app_name` — "Sebastian"
- 🌍 `environment` — "development" / "production"
- 🪵 `log_level` — "INFO" / "DEBUG" / etc.
- 🔐 `model_api_key` — optional external API key
- 📥 `load_settings()` — reads from environment variables

### 🪵 `logging.py` — Log Configuration
- 🔧 `configure_logging(settings)` — sets up Python's logging with consistent format:
  `timestamp | LEVEL | component | message`

---

## 🗺️ `app/planning/` — Turning Intent Into Action

### 📋 `models.py` — Planning Data Structures
```
🗺️ Plan
  ├── 🎯 goal (what we want)
  ├── 🧩 actions[] (how we'll do it)
  └── ✅ success_criteria[] (how we'll know it worked)

🧩 Action
  ├── 🆔 action_id
  ├── 🧰 tool (which tool to use)
  ├── 📦 arguments
  ├── 🔒 preconditions
  ├── 🎯 expected_result
  ├── ⚠️ risk (LOW/MEDIUM/HIGH)
  ├── ⏱️ timeout_seconds (default 30)
  ├── 🔁 retry_policy (NEVER/SAFE/ALWAYS)
  ├── ✅ verification_method
  └── ↩️ rollback_strategy

📦 ResolvedArguments
  ├── 🏷️ tool_name
  └── 📦 arguments
```

### 🧩 `capabilities.py` — What Sebastian Can Do
> 🎯 **10 capabilities with risk levels:**

| Capability | Risk | Description |
|---|---|---|
| 📖 `read_file` | 🟢 low | Read file contents |
| 📂 `list_directory` | 🟢 low | List directory contents |
| ✏️ `write_file` | 🟡 medium | Write text to a file |
| 📁 `create_directory` | 🟡 medium | Create a directory |
| 🔀 `move_file` | 🟡 medium | Move a file |
| ⌨️ `run_command` | 🔴 high | Run an approved command |
| 🐍 `run_python` | 🔴 high | Run a Python script |
| 🐙 `git_status` | 🟢 low | Check git working tree |
| 🐙 `git_diff` | 🟢 low | Inspect git diff |
| 🐙 `git_log` | 🟢 low | View recent commits |

### 🔍 `selector.py` — Picking the Right Tools
```
🎯 Intent
    ↓
🔍 CapabilitySelector.select()
    ↓
📖 Is it a file read request? → read_file
📂 Is it a directory listing? → list_directory
🧪 Is it running tests? → run_command
🐍 Is it running a Python script? → run_python
🔀 Is it moving files? → move_file
🐙 Is it a git operation? → git_status/diff/log
    ↓
🧹 Deduplicate
    ↓
✅ list[Capability]
```

**How it works:**
- Uses keyword matching on the intent's `goal` and `expected_outcome`
- Explicit term lists (e.g., "read file", "open file", "file contents" → `read_file`)
- Deduplicates results to avoid running the same tool twice

### 🧠 `planner.py` — Building the Plan
```
🎯 Intent
    ↓
❓ Has missing_information?
   YES → 📋 Plan with "ask_user" action
    ↓
🔍 CapabilitySelector.select(intent)
    ↓
🧩 No capabilities found?
   YES → 📋 Plan with "ask_user" for clarification
    ↓
🗺️ Build Plan from capabilities
    ↓
📋 Plan(goal, actions[], success_criteria[])
```

**Smart behavior:**
- If intent has `missing_information` → generates an `ask_user` plan to gather info first
- If no capabilities match → generates a clarification request instead of guessing
- Each capability becomes an Action with its risk level and default timeout

### 🧠 `argument_resolver.py` — Filling In Tool Arguments
```
🎯 Intent + 🧰 ToolDefinition
    ↓
🧠 LLM asked: "What arguments does this tool need?"
    ↓
📥 LLM returns ResolvedArguments
    ↓
✅ Validated: tool_name must match
    ↓
📦 dict of concrete arguments
```

**What it does:**
- Sends the intent + tool schema to the LLM
- LLM produces the specific arguments needed (e.g., `{"path": "main.py"}`)
- Validates that the resolved tool name matches the requested tool
- Returns empty dict if info is unavailable (never invents data)

### 🔧 `compiler.py` — Plan → Executable ToolCalls
```
🧩 Action (from Plan)
    ↓
🔍 Is tool registered in ToolRegistry?
   NO → 💥 ValueError
    ↓
🧰 ToolCall(tool_name, arguments)
```

**What it does:**
- Takes a planning `Action` and converts it to an executable `ToolCall`
- Validates that the tool exists in the registry before compiling
- Raises `ValueError` for unknown tools — prevents executing unregistered tools

### 🏭 `engine.py` — The Planning Facade
```
🎯 Intent
    ↓
🗺️ Planner.build(intent) → Plan
    ↓
🔧 PlanCompiler.compile(action) for each action
    ↓
📋 list[ToolCall] ready for execution
```

**What it does:**
- `PlanningEngine.compile_intent(intent)` — the one-call entry point
- Orchestrates: planner builds the plan → compiler turns each action into a ToolCall
- Returns a flat list of executable ToolCalls

---

## 🛡️ `app/security/` — Keeping Things Safe

### 📦 `__init__.py`
> 🏷️ Marks this as the security package

### 🔐 `permissions.py` — Permission Gate
```
🧰 Tool name
    ↓
🔍 PermissionKernel.check()
    ↓
🟢 AUTONOMOUS → PermissionDecision(allowed=True)
🟡 APPROVAL → PermissionDecision(requires_approval=True)
🔴 BLOCKED → PermissionDecision(allowed=False)
❓ Unknown → BLOCKED by default (safe fallback)
```

**Key design:**
- `PermissionKernel` stores a `dict[tool_name → PermissionLevel]`
- Unknown tools are **BLOCKED** — safe default prevents unregistered tools from running
- Returns `PermissionDecision` with `allowed`, `requires_approval`, and `reason`

### 🔒 `safety.py` — Workspace-Bounded Safety
```
🧰 ToolCall
    ↓
🔒 ToolSafety.check()
    ↓
📁 Filesystem tools → path must be inside workspace
🔀 move_file → BOTH paths inside workspace
⌨️ run_command → only allowed executables (python, pytest, git)
🐍 run_python → must be .py file inside workspace
🐙 git tools → restricted to workspace repo
🏷️ Empty tool name → rejected
```

**How path safety works:**
1. Takes the path argument
2. If relative → joins with workspace path
3. `Path.resolve()` to eliminate `..` and symlinks
4. `relative_to(workspace)` — if this fails, path is OUTSIDE workspace → **BLOCKED**

**Allowed commands:** `python`, `python.exe`, `pytest`, `pytest.exe`, `git`, `git.exe`

---

## 🛠️ `app/tools/` — Sebastian's Hands

### 📦 `__init__.py`
> 🏷️ Marks this as the tools package

### 📋 `definition.py` — Tool Blueprint
- 📛 `name` — tool identifier
- 📝 `description` — what it does
- ⚙️ `handler` — the actual function to call
- 🌍 `uses_context` — does it need the workspace path?
- 📐 `argument_schema` — optional JSON schema for arguments

### 🗂️ `registry.py` — Tool Catalogue
```
🧰 ToolDefinition
    ↓
📋 ToolRegistry.register(tool)
    ↓
🔍 registry.get("read_file") → ToolDefinition
📜 registry.list_tools() → all registered tools
```

- 🚫 Prevents duplicate registration
- ❌ Raises `KeyError` for missing tools

### ⚙️ `runtime.py` — Tool Execution Wrapper
```
🧰 ToolDefinition + 📦 arguments + 🌍 context
    ↓
⚙️ ToolRuntime.execute()
    ↓
🌍 uses_context? → handler(context=..., **args)
📦 no context? → handler(**args)
    ↓
✅ ToolResult(SUCCESS, data=result)
❌ Exception? → ToolResult(FAILED, error=str(exc))
```

### 📍 `context.py` — Execution Context
- 🌍 `ExecutionContext` — frozen dataclass with `workspace: Path`
- Used by tools that need to know the working directory

### 📝 `audit.py` — Audit Trail
- 📚 `AuditRecorder` — in-memory append-only event list
- ➕ `record(event)` — adds an `AuditEvent`
- 📜 `events()` — returns a **copy** (prevents tampering)

### 🚦 `executor.py` — The Full Pipeline
```
🧰 ToolCall
    ↓
🔍 Step 1: Registry lookup (tool exists?)
   ❌ Not found → FAILED
    ↓
🔐 Step 2: Permission check
   🟡 Needs approval → WAITING_APPROVAL
   🔴 Blocked → BLOCKED
    ↓
🔒 Step 3: Safety check
   ❌ Unsafe → FAILED
    ↓
⚙️ Step 4: Runtime execution
   ✅ Success → ToolResult(SUCCESS)
   ❌ Error → ToolResult(FAILED)
    ↓
📝 Step 5: Audit event recorded (always)
```

---

## 🛠️ `app/tools/builtin/` — The Actual Tool Implementations

### 📦 `__init__.py`
> 🏷️ Marks this as the builtin tools package

### ⌨️ `command.py` — Shell Command Runner
```python
run_command(command: list[str]) → {"return_code": int, "stdout": str, "stderr": str}
```
- 🔒 Uses `shell=False` — prevents shell injection attacks
- 📊 Returns structured result with exit code + output

### 📁 `filesystem.py` — File Operations
```python
read_file(path)        → str           # 📖 Read UTF-8 text file
list_directory(path)   → list[str]     # 📂 Alphabetically sorted entries
write_file(path, content) → None       # ✏️ Write UTF-8 text
create_directory(path) → None          # 📁 Create with parents
move_file(source, destination) → None  # 🔀 Rename/move
```

### 🐙 `git.py` — Git Operations
```python
git_status(context)    → {"return_code", "stdout", "stderr"}  # 🔍 git status --short
git_diff(context)      → {"return_code", "stdout", "stderr"}  # 📊 git diff
git_log(context)       → {"return_code", "stdout", "stderr"}  # 📜 git log --oneline -10
```
- 🌍 All git tools use `ExecutionContext` — they need the workspace path
- 🔒 Run via subprocess with `shell=False`

### 🐍 `python.py` — Python Script Runner
```python
run_python(script: str) → {"return_code", "stdout", "stderr"}
```
- 🐍 Uses `sys.executable` — runs with the same Python that runs Sebastian
- 🔒 Subprocess with `shell=False`

---

## 🧪 `tests/` — 40 Test Files

| Category | Files | What They Test |
|---|---|---|
| 📝 Models | `test_action`, `test_audit`, `test_checkpoint`, `test_config`, `test_execution_event`, `test_logging`, `test_permission`, `test_plan`, `test_task`, `test_tool_call`, `test_verification` | Domain models, state transitions, serialization |
| 🎯 Intent | `test_intent`, `test_intent_cases`, `test_intent_engine`, `test_real_groq_intent` | Intent extraction, edge cases, live API |
| 🗺️ Planning | `test_argument_resolver`, `test_capability_selector`, `test_plan_compiler`, `test_planner`, `test_planning_engine`, `test_planning_models` | Capability selection, plan generation, compilation |
| 🛠️ Tools | `test_command_tool`, `test_filesystem_tools`, `test_git_tools`, `test_python_tool`, `test_tool_call`, `test_tool_definition`, `test_tool_executor`, `test_tool_registry`, `test_tool_runtime` | Tool registration, execution, safety |
| 🛡️ Security | `test_safety`, `test_permission`, `test_permissions` | Path traversal, command filtering, permission levels |
| 📡 API | `test_api` | HTTP endpoints |
| 🔗 Integration | `test_phase1_gate`, `test_phase1_final_gate` | End-to-end Phase 1 validation |
| 🤖 LLM | `test_groq_config`, `test_groq_gateway`, `test_model_gateway` | LLM client, auth, responses |
| 💾 Database | `test_database`, `test_task_repository` | Persistence, CRUD |
| 💨 Smoke | `test_smoke` | Basic import check |

---

## 🔄 The Big Picture — How It All Connects

```
👤 USER
   │
   │ "Fix this project"
   ▼
📡 POST /tasks ──────────────────────────────────────────── app/api/main.py
   │
   ▼
💾 TaskRepository.create(task) ──────────────────────────── app/db/repositories/
   │
   ▼
🎯 IntentEngine.parse(goal) ─────────────────────────────── app/intent/engine.py
   │
   ├── 🧠 GroqModelGateway.generate(messages) ──────────── app/llm/groq.py
   │        │
   │        └── 📡 Groq API → structured JSON
   │
   └── ✅ Intent(goal, constraints, forbidden_actions...) ─ app/intent/models.py
   │
   ▼
🗺️ PlanningEngine.compile_intent(intent) ───────────────── app/planning/engine.py
   │
   ├── 🔍 CapabilitySelector.select(intent) ────────────── app/planning/selector.py
   │        │
   │        └── 🧩 [read_file, run_command, ...] ────────── app/planning/capabilities.py
   │
   ├── 🗺️ Planner.build(intent) ────────────────────────── app/planning/planner.py
   │        │
   │        └── 📋 Plan(actions=[...]) ──────────────────── app/planning/models.py
   │
   └── 🔧 PlanCompiler.compile(action) ─────────────────── app/planning/compiler.py
   │
   ▼
🚦 ToolExecutor.execute(tool_call) ──────────────────────── app/tools/executor.py
   │
   ├── 🔍 ToolRegistry.get(name) ───────────────────────── app/tools/registry.py
   ├── 🔐 PermissionKernel.check(name) ─────────────────── app/security/permissions.py
   ├── 🔒 ToolSafety.check(call) ───────────────────────── app/security/safety.py
   ├── ⚙️ ToolRuntime.execute(tool, args) ──────────────── app/tools/runtime.py
   │        │
   │        └── 🛠️ Built-in handlers ───────────────────── app/tools/builtin/
   │             ├── 📁 filesystem.py (read, write, list, move)
   │             ├── ⌨️ command.py (run_command)
   │             ├── 🐙 git.py (status, diff, log)
   │             └── 🐍 python.py (run_python)
   │
   └── 📝 AuditRecorder.record(event) ──────────────────── app/tools/audit.py
   │
   ▼
📊 ToolResult(status, data, error) ──────────────────────── app/models/tool_result.py
   │
   ▼
🏁 Response to user
```

---

> 🎩 *"Sebastian turns natural-language outcomes into verified digital actions."*
