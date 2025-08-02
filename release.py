#!/usr/bin/env python3
"""
Release script for Convo Programming Language v0.0.1
Initial production release with core features
"""

import subprocess
import sys
import os
from datetime import datetime

# Current version for initial release
CURRENT_VERSION = "v0.0.1"
RELEASE_NAME = "Initial Release - Core Programming Language"

def run_command(cmd):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def get_current_version():
    """Get the current version from git tags"""
    try:
        return run_command("git describe --tags --abbrev=0")
    except:
        return "v0.0.0"

def create_release(version, message):
    """Create a new release"""
    print(f"Creating production release {version}...")
    
    # Run tests first
    print("Running tests...")
    run_command("python -m pytest tests/ -v")
    print("✅ All tests passed!")
    
    # Create git tag
    print(f"Creating tag {version}...")
    run_command(f'git tag -a {version} -m "{message}"')
    
    # Push tag
    print("Pushing tag to GitHub...")
    run_command(f"git push origin {version}")
    
    print(f"🎉 Release {version} created successfully!")
    print(f"View at: https://github.com/DreadHeadHippy/Convo/releases/tag/{version}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python release.py <version> <message>")
        print("Example: python release.py v0.0.1 'Initial production release'")
        sys.exit(1)
    
    version = sys.argv[1]
    message = sys.argv[2]
    
    if not version.startswith('v'):
        version = 'v' + version
    
    # Ensure we're on main branch
    current_branch = run_command("git branch --show-current")
    if current_branch != "main":
        print("Error: Must be on main branch to create release")
        sys.exit(1)
    
    # Ensure working directory is clean
    status = run_command("git status --porcelain")
    if status:
        print("Error: Working directory must be clean")
        print("Commit or stash your changes first")
        sys.exit(1)
    
    create_release(version, message)

if __name__ == "__main__":
    main()
