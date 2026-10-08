import os
import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.session_manager import check_session_exists, get_session_path
from backend.file_manager import read_file, write_file, list_files
from backend.llm_manager import get_llm_response, ALERTS_LOG_PATH

client = TestClient(app)

def test_session_lifecycle():
    # 1. Create session
    response = client.post("/session/create")
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    session_id = data["session_id"]
    assert check_session_exists(session_id) is True
    
    # Verify the actual directory exists on disk
    session_dir = get_session_path(session_id)
    assert os.path.exists(session_dir) is True
    assert os.path.isdir(session_dir) is True

    # 2. Destroy session
    del_response = client.delete(f"/session/{session_id}")
    assert del_response.status_code == 200
    assert check_session_exists(session_id) is False
    
    # Verify the actual directory is deleted properly from disk
    assert os.path.exists(session_dir) is False

def test_file_crud_operations():
    # Create temp session
    response = client.post("/session/create")
    session_id = response.json()["session_id"]

    try:
        # Create a file
        create_res = client.post(
            f"/files/{session_id}",
            json={"path": "subfolder/hello.py", "type": "file", "content": "print('hello world')"}
        )
        assert create_res.status_code == 200
        
        # Read the file
        read_res = client.get(f"/files/{session_id}/subfolder/hello.py")
        assert read_res.status_code == 200
        file_data = read_res.json()
        assert file_data["content"] == "print('hello world')"
        assert file_data["language"] == "python"

        # Update the file
        update_res = client.put(
            f"/files/{session_id}/subfolder/hello.py",
            json={"content": "print('hello new world')"}
        )
        assert update_res.status_code == 200

        # Read again to verify change
        read_res2 = client.get(f"/files/{session_id}/subfolder/hello.py")
        assert read_res2.json()["content"] == "print('hello new world')"

        # Delete file
        delete_res = client.delete(f"/files/{session_id}/subfolder/hello.py")
        assert delete_res.status_code == 200

        # Read should return 404 now
        read_res3 = client.get(f"/files/{session_id}/subfolder/hello.py")
        assert read_res3.status_code == 404

    finally:
        client.delete(f"/session/{session_id}")

def test_code_runner_execution():
    # Create temp session
    response = client.post("/session/create")
    session_id = response.json()["session_id"]

    try:
        # Write buggy python file
        client.post(
            f"/files/{session_id}",
            json={"path": "buggy.py", "type": "file", "content": "print(1 / 0)"}
        )

        # Run buggy python file
        run_res = client.post(f"/run/{session_id}", json={"path": "buggy.py"})
        assert run_res.status_code == 200
        run_data = run_res.json()
        assert "ZeroDivisionError" in run_data["stderr"]
        assert run_data["exit_code"] != 0

        # Write clean python file
        client.post(
            f"/files/{session_id}",
            json={"path": "clean.py", "type": "file", "content": "print('100% correct')" }
        )

        # Run clean python file
        run_clean_res = client.post(f"/run/{session_id}", json={"path": "clean.py"})
        assert run_clean_res.status_code == 200
        run_clean_data = run_clean_res.json()
        assert "100% correct" in run_clean_data["stdout"].strip()
        assert run_clean_data["exit_code"] == 0

    finally:
        client.delete(f"/session/{session_id}")

def test_agent_websocket_handshake():
    # Create session
    response = client.post("/session/create")
    session_id = response.json()["session_id"]

    try:
        # Connect to websocket
        with client.websocket_connect(f"/ws/{session_id}") as websocket:
            # We just close it to verify handshake completes successfully
            pass
    finally:
        client.delete(f"/session/{session_id}")

def test_agent_memory():
    # Programmatically verify that the WebSocket connection preserves conversation history across prompts
    response = client.post("/session/create")
    session_id = response.json()["session_id"]

    received_histories = []

    # Mock the execute_agent_loop to just record the history it received and simulate a response
    async def mock_execute_agent_loop(sid, prompt, cb, hist):
        # The real agent.py appends the user prompt to the history when it starts
        hist.append({"role": "user", "content": prompt})
        
        # Record a copy of the history at this point
        received_histories.append(list(hist))
        
        # Simulate the LLM's final answer being appended to history
        hist.append({"role": "assistant", "content": "mock final answer"})
        
        # Send the final answer back to the client
        await cb({"type": "final_answer", "text": "mock final answer"})

    try:
        with patch("backend.main.execute_agent_loop", new=mock_execute_agent_loop):
            with client.websocket_connect(f"/ws/{session_id}") as websocket:
                # Turn 1
                websocket.send_json({"prompt": "Hello!"})
                # Read the response
                resp1 = websocket.receive_json()
                assert resp1["type"] == "final_answer"
                
                # Turn 2
                websocket.send_json({"prompt": "My favorite color is indigo."})
                resp2 = websocket.receive_json()
                assert resp2["type"] == "final_answer"
                
        # Verification
        assert len(received_histories) == 2
        hist1 = received_histories[0]
        hist2 = received_histories[1]
        
        # Turn 1 history should be: [System Prompt, User: "Hello!"]
        assert len(hist1) == 2
        assert hist1[0]["role"] == "system"
        assert hist1[1]["role"] == "user"
        assert hist1[1]["content"] == "Hello!"
        
        # Turn 2 history should be: [System Prompt, User: "Hello!", Assistant: "mock...", User: "My favorite..."]
        assert len(hist2) == 4
        assert hist2[2]["role"] == "assistant"
        assert hist2[2]["content"] == "mock final answer"
        assert hist2[3]["role"] == "user"
        assert hist2[3]["content"] == "My favorite color is indigo."
        
    finally:
        client.delete(f"/session/{session_id}")

