# 🚀 SEBASTIAN — MASTER ROADMAP

> **Build the smallest Sebastian that can reliably finish real tasks, then earn every additional capability.**

## 🎯 Product vision

**Sebastian** is a named AI entity that takes a natural-language outcome and turns it into a **verified digital result**.

### 🔄 Core loop

```text
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
```

### 🧠 AI strategy

Use **pretrained models**. Do **not** train a foundation model.

```text
🤖 Pretrained LLM
      +
🎯 Intent
      +
🔎 Context
      +
🧰 Tools
      +
🗺️ Planning
      +
🛡️ Permissions
      +
⚙️ Execution
      +
✅ Verification
      +
🔁 Recovery
      ↓
🚀 Sebastian
```

The engineering focus is the **harness around the model**, not foundation-model training. fileciteturn11file0L12-L18 fileciteturn11file0L47-L81

---

# 🗺️ Version map

| Version | Phases | Theme | Status |
|---|---:|---|---|
| 🟢 **V1** | **0–11** | Core Execution Engine | 🚧 In progress |
| 🔵 **V2** | **12–13** | Web & Controlled Computer Execution | 🔒 Future |
| 🟣 **V3** | **14–16** | Connected Digital Environment | 🔒 Future |
| 🟠 **V4** | **17** | Persistent Sebastian | 🔒 Future |
| 🔴 **V5** | **18** | Adaptive Sebastian | 🔒 Future |

V1 covers Phases 0–11; V2 covers 12–13; V3 covers 14–16; V4 is Phase 17; and V5 is Phase 18. fileciteturn11file1L623-L664 fileciteturn11file1L668-L718 fileciteturn11file1L722-L730 fileciteturn11file1L409-L446 fileciteturn11file1L450-L487

> **Current working point:** 🟢 **V1 → Phase 2**

---

# 🟢 V1 — CORE EXECUTION ENGINE

**Goal:** Make Sebastian reliably execute real digital tasks on the local computer: files, terminal, Python, Git, documents/data, while building intent, context, planning, permissions, execution, observation, verification, recovery, persistent state, and cancellation. V1 ends at Phase 11. fileciteturn11file1L623-L664

## 🧱 Phase 0 — Foundation

### 🎯 Goal
Build the boring infrastructure correctly.

### 🛠️ Build

- 🐍 Python
- ⚡ FastAPI
- 🗄️ SQLite
- 📐 Pydantic
- 🗃️ SQLAlchemy / SQLModel
- 🧪 pytest
- 📝 structured logging
- ⚙️ configuration
- 🔐 secret handling

### 🧩 Minimum data model

```text
Task
Action
Plan
ToolCall
ExecutionEvent
Permission
Verification
Checkpoint
```

### 🔄 Task lifecycle

```text
PENDING
  ↓
PLANNING
  ↓
WAITING_APPROVAL
  ↓
EXECUTING
  ↓
PAUSED
  ↓
VERIFYING
  ↓
RECOVERING
  ↓
COMPLETED / FAILED / CANCELLED
```

### ✅ Deliverable
A task can be created through the API and persisted.

### 🚦 Gate
Do not proceed until tests run reliably, state persists, failures are logged, and configuration is clean. fileciteturn11file0L86-L156

---

## 🛠️ Phase 1 — Tool Runtime + Permission Kernel

### 🎯 Goal
Make Sebastian able to perform **one controlled action at a time**.

### 🧰 Initial tools

```text
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
```

### 🔐 Every tool follows

```text
📨 Request
   ↓
📐 Schema validation
   ↓
🛡️ Permission check
   ↓
🔒 Safety check
   ↓
⚙️ Execution
   ↓
📦 Structured result
   ↓
📝 Audit event
```

### 🛡️ Permission levels

```text
🟢 AUTONOMOUS
🟡 APPROVAL
🔴 BLOCKED
```

### ✅ Deliverable
Sebastian can safely execute individual actions **without an LLM**.

