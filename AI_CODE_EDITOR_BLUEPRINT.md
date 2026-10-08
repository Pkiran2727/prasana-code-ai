# 🚀 AI Code Editor — Complete Project Blueprint (A to Z)

> **Project Name:** LiveCodeAI  
> **Host:** HuggingFace Docker Space  
> **Stack:** React + Vite + FastAPI + LangChain + Monaco Editor + Piston API  
> **LLMs:** Qwen3-VL-Demo (primary) + Qwen backup (fallback)  
> **Alert System:** Gmail SMTP (Python smtplib)

---

## ❓ Do You Need a Database?

**Short answer: NO — not for MVP.**

| Data | Storage Method | Why |
|------|---------------|-----|
| Files (code) | In-memory dict + temp `/sessions/{id}/` folder | Per session, wiped on disconnect |
| Chat history | In-memory list per session | Sent with each LLM call as context |
| Language preference | React state / localStorage | Frontend only |
| Run output | In-memory, shown in terminal | Not persisted |
| Email alert cooldown | In-memory flag | Prevent spam alerts |

**When you WILL need a DB (future):**
- User login / accounts
- Save projects across sessions
- Chat history persistence
- Usage analytics

**For now:** No DB. Session-based in-memory storage is enough.

---

## 📁 Complete File Structure (A to Z)

```
LiveCodeAI/                          ← Root (HuggingFace Space repo)
│
├── Dockerfile                       ← Builds + runs both frontend & backend
├── requirements.txt                 ← Python dependencies
├── .env.example                     ← Template for secrets (no real secrets here)
├── README.md                        ← HuggingFace Space description
│
├── backend/                         ← Python FastAPI server
│   ├── main.py                      ← App entry point, routes, WebSocket
│   ├── agent.py                     ← LangChain agent loop + tool orchestration
│   ├── llm_manager.py               ← Primary + fallback LLM logic
│   ├── tools.py                     ← All agent tools (read, write, run, list...)
│   ├── file_manager.py              ← Virtual per-session file system
│   ├── code_runner.py               ← Piston API integration (50+ languages)
│   ├── mcp_server.py                ← MCP protocol handler
│   ├── alert.py                     ← Gmail SMTP email alerter
│   ├── session_manager.py           ← Session create/destroy/cleanup
│   └── config.py                    ← All constants, env vars, LLM configs
│
└── frontend/                        ← React + Vite app
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.jsx                 ← React entry point
        ├── App.jsx                  ← Root layout (split panels)
        ├── api/
        │   ├── agentApi.js          ← WebSocket chat + agent calls
        │   └── runnerApi.js         ← Code execution API calls
        ├── hooks/
        │   ├── useSession.js        ← Session ID management
        │   ├── useAgent.js          ← Agent chat state + streaming
        │   ├── useFileSystem.js     ← File tree state management
        │   └── useCodeRunner.js     ← Run code + output state
        ├── components/
        │   ├── layout/
        │   │   ├── Navbar.jsx       ← Top bar (logo, language, run button)
        │   │   └── SplitLayout.jsx  ← Resizable 3-panel layout
        │   ├── editor/
        │   │   ├── MonacoEditor.jsx ← Monaco wrapper with language sync
        │   │   ├── EditorTabs.jsx   ← Open file tabs (like VS Code)
        │   │   └── EditorToolbar.jsx← Format, copy, fullscreen buttons
        │   ├── filetree/
        │   │   ├── FileTree.jsx     ← Collapsible folder/file explorer
        │   │   ├── FileItem.jsx     ← Single file/folder row
        │   │   └── FileContextMenu.jsx ← Right-click rename/delete menu
        │   ├── chat/
        │   │   ├── ChatPanel.jsx    ← Full chat UI container
        │   │   ├── ChatMessage.jsx  ← Single message bubble (user/AI)
        │   │   ├── ChatInput.jsx    ← Text input + send button
        │   │   └── AgentStatus.jsx  ← "Reading file..." / "Running code..." indicator
        │   ├── terminal/
        │   │   ├── Terminal.jsx     ← Output panel
        │   │   └── TerminalLine.jsx ← Colored output lines (error/success/info)
        │   └── shared/
        │       ├── LanguageSelector.jsx ← Dropdown: Python, JS, Java, C++...
        │       ├── StatusBadge.jsx  ← LLM online/offline indicator
        │       └── LoadingSpinner.jsx
        └── styles/
            ├── globals.css          ← Base styles, dark theme vars
            └── editor.css           ← Monaco overrides
```

