#!/usr/bin/env python3
"""
MindMate Backend Test Script
Tests the /chat endpoint with various scenarios
"""

import requests
import json
import sys
import time

# Configuration
BACKEND_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_123"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def test_health():
    """Test health check endpoint"""
    print_info("Testing /health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            print_success("Health check passed")
            print(f"  Status: {response.json()['status']}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is it running on port 5000?")
        return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_chat(message, user_id=TEST_USER_ID):
    """Test chat endpoint with a message"""
    try:
        payload = {
            "message": message,
            "userId": user_id
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            return False, response.json()
    except requests.exceptions.Timeout:
        return False, {"error": "Request timeout (Gemini API may be slow)"}
    except Exception as e:
        return False, {"error": str(e)}

def run_tests():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}MindMate Backend Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Test 1: Health check
    print_info("Test 1/5: Health Check")
    health_ok = test_health()
    time.sleep(1)
    
    if not health_ok:
        print_error("Backend is not running. Please start it with: python app.py")
        sys.exit(1)
    
    # Test 2: Normal conversation
    print_info("\nTest 2/5: Normal Conversation")
    print("  Sending: 'I'm feeling stressed about placements'")
    success, response = test_chat("I'm feeling stressed about placements")
    
    if success:
        print_success(f"Response received")
        print(f"  Reply: {response.get('reply', 'N/A')[:100]}...")
        print(f"  Warning: {response.get('warning', False)}")
    else:
        print_error(f"Failed: {response.get('error', 'Unknown error')}")
    
    time.sleep(1)
    
    # Test 3: Distress detection
    print_info("\nTest 3/5: Distress Detection")
    print("  Sending: 'I want to end it all'")
    success, response = test_chat("I want to end it all")
    
    if success:
        print_success(f"Response received")
        if response.get('warning'):
            print_success("⚠️  Distress detected correctly")
            print(f"  Safety Message: {response.get('safetyMessage', 'N/A')[:80]}...")
            if response.get('resources'):
                print(f"  Resources provided: {len(response.get('resources', []))} items")
        else:
            print_warning("Distress keyword not detected (may need adjustment)")
    else:
        print_error(f"Failed: {response.get('error', 'Unknown error')}")
    
    time.sleep(1)
    
    # Test 4: Empty message
    print_info("\nTest 4/5: Error Handling (Empty Message)")
    print("  Sending: '' (empty)")
    success, response = test_chat("")
    
    if not success:
        print_success(f"Error handled correctly: {response.get('error', 'N/A')}")
    else:
        print_error("Empty message should be rejected")
    
    time.sleep(1)
    
    # Test 5: Long message
    print_info("\nTest 5/5: Error Handling (Long Message)")
    long_msg = "a" * 6000
    print(f"  Sending: {len(long_msg)} character message")
    success, response = test_chat(long_msg)
    
    if not success:
        print_success(f"Long message rejected: {response.get('error', 'N/A')[:50]}...")
    else:
        print_error("Long message should be rejected")
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print_success("All tests completed!")
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(0)
