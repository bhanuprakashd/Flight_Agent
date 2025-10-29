#!/usr/bin/env python
"""Verify MCP server dependencies are installed"""
import sys

def check_dependency(name, package_name=None):
    """Check if a dependency is available"""
    if package_name is None:
        package_name = name
    try:
        __import__(name)
        print(f"✓ {package_name} is available")
        return True
    except ImportError as e:
        print(f"✗ {package_name} is NOT available: {e}")
        return False

def main():
    print("=" * 60)
    print("MCP Server Dependency Check")
    print("=" * 60)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print()
    
    dependencies = [
        ("mcp", "mcp"),
        ("primp", "primp"),
        ("google.protobuf", "protobuf"),
        ("selectolax", "selectolax"),
        ("playwright", "playwright"),
    ]
    
    all_ok = True
    for module_name, package_name in dependencies:
        if not check_dependency(module_name, package_name):
            all_ok = False
    
    print()
    if all_ok:
        print("=" * 60)
        print("✓ All dependencies are available!")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("✗ Some dependencies are missing!")
        print("Install them with:")
        print("  pip install mcp primp protobuf selectolax playwright")
        print("  playwright install")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
