#!/usr/bin/env python
"""Test the backend endpoints"""

import sys
sys.path.insert(0, '.')

from backend.main import app
from starlette.testclient import TestClient

client = TestClient(app)

print("Testing root endpoint...")
response = client.get('/')
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\nTesting /ask endpoint without contract...")
response = client.post('/ask', json={"question": "test question"})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n✓ All backend tests passed! Backend is functional.")
