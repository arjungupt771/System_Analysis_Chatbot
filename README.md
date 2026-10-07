# 🖥️ System Analysis Chatbot

> An AI-powered Windows system analysis assistant that combines **Google Gemini**, deterministic system diagnostics, natural-language command routing, controlled Windows tools, and a risk-based safety layer.

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Tests](https://img.shields.io/badge/Tests-28%2F28%20Passing-2ea44f)](#-testing)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)](#-platform-support)

</p>

---

## 📌 Overview

**System Analysis Chatbot** is a local AI-powered desktop assistant designed to help users inspect and interact with their Windows system through natural-language commands.

The project combines:

- 🤖 Google Gemini for conversational AI and system explanation
- 🧠 Intent-based command routing
- 🖥️ Windows system analysis
- 📦 Installed software discovery
- ⚙️ Process analysis
- 🚀 Startup application analysis
- 💾 Large-file and storage analysis
- 📥 Controlled software installation and verification
- 🔐 Risk-based safety and approval
- 🛡️ Allowlisted Windows application launching
- 🧪 Automated testing

The project intentionally separates **AI reasoning from system execution**.

Instead of allowing an LLM to directly execute arbitrary operating-system commands, requests pass through a controlled execution pipeline.

---

# 🧠 Core Architecture

```text
                    ┌──────────────────────┐
                    │     User Input       │
                    │  Natural Language    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Command Router    │
                    │                      │
                    │ Intent + Confidence  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Safety / Approval  │
                    │                      │
                    │ Risk Classification  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Tool Executor     │
                    │                      │
                    │ Controlled Dispatch  │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │  Software   │  │   System    │  │   Windows   │
       │    Tools    │  │   Analysis  │  │   Actions   │
       │             │  │             │  │             │
       │ Scan        │  │ Processes   │  │ Open URL    │
       │ Install     │  │ Startup     │  │ Launch App  │
       │ Verify      │  │ Storage     │  │             │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Structured Results   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Gemini Analysis    │
                    │ & Human Explanation  │
                    └──────────────────────┘
```

### Design Principle

> **AI interprets what the user wants. Deterministic tools determine what is actually happening.**

This separation makes the system easier to test, extend, and control.

---

# ✨ Features

## 🤖 Gemini-Powered System Diagnosis

The application combines deterministic system measurements with Gemini-powered reasoning.

Gemini can explain findings related to:

- CPU health
- Memory utilization
- Storage conditions
- Installed software
- Software-health findings
- Overall system-health observations

The AI is **not treated as the source of truth for raw system measurements**.

Instead:

```text
System Metrics
      ↓
Deterministic Analysis
      ↓
Structured Findings
      ↓
Gemini
      ↓
Human-readable Explanation
```

This reduces the possibility of the model inventing system facts.

---

## 🧠 Natural-Language Command Routing

User commands are converted into structured intents before reaching system tools.

### Supported intents

| Intent | Purpose |
|---|---|
| `SYSTEM_INFO` | Retrieve system information |
| `SOFTWARE_SCAN` | Scan installed software |
| `PROCESS_ANALYSIS` | Analyze running processes |
| `STARTUP_ANALYSIS` | Analyze Windows startup applications |
| `STORAGE_ANALYSIS` | Find large files |
| `SOFTWARE_INSTALL` | Install supported software |
| `OPEN_URL` | Open a URL |
| `LAUNCH_APPLICATION` | Launch an approved Windows application |
| `CHAT` | Normal conversational interaction |
| `UNKNOWN` | Unrecognized command |

### Example

```text
"show running processes"
          │
          ▼
    Command Router
          │
          ▼
 PROCESS_ANALYSIS
          │
          ▼
 Process Analyzer
          │
          ▼
 Structured Result
```

The router therefore keeps **intent recognition separate from execution**.

---

# 🖥️ Windows System Analysis

The current implementation is focused specifically on **Windows**.

Windows-specific APIs and system interfaces are used where appropriate, while the higher-level architecture remains modular enough to support additional platforms later.

---

## 📦 Installed Software Analysis

Installed Windows software can be discovered using:

- Windows AppX packages
- Windows Registry
- Win32 application registry entries
- 32-bit registry entries

Collected information can include:

- Application name
- Version
- Publisher
- Installation location
- Installation metadata

### Software Health Analysis

The software-health layer can identify:

- Missing installation paths
- Missing versions
- Missing publishers
- Duplicate application names
- Large installed applications

---

## ⚙️ Process Analysis

The process analyzer uses `psutil` to inspect running Windows processes.

It can analyze:

- CPU usage
- Memory usage
- Process count
- Process status
- Process ownership

### Example commands

```text
show running processes
```

```text
what is using my cpu
```

```text
show top memory processes
```

The analyzer produces structured results that can then be displayed or passed into the AI explanation layer.

---

## 🚀 Windows Startup Analysis

The startup analyzer inspects Windows Registry startup locations.

Currently checked locations include:

```text
HKCU
HKLM
HKLM 32-bit
```

### Example commands

```text
startup apps
```

```text
show startup programs
```

```text
what starts with Windows
```

Returned information includes:

- Application name
- Startup command
- Registry source

---

## 💾 Storage Analysis

The storage analyzer searches the Windows filesystem for large files.

It supports:

- Configurable traversal depth
- Configurable result limits
- File-size sorting
- Permission-error handling
- Missing-file handling
- Windows system-directory exclusions

### Example commands

```text
show largest files
```

```text
find large files
```

```text
what is using my storage
```

Results include:

- File name
- Full path
- Size in MB
- Size in GB

---

# 📥 Software Installation & Verification

The project includes a controlled software installation pipeline.

```text
User Request
     │
     ▼
Command Router
     │
     ▼
Safety Layer
     │
     ▼
User Approval
     │
     ▼
Download
     │
     ▼
Windows Installer
     │
     ▼
Installation Verification
     │
     ▼
Confirmed Result
```

A completed installer process alone is **not considered sufficient evidence of successful installation**.

After installation, the application performs a verification step to determine whether the software is actually detected on the system.

---

# 🔐 Safety & Approval System

Every executable system action is associated with a risk level.

| Action | Risk | Confirmation |
|---|---|---|
| System information | 🟢 Low | No |
| Software scan | 🟢 Low | No |
| Process analysis | 🟢 Low | No |
| Startup analysis | 🟢 Low | No |
| Storage analysis | 🟢 Low | No |
| Open URL | 🟢 Low | No |
| Launch application | 🟡 Medium | Yes |
| Software installation | 🔴 High | Yes |
| Unknown action | 🔴 High | Yes |

The safety layer is implemented independently from the Streamlit UI.

This means an action cannot simply bypass the normal safety policy by reaching an underlying tool through the standard execution pipeline.

---

# 🛡️ Controlled Windows Actions

## Application Allowlist

The project does not allow arbitrary application strings to be passed directly to a shell.

Currently supported applications include:

```text
notepad
calculator
calc
```

Application launching uses:

```python
subprocess.Popen(
    ["notepad.exe"],
    shell=False
)
```

rather than unrestricted shell execution.

This provides an additional protection layer against arbitrary command execution.

---

## URL Actions

URLs can be opened through a dedicated tool:

```text
open https://example.com
```

URL handling is separated from application launching and follows its own execution path.

---

# 🏗️ Tool-Based Architecture

The system uses a registry and executor pattern for system capabilities.

```text
User Command
     │
     ▼
Command Router
     │
     ▼
Structured Intent
     │
     ▼
Tool Registry
     │
     ▼
Safety Policy
     │
     ▼
Tool Executor
     │
     ▼
Controlled Function
     │
     ▼
Structured Result
```

This architecture allows new system capabilities to be added without turning the chatbot into an unrestricted command shell.

---

# 🧩 Core Components

## `command_router.py`

Converts natural-language commands into structured `RoutedCommand` objects.

Example:

```python
RoutedCommand(
    intent=CommandIntent.PROCESS_ANALYSIS,
    command="show running processes",
    confidence=0.90
)
```

The router determines:

- User intent
- Original command
- Confidence score
- Whether confirmation may be required

---

## `tool_registry.py`

Maintains the controlled mapping between command intents and executable tools.

Conceptually:

```text
Intent
  ↓
Tool Registry
  ↓
Approved Function
```

This prevents arbitrary user input from being directly mapped to arbitrary Python functions.

---

## `tool_executor.py`

Responsible for controlled tool execution.

The executor:

1. Receives a routed command
2. Resolves the associated tool
3. Retrieves its safety policy
4. Determines whether confirmation is required
5. Executes the tool if permitted
6. Returns a structured result
7. Handles execution errors

---

## `safety.py`

Centralizes risk classification and approval policies.

Unknown actions use a restrictive policy that requires confirmation.

This keeps security decisions independent from the UI.

---

## `system_diagnosis.py`

Provides deterministic system-health calculations and Gemini-based diagnosis.

The deterministic layer establishes the actual system measurements.

Gemini is then used to explain those findings.

---

## `windows_actions.py`

Contains controlled Windows actions such as:

- Opening URLs
- Launching allowlisted applications

Platform checks prevent these actions from executing on unsupported operating systems.

---

# 📂 Project Structure

```text
System_Analysis_Chatbot/
│
├── app.py
│
├── utils/
│   ├── chat_db.py
│   ├── chats.py
│   ├── command_router.py
│   ├── installexe.py
│   ├── model.py
│   ├── process_analysis.py
│   ├── safety.py
│   ├── software_details.py
│   ├── software_health.py
│   ├── startup_analysis.py
│   ├── storage_analysis.py
│   ├── system_diagnosis.py
│   ├── tool_executor.py
│   ├── tool_registry.py
│   └── windows_actions.py
│
├── tests/
│   ├── test_command_router.py
│   ├── test_windows_process_analysis.py
│   ├── test_windows_startup.py
│   ├── test_windows_storage.py
│   ├── test_windows_actions.py
│   └── test_windows_action_execution.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🧪 Testing

The project includes a Windows-focused automated test suite.

Windows-specific behavior is mocked where necessary so the implementation can be tested safely from the development environment.

### Test coverage includes

- Command routing
- Process analysis
- Startup analysis
- Storage analysis
- Windows URL actions
- Windows application launching
- Application allowlisting
- Safety confirmation
- Tool execution
- Error handling

### Run tests

```bash
pytest -q
```

### Current result

```text
28 passed
```

> **28/28 tests currently pass.**

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application |
| **Streamlit** | Local user interface |
| **Google Gemini** | AI conversation and analysis |
| **psutil** | Process and system information |
| **PowerShell** | Windows software discovery |
| **Windows Registry** | Software and startup discovery |
| **python-dotenv** | Environment configuration |
| **pytest** | Automated testing |

---

# 🚀 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/arjungupt771/System_Analysis_Chatbot.git
cd System_Analysis_Chatbot
```

---

## 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Gemini

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

A template is available at:

```text
.env.example
```

### ⚠️ Important

Never commit your actual `.env` file or API key to GitHub.

---

## 5. Start the application

```bash
streamlit run app.py
```

The Streamlit interface will open in your browser.

---

# 💬 Example Commands

### System information

```text
system info
```

```text
show system information
```

### Software

```text
scan apps
```

```text
show installed software
```

### Processes

```text
show running processes
```

```text
what is using my cpu
```

```text
show top memory processes
```

### Startup

```text
startup apps
```

```text
show startup programs
```

### Storage

```text
show largest files
```

```text
find large files
```

```text
what is using my storage
```

### Software installation

```text
install vlc
```

Software installation is classified as a **high-risk action** and therefore requires explicit approval.

### URL

```text
open https://example.com
```

### Application

```text
open notepad
```

```text
open calculator
```

Application launching requires confirmation because it performs an external system action.

---

# 🔒 Security Design

The project intentionally avoids giving the language model unrestricted access to the operating system.

The execution pipeline is:

```text
User Input
    ↓
Intent Recognition
    ↓
Tool Validation
    ↓
Safety Policy
    ↓
Approval if Required
    ↓
Controlled Tool
    ↓
Structured Result
```

### Security properties

- No unrestricted shell execution
- Explicit tool registry
- Risk-based action policies
- Confirmation for sensitive operations
- Application allowlisting
- `shell=False` for process launching
- Windows platform guards
- Input validation
- Installation verification
- Structured execution results
- Restrictive handling of unknown intents

---

# 🎯 Design Philosophy

The system deliberately separates **AI reasoning** from **system execution**.

### Avoided architecture

```text
User
  ↓
LLM
  ↓
Arbitrary OS Command
```

### Implemented architecture

```text
User
  ↓
AI / Intent Router
  ↓
Structured Intent
  ↓
Safety Layer
  ↓
Approved Tool
  ↓
Actual System Data
  ↓
AI Explanation
```

This makes the system:

- More predictable
- Easier to test
- Easier to extend
- Safer to operate
- Less dependent on LLM-generated system facts

---

# 🧱 Extensibility

Adding a new system capability follows a controlled pattern:

```text
New Intent
    ↓
New Tool
    ↓
Tool Registry Entry
    ↓
Safety Policy
    ↓
Executor Integration
    ↓
Tests
```

This allows the assistant to grow without turning the project into an unrestricted operating-system command interface.

---

# 🪟 Platform Support

| Platform | Status |
|---|---|
| Windows | ✅ Supported |
| Linux | 🚧 Future |
| macOS | 🚧 Future |

The current implementation intentionally prioritizes Windows-specific functionality.

The routing, registry, safety, and executor architecture can later be reused for platform-specific implementations.

---

# 📊 Project Status

## Implemented

- [x] Gemini integration
- [x] Deterministic system-health analysis
- [x] Software-health analysis
- [x] Windows software discovery
- [x] Software installation verification
- [x] Natural-language command routing
- [x] Tool registry
- [x] Tool executor
- [x] Windows process analysis
- [x] Windows startup analysis
- [x] Windows storage analysis
- [x] Safety and approval layer
- [x] Windows URL actions
- [x] Controlled application launching
- [x] Application allowlisting
- [x] Windows-focused automated tests
- [x] 28/28 tests passing
- [x] GitHub documentation

## Future Scope

- [ ] Linux system-analysis support
- [ ] Additional Windows diagnostics
- [ ] More controlled Windows automation
- [ ] Expanded system-health recommendations
- [ ] Additional AI-assisted troubleshooting

---

# ⚠️ Limitations

The current project has several intentional limitations:

1. **Windows is the supported runtime platform.**
2. Some capabilities depend on Windows APIs, Registry access, and PowerShell.
3. Application launching is restricted to an explicit allowlist.
4. Sensitive actions require explicit confirmation.
5. Software installation depends on configured installer sources.
6. Storage analysis is bounded by traversal depth and result limits.
7. Gemini functionality requires a valid API key.

These limitations are intentional design decisions that keep system interaction controlled.

---

# 👨‍💻 Author

## Arjun Gupta

**B.Tech — Information Technology**  
**VIT Vellore**

GitHub:  
https://github.com/arjungupt771

---

# 📄 License

No license has currently been specified for this repository.

If the project is later released for redistribution or open-source use, an appropriate license can be added.

---

<p align="center">
  Built with Python · Streamlit · Google Gemini · Windows System Tooling
</p>
