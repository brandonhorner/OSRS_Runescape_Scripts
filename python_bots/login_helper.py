"""
Global OSRS login helper. Reusable entry point for any bot.

Login logic lives in screen_interactor (resolveLogin and related methods).
This module provides a single import and optional standalone script so bots can:

  from login_helper import ensure_logged_in

  si = ScreenInteractor()
  if not ensure_logged_in(si, post_login_callback=my_setup):
      print("Login failed")
      return

Or run once from the command line to resolve login and exit:

  python login_helper.py
"""

import time


def ensure_logged_in(si=None, post_login_callback=None):
    """
    Ensure the game is logged in. Handles errors (failed login, disconnected,
    account logged in elsewhere, servers updating) and login prompts (Play Now,
    Click here to play). Uses Jagex Launcher / RuneLite where needed.

    Args:
        si: ScreenInteractor instance. If None, one is created.
        post_login_callback: Optional callable run after a successful login
            (e.g. to run bot setup). Not called if already logged in.

    Returns:
        True if logged in (or already was), False if login resolution failed.
    """
    if si is None:
        from screen_interactor import ScreenInteractor
        si = ScreenInteractor()
    return si.resolveLogin(post_login_callback=post_login_callback)


def main():
    """Standalone: check/resolve login then exit."""
    from screen_interactor import ScreenInteractor
    print("Login helper (standalone). Resolving login...")
    si = ScreenInteractor()
    ok = ensure_logged_in(si)
    if ok:
        print("Login OK. Exiting.")
    else:
        print("Login resolution failed. Exiting.")
    time.sleep(2)


if __name__ == "__main__":
    main()
