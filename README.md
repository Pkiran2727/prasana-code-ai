# Prasana Code AI 🚀

> **Web-Based AI-Powered Code Editor, Compiler & Gamified Interactive Programming Platform**  
> *Created by [@itsprasana](https://github.com/Pkiran2727)*

---

## 🌟 Overview

**Prasana Code AI** is a state-of-the-art interactive coding platform combining a high-performance cloud sandbox IDE, gamified curriculum tracks (Python, Web Dev, DSA, C++, AI), and an intelligent AI Tutor. Inspired by leading platforms like Coddy.tech and modern cloud IDEs, it provides immediate feedback, automated test execution, and hints without spoiling answers.

---

## ✨ Features

- **⚡ Multi-Language Sandboxed Runner:**
  - Fast execution for **Python 3.11**, **JavaScript (Node.js)**, **TypeScript**, **C++ (g++)**, **ANSI C (gcc)**, and **Bash**.
  - Built-in time limits, memory bounds, and secure containerized execution.

- **🗺️ Gamified Learning Journeys:**
  - Structured tracks: *Python Developer Journey*, *Full Stack Web Development*, *DSA & Problem Solving Mastery*, *Modern C++ Systems*, *AI Engineering & LLMs*.
  - Step-by-step interactive lessons with automated test case evaluation.

- **🤖 AI Tutor Integration:**
  - Error diagnosis, line-by-line debugging hints, and conceptual explanations via WebSocket token streaming.
  - Resilient LLM routing with fallback modes.

- **💻 Full-Featured Web IDE:**
  - Monaco Editor (VS Code core) with syntax highlighting, autocomplete, and multi-file tab switching.
  - Virtual session file explorer, integrated terminal output, and real-time chat split-view.

- **🎨 Multi-Theme System:**
  - High-contrast, accessibility-tested themes: **Executive Dark**, **High Contrast Dark**, **Light Mode**, and **High Contrast Light**.

- **💳 Monetization & Gamification:**
  - Daily streaks, XP rewards (idempotent, first-time pass rewards), badges, and leaderboard tracking.
  - Razorpay order creation and direct UPI QR settlement support.

---

## 🏗️ Architecture & Tech Stack

- **Frontend:** React 18, Vite, Tailwind CSS, Monaco Editor, Lucide Icons
- **Backend:** FastAPI, Uvicorn, WebSockets, Subprocess Sandboxing, Asyncio
- **Database:** PostgreSQL (Schema with courses, modules, lessons, challenges, test cases, user progress, submissions)
- **Deployment:** Docker & Docker Compose (`backend`, `frontend`, `database`)

---

## 🚀 Quick Start (Docker Compose)

### 1. Clone the repository
```bash
git clone https://github.com/Pkiran2727/prasana-code-ai.git
cd prasana-code-ai
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

### 3. Start the Platform
```bash
docker compose up -d --build
```

- **Frontend UI:** Open [http://localhost:5173](http://localhost:5173)
- **Backend API:** Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database:** PostgreSQL on port `5432`

---

## 📜 License

MIT License. Designed and developed with ❤️ by **Manda Prasanna Kiran** (@itsprasana).