### 🚦 Gate
Every initial tool must validate input, enforce permission, return structured evidence, log what happened, and fail safely. fileciteturn11file0L160-L257

---

## 🧠 Phase 2 — LLM Gateway + Intent Engine

### 🎯 Goal
Bring the actual model into the system early.

### 🤖 Model abstraction

```text
ModelGateway
├── provider
├── model
├── structured output
├── tool calling
└── usage metadata
```

Start with **one provider**. Do not build provider soup. The architecture should allow adding another provider later.

### 🎯 Intent transformation

Example input:

> “Clean this folder and don't delete anything.”

The output should capture:

```text
🎯 Goal
📏 Constraints
🏁 Expected outcome
🚫 Forbidden actions
❓ Missing information
🛡️ Required permissions
✅ Success criteria
```

### 🧠 Core principle
Sebastian must understand:

> **what should happen**

before deciding:

> **how to make it happen**.

### ✅ Deliverable
Natural language → validated structured task.

### 🚦 Gate
Run varied instructions and confirm that structured intent is stable and predictable. fileciteturn9file0L17-L68

---

## 🔎 Phase 3 — Context Compiler

### 🎯 Goal
Find the **minimum useful context**. Never dump the entire computer into the model.

### 🔍 Progressive discovery

```text
🎯 Goal
 ↓
📚 Candidate sources
 ↓
⚡ Cheap inspection
 ↓
🎯 Relevance filtering
 ↓
🔬 Deep inspection only when needed
 ↓
📦 Context Package
```

### Initial context sources

```text
📁 filesystem
📂 project structure
🐙 Git state
📄 documents
🐍 Python environment
📍 working directory
```

### Context Package

```text
🎯 Goal
📏 Constraints
📚 Relevant context
❓ Missing information
🛡️ Permissions
✅ Success criteria
🔎 Evidence
```

### ✅ Deliverable
Sebastian can discover relevant context for a task.

### 🚦 Gate
Test context selection independently from execution and make it possible to inspect why particular files were considered relevant. fileciteturn9file0L72-L163

---

## 🗺️ Phase 4 — Planner + Action Graph

### 🎯 Goal
Turn intent + context + constraints + permissions + success criteria into a structured plan.

### Each action contains

```text
🆔 action_id
🧰 tool
🧾 arguments
🔒 preconditions
🎯 expected_result
⚠️ risk
⏱️ timeout
🔁 retry_policy
✅ verification_method
↩️ rollback_strategy
```

### 🔀 Branching

```text
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
```

### ✅ Deliverable
Sebastian can generate a complete multi-step action graph.

### 🚦 Gate
The planned graph must be inspectable before execution. fileciteturn9file0L167-L235

---

## ⚙️ Phase 5 — Execution Engine

### 🎯 Goal
Connect Planner → Action Graph → Tool Runtime.

### Implement

```text
➡️ sequential execution
🔀 branching
⏱️ timeouts
🔁 safe retries
🔗 dependencies
📊 action state
🛑 cancellation
```

### 🛑 Cancellation is mandatory

```text
🛑 STOP
 ↓
stop scheduling
 ↓
cancel current cancellable action
 ↓
persist state
 ↓
mark task PAUSED / CANCELLED
```

### ✅ Deliverable
Sebastian can execute multi-step local workflows.

### 🚦 Gate
**No uncontrolled execution.** Every action passes through the runtime. fileciteturn9file0L239-L300

---

## 👀 Phase 6 — Observation + Evidence

### 🎯 Goal
Make actual environment state visible to Sebastian. Every action generates evidence.

### Evidence examples

```text
📁 filesystem changes
⌨️ command output
🔢 exit code
📝 changed files
🐙 Git status
📄 generated files
⚙️ process state
```

### Flow

```text
⚙️ Action
 ↓
🧰 Tool
 ↓
👀 Observation
 ↓
🔎 Evidence
```

