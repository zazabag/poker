#!/usr/bin/env python3
import os
import sys
import subprocess

# Add project to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def start_api():
    print("🚀 Starting API server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_bot():
    print("🤖 Starting Telegram bot...")
    subprocess.run([sys.executable, "-m", "bot.main"])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["api", "bot", "all"], default="all", nargs="?")
    args = parser.parse_args()
    
    if args.command == "api":
        start_api()
    elif args.command == "bot":
        start_bot()
    else:
        print("Use: python start.py [api|bot]")
        print("For development, run API and bot in separate terminals.")
