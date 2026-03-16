"""
Shared bot configuration (e.g. resolution). Written by setup_config.py.
Scripts that depend on it should call require_config() at startup and exit if missing.
"""
import json
import os
import sys

CONFIG_FILENAME = "bot_config.json"
RESOLUTION_KEY = "resolution"
OS_KEY = "os"
OS_WINDOWS = "windows"
OS_LINUX = "linux"


def get_os(config=None):
    """Return config OS: 'windows' or 'linux'. Uses config if provided, else load_config(). Defaults to 'windows' if missing."""
    if config is None:
        config = load_config()
    if config is None:
        return OS_WINDOWS
    return config.get(OS_KEY, OS_WINDOWS).lower().strip() or OS_WINDOWS


def is_windows(config=None):
    """True if config OS is Windows."""
    return get_os(config) == OS_WINDOWS


def _script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_config_path():
    """Absolute path to the bot config file."""
    return os.path.join(_script_dir(), CONFIG_FILENAME)


def load_config():
    """Load config dict. Returns None if file missing or invalid."""
    path = get_config_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def require_config():
    """
    Load config. If missing or missing required keys (resolution, os), print message and exit with code 1.
    Returns the config dict so callers can read e.g. resolution, os.
    """
    config = load_config()
    if config is None:
        print("Configuration file is missing. Please run setup first:")
        print("  python setup_config.py")
        print(f"  (Expected file: {get_config_path()})")
        sys.exit(1)
    if not config.get(RESOLUTION_KEY):
        print("Configuration is missing 'resolution'. Please run setup again: python setup_config.py")
        sys.exit(1)
    # 'os' is optional; get_os() defaults to 'windows' if missing (re-run setup to set for Linux/Pi)
    return config
