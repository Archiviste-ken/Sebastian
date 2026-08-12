🚀 SEBASTIAN — FINAL EXECUTABLE ROADMAP
The final product
Sebastian

A named AI entity that takes a natural-language outcome and turns it into a verified digital result.

🔄 The core loop
🎯 INTENT
    ↓
🔎 CONTEXT
    ↓
🗺️ PLAN
    ↓
🛡️ PERMISSION
    ↓
⚙️ EXECUTE
    ↓
👀 OBSERVE
    ↓
✅ VERIFY
    ↓
🔁 RECOVER
    ↓
💾 PERSIST
    ↓
🏁 VERIFIED OUTCOME
Philosophy

You give Sebastian the outcome. You do not micromanage the procedure.

🧠 AI strategy

Use pretrained models.

Do not train a foundation model.

Your engineering work is the harness around the model:

Pretrained LLM
    +
Intent
    +
Context
    +
Tools
    +
Planning
    +
Permissions
    +
Execution
    +
Verification
    +
Recovery
    ↓
Sebastian

🧱 PHASE 0 — FOUNDATION

🎯 Goal

Build the boring infrastructure correctly.

🛠️ Build
🐍 Python
⚡ FastAPI
🗄️ SQLite
📐 Pydantic
🗃️ SQLAlchemy/SQLModel
🧪 pytest
📝 structured logging
⚙️ configuration
🔐 secret handling

Create the minimum data model:

Task
Action
Plan
ToolCall
ExecutionEvent
Permission
Verification
Checkpoint
🔄 Task lifecycle

Define the state machine early:

PENDING
PLANNING
WAITING_APPROVAL
EXECUTING
PAUSED
VERIFYING
RECOVERING
COMPLETED
FAILED
CANCELLED
✅ Deliverable

You can create a task through the API and persist it.

🚦 Gate

Do not proceed until:

tests run reliably
state persists
failures are logged
configuration is clean
🛠️ PHASE 1 — TOOL RUNTIME + PERMISSION KERNEL
🎯 Goal

Make Sebastian able to perform one controlled action at a time.

Initial tools
📖 read_file()
📂 list_directory()
✏️ write_file()
📁 create_directory()
🔀 move_file()
⌨️ run_command()
🐍 run_python()
🐙 git_status()
🐙 git_diff()
🐙 git_log()
🔐 Every tool follows
Request
 ↓
Schema validation
 ↓
Permission check
 ↓
Safety check
 ↓
Execution
 ↓
Structured result
 ↓
Audit event
🛡️ Permission kernel

Start with:

🟢 AUTONOMOUS
🟡 APPROVAL
🔴 BLOCKED
📦 Tool result

Never:

"done"

Use structured results:

{
  "success": true,
  "exit_code": 0,
  "stdout": "...",
  "stderr": "...",
  "evidence": {},
  "side_effects": []
}
✅ Deliverable

Sebastian can safely execute individual actions without an LLM.

🚦 Gate

Every initial tool must:

validate input
enforce permission
return structured evidence
log what happened
fail safely
🧠 PHASE 2 — LLM GATEWAY + INTENT ENGINE
🎯 Goal

Bring the actual model into the system early.

Model abstraction
ModelGateway
 ├── provider
 ├── model
 ├── structured output
 ├── tool calling
 └── usage metadata

Start with one provider.

Do not build provider soup.

The architecture should allow adding another provider later.

🎯 Intent transformation

Input:

“Clean this folder and don't delete anything.”

Output:

Goal
Constraints
Expected outcome
Forbidden actions
Missing information
Required permissions
Success criteria
Important

Sebastian must understand:

what should happen

before deciding:

how to make it happen.

✅ Deliverable

Natural language → validated structured task.

🚦 Gate

Run a test set of varied instructions and confirm that structured intent is stable and predictable.

🔎 PHASE 3 — CONTEXT COMPILER
🎯 Goal

Find the minimum useful context.

Never dump the entire computer into the model.

Progressive discovery
Goal
 ↓
Candidate sources
 ↓
Cheap inspection
 ↓
Relevance filtering
 ↓
Deep inspection only when needed
 ↓
