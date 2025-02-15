# chat_monitor.py
import threading
import time
import pyautogui
import pytesseract

class ChatMonitor(threading.Thread):
    def __init__(self, chat_region, target_message="can't carry any", check_interval=1.0):
        """
        :param chat_region: A tuple (x, y, width, height) defining the chatbox region.
        :param target_message: The text to look for in the chat.
        :param check_interval: How often (in seconds) to check the chat.
        """
        super().__init__(daemon=True)  # daemon thread so it won't block exit
        self.chat_region = chat_region
        self.target_message = target_message
        self.check_interval = check_interval
        self.message_found = threading.Event()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Take a screenshot of the chat region
            screenshot = pyautogui.screenshot(region=self.chat_region)
            # Use OCR to extract text from the screenshot.
            # (Make sure you have pytesseract installed and properly configured)
            text = pytesseract.image_to_string(screenshot)
            if self.target_message in text:
                self.message_found.set()
                break
            time.sleep(self.check_interval)

    def stop(self):
        self._stop_event.set()

    def wait_for_message(self, timeout=None):
        """
        Wait until the target message is detected (or until the timeout).
        Returns True if the message is found, else False.
        """
        return self.message_found.wait(timeout)