---

## 🎨 UI Design — Full Layout Spec

### Color Palette (Dark Theme — VS Code inspired)

```
Background panels  → #1e1e1e
Sidebar bg         → #252526
Editor bg          → #1e1e1e
Chat bg            → #252526
Terminal bg        → #0d0d0d
Navbar bg          → #333333
Border color       → #3c3c3c
Text primary       → #d4d4d4
Text muted         → #858585
Accent blue        → #0078d4  ← Run button, links
Accent green       → #4ec9b0  ← Success output
Accent red         → #f44747  ← Error output
Accent yellow      → #dcdcaa  ← Warnings
```

### Full Screen Layout (Desktop — 1440px)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🔷 LiveCodeAI     [Python 🐍 ▼]   [● LLM Online]        [▶ Run  Ctrl+↵]│  ← Navbar 48px
├──────────────┬──────────────────────────────────┬───────────────────────┤
│              │  📄 main.py  ✕   utils.py  ✕     │                       │
│  📁 FILES    │─────────────────────────────────  │   💬 AI AGENT         │
│              │                                   │                       │
│  ▼ 📂 project│   def fibonacci(n):               │  🤖 Agent             │
│    📄 main.py│       if n <= 1:                  │  ───────────────────  │
│    📄 utils  │           return n                │  I can see your       │
│    📄 test   │       return fib(n-1) + fib(n-2)  │  fibonacci function.  │
│              │                                   │  Line 4 has a bug —   │
│  ▼ 📂 tests  │                                   │  you called `fib`     │
│    📄 test1  │                                   │  instead of           │
│              │                                   │  `fibonacci`. I'll    │
│  [+ New File]│                                   │  fix it now...        │
│  [+ New Dir] │                                   │                       │
│              │─────────────────────────────────  │  🔧 read_file main.py │
│              │  ⚡ TERMINAL                       │  ✅ write_file done   │
│              │                                   │  🔄 run_code...       │
│              │  $ python main.py                 │  ───────────────────  │
│              │  > 0 1 1 2 3 5 8 13 21 34         │  You                  │
│              │  > Execution: 0.12s               │  ───────────────────  │
│              │  >                                │  fix the bug and run  │
│              │                                   │                       │
│              │                                   │  [Ask the agent... ] 💬│
└──────────────┴──────────────────────────────────┴───────────────────────┘
  ← 220px →    ←──────── flex-1 (editor+terminal) ──────────→  ← 320px →
```

### Panel Proportions

| Panel | Default Width | Min | Resizable? |
|-------|-------------|-----|-----------|
| File Tree | 220px | 160px | Yes (drag) |
| Editor + Terminal | flex-1 | 400px | Yes |
| Chat Panel | 320px | 260px | Yes |
| Terminal height | 220px | 120px | Yes (drag up) |

### Navbar Items (Left to Right)

```
[🔷 LiveCodeAI logo]  [Language Dropdown ▼]  [spacer flex-1]  [● LLM Status]  [▶ Run Ctrl+Enter]
```

### Language Dropdown Options

```
Python 🐍 | JavaScript ⚡ | TypeScript | Java ☕ | C++ | C | Go | Rust
Ruby | PHP | Kotlin | Swift | R | Bash | SQL | Lua | Perl | Haskell
```

---

## ⚙️ Backend — File by File Explained

### `config.py`
```
- LLM_CONFIG list (2 LLMs with name, space, api_name, priority)
- PISTON_API_URL
- EMAIL_FROM, EMAIL_TO, GMAIL_APP_PASSWORD
- SESSION_TTL (how long inactive sessions live)
- SUPPORTED_LANGUAGES dict (name → piston language string)
- CORS origins
- All loaded from environment variables
```

### `main.py` — FastAPI App
```
Routes:
  POST /session/create          → create new session, return session_id
  DELETE /session/{id}          → cleanup session files
  GET  /files/{session_id}      → list all files
  POST /files/{session_id}      → create file
  GET  /files/{session_id}/{path} → read file content
  PUT  /files/{session_id}/{path} → update file content
  DELETE /files/{session_id}/{path} → delete file
  POST /run                     → run code via Piston
  WebSocket /ws/{session_id}    → agent chat (streaming)
