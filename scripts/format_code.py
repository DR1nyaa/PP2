#!/usr/bin/env python3
"""
Script to format code according to PEP8 standards.
"""
import os
import subprocess
import sys


def run_command(command):
    """Run shell command and return result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"Error running command: {e}")
        return 1, "", str(e)


def main():
    """Main function to format code."""
    print("Formatting code with Black...")
    returncode, stdout, stderr = run_command("black .")
    if returncode != 0:
        print(f"Black error: {stderr}")
        return returncode

    print("Sorting imports with isort...")
    returncode, stdout, stderr = run_command("isort .")
    if returncode != 0:
        print(f"isort error: {stderr}")
        return returncode

    print("Checking code style with flake8...")
    returncode, stdout, stderr = run_command("flake8 .")
    if returncode != 0:
        print(f"flake8 found issues: {stdout}")
        # Don't fail, just show warnings
        return 0

    print("Code formatting completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())