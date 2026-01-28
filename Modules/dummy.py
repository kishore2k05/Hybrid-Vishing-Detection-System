#!/usr/bin/env python3
import sys
import os

# Add the Modules directory to path
sys.path.append(os.path.dirname(__file__))

# Import the function
from gemini_module import convert_with_gemini

print("="*60)
print("TESTING GEMINI MODULE")
print("="*60)

# Test 1: Simple Tanglish translation
print("\nTest 1: Translating to Tanglish...")
text = "The printer is not working"
result = convert_with_gemini(text, "Tanglish")

if result:
    print(f"✓ SUCCESS!")
    print(f"Input: {text}")
    print(f"Output: {result}")
else:
    print(f"✗ FAILED - Function returned None")

# Test 2: Simple Hinglish translation
print("\n" + "="*60)
print("\nTest 2: Translating to Hinglish...")
text = "The computer is not turning on"
result = convert_with_gemini(text, "Hinglish")

if result:
    print(f"✓ SUCCESS!")
    print(f"Input: {text}")
    print(f"Output: {result}")
else:
    print(f"✗ FAILED - Function returned None")

print("\n" + "="*60)
print("TESTING COMPLETE")
print("="*60)