Context Package
Initial context sources
📁 filesystem
📂 project structure
🐙 Git state
📄 documents
🐍 Python environment
📍 working directory
Context package
Goal
Constraints
Relevant context
Missing information
Permissions
Success criteria
Evidence
Example

“Fix this Python project.”

Sebastian should discover:

project location
↓
project metadata
↓
dependencies
↓
entry points
↓
tests
↓
failure

not recursively read everything.

✅ Deliverable

Sebastian can discover relevant context for a task.

🚦 Gate

Test context selection independently from execution.

You should be able to inspect:

“Why did Sebastian decide these files were relevant?”

🗺️ PHASE 4 — PLANNER + ACTION GRAPH
🎯 Goal

Turn:

Intent
+
Context
+
Constraints
+
Permissions
+
Success criteria

into a structured plan.

Each action
action_id
tool
arguments
preconditions
expected_result
risk
timeout
retry_policy
verification_method
rollback_strategy
🔀 Support branching
Run project
   ↓
success?
 ┌─┴─┐
yes  no
 ↓    ↓
verify diagnose
       ↓
      fix
       ↓
      retry
✅ Deliverable

Sebastian can generate a complete multi-step action graph.

🚦 Gate

Before executing anything, you can inspect the planned graph.

This gives you debuggability.

⚙️ PHASE 5 — EXECUTION ENGINE
🎯 Goal

Connect:

Planner
 ↓
Action Graph
 ↓
Tool Runtime
Implement
➡️ sequential execution
🔀 branching
⏱️ timeouts
🔁 safe retries
🔗 dependencies
📊 action state
🛑 cancellation
🛑 Cancellation is mandatory

User can always:

STOP

Then:

stop scheduling
↓
cancel current cancellable action
↓
persist state
↓
mark task PAUSED/CANCELLED
✅ Deliverable

Sebastian can execute multi-step local workflows.

🚦 Gate

No uncontrolled execution.

Every action passes through the runtime.

👀 PHASE 6 — OBSERVATION + EVIDENCE
🎯 Goal

Make actual environment state visible to Sebastian.

Every action generates evidence.

Examples:

📁 filesystem changes
⌨️ command output
🔢 exit code
📝 changed files
🐙 Git status
📄 generated files
⚙️ process state
Flow
Action
 ↓
Tool
 ↓
Observation
 ↓
Evidence
✅ Deliverable

Sebastian can distinguish:

what it intended to happen

from:

what actually happened.

✅ PHASE 7 — VERIFICATION ENGINE

This is one of the most important phases.

🚨 Non-negotiable rule

Sebastian cannot declare success because the model feels successful.

Build explicit verifiers
FileExistsVerifier
FileContentVerifier
CommandVerifier
TestSuiteVerifier
GitVerifier
DocumentVerifier

Later:

BrowserStateVerifier
APIResponseVerifier
ArtifactVerifier
Verification
ACTION
 ↓
OBSERVATION
 ↓
EXPECTED
 ↓
ACTUAL
 ↓
PASS / FAIL
Example — Code task
modify
 ↓
run tests
 ↓
test result
 ↓
verify behavior
Example — File task
move
 ↓
check source
 ↓
check destination
 ↓
check integrity
✅ Deliverable

No fake “Done.”

🚦 Gate

Every important V1 workflow has explicit verification logic.

🔁 PHASE 8 — RECOVERY ENGINE
🎯 Goal

Failure becomes a normal state.

Handle:

❌ command failure
📦 missing dependency
⏱️ timeout
🔐 permission denial
🌐 network failure
🌀 unexpected state
💥 bad patch
🛠️ wrong tool
Recovery
FAIL
 ↓
Gather evidence
 ↓
Diagnose
 ↓
Determine retryability
 ↓
Replan
 ↓
Alternative action
 ↓
Verify
Important rule

Not every failure is retryable.

network timeout → likely retry
missing package → diagnose
permission denied → ask
unexpected deletion → stop
irreversible action → never blindly retry
✅ Deliverable

Sebastian can recover from meaningful failures without blindly restarting.

💾 PHASE 9 — PERSISTENT EXECUTION STATE
🎯 Goal

Make tasks durable.

Store:

