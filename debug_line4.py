#!/usr/bin/env python3
"""
Debug script to check line 4 of app.py
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print(f"Total lines: {len(lines)}")
print(f"Line 4: '{lines[3].strip()}'")
print(f"Line 4 repr: {repr(lines[3])}")

# Show first 10 lines
print("\nFirst 10 lines:")
for i, line in enumerate(lines[:10], 1):
    print(f"{i:2d}: {repr(line)}")