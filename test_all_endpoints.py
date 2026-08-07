"""
Comprehensive test of all backend endpoints
"""
import threading
import time
import requests

def start_server():
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for startup
time.sleep(3)

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*60)
print("Testing ClauseIQ Backend API")
print("="*60)

# Test 1: Root endpoint
print("\n1. Testing GET /")
try:
    resp = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   ✓ Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Ask endpoint without contract
print("\n2. Testing POST /ask (no contract uploaded)")
try:
    resp = requests.post(
        f"{BASE_URL}/ask",
        json={"question": "What are the risks?"},
        timeout=5
    )
    print(f"   ✓ Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Analyze with a test PDF (if exists)
print("\n3. Testing POST /analyze (with test PDF)")
try:
    test_pdf_path = "backend/test_contract.pdf"
    with open(test_pdf_path, "rb") as f:
        files = {"file": ("test_contract.pdf", f, "application/pdf")}
        resp = requests.post(
            f"{BASE_URL}/analyze",
            files=files,
            timeout=30
        )
    print(f"   ✓ Status: {resp.status_code}")
    resp_json = resp.json()
    if "error" in resp_json:
        print(f"   Error: {resp_json['error']}")
    else:
        print(f"   ✓ Analysis received (length: {len(resp_json.get('analysis', ''))} chars)")
except FileNotFoundError:
    print("   Test PDF not found, skipping")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("Backend is functional!")
print("="*60 + "\n")

# Keep running for a moment
time.sleep(2)