Goal
Constraints
Context
Plan
Actions
Completed actions
Current action
Remaining actions
Permissions
Checkpoints
Errors
Evidence
Verification results
💥 Crash recovery
Sebastian crashes
 ↓
Restart
 ↓
Load task
 ↓
Load checkpoint
 ↓
Inspect actual environment
 ↓
Determine safe continuation
 ↓
Resume
Important

Do not blindly resume from a saved action.

Re-check actual state first.

✅ Deliverable

Long-running tasks survive crashes and restarts where safe.

🧪 PHASE 10 — EARLY BENCHMARK

Before adding browser automation, test the core engine.

Build roughly 10–15 representative tasks.

Categories
📁 files
🐍 Python
🐙 Git
📊 data
📄 documents
💥 failure cases
🛡️ permission cases
Track
🎯 success
🔎 context correctness
🛠️ tool correctness
✅ verification correctness
🔁 recovery
👤 intervention
🛡️ policy compliance
⚡ latency
✅ Deliverable

A measurable baseline.

🏆 PHASE 11 — V1 CAPSTONE

This is the hard gate.

Now Sebastian must prove the core idea.

🧑‍💻 Demo 1 — Developer

“This Python project is broken. Fix it.”

discover
 ↓
context
 ↓
plan
 ↓
run
 ↓
observe
 ↓
diagnose
 ↓
modify
 ↓
test
 ↓
verify
📊 Demo 2 — Data

“Analyze this dataset and create the report.”

find data
 ↓
understand
 ↓
plan
 ↓
analyze
 ↓
create artifact
 ↓
save
 ↓
verify
🧹 Demo 3 — Files

“Clean up this folder. Don't permanently delete anything.”

inspect
 ↓
classify
 ↓
organize
 ↓
detect duplicates
 ↓
respect policy
 ↓
verify
✅ V1 acceptance criteria

Sebastian must demonstrate:

✅ intent understanding
✅ context discovery
✅ planning
✅ typed tools
✅ permission enforcement
✅ execution
✅ structured observation
✅ verification
✅ failure handling
✅ persistent state
✅ cancellation
🚨 THE RULE

If Sebastian is unreliable here:

STOP EXPANDING.

Do not touch:

Gmail
Calendar
MCP
RAG
multi-agent systems
desktop control
long-running workflows

Fix Sebastian.

🌐 PHASE 12 — BROWSER EXECUTION

Only after V1 passes.

🎯 Goal

Introduce a controlled browser.

Use Playwright or equivalent.

Browser flow
Inspect page
 ↓
Determine state
 ↓
Plan browser action
 ↓
Execute
 ↓
Observe
 ↓
Verify

Not:

click
click
click
hope
Handle
🔐 authentication
🌀 dynamic UI
⏳ session expiration
🌐 network problems
🧩 unexpected layouts
🧱 CAPTCHAs
✅ Deliverable

Several meaningful browser workflows that survive normal state changes.

🖥️ PHASE 13 — CONTROLLED DESKTOP INTERACTION
🎯 Goal

Expand into selected OS/application interaction.

Potential capabilities
📸 screenshots
📋 clipboard
🪟 window inspection
🚀 application launching
🖱️ basic application interaction
🔔 notifications

Every action:

request
 ↓
validation
 ↓
permission
 ↓
safety
 ↓
execution
 ↓
observation
 ↓
verification
 ↓
audit
✅ Deliverable

Sebastian can safely interact with selected desktop capabilities.

Not unrestricted control.

🧠 PHASE 14 — MODEL ENGINEERING / OPTIMIZATION

Now improve the AI layer.

Potential improvements
🔀 model routing
🛟 fallback models
📐 structured output reliability
🛠️ tool-selection improvement
🗜️ context compression
💸 cost optimization
⚡ latency optimization
🔌 provider abstraction
Potential model roles
🎯 intent
🗺️ planning
🧠 diagnosis
🔎 context selection
❓ ambiguous decisions

Deterministic code remains responsible for:

🛡️ permissions
💾 state
⏱️ timeouts
🔁 retry logic
🔐 security
✅ verification
🚫 No foundation-model training.

You are an AI engineer building systems around models.

📊 PHASE 15 — FULL EVALUATION

Now build the serious benchmark.

Target

50–100 tasks

