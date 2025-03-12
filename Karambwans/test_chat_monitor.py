# test_chat_monitor.py
# this is a test file for the ChatMonitor class
# We will test the ChatMonitor class by creating an instance of it and running it in a separate thread.
# We will then check if the target message is found in the desired region of the screen.

import time
from screen_interactor import ScreenInteractor
from chat_monitor import ChatMonitor

def test_chat_monitor():
    si = ScreenInteractor()
    chat_region = si.get_scan_area("activity_pane")
    chat_monitor = ChatMonitor(chat_region=chat_region, target_message="NOT cooking", check_interval=4.0)
    chat_monitor.start()

    # Wait for the chat monitor to find the target message
    if chat_monitor.wait_for_message(timeout=60):
        print("Target message found in chat.")
    else:
        print("Timeout reached without finding the target message.")

    chat_monitor.stop()


if __name__ == "__main__":
    test_chat_monitor()