```

### `llm_manager.py` — LLM with Fallback
```
Function: call_llm(prompt, history) → response_text

Logic:
  1. Try LLM #1 (Qwen3-VL-Demo)
     - gradio_client.Client(space1)
     - call /add_message
     - return response
  2. On failure → Try LLM #2 (backup space)
     - same flow
  3. Both fail →
     - send_alert(error_details)       ← Gmail SMTP
     - return None → frontend shows banner

Failure detection:
  - Timeout after 90 seconds
  - Exception catch
  - Empty/None response check
  - Threading with join(timeout=90)

Alert cooldown:
  - In-memory flag: last_alert_time
  - Don't send email if last alert was < 30 minutes ago
```

### `agent.py` — LangChain Agent
```
Uses: LangChain AgentExecutor with custom tools

Tool selection priority logic:
  Agent gets: user message + current file + language + file list
  LLM decides which tools to call in which order

Streaming:
  - Uses LangChain callbacks
  - Each tool call event → sent via WebSocket to frontend
  - Shows: "📖 Reading main.py...", "✏️ Writing fix...", "▶️ Running..."
  - Final text response streamed token by token
```

### `tools.py` — All Agent Tools

```
Tool 1: read_file(session_id, path)
  → reads file from /sessions/{id}/{path}
  → returns content string

Tool 2: write_file(session_id, path, content)
  → writes to /sessions/{id}/{path}
  → emits file_updated event to frontend via WebSocket
  → frontend Monaco editor refreshes automatically

Tool 3: list_files(session_id)
  → walks /sessions/{id}/
  → returns tree structure JSON

Tool 4: create_file(session_id, path, content="")
  → creates file (and parent dirs)
  → emits new_file event to frontend

Tool 5: delete_file(session_id, path)
  → deletes file
  → emits file_deleted event to frontend

Tool 6: run_code(language, code)
  → calls Piston API
  → returns stdout + stderr + execution_time
  → emits run_result event to frontend (shows in terminal)

Tool 7: search_code(session_id, query)
  → grep-like search across all files
  → returns matches with line numbers

Tool 8: create_folder(session_id, path)
  → mkdir -p equivalent
```

### `code_runner.py` — Piston API
```
POST https://emkc.org/api/v2/piston/execute
Body:
  {
    "language": "python",
    "version": "*",
    "files": [{"name": "main.py", "content": "<code>"}]
  }
Response:
  {
    "run": {
      "stdout": "Hello World\n",
      "stderr": "",
      "code": 0
    }
  }

Timeout: 30 seconds
Max output: 10,000 chars (truncate if more)
```

### `mcp_server.py` — MCP Protocol
```
Implements MCP (Model Context Protocol) so tools are described in standard format

Endpoint: GET /mcp/tools → returns tool schema list
Endpoint: POST /mcp/call → executes a tool by name with args

This allows:
  - External MCP clients to connect to your IDE
  - Future: Claude Desktop / Cursor to use your tools
  - Agent calls tools via MCP internally
```

### `alert.py` — Email Alert
```python
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_alert(error_details: str):
    """Send Gmail alert when both LLMs are down."""
    body = f"""
    ⚠️ LiveCodeAI — Both LLMs are DOWN
    Time: {datetime.now()}
    
    LLM 1 (Qwen3-VL-Demo): Failed
    LLM 2 (Backup): Failed
    
    Error: {error_details}
    
    Action needed: Check HuggingFace Space status.
    """
    msg = MIMEText(body)
    msg["Subject"] = "🚨 LiveCodeAI LLMs Down"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, GMAIL_APP_PASSWORD)
        server.send_message(msg)