Categories
📁 file operations
🧑‍💻 developer workflows
📊 data tasks
📄 documents
🐙 Git
🌐 browser
🔎 research
🔀 mixed workflows
💥 failure scenarios
🛡️ permission scenarios
Measure
🎯 completion rate
🔎 context accuracy
🛠️ tool selection accuracy
✅ verification accuracy
🔁 recovery rate
👤 intervention rate
🛡️ policy compliance
⚡ latency
💸 cost

Separate:

✅ success
🟡 partial success
🛡️ safe failure
🔴 unsafe behavior
❌ false success
👤 unnecessary intervention
🚨 Important

False success is particularly serious.

A system that says:

“Done”

when it isn't done is worse than one that admits failure.

🔌 PHASE 16 — EXTERNAL SERVICES

Only now.

Possible additions:

📧 Gmail
📅 Calendar
☁️ Drive
🐙 GitHub APIs
📝 Notion
💬 Slack
📱 Telegram

Each integration is a tool domain.

There should not be:

Gmail Agent
Calendar Agent
Notion Agent

The same Sebastian runtime should operate them.

✅ Deliverable

One unified execution system across multiple external services.

⏳ PHASE 17 — LONG-RUNNING EXECUTION

Now Sebastian can maintain responsibility over time.

Task
 ↓
Wait
 ↓
Event
 ↓
Re-evaluate context
 ↓
Act
 ↓
Verify
 ↓
Wait again

Examples:

“Watch this GitHub issue and act when the reviewer responds.”

“Track this application and tell me when I need to respond.”

✅ Deliverable

Persistent tasks with safe event-driven execution.

🧠 PHASE 18 — WORKFLOW LEARNING

Final stretch.

Sebastian recognizes repetitive workflows:

Observe repeated behavior
 ↓
Detect pattern
 ↓
Identify variables
 ↓
Generalize workflow
 ↓
Suggest automation
 ↓
User approves
 ↓
Create reusable workflow

Example:

“You perform this exact process every Monday. Would you like me to automate it?”

Important

Sebastian suggests automation.

It does not secretly create autonomous behavior.

🏁 WHAT “FINISHED” MEANS

The project is finished when Sebastian can reliably do the following.

Core
Natural language outcome
        ↓
Intent
        ↓
Context
        ↓
Plan
        ↓
Permissions
        ↓
Execution
        ↓
Observation
        ↓
Verification
        ↓
Recovery
        ↓
Persistent state
        ↓
Verified result
Environment

At minimum:

💻 Local computer
📁 Files
⌨️ Terminal
🐍 Python
🐙 Git/GitHub
📄 Documents
🌐 Browser
Reliability

It can:

🔁 recover
⏸️ pause
🛑 cancel
▶️ resume
✅ verify
🛡️ refuse unsafe actions
❓ ask when necessary
Evaluation

It has a real benchmark demonstrating:

🎯 completion
✅ verification
🔁 recovery
🔎 context accuracy
🛠️ tool accuracy
🛡️ policy compliance
👤 human intervention

At that point, you have a completed serious AI-engineering project.

Everything after that is expansion.

🚫 PERMANENTLY OUT OF SCOPE UNLESS A REAL NEED APPEARS

These are not milestones you must finish:

❌ Training your own foundation model
❌ Building GPT from scratch
❌ CUDA research
❌ Custom transformer architecture
❌ Multi-agent swarm
❌ Vector database for no reason
❌ RAG for no reason
❌ MCP everywhere
❌ Kubernetes
❌ Microservice explosion
❌ Distributed queues just for architecture points
❌ Voice assistant
❌ Mobile app
❌ Billing system
❌ Multi-tenant SaaS

If a future requirement genuinely needs one of them, reassess it then.

🧠 THE TECHNOLOGY RULE

Prefer:

✅ simple
✅ observable
✅ typed
✅ testable
✅ replaceable

over:

❌ fashionable
❌ distributed
❌ complicated
❌ “enterprise”

A modular monolith is completely acceptable.

A Python/FastAPI + SQLite/Postgres + model API + typed tool runtime + Playwright system is enough to make this project extremely serious.

You do not need 15 infrastructure technologies to prove you're an AI engineer.