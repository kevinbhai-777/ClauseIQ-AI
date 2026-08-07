"""
Test script to debug Uvicorn request handling
"""
import sys
import threading
import time

def start_server():
    import uvicorn
    try:
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="debug",
            access_log=True
        )
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()

# Start server in background thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(3)

# Test endpoint
try:
    import requests
    print("Testing root endpoint...")
    response = requests.get("http://127.0.0.1:8000/", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

time.sleep(2)