### ✅ Deliverable
Sebastian can distinguish **what it intended to happen** from **what actually happened**. fileciteturn9file0L304-L350

---

## ✅ Phase 7 — Verification Engine

### 🚨 Non-negotiable rule

> **Sebastian cannot declare success because the model feels successful.**

### Explicit verifiers

```text
📄 FileExistsVerifier
📝 FileContentVerifier
⌨️ CommandVerifier
🧪 TestSuiteVerifier
🐙 GitVerifier
📄 DocumentVerifier
```

Later:

```text
🌐 BrowserStateVerifier
🔌 APIResponseVerifier
📦 ArtifactVerifier
```

### Verification flow

```text
ACTION
 ↓
OBSERVATION
 ↓
EXPECTED
 ↓
ACTUAL
 ↓
PASS / FAIL
```

### ✅ Deliverable
**No fake “Done.”**

### 🚦 Gate
Every important V1 workflow has explicit verification logic. fileciteturn9file0L354-L440

---

## 🔁 Phase 8 — Recovery Engine

### 🎯 Goal
Failure becomes a normal state.

### Handle

```text
❌ command failure
📦 missing dependency
⏱️ timeout
🔐 permission denial
🌐 network failure
🌀 unexpected state
💥 bad patch
🛠️ wrong tool
```

### Recovery loop

```text
❌ FAIL
 ↓
🔎 Gather evidence
 ↓
🧠 Diagnose
 ↓
🔁 Determine retryability
 ↓
🗺️ Replan
 ↓
🛠️ Alternative action
 ↓
✅ Verify
```

### Important rule
Not every failure is retryable:

```text
🌐 network timeout → likely retry
📦 missing package → diagnose
🔐 permission denied → ask
🗑️ unexpected deletion → stop
⚠️ irreversible action → never blindly retry
```

### ✅ Deliverable
Sebastian can recover from meaningful failures without blindly restarting. fileciteturn10file0L90-L150

---

## 💾 Phase 9 — Persistent Execution State

### 🎯 Goal
Make tasks durable.

### Persist

```text
🎯 Goal
📏 Constraints
🔎 Context
🗺️ Plan
🧩 Actions
✅ Completed actions
▶️ Current action
⏭️ Remaining actions
🛡️ Permissions
📍 Checkpoints
❌ Errors
🔎 Evidence
✅ Verification results
```

### 💥 Crash recovery

```text
💥 Sebastian crashes
 ↓
🔄 Restart
 ↓
📂 Load task
 ↓
📍 Load checkpoint
 ↓
👀 Inspect actual environment
 ↓
🧠 Determine safe continuation
 ↓
▶️ Resume
```

Never blindly resume from a saved action. Re-check the actual state first.

### ✅ Deliverable
Long-running tasks survive crashes and restarts where safe. fileciteturn10file0L154-L210

---

## 🧪 Phase 10 — Early Benchmark

### 🎯 Goal
Before browser automation, test the core engine.

Build roughly **10–15 representative tasks** across:

```text
📁 files
🐍 Python
🐙 Git
📊 data
📄 documents
💥 failure cases
🛡️ permission cases
```

### Track

```text
🎯 success
🔎 context correctness
🛠️ tool correctness
✅ verification correctness
🔁 recovery
👤 intervention
🛡️ policy compliance
⚡ latency
```

### ✅ Deliverable
A measurable baseline. fileciteturn10file0L214-L253

---

## 🏆 Phase 11 — V1 Capstone

### 🎯 Goal
Prove the core idea with real end-to-end tasks.

### 🧑‍💻 Demo 1 — Developer

> “This Python project is broken. Fix it.”

```text
🔎 discover
 ↓
📚 context
 ↓
🗺️ plan
 ↓
⚙️ run
 ↓
👀 observe
 ↓
🧠 diagnose
 ↓
✏️ modify
 ↓
🧪 test
 ↓
✅ verify
```

### 📊 Demo 2 — Data

