#!/usr/bin/env python3
"""
R U Serious? - Development Server Runner

This script provides an easy way to run the FastAPI server with proper configuration.
"""

import argparse
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))


def check_environment():
    """Check if environment is properly configured"""
    env_file = Path(__file__).parent / ".env"

    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("📝 Creating .env from .env.example...")

        example_file = Path(__file__).parent / ".env.example"
        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print("✅ Created .env file")
            print("🔧 Please edit .env and add your API keys before running the server")
            return False
        else:
            print("❌ .env.example not found!")
            return False

    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)

    required_vars = ["SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"⚠️  Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("🔧 Please edit .env and add the missing values")
        return False

    return True


def check_directories():
    """Ensure required directories exist"""
    data_dir = Path(__file__).parent / "data"
    dirs = [
        data_dir / "csv",
        data_dir / "media" / "avatars",
        data_dir / "media" / "characters",
        data_dir / "media" / "generated_images",
        data_dir / "media" / "generated_videos",
        data_dir / "media" / "audio",
        data_dir / "media" / "uploads",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    print("✅ Directory structure verified")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run R U Serious? Backend Server")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip environment checks"
    )

    args = parser.parse_args()

    # Run checks
    if not args.skip_checks:
        print("=" * 60)
        print("🔍 Running pre-flight checks...")
        print("=" * 60)

        if not check_environment():
            sys.exit(1)

        check_directories()

    # Start server
    print("\n" + "=" * 60)
    print("🚀 Starting R U Serious? Backend Server")
    print("=" * 60)
    print(f"📍 Host: {args.host}")
    print(f"📍 Port: {args.port}")
    print(f"🔄 Reload: {'Enabled' if args.reload else 'Disabled'}")
    print(f"👥 Workers: {args.workers}")
    print("=" * 60)

    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
