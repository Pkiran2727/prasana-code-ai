import os
import json
import logging
import asyncio
from datetime import datetime, date
from backend.file_manager import list_files, read_file, write_file
from backend.code_runner import run_code
from backend.llm_manager import get_llm_response
from backend.web_tools import execute_search_web, execute_search_wikipedia
from json_repair import repair_json
from backend.db import get_cursor

logger = logging.getLogger(__name__)

PRIMARY_MODEL = "GLM"  # Options: "QWEN" or "GLM"

SYSTEM_PROMPT = """You are "Mitra", a friendly programming tutor inside Prasana Code AI (by @itsprasana).
Your goal is to help students learn programming, debug code, and master software engineering using the "Chudu -> Try -> Test -> Telusuko" teaching philosophy.

LANGUAGE SETTINGS:
- Default Language: English
- Multilingual Support: If the user communicates in Telugu, Hindi, Spanish, or any other language, you MUST seamlessly switch and reply in their language.

TUTORING METHODOLOGY (PRASANA CODE AI STYLE):
1. **Guide, Don't Spoil:** When a student is solving a lesson or problem, NEVER directly provide the full solution code. Instead, analyze their code, explain the error, point to the exact line number causing the issue, and provide a clear hint.
2. **Error Diagnosis:** When code execution fails, inspect stdout/stderr. Tell the student *why* it failed in simple language.
3. **Workspace Tools:** You have access to `read_file`, `write_file`, `list_files`, `run_code`, `search_web`, and `search_wikipedia`. Use them to inspect their code and test fixes.

To accomplish your goals, you MUST respond in a structured JSON format. 

Every response must be a valid JSON object containing exactly one of the following schemas:

If you need to call a tool:
{
  "thought": "Reasoning about what to do next",
  "tool": "tool_name",
  "args": { "arg_name": "arg_value" }
}

Available tools:
- "list_files": { "path": "/workspace" }
- "read_file": { "path": "relative/path.ext" }
- "write_file": { "path": "relative/path.ext", "content": "text content..." }
- "run_code": { "path": "relative/path.ext" }
- "search_web": { "query": "formal english keywords" }
- "search_wikipedia": { "query": "Topic" }

If you have finished your work and want to give a final answer:
{
  "thought": "I have explained the hint / diagnosed the bug.",
  "final_answer": "Direct friendly response to the student with markdown, code snippets, line references, and hints."
}

Do not output any markdown code blocks (like ```json) or extra text outside the JSON object. Just return the raw JSON object.
"""

def record_ai_usage(user_id: str, feature: str = "tutor", tokens_in: int = 100, tokens_out: int = 100):
    """
    Enforces and tracks per-user AI quota in ai_usage table.
    """
    if not user_id:
        return
    try:
        with get_cursor() as cur:
            today = date.today()
            cur.execute("""
                INSERT INTO ai_usage (user_id, day, feature, calls, tokens_in, tokens_out)
                VALUES (%s, %s, %s, 1, %s, %s)
                ON CONFLICT (user_id, day, feature)
                DO UPDATE SET calls = ai_usage.calls + 1,
                              tokens_in = ai_usage.tokens_in + EXCLUDED.tokens_in,
                              tokens_out = ai_usage.tokens_out + EXCLUDED.tokens_out
            """, (user_id, today, feature, tokens_in, tokens_out))
    except Exception as e:
        logger.warning(f"Failed to record ai_usage: {e}")

