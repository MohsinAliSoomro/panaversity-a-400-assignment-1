#!/usr/bin/env python3
"""
Test script to demonstrate JWT authentication flow
"""

from agent import generate, session

print("=" * 60)
print("JWT Authentication Flow Test")
print("=" * 60)

# Test 1: Try to create task without login (should fail)
print("\n[TEST 1] Attempting to create task WITHOUT login...")
print("-" * 60)
generate("Create a task to buy groceries with high priority")

print("\n" + "=" * 60)

# Test 2: Login first
print("\n[TEST 2] Logging in user...")
print("-" * 60)
generate("Login user with email mohsin@gmail.com and password Test@123")

print("\n" + "=" * 60)

# Test 3: Now create task (should succeed)
print("\n[TEST 3] Creating task AFTER login...")
print("-" * 60)
generate("Create a task to buy groceries with high priority")

print("\n" + "=" * 60)

# Test 4: Get all tasks
print("\n[TEST 4] Getting all tasks...")
print("-" * 60)
generate("Show me all my tasks")

print("\n" + "=" * 60)
print(f"\nFinal Session Status: {'Authenticated ✅' if session.is_authenticated() else 'Not authenticated ❌'}")
if session.user_email:
    print(f"User Email: {session.user_email}")
print("=" * 60)