```

### `session_manager.py`
```
- create_session() → returns unique session_id (UUID)
- get_session_path(session_id) → /tmp/sessions/{id}/
- destroy_session(session_id) → deletes folder
- cleanup_old_sessions() → runs every 30 min, deletes sessions > TTL
- Pre-creates a "welcome" main.py file in every new session
```

---

## ⚛️ Frontend — Component by Component Explained

### `App.jsx`
```
- Creates session on mount (POST /session/create)
- Stores session_id in state
- Opens WebSocket connection
- Renders SplitLayout with all 3 panels
- Handles LLM status banner (if both LLMs down)
```

### `MonacoEditor.jsx`
```
- Loads Monaco with all language support
- Syncs language from LanguageSelector
- On file switch → loads new content
- On content change → debounce 500ms → PUT /files/... (auto-save)
- Listens for write_file WebSocket events → refreshes content
- Ctrl+Enter → triggers Run
- Dark theme: vs-dark
```

### `EditorTabs.jsx`
```
- Shows open files as tabs (like VS Code)
- Click tab → switch active file
- X button → close tab
- Unsaved indicator → dot on tab name
```

### `FileTree.jsx`
```
- Fetches file tree on mount and on new_file/file_deleted events
- Renders nested folder structure
- Click file → opens in editor tab
- Right click → context menu (rename, delete, new file here)
- [+ New File] button at bottom
- [+ New Folder] button at bottom
```

### `ChatPanel.jsx`
```
- Shows message history (scrollable)
- User messages: right-aligned, blue bg
- AI messages: left-aligned, dark bg, markdown rendered
- Agent tool events: shown as small status pills between messages
  e.g. [🔧 read_file: main.py] [✏️ write_file: main.py] [▶️ run_code]
- Input: textarea (Enter to send, Shift+Enter for newline)
- Sends: {message, current_file, current_language, session_id}
```

### `AgentStatus.jsx`
```
Shows real-time agent activity between messages:
  🔍 "Reading main.py..."
  ✏️  "Writing fix to main.py..."
  ▶️  "Running Python code..."
  🔎 "Searching for 'fibonacci'..."
  
Animated: pulsing dot + fade in/out
```

### `Terminal.jsx`
```
- Shows run output
- Green text → stdout
- Red text → stderr  
- Gray text → system messages (execution time, exit code)
- [Clear] button top right
- Auto-scrolls to bottom
- Also shows when agent runs code (labeled "Agent ran:")
```

### `LanguageSelector.jsx`
```
Dropdown with 20+ languages
Each option has emoji icon
On change:
  → updates Monaco editor language
  → updates run language
  → tells agent current language via system prompt
```

### `StatusBadge.jsx`
```
● Green  "LLM Online"     → both/one LLM working
● Red    "LLM Offline"    → both failed, shows banner
● Yellow "LLM Slow"       → response taking > 15s
```

---

## 🔌 WebSocket Message Protocol

### Frontend → Backend
```json
{
  "type": "chat",
  "message": "fix the bug in main.py",
  "session_id": "abc-123",
  "current_file": "main.py",
  "current_code": "def fib(n):\n    ...",
  "language": "python"
}
```

### Backend → Frontend (stream events)
```json
{ "type": "agent_token",    "data": "I can see" }
{ "type": "agent_token",    "data": " the issue..." }
{ "type": "tool_start",     "tool": "read_file",  "args": {"path": "main.py"} }
{ "type": "tool_end",       "tool": "read_file",  "status": "success" }
{ "type": "tool_start",     "tool": "write_file", "args": {"path": "main.py"} }
{ "type": "file_updated",   "path": "main.py",    "content": "def fibonacci..." }
{ "type": "tool_end",       "tool": "write_file", "status": "success" }
{ "type": "run_result",     "stdout": "0 1 1 2",  "stderr": "", "time": "0.1s" }
{ "type": "agent_done",     "full_response": "Fixed! The function name was wrong..." }
{ "type": "llm_error",      "message": "Both LLMs are currently unavailable..." }
```

---

## 🐋 Dockerfile

```dockerfile
FROM python:3.11-slim

# Install Node.js for React build
RUN apt-get update && apt-get install -y nodejs npm curl

WORKDIR /app

# Build React frontend
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build
# Built files → frontend/dist/

# Install Python backend
COPY backend/ ./backend/
COPY requirements.txt .
RUN pip install -r requirements.txt

# FastAPI serves React static files too
EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## 📦 Requirements

### `requirements.txt` (Python)
```
fastapi
uvicorn[standard]
python-dotenv
langchain
langchain-community
gradio_client
httpx
aiofiles
websockets
```

### `package.json` key deps (Node)
```
react
react-dom
vite
@monaco-editor/react
tailwindcss
react-markdown
remark-gfm         ← renders code blocks in chat
react-resizable-panels  ← draggable split panels
```

---

## 🌿 Environment Variables (`.env`)

