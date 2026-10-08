# 🎯 LiveCodeAI — Vision & Purpose

## What Are We Building?

A **web-based AI-powered code editor** hosted on HuggingFace as a Docker Space.

Think of it as a **mini Cursor IDE that runs in a browser** — where:
- You write code in a real editor (Monaco — same as VS Code)
- You run that code live in any language (Python, Java, C++, JS, 50+ more)
- An AI agent sits beside you, understands your files, and helps you code
- The AI can read your files, fix bugs, write new code, and run it — all by itself
- You manage multiple files in a project with a file explorer

---

## Why Are We Building This?

**Problem:** Existing AI coding tools (Cursor, Copilot, Windsurf) are:
- Desktop apps — not shareable via a URL
- Paid / require accounts
- Not hostable for free

**Our Solution:** A fully free, URL-shareable AI code editor hosted on HuggingFace Spaces that anyone can open in a browser and start coding with AI assistance immediately — no install, no account.

**Personal Use Case:** Practice any programming language with AI guidance, get instant feedback, and have the AI write + run code for you — all in one tab.

---

## What Does the Final Product Look Like?

Open the HuggingFace Space URL → Browser shows:

```
┌─────────────────────────────────────────────────────────────┐
│ 🔷 LiveCodeAI  [Python ▼]  [● LLM Online]    [▶ Run Ctrl+↵]│
├─────────────┬───────────────────────────┬────────────────────┤
│ 📁 Files    │  Monaco Code Editor       │  💬 AI Agent Chat  │
│             │  (write code here)        │  (talk to AI here) │
│             ├───────────────────────────│                    │
│             │  ⚡ Terminal Output        │                    │
└─────────────┴───────────────────────────┴────────────────────┘
```

**User Flow — Example:**
1. User opens URL → sees a Python file ready to edit
2. User writes a function → clicks ▶ Run → sees output in terminal
3. User types in chat: *"this isn't working, fix it"*
4. Agent reads the file → fixes the bug → saves it → runs it → shows result
5. User sees the fixed code appear live in the editor + output in terminal
6. User switches language to JavaScript → writes JS code → runs it

**That's the final product.**

---

## Core Features (Must Have)

| Feature | Description |
|---------|-------------|
| Monaco Editor | VS Code-quality editor in browser with syntax highlighting |
| File Explorer | Create, rename, delete files and folders per session |
| Run Any Language | Python, JS, Java, C++, Go, Rust, 50+ via Piston API |
| AI Agent Chat | Talk to AI, it understands your code and project |
| Agent Tool Use | AI can read/write files, run code, create files autonomously |
| LLM Fallback | If primary LLM fails, auto-switches to backup LLM |
| Email Alert | If both LLMs fail, sends email alert to owner |
| MCP Support | Tools exposed via MCP protocol for extensibility |
| HF Deployment | Runs as a Docker Space on HuggingFace — free hosting |

---

## Tech Decisions (Already Finalized)

| Concern | Decision | Reason |
|---------|----------|--------|
| Frontend | React + Vite + Tailwind | Fast, component-based |
| Editor | Monaco Editor | Industry standard, 50+ languages |
| Code Execution | Piston API (free) | Sandboxed, no setup, 50+ languages |
| Backend | FastAPI (Python) | Async, WebSocket support, easy |
| AI Agent | LangChain | Tool orchestration, streaming |
| LLM Connection | HuggingFace Gradio Client | Connects to user's HF Spaces |
| Realtime | WebSocket | Streams agent tokens + tool events live |
| Deployment | HuggingFace Docker Space | Free, URL-shareable |
| Database | None (MVP) | Session files in temp dirs, in-memory state |
| Email | Gmail SMTP (smtplib) | Free, built into Python |

---

## LLM Setup

- **Primary LLM:** `Qwen/Qwen3-VL-Demo` (HuggingFace Gradio Space)
- **Fallback LLM:** `Qwen/Qwen2.5-VL-Demo` (backup Gradio Space)
- Both called via `gradio_client` Python library
- No image input needed — text-only chat
- If both fail → show error banner in UI + send Gmail alert to owner

---

## What the AI Agent Can Do (Tools)

The agent is not just a chatbot. It has **tools** that let it act:

1. `read_file` — read any file in your project
2. `write_file` — create or edit any file (Monaco updates live)
3. `list_files` — see the full file tree
4. `create_file` — create a new file
5. `delete_file` — delete a file
6. `run_code` — execute code and see the output (Terminal updates live)
7. `search_code` — search for text across all files
8. `create_folder` — make new directories

The agent picks tools based on what the user asks. Example:
- *"build a flask app"* → agent calls `create_file` 5 times + `run_code`
- *"why is this failing?"* → agent calls `read_file` + `run_code` + replies
- *"refactor all files"* → agent calls `list_files` → `read_file` each → `write_file` each

---

## Deployment Target

- Platform: **HuggingFace Spaces** (Docker type)
- URL: `https://huggingface.co/spaces/YOUR_USERNAME/LiveCodeAI`
- Free tier: enough for personal use
- Secrets stored as HF Space environment variables

---

## Out of Scope (Not Building Now)

- User login / authentication
- Persistent project storage across sessions
- Git integration
- Terminal with full shell access
- Mobile layout (desktop only for now)
