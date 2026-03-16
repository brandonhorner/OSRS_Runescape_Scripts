"""
One-time setup: detect or ask for screen resolution and OS, save to bot_config.json.
Run this before using bots that depend on resolution/OS (e.g. mining_gem_shilo).
  python setup_config.py
"""
import json
import os
import sys
import platform

import pyautogui

# Use same config location as bot_config.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = "bot_config.json"
RESOLUTION_KEY = "resolution"
OS_KEY = "os"
OS_WINDOWS = "windows"
OS_LINUX = "linux"


def get_config_path():
    return os.path.join(SCRIPT_DIR, CONFIG_FILENAME)


def main():
    print("Bot setup – screen resolution and OS")
    print("-" * 40)
    try:
        width, height = pyautogui.size()
    except Exception as e:
        print(f"Could not detect screen size: {e}")
        sys.exit(1)
    detected_res = f"{width}x{height}"
    print(f"Detected resolution: {detected_res}")
    try:
        answer = input("Use this resolution? [Y/n]: ").strip().lower()
    except EOFError:
        answer = "y"
    if answer in ("n", "no"):
        try:
            resolution = input("Enter resolution (e.g. 1920x1080): ").strip()
        except EOFError:
            resolution = detected_res
        if not resolution or "x" not in resolution:
            print("Invalid format. Using detected resolution.")
            resolution = detected_res
    else:
        resolution = detected_res

    # OS: detect and confirm (zoom behavior: Windows vs Linux/Pi)
    raw = platform.system().lower()
    detected_os = OS_WINDOWS if raw == "windows" else OS_LINUX
    print(f"Detected OS: {detected_os}")
    try:
        ans = input("Use this OS? [Y/n]: ").strip().lower()
    except EOFError:
        ans = "y"
    if ans in ("n", "no"):
        try:
            os_choice = input("Enter OS (windows / linux): ").strip().lower()
        except EOFError:
            os_choice = detected_os
        if os_choice in (OS_WINDOWS, OS_LINUX):
            detected_os = os_choice
        else:
            print("Using detected OS.")
    os_value = detected_os

    config = {RESOLUTION_KEY: resolution, OS_KEY: os_value}
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"Saved: {path}")
    print("Setup complete. You can run the bot scripts now.")


if __name__ == "__main__":
    main()