```env
# LLM Spaces
LLM_PRIMARY_SPACE=Qwen/Qwen3-VL-Demo
LLM_FALLBACK_SPACE=Qwen/Qwen2.5-VL-Demo

# Email Alert
GMAIL_FROM=youremail@gmail.com
GMAIL_TO=youremail@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Session config
SESSION_TTL_MINUTES=60
MAX_SESSIONS=50

# Piston API
PISTON_API_URL=https://emkc.org/api/v2/piston/execute
```

> ⚠️ On HuggingFace: add these as **Space Secrets** — never commit `.env` to repo.

---

## 🚀 Build Phases — Execution Order

### Phase 1 — React Layout (No logic, just UI skeleton)
```
- Vite + React + Tailwind setup
- SplitLayout with 3 resizable panels
- Navbar with dummy buttons
- Monaco Editor renders (hardcoded language: Python)
- FileTree renders (hardcoded dummy files)
- ChatPanel renders (hardcoded dummy messages)
- Terminal renders (hardcoded dummy output)
Deliverable: Full visual UI, nothing works yet
```

### Phase 2 — FastAPI Backend Setup
```
- FastAPI app with all routes defined (return dummy data)
- Session create/destroy
- File system manager (create, read, write, delete, list)
- Static file serving for React build
Deliverable: Backend running locally, file CRUD works via curl
```

### Phase 3 — Connect Frontend ↔ Backend (Files)
```
- React fetches real file tree on mount
- Create file / delete file works from UI
- Click file → loads real content in Monaco
- Monaco auto-saves on edit (debounced PUT)
Deliverable: Full working file explorer + editor (no AI yet)
```

### Phase 4 — Code Execution (Piston API)
```
- Run button → POST /run → Piston → shows in Terminal
- Language selector changes Monaco syntax + run language
- Ctrl+Enter shortcut works
- Error output in red, success in green
Deliverable: Working code editor that runs all languages
```

### Phase 5 — LLM Manager + Fallback
```
- llm_manager.py with primary + fallback logic
- Threading + timeout (90s)
- Alert cooldown logic
- Gmail SMTP alert on double failure
- /chat HTTP endpoint (non-streaming, for testing)
Deliverable: LLM calls work, fallback tested, email alert tested
```

### Phase 6 — LangChain Agent + Tools
```
- All 8 tools defined
- Agent with tool descriptions
- Agent decides which tools to call based on user message
- tool_start / tool_end events emitted
Deliverable: Agent can read/write files and run code autonomously
```

### Phase 7 — WebSocket Streaming
```
- /ws/{session_id} WebSocket endpoint
- Agent streams tokens via WebSocket
- Frontend displays streaming text in chat
- tool_start events → AgentStatus indicator
- file_updated events → Monaco refreshes live
- run_result events → Terminal updates live
Deliverable: Full real-time agent experience
```

### Phase 8 — MCP Server
```
- GET /mcp/tools → standard tool schema
- POST /mcp/call → execute tool
- Agent internally routes tool calls via MCP
Deliverable: MCP-compatible IDE (can connect external clients)
```

### Phase 9 — Docker + HuggingFace Deploy
```
- Dockerfile builds React then serves via FastAPI
- Test locally: docker build + docker run
- Push to HuggingFace Space repo
- Add all env vars as HF Secrets
- Test live URL
Deliverable: 🎉 Live AI Code Editor on HuggingFace
```

---

## 🔒 Security Notes

```
- Session IDs are UUID4 (unguessable)
- Each session has its own isolated folder
- Piston API runs code in sandboxed containers (safe)
- No user auth needed for MVP (single user = you)
- HF Secrets keep credentials safe
- Rate limit /run endpoint: max 10 requests/minute per session
```

---

## 📊 Summary

| Feature | Tool Used | Status |
|---------|-----------|--------|
| Code Editor | Monaco Editor | Phase 1 |
| File Explorer | Custom React + FastAPI | Phase 2-3 |
| Multi-language Run | Piston API (free) | Phase 4 |
| LLM Chat | HuggingFace Gradio Client | Phase 5 |
| LLM Fallback | 2-LLM chain logic | Phase 5 |
| Email Alert | Gmail SMTP (smtplib) | Phase 5 |
| AI Agent | LangChain AgentExecutor | Phase 6 |
| Streaming | WebSocket | Phase 7 |
| MCP Support | Custom MCP server | Phase 8 |
| Deployment | HuggingFace Docker Space | Phase 9 |
| Database | ❌ Not needed for MVP | — |

---

*Blueprint version 1.0 — Ready to build. Start with "Phase 1" to begin.*