> “Analyze this dataset and create the report.”

```text
🔎 find data
 ↓
🧠 understand
 ↓
🗺️ plan
 ↓
📊 analyze
 ↓
📦 create artifact
 ↓
💾 save
 ↓
✅ verify
```

### 🧹 Demo 3 — Files

> “Clean up this folder. Don't permanently delete anything.”

```text
🔎 inspect
 ↓
🏷️ classify
 ↓
🗂️ organize
 ↓
♻️ detect duplicates
 ↓
🛡️ respect policy
 ↓
✅ verify
```

### ✅ V1 acceptance criteria

Sebastian must demonstrate:

```text
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
```

### 🚨 Rule
If Sebastian is unreliable at this capstone, **STOP EXPANDING.** Fix the core system before adding Gmail, Calendar, MCP, RAG, multi-agent systems, desktop control, or long-running workflows. fileciteturn10file0L257-L376

---

# 🔵 V2 — WEB & CONTROLLED COMPUTER EXECUTION

**Phases 12–13**

Goal: Expand Sebastian from local execution into reliable interaction with the web and selected desktop capabilities. fileciteturn11file1L668-L718

## 🌐 Phase 12 — Browser Execution

### 🎯 Goal
Introduce a controlled browser using Playwright or an equivalent approach.

### Browser flow

```text
🔎 Inspect page
 ↓
🧠 Determine state
 ↓
🗺️ Plan browser action
 ↓
⚙️ Execute
 ↓
👀 Observe
 ↓
✅ Verify
```

Not blind click sequences.

### Handle

```text
🔐 authentication
🌀 dynamic UI
⏳ session expiration
🌐 network problems
🧩 unexpected layouts
🧱 CAPTCHAs
```

### ✅ Deliverable
Several meaningful browser workflows that survive normal state changes. fileciteturn10file0L380-L437

---

## 🖥️ Phase 13 — Controlled Desktop Interaction

### 🎯 Goal
Expand into selected OS/application interaction.

### Potential capabilities

```text
📸 screenshots
📋 clipboard
🪟 window inspection
🚀 application launching
🖱️ basic application interaction
🔔 notifications
```

Every action remains:

```text
📨 request
 ↓
📐 validation
 ↓
🛡️ permission
 ↓
🔒 safety
 ↓
⚙️ execution
 ↓
👀 observation
 ↓
✅ verification
 ↓
📝 audit
```

**Not unrestricted control.** fileciteturn10file0L441-L488

---

# 🟣 V3 — CONNECTED DIGITAL ENVIRONMENT

**Phases 14–16**

Goal: Make Sebastian useful across connected digital services while improving the AI harness itself. fileciteturn11file1L722-L730

## 🧠 Phase 14 — Model Engineering / Optimization

Improve:

```text
🔀 model routing
🛟 fallback models
📐 structured-output reliability
🛠️ tool-selection quality
🗜️ context compression
💸 cost
⚡ latency
🔌 provider abstraction
```

Potential model roles:

```text
🎯 intent
🗺️ planning
🧠 diagnosis
🔎 context selection
❓ ambiguous decisions
```

Deterministic code remains responsible for:

```text
🛡️ permissions
💾 state
⏱️ timeouts
🔁 retry logic
🔐 security
✅ verification
```

🚫 **No foundation-model training.** fileciteturn10file0L492-L543

---

## 📊 Phase 15 — Full Evaluation

### 🎯 Goal
Build the serious benchmark: **50–100 tasks**.

### Categories

```text
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
```

### Measure

```text
🎯 completion rate
🔎 context accuracy
🛠️ tool-selection accuracy
✅ verification accuracy
🔁 recovery rate
👤 intervention rate
🛡️ policy compliance
⚡ latency
💸 cost
```

Separate success from safe failure, unsafe behavior, false success, and unnecessary intervention. **False success is particularly serious.** fileciteturn10file0L545-L610

---

## 🔌 Phase 16 — External Services

