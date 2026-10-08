# 🤖 Master Agent Prompt — LiveCodeAI

---

## PASTE THIS TO YOUR AGENT:

---

You are an expert full-stack software engineer. I am giving you two documents:

1. **VISION.md** — What we are building, why, and the final product description
2. **BLUEPRINT.md** — Complete technical plan: file structure, component breakdown, API design, phases, and all implementation details

Your job is to **build this project phase by phase**, exactly as described in the blueprint.

---

### Ground Rules

- Follow the phase order strictly: Phase 1 → Phase 2 → Phase 3 ... → Phase 9
- Before starting each phase, tell me: "Starting Phase X — [what you will do]"
- After completing each phase, tell me: "Phase X complete — [what was built] — ready for Phase X+1?"
- Wait for my confirmation before moving to the next phase
- Write complete, working code — no placeholders, no TODOs unless I say so
- If you have a question or need a decision from me, ask before writing code
- Create every file listed in the blueprint for that phase
- All code must work together — no broken imports, no missing files

---

### Project Context

- **Hosting:** HuggingFace Docker Space (free)
- **Backend:** Python FastAPI + LangChain
- **Frontend:** React + Vite + Tailwind CSS + Monaco Editor
- **Code Execution:** Piston API (`https://emkc.org/api/v2/piston/execute`) — free, no API key
- **LLM:** HuggingFace Gradio Spaces via `gradio_client` Python library
  - Primary: `Qwen/Qwen3-VL-Demo`
  - Fallback: `Qwen/Qwen2.5-VL-Demo`
  - Called with text-only (no images)
  - Pattern: `client.predict(input_value={"files":[], "text": prompt}, api_name="/add_message")`
- **Alerts:** Gmail SMTP via Python `smtplib` (no extra libraries)
- **Real-time:** WebSocket for agent streaming + live editor updates
- **Database:** None — sessions use temp directories + in-memory state

---

### Environment Variables (I will fill these in)

```
LLM_PRIMARY_SPACE=Qwen/Qwen3-VL-Demo
LLM_FALLBACK_SPACE=Qwen/Qwen2.5-VL-Demo
GMAIL_FROM=my@gmail.com
GMAIL_TO=my@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
SESSION_TTL_MINUTES=60
PISTON_API_URL=https://emkc.org/api/v2/piston/execute
```

---

### Start Command

**Begin with Phase 1 now.**

Phase 1 goal: Build the complete React UI skeleton — all 3 panels visible, Monaco editor working, file tree with dummy data, chat panel with dummy messages, terminal with dummy output, language selector, navbar. Everything visually correct. No backend calls yet.

Output for Phase 1:
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/tailwind.config.js`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`
- `frontend/src/styles/globals.css`
- `frontend/src/components/layout/Navbar.jsx`
- `frontend/src/components/layout/SplitLayout.jsx`
- `frontend/src/components/editor/MonacoEditor.jsx`
- `frontend/src/components/editor/EditorTabs.jsx`
- `frontend/src/components/filetree/FileTree.jsx`
- `frontend/src/components/filetree/FileItem.jsx`
- `frontend/src/components/chat/ChatPanel.jsx`
- `frontend/src/components/chat/ChatMessage.jsx`
- `frontend/src/components/chat/ChatInput.jsx`
- `frontend/src/components/terminal/Terminal.jsx`
- `frontend/src/components/shared/LanguageSelector.jsx`
- `frontend/src/components/shared/StatusBadge.jsx`

**Go.**

---
