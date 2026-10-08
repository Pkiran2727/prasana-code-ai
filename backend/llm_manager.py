import os
import time
import re
import logging, json
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
from backend.config import BASE_DIR

logger = logging.getLogger(__name__)

# Configure primary GLM-4.7-Flash credentials
GLM_API_KEY = os.environ.get("GLM_API_KEY", "")
GLM_BASE_URL = "https://api.z.ai/api/paas/v4/"
GLM_MODEL_NAME = "glm-4.7-Flash"

ALERT_EMAIL_TARGET = "mandaprasannakiran@gmail.com"
ALERTS_LOG_PATH = os.path.join(BASE_DIR, "backend", "alerts.log")

def log_and_send_email_alert(subject: str, body_text: str, send_email: bool = True):
    """
    Logs email alert to alerts.log (Option 3) and dispatches real email via Resend API (Option 2) if configured.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"=== ALERT [{timestamp}] ===\nSubject: {subject}\nTo: {ALERT_EMAIL_TARGET}\n\n{body_text}\n"
    
    # 1. ALWAYS write to local alerts.log file (Option 3)
    try:
        with open(ALERTS_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry + "\n")
        logger.info(f"LLM Alert written to local alert log file: {ALERTS_LOG_PATH}")
    except Exception as log_err:
        logger.error(f"Failed to write to alert log file: {log_err}")

    if not send_email:
        return

    # 2. Check for Resend API Key (Option 2)
    resend_api_key = os.environ.get("RESEND_API_KEY", "")
    if resend_api_key:
        try:
            import urllib.request
            req_data = json.dumps({
                "from": "Prasana Code AI Alert <onboarding@resend.dev>",
                "to": [ALERT_EMAIL_TARGET],
                "subject": subject,
                "text": body_text
            }).encode("utf-8")
            
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            req = urllib.request.Request("https://api.resend.com/emails", data=req_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                logger.info(f"Alert email dispatched via Resend API to {ALERT_EMAIL_TARGET}. Status: {resp.status}")
                return
        except Exception as resend_err:
            logger.error(f"Failed to send email via Resend API: {resend_err}")

    # 3. Fallback to standard SMTP if configured
    smtp_server = os.environ.get("SMTP_SERVER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    if smtp_server and smtp_password:
        try:
            msg = MIMEText(body_text)
            msg["Subject"] = subject
            msg["From"] = ALERT_EMAIL_TARGET
            msg["To"] = ALERT_EMAIL_TARGET

            with smtplib.SMTP(smtp_server, int(os.environ.get("SMTP_PORT", "587"))) as server:
                server.starttls()
                server.login(ALERT_EMAIL_TARGET, smtp_password)
                server.sendmail(ALERT_EMAIL_TARGET, [ALERT_EMAIL_TARGET], msg.as_string())
            logger.info(f"Alert email sent successfully to {ALERT_EMAIL_TARGET} via SMTP.")
        except Exception as smtp_err:
            logger.error(f"Failed to dispatch SMTP email: {smtp_err}")

def call_glm_primary(prompt: str, sys_prompt: str = "") -> str:
    """
    Calls primary GLM-4.7-Flash with 2 retries (total 3 attempts).
    """
    if not sys_prompt:
        sys_prompt = (
            "You are a highly capable AI coding assistant. "
            "Help the user edit, write, and run code."
        )

    client = OpenAI(
        api_key=GLM_API_KEY,
        base_url=GLM_BASE_URL
    )

    max_attempts = 3  # Initial + 2 retries
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Calling GLM-4.7-Flash (Attempt {attempt}/{max_attempts})...")
            response = client.chat.completions.create(
                model=GLM_MODEL_NAME,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=False,
                extra_body={
                    "thinking": {
                        "type": "enabled",
                    },
                },
                timeout=30.0
            )
            content = response.choices[0].message.content
            logger.info("Successfully received response from GLM-4.7-Flash.")
            return content
        except Exception as err:
            logger.warning(f"GLM-4.7-Flash attempt {attempt} failed: {err}")
            if attempt < max_attempts:
                # Wait 1.5 seconds before retrying
                time.sleep(1.5)
            else:
                # Exhausted all attempts
                raise err

def extract_json_block(response_text: str) -> str:
    logger.debug("🧩 In the extraction function...")
    logger.debug("=" * 80)
    logger.debug("📄 FULL RESPONSE TEXT:")
    logger.debug(response_text)
    logger.debug("=" * 80)
    logger.debug(f"📏 Response length: {len(response_text)} characters")
    
    # 2. Try to extract code block
    logger.debug("🔍 Step 2: Checking for code blocks...")
    
    # First try ```json ... ```
    match = re.search(r"```json\s*([\s\S]*?)\s*```", response_text)
    if match:
        logger.debug("✅ Found ```json code block")
        return match.group(1).strip()
    
    # Then try any ``` ... ```
    match = re.search(r"```\s*(?:json)?\s*([\s\S]*?)\s*```", response_text)
    if match:
        logger.debug("✅ Found ``` code block")
        candidate = match.group(1).strip()
        # Remove language identifier if present at the start
        if candidate.startswith(('json', 'JSON')):
            candidate = candidate[4:].strip()
        return candidate
    
    logger.debug("✗ No code blocks found")
    
    # 1. Try to extract from **Answer**: section if present
    logger.debug("🔍 Step 1: Checking for **Answer**: section...")
    answer_match = re.search(r'\*\*Answer\*\*:\s*([\s\S]*)', response_text, re.IGNORECASE)
    if answer_match:
        logger.debug("✓ Found **Answer**: section")
        answer_section = answer_match.group(1).strip()
        logger.debug("✅ Extracted content from **Answer**: section")
        return answer_section
    else:
        logger.debug("✗ No **Answer**: section found")
    
    # 3. Try to find content between first { and last }
    logger.debug("🔍 Step 3: Looking for content between first { and last }...")
    first_brace = response_text.find('{')
    last_brace = response_text.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        extracted = response_text[first_brace:last_brace + 1]
        logger.debug(f"✅ Found content between braces (from position {first_brace} to {last_brace})")
        logger.debug("=" * 80)
        logger.debug("📦 EXTRACTED CONTENT:")
        logger.debug(extracted)
        logger.debug("=" * 80)
        return extracted
    else:
        logger.debug("✗ No valid brace pairs found")
    
    # 4. Return the entire response as-is
    logger.debug("🔍 Step 4: Returning entire response as-is...")
    logger.debug("✅ Returning full response text")
    return response_text.strip()

def wrap_in_json_if_needed(response_text: str) -> str:
    """
    Ensures that fallback model output is a valid JSON string containing final_answer.
    If the response is plain text or invalid JSON structure, wraps it appropriately.
    """
    cleaned = extract_json_block(response_text)

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            if "final_answer" not in parsed and "tool" not in parsed:
                # LLM returned valid JSON but with wrong schema (e.g. {"response": "..."})
                extracted_text = ""
                if "response" in parsed:
                    extracted_text = parsed["response"]
                elif "message" in parsed:
                    extracted_text = parsed["message"]
                elif "text" in parsed:
                    extracted_text = parsed["text"]
                elif "answer" in parsed:
                    extracted_text = parsed["answer"]
                else:
                    # Just stringify the values if we don't recognize the key
                    extracted_text = " ".join(str(v) for v in parsed.values())
                    
                return json.dumps({
                    "thought": "Extracted response from fallback model",
                    "final_answer": extracted_text
                })
        return cleaned
    except Exception:
        # Wrap plain text in standard response format
        return json.dumps({
            "thought": "Responding in system fallback mode",
            "final_answer": response_text
        })

def call_qwen_openrouter(prompt: str, sys_prompt: str = "") -> str:
    """
    Calls qwen/qwen3-next-80b-a3b-instruct:free via OpenRouter.
    """
    if not sys_prompt:
        sys_prompt = "You are a highly capable AI coding assistant."
        
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")
        
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Calling OpenRouter Qwen (Attempt {attempt}/{max_attempts})...")
            response = client.chat.completions.create(
                model="qwen/qwen3-next-80b-a3b-instruct:free",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ],
            )
            content = response.choices[0].message.content
            logger.info("Successfully received response from OpenRouter Qwen.")
            return content
        except Exception as e:
            logger.warning(f"OpenRouter Qwen attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(1.5)
            else:
                raise e

def get_llm_response(prompt: str, sys_prompt: str = "", model: str = "GLM") -> str:
    """
    Routes to either GLM or QWEN based on the model parameter.
    If remote API keys are unavailable or rate-limited, provides an offline educational response.
    """
    try:
        if model == "QWEN":
            return call_qwen_openrouter(prompt, sys_prompt)
        else:
            return call_glm_primary(prompt, sys_prompt)
    except Exception as err:
        err_msg = f"LLM call failed for model {model}: {str(err)}"
        logger.warning(err_msg)
        
        # Log to alerts.log
        log_and_send_email_alert(
            subject=f"CRITICAL: Prasana Code AI LLM Provider Outage ({model})",
            body_text=f"LLM Provider status: {err_msg}",
            send_email=False
        )
        
        # Educational fallback response generator for story or coding questions
        prompt_lower = prompt.lower()
        if "story" in prompt_lower or "kids" in prompt_lower:
            story_text = (
                "Once upon a time in a magical digital kingdom named CodeLand, there was a friendly little AI robot named Sparky. "
                "Sparky loved to help children solve puzzles by putting colorful blocks of code together. "
                "One sunny afternoon, Sparky helped a young kitten write a Python script to count all the stars in the night sky! "
                "The kitten learned that with loops and conditionals, any big dream can be built line by line. "
                "And from that day on, all the young coders in CodeLand created amazing games and lived happily ever after."
            )
            return json.dumps({
                "thought": "Generated kid-friendly educational story fallback response.",
                "final_answer": story_text
            })
            
        return json.dumps({
            "thought": "Providing Prasana AI Tutor coding fallback guidance.",
            "final_answer": (
                "🤖 **Prasana AI Tutor Guidance:**\n\n"
                "I am here to help you debug and master your code! "
                "Check your variables, ensure your loops have proper exit conditions, and try running the test cases again."
            )
        })