Potential integrations:

```text
📧 Gmail
📅 Calendar
☁️ Drive
🐙 GitHub APIs
📝 Notion
💬 Slack
📱 Telegram
```

These are tool domains **inside the same Sebastian runtime**, not separate “agents.”

### 🎯 V3 goal
> **Sebastian becomes a unified execution layer across the user's connected digital environment.** fileciteturn11file1L381-L405

---

# 🟠 V4 — PERSISTENT SEBASTIAN

## ⏳ Phase 17 — Long-Running Responsibility

### 🎯 Goal
Move from one-shot tasks to **long-running responsibility**.

```text
🎯 Task
 ↓
⏳ Wait
 ↓
🔔 Event
 ↓
🔎 Re-evaluate context
 ↓
⚙️ Act
 ↓
✅ Verify
 ↓
⏳ Continue waiting
```

Example responsibilities:

> “Watch this GitHub issue and act when the reviewer responds.”

> “Track this application and tell me when I need to respond.”

### 🎯 V4 goal
Sebastian can remain responsible for a task over time instead of only acting once. fileciteturn11file1L409-L446

---

# 🔴 V5 — ADAPTIVE SEBASTIAN

## 🧩 Phase 18 — Reusable Automation

### 🎯 Goal
Recognize repeated workflows and propose turning them into reusable automations.

```text
👀 Observe repeated behavior
 ↓
🧩 Detect pattern
 ↓
🔎 Identify variables
 ↓
🧠 Generalize workflow
 ↓
💡 Suggest automation
 ↓
👤 User approves
 ↓
⚡ Reusable workflow
```

### 🔐 Important
Sebastian **suggests** automation. It does **not** secretly create autonomous behavior.

### 🎯 V5 goal
Sebastian becomes increasingly useful by learning which workflows the user repeatedly performs. fileciteturn11file1L450-L487

---

# 🧭 Overall evolution

```text
🟢 V1 — CORE EXECUTION
"Sebastian can do real work."
        ↓
🔵 V2 — WEB + COMPUTER
"Sebastian can operate digital interfaces."
        ↓
🟣 V3 — CONNECTED ENVIRONMENT
"Sebastian can work across my services."
        ↓
🟠 V4 — PERSISTENT EXECUTION
"Sebastian can stay responsible for work."
        ↓
🔴 V5 — ADAPTIVE AUTOMATION
"Sebastian can recognize and automate repeated work."
```

---

# 🧠 Engineering rules

## 🎯 Permanent success metric

> **How reliably can Sebastian turn an outcome into a verified result?**

## 🤖 AI vs deterministic engineering

### Use AI for

```text
🧠 interpretation
🗺️ planning
🔎 context selection
🧠 diagnosis
❓ ambiguous decisions
```

### Use deterministic code for

```text
🛡️ permissions
💾 state
⏱️ timeouts
🔁 retries
🔐 security
✅ validation
✅ verification
```

Do not use an LLM everywhere just because it is possible. fileciteturn8file4L1004-L1026

## 🏗️ Architecture philosophy

Prefer:

```text
✅ simple
✅ modular
✅ observable
✅ typed
✅ testable
✅ replaceable
```

over:

```text
❌ fashionable
❌ distributed
❌ complicated
❌ "enterprise"
```

A modular monolith is completely acceptable. Do not introduce Kubernetes, Kafka, Redis, BullMQ, microservices, vector databases, etc. without a real requirement. fileciteturn8file3L756-L776

## 🚫 Scope-control rule

Before adding a feature or technology, ask:

> **Does this directly improve Sebastian's ability to turn an outcome into a verified result?**

If not:

> **DEFER IT.**

## 🎩 Sebastian's behavior

Sebastian should feel:

> **Calm. Competent. Transparent. Cautious. Persistent.**

Never claim “Done” without evidence. fileciteturn8file3L796-L814

## 🔒 Development rule

The roadmap is **frozen**.

