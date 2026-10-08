import requests
import json

response = requests.post("http://127.0.0.1:8001/chat", json={
    "session_id": "test-session-123",
    "message": "e roju special news enti?"
})
print(response.json())