async def execute_agent_loop(session_id: str, user_prompt: str, callback_fn, conversation_history: list, user_id: str = None) -> None:
    """
    Executes the custom agent loop, calling tools and sending status/output logs
    back to the client via `callback_fn`.
    """
    # Record AI tutor usage quota
    if user_id:
        record_ai_usage(user_id, feature="tutor")

    # Append the new user message to the persistent history
    conversation_history.append({"role": "user", "content": user_prompt})

    max_steps = 8
    step = 0

    while step < max_steps:
        step += 1
        
        # 1. Notify frontend: Agent is thinking
        await callback_fn({
            "type": "status",
            "status": "thinking",
            "file": None
        })

        # 2. Build multi-turn context
        prompt_lines = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dynamic_system = f"{SYSTEM_PROMPT}\n\nCurrent System Time: {current_time}"
        prompt_lines.append(f"System: {dynamic_system}")

        for msg in conversation_history:
            role_tag = "Assistant" if msg["role"] == "assistant" else "System" if msg["role"] == "system" else "User"
            prompt_lines.append(f"{role_tag}: {msg['content']}")
        llm_prompt = "\n".join(prompt_lines) + "\nAssistant:"

        # 3. Call LLM Manager
        loop = asyncio.get_running_loop()
        raw_response = await loop.run_in_executor(None, get_llm_response, llm_prompt, "", PRIMARY_MODEL)
        
        # Clean response string
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()

        # 4. Parse LLM response JSON
        try:
            repaired = repair_json(cleaned_response)
            action = json.loads(repaired)
        except Exception as parse_err:
            logger.error(f"Failed to parse agent actions: {parse_err}. Response was: {cleaned_response}")
            error_msg = f"Parser Error: Your response was not valid JSON. Please repeat using valid JSON format."
            conversation_history.append({"role": "assistant", "content": cleaned_response})
            conversation_history.append({"role": "user", "content": error_msg})
            continue

        # Log reasoning
        thought = action.get("thought", "Thinking...")
        logger.info(f"Agent Thought: {thought}")

        # 5. Check if it is a final answer
        if "final_answer" in action:
            final_text = action["final_answer"]
            conversation_history.append({"role": "assistant", "content": json.dumps(action)})
            await callback_fn({
                "type": "final_answer",
                "text": final_text
            })
            return

        # 6. Check if it is a tool execution
        tool_name = action.get("tool")
        args = action.get("args", {})

        if not tool_name:
            error_msg = "Error: You must specify either 'tool' or 'final_answer'."
            conversation_history.append({"role": "assistant", "content": json.dumps(action)})
            conversation_history.append({"role": "user", "content": error_msg})
            continue

        tool_result = ""
        logger.info(f"Executing tool {tool_name} with args {args}")

        try:
            if tool_name == "list_files":
                await callback_fn({"type": "status", "status": "reading", "file": "directory tree"})
                files = list_files(session_id)
                tool_result = json.dumps({"files": files})

            elif tool_name == "read_file":
                path = args.get("path", "")
                await callback_fn({"type": "status", "status": "reading", "file": path})
                await asyncio.sleep(0.5)
                file_content = read_file(session_id, path)
                tool_result = json.dumps({"content": file_content})

            elif tool_name == "write_file":
                path = args.get("path", "")
                content = args.get("content", "")
                await callback_fn({"type": "status", "status": "writing", "file": path})
                await asyncio.sleep(0.5)
                write_file(session_id, path, content)
                tool_result = json.dumps({"status": "success", "message": f"File '{path}' written successfully."})
                await callback_fn({"type": "file_modified", "path": path, "content": content})

            elif tool_name == "run_code":
                path = args.get("path", "")
                await callback_fn({"type": "status", "status": "running", "file": path})
                await asyncio.sleep(0.5)
                exec_result = await run_code(session_id, path)
                tool_result = json.dumps(exec_result)

            elif tool_name == "search_web":
                query = args.get("query", "")
                await callback_fn({"type": "status", "status": "searching", "file": query})
                await asyncio.sleep(0.5)
                loop = asyncio.get_running_loop()
                search_result = await loop.run_in_executor(None, execute_search_web, query)
                tool_result = json.dumps(search_result)

            elif tool_name == "search_wikipedia":
                query = args.get("query", "")
                await callback_fn({"type": "status", "status": "wikipedia", "file": query})
                loop = asyncio.get_running_loop()
                res = await loop.run_in_executor(None, execute_search_wikipedia, query)
                tool_result = json.dumps(res)

            else:
                tool_result = json.dumps({"error": f"Unknown tool name: {tool_name}"})

        except Exception as tool_err:
            logger.error(f"Tool {tool_name} failed: {tool_err}")
            tool_result = json.dumps({"status": "error", "message": str(tool_err)})

        await callback_fn({
            "type": "tool_executed",
            "tool": tool_name,
            "args": args,
            "result": tool_result
        })

        conversation_history.append({"role": "assistant", "content": json.dumps(action)})
        conversation_history.append({"role": "user", "content": f"Tool '{tool_name}' result: {tool_result}"})

    await callback_fn({
        "type": "final_answer",
        "text": "I attempted to resolve the task but exceeded the maximum execution steps. Please try running the tests or checking the code logs."
    })