```text
🔒 Frozen Context
      ↓
📋 Roadmap
      ↓
🧱 Current Phase
      ↓
🛠️ Implement
      ↓
🧪 Test
      ↓
✅ Pass Gate
      ↓
➡️ Next Phase
```

Do not redesign Sebastian, randomly add integrations, jump ahead, train models, overengineer infrastructure, or skip gates. fileciteturn8file3L818-L858

---

# 🏆 Version gates

## 🟢 V1 hard gate — Phase 11

Before leaving V1, Sebastian must prove:

```text
✅ Intent understanding
✅ Context discovery
✅ Planning
✅ Typed tools
✅ Permission enforcement
✅ Execution
✅ Structured observation
✅ Verification
✅ Failure handling
✅ Persistent state
✅ Cancellation
```

If V1 is unreliable: **STOP EXPANDING. Fix Sebastian.** fileciteturn8file4L938-L967

## 🔵 V2 gate

V2 expands into web and selected desktop environments only after V1 is reliable.

## 🟣 V3 gate

V3 expands into connected services and stronger model/evaluation infrastructure only after the earlier system is reliable.

## 🟠 V4 gate

V4 adds long-running responsibility only when persistent execution is trustworthy.

## 🔴 V5 gate

V5 adds reusable automation suggestions while preserving explicit user approval.

> **Versions are not deadlines. They are earned through reliability.** fileciteturn11file1L520-L538

---

# 📋 Phase tracker

| Phase | Version | Theme | Status |
|---:|---|---|---|
| 0 | 🟢 V1 | 🧱 Foundation | ✅ Complete |
| 1 | 🟢 V1 | 🛠️ Tool Runtime + Permission Kernel | ✅ Complete |
| 2 | 🟢 V1 | 🧠 LLM Gateway + Intent Engine | 🚀 **Current** |
| 3 | 🟢 V1 | 🔎 Context Compiler | 🔒 Locked |
| 4 | 🟢 V1 | 🗺️ Planner + Action Graph | 🔒 Locked |
| 5 | 🟢 V1 | ⚙️ Execution Engine | 🔒 Locked |
| 6 | 🟢 V1 | 👀 Observation + Evidence | 🔒 Locked |
| 7 | 🟢 V1 | ✅ Verification Engine | 🔒 Locked |
| 8 | 🟢 V1 | 🔁 Recovery Engine | 🔒 Locked |
| 9 | 🟢 V1 | 💾 Persistent Execution State | 🔒 Locked |
| 10 | 🟢 V1 | 🧪 Early Benchmark | 🔒 Locked |
| 11 | 🟢 V1 | 🏆 V1 Capstone | 🔒 Locked |
| 12 | 🔵 V2 | 🌐 Browser Execution | 🔒 Locked |
| 13 | 🔵 V2 | 🖥️ Controlled Desktop Interaction | 🔒 Locked |
| 14 | 🟣 V3 | 🧠 Model Engineering / Optimization | 🔒 Locked |
| 15 | 🟣 V3 | 📊 Full Evaluation | 🔒 Locked |
| 16 | 🟣 V3 | 🔌 External Services | 🔒 Locked |
| 17 | 🟠 V4 | ⏳ Persistent / Long-Running Responsibility | 🔒 Locked |
| 18 | 🔴 V5 | 🧩 Adaptive Automation | 🔒 Locked |

---

# 🔥 THE ONE RULE

> **Build the smallest Sebastian that can reliably finish real tasks, then earn every additional capability.**

### 🎯 Permanent success metric

> **How reliably can Sebastian turn an outcome into a verified result?**

---

## 📚 Source basis

This roadmap preserves the phase structure, gates, version grouping, scope-control rules, and long-term evolution from the frozen Sebastian roadmap used for the project. fileciteturn11file0L86-L160 fileciteturn9file0L167-L300 fileciteturn10file0L257-L376 fileciteturn11file1L623-L718
