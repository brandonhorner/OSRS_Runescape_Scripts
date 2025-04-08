# chat_monitor.py
import threading
import time
import pyautogui
import pytesseract
from PIL import Image, ImageOps

class ChatMonitor(threading.Thread):
    def __init__(self, chat_region, target_message="You can't carry any", check_interval=1.0):
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
        print(f"ChatMonitor initialized with chat_region={chat_region}, target_message={target_message}, check_interval={check_interval}")

    def run(self):
        while not self._stop_event.is_set():
            screenshot = pyautogui.screenshot(region=self.chat_region)
            # Preprocess the image
            screenshot = ImageOps.grayscale(screenshot)
            screenshot = ImageOps.invert(screenshot.convert('RGB'))
            text = pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6')
            print(f"Found text: {text}")
            if self.target_message in text:
                print(f"Target message '{self.target_message}' found in the chat")
                self.message_found.set()
                break
            time.sleep(self.check_interval)
        print("ChatMonitor thread is stopping")

    def stop(self):
        print("Stopping ChatMonitor thread")
        self._stop_event.set()

    def wait_for_message(self, timeout=None):
        """
        Wait until the target message is detected (or until the timeout).
        Returns True if the message is found, else False.
        """
        print(f"Waiting for target message '{self.target_message}' with timeout {timeout}")
        result = self.message_found.wait(timeout)
        print(f"Wait result: {result}")
        return result