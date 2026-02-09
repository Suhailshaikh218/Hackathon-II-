from fastapi.testclient import TestClient
from main import app

# Simple test without overriding dependencies
client = TestClient(app)

# Test the root endpoint
response = client.get("/")
print("Status Code:", response.status_code)
print("Response:", response.json())

print("\nTesting completed successfully!")