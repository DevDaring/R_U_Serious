#!/usr/bin/env python3
"""
R U Serious? Backend - Installation Verification Script

This script verifies that all files are in place and the system is ready to run.
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def check_file_exists(file_path: Path) -> bool:
    """Check if a file exists"""
    return file_path.exists() and file_path.is_file()


def check_directory_exists(dir_path: Path) -> bool:
    """Check if a directory exists"""
    return dir_path.exists() and dir_path.is_dir()


def print_status(message: str, status: bool):
    """Print status with color"""
    symbol = f"{GREEN}[OK]{RESET}" if status else f"{RED}[FAIL]{RESET}"
    print(f"  {symbol} {message}")


def main():
    """Main verification function"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}R U Serious? Backend - Installation Verification{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")

    backend_dir = Path(__file__).parent
    all_checks_passed = True

    # Core files to check
    print(f"{YELLOW}Checking Core Files...{RESET}")
    core_files = [
        "app/main.py",
        "app/config.py",
        "app/api/dependencies.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
    ]

    for file_path in core_files:
        full_path = backend_dir / file_path
        exists = check_file_exists(full_path)
        print_status(file_path, exists)
        if not exists:
            all_checks_passed = False

    # Route files
    print(f"\n{YELLOW}Checking API Route Files...{RESET}")
    route_files = [
        "app/api/routes/auth.py",
        "app/api/routes/users.py",
        "app/api/routes/learning.py",
        "app/api/routes/quiz.py",
        "app/api/routes/avatar.py",
        "app/api/routes/characters.py",
        "app/api/routes/voice.py",
        "app/api/routes/video.py",
        "app/api/routes/tournaments.py",
        "app/api/routes/teams.py",
        "app/api/routes/chat.py",
        "app/api/routes/admin.py",
    ]

    for file_path in route_files:
        full_path = backend_dir / file_path
        exists = check_file_exists(full_path)
        print_status(file_path, exists)
        if not exists:
            all_checks_passed = False

    # Utility files
    print(f"\n{YELLOW}Checking Utility Files...{RESET}")
    utility_files = [
        "app/utils/helpers.py",
        "run.py",
        "start.bat",
        "start.sh",
    ]

    for file_path in utility_files:
        full_path = backend_dir / file_path
        exists = check_file_exists(full_path)
        print_status(file_path, exists)
        if not exists:
            all_checks_passed = False

    # Documentation files
    print(f"\n{YELLOW}Checking Documentation...{RESET}")
    doc_files = [
        "README.md",
        "API_DOCUMENTATION.md",
        "IMPLEMENTATION_SUMMARY.md",
    ]

    for file_path in doc_files:
        full_path = backend_dir / file_path
        exists = check_file_exists(full_path)
        print_status(file_path, exists)
        if not exists:
            all_checks_passed = False

    # Directory structure
    print(f"\n{YELLOW}Checking Directory Structure...{RESET}")
    required_dirs = [
        "app",
        "app/api",
        "app/api/routes",
        "app/services",
        "app/database",
        "app/models",
        "app/utils",
        "data",
        "data/csv",
        "data/media",
        "data/media/avatars",
        "data/media/characters",
        "data/media/generated_images",
        "data/media/generated_videos",
        "data/media/audio",
        "data/media/uploads",
    ]

    for dir_path in required_dirs:
        full_path = backend_dir / dir_path
        exists = check_directory_exists(full_path)
        print_status(dir_path + "/", exists)
        if not exists:
            all_checks_passed = False

    # Check for .env file
    print(f"\n{YELLOW}Checking Configuration...{RESET}")
    env_file = backend_dir / ".env"
    env_exists = check_file_exists(env_file)

    if env_exists:
        print_status(".env file exists", True)
    else:
        print_status(".env file exists", False)
        print(f"    {YELLOW}Note: Copy .env.example to .env and configure API keys{RESET}")

    # Check Python version
    print(f"\n{YELLOW}Checking Python Environment...{RESET}")
    py_version = sys.version_info
    py_version_ok = py_version.major == 3 and py_version.minor >= 11
    print_status(f"Python version: {py_version.major}.{py_version.minor}.{py_version.micro}", py_version_ok)

    if not py_version_ok:
        print(f"    {YELLOW}Warning: Python 3.11+ recommended{RESET}")

    # Try to import required packages
    print(f"\n{YELLOW}Checking Dependencies...{RESET}")
    required_packages = [
        "fastapi",
        "uvicorn",
        "pandas",
        "pydantic",
        "httpx",
        "passlib",
        "jose",
        "dotenv",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            elif package == "jose":
                __import__("jose")
            else:
                __import__(package)
            print_status(f"{package} installed", True)
        except ImportError:
            print_status(f"{package} installed", False)
            missing_packages.append(package)

    if missing_packages:
        print(f"\n    {YELLOW}Run: pip install -r requirements.txt{RESET}")

    # Final summary
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    if all_checks_passed and not missing_packages:
        print(f"{GREEN}[SUCCESS] All checks passed! System is ready to run.{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. Configure .env file with your API keys" if not env_exists else "  1. [OK] .env file configured")
        print("  2. Run: python run.py --reload")
        print("  3. Visit: http://localhost:8000/docs")
    else:
        print(f"{RED}[FAILED] Some checks failed. Please review the output above.{RESET}")
        all_checks_passed = False

    print(f"{BLUE}{'=' * 60}{RESET}\n")

    return 0 if all_checks_passed and not missing_packages else 1


if __name__ == "__main__":
    sys.exit(main())
