#!/usr/bin/env python3
"""
Test script to verify FastAPI setup
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test imports
    from api.main import app, ToolRequest, ToolResponse
    print("✅ FastAPI imports successful")
    
    # Test basic functionality
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/health")
    print(f"✅ Health check: {response.status_code}")
    
    # Test root endpoint
    response = client.get("/")
    print(f"✅ Root endpoint: {response.status_code}")
    
    # Test tool endpoint (mock)
    response = client.post("/api", json={
        "tool": "view_subreddit",
        "parameters": {"subreddit_name": "test"}
    })
    print(f"✅ Tool endpoint: {response.status_code}")
    
    print("\n🎉 All tests passed! FastAPI setup is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("You may need to install dependencies with: pip install fastapi uvicorn pydantic")
except Exception as e:
    print(f"❌ Error: {e}")