def test_llm_outage_alert_logging():
    initial_log_exists = os.path.exists(ALERTS_LOG_PATH)
    initial_size = os.path.getsize(ALERTS_LOG_PATH) if initial_log_exists else 0

    # Mock call_glm_primary to fail so fallback and alerts are triggered
    # Mock call_hy3_fallback to return a successful mock response
    with patch("backend.llm_manager.call_glm_primary", side_effect=Exception("API Key revoked or network down")), \
         patch("backend.llm_manager.call_hy3_fallback", return_value='{"thought": "fixing bug", "final_answer": "recursion bug in the Fibonacci"}'):
        response = get_llm_response("fix the bug in main.py")
        assert "recursion bug in the Fibonacci" in response

    # Verify that a new entry was appended to the alerts.log file
    assert os.path.exists(ALERTS_LOG_PATH) is True
    new_size = os.path.getsize(ALERTS_LOG_PATH)
    assert new_size > initial_size

    # Verify the contents of the log contains the outage header
    with open(ALERTS_LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()
        assert "CRITICAL: LiveCodeAI LLM Provider Outage" in log_content
        assert "API Key revoked or network down" in log_content

def test_total_system_failure():
    # Programmatically test the scenario where BOTH the primary LLM and all fallback models crash.
    # The system must not crash the web loop, but instead log an "ALL Services Offline" email and send a UI message.
    
    with patch("backend.llm_manager.call_glm_primary", side_effect=Exception("Primary Down")), \
         patch("backend.llm_manager.call_hy3_fallback", side_effect=Exception("Hy3 Down")), \
         patch("backend.llm_manager.call_minimax_fallback", side_effect=Exception("MiniMax Down")):
        
        # This should return the formatted JSON error instead of raising an unhandled exception
        response_json_str = get_llm_response("write a sorting function")
        
        # Verify JSON is valid and contains the critical message
        parsed = json.loads(response_json_str)
        assert "final_answer" in parsed
        assert "CRITICAL SYSTEM FAILURE" in parsed["final_answer"]
        
    # Verify the catastrophic failure was logged via the email alert system
    with open(ALERTS_LOG_PATH, "r", encoding="utf-8") as f:
        log_contents = f.read()
        assert "CRITICAL: ALL LiveCodeAI Services Offline" in log_contents
        assert "CATASTROPHIC FAILURE" in log_contents

def test_all_languages_runners():
    response = client.post("/session/create")
    session_id = response.json()["session_id"]

    try:
        # 1. Javascript
        client.post(f"/files/{session_id}", json={"path": "script.js", "type": "file", "content": "console.log('hello js');"})
        js_res = client.post(f"/run/{session_id}", json={"path": "script.js"})
        assert js_res.status_code == 200
        assert "hello js" in js_res.json()["stdout"].strip()

        # 2. TypeScript
        client.post(f"/files/{session_id}", json={"path": "script.ts", "type": "file", "content": "const msg: string = 'hello ts'; console.log(msg);"})
        ts_res = client.post(f"/run/{session_id}", json={"path": "script.ts"})
        assert ts_res.status_code == 200
        assert "hello ts" in ts_res.json()["stdout"].strip()

        # 3. Bash
        client.post(f"/files/{session_id}", json={"path": "script.sh", "type": "file", "content": "echo 'hello bash'"})
        sh_res = client.post(f"/run/{session_id}", json={"path": "script.sh"})
        assert sh_res.status_code == 200
        assert "hello bash" in sh_res.json()["stdout"].strip()

        # 4. C++
        cpp_code = """#include <iostream>
int main() {
    std::cout << "hello cpp" << std::endl;
    return 0;
}"""
        client.post(f"/files/{session_id}", json={"path": "script.cpp", "type": "file", "content": cpp_code})
        cpp_res = client.post(f"/run/{session_id}", json={"path": "script.cpp"})
        assert cpp_res.status_code == 200
        assert "hello cpp" in cpp_res.json()["stdout"].strip()

        # 5. C
        c_code = """#include <stdio.h>
int main() {
    printf("hello c\\n");
    return 0;
}"""
        client.post(f"/files/{session_id}", json={"path": "script.c", "type": "file", "content": c_code})
        c_res = client.post(f"/run/{session_id}", json={"path": "script.c"})
        assert c_res.status_code == 200
        assert "hello c" in c_res.json()["stdout"].strip()

    finally:
        client.delete(f"/session/{session_id}")
