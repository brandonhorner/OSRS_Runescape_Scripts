import threading
import time
import random
import pyautogui

class PixelMonitor(threading.Thread):
    """
    Monitors a given region for a specific pixel color to appear or disappear.
    
    Usage example:
      pm = PixelMonitor(screen_interactor, color_hex="AA00FF", 
                        region="v2", tolerance=10, 
                        check_interval=0.5, wait_for="appear")
      pm.start()
      if pm.wait_for_condition(timeout=60):
          print("Purple color detected!")
      else:
          print("Timeout waiting for color to appear.")
      pm.stop()
    """
    def __init__(self, screen_interactor, color_hex, 
                 region=None, tolerance=10, check_interval=0.5,
                 wait_for="appear"):
        """
        :param screen_interactor: An instance of ScreenInteractor
        :param color_hex: Color to look for in hex format (e.g., "AA00FF")
        :param region: Region label (str) or tuple (x, y, w, h)
        :param tolerance: Color matching tolerance (0-255)
        :param check_interval: How often (in seconds) to check
        :param wait_for: "appear" or "disappear"
        """
        super().__init__(daemon=True)
        self.si = screen_interactor
        self.color_hex = color_hex
        self.region = self.si.resolve_region(region) if region is not None else None
        self.tolerance = tolerance
        self.check_interval = check_interval
        self.wait_for = wait_for.lower().strip()
        self._stop_event = threading.Event()
        self.condition_met = threading.Event()
        self.found_location = None
        
    def run(self):
        while not self._stop_event.is_set():
            # Use the find_pixel method from ScreenInteractor
            location = self.si.find_pixel(self.color_hex, region=self.region, tolerance=self.tolerance)
            
            if self.wait_for == "disappear":
                # Condition is met if the pixel is no longer found
                if location is None:
                    self.condition_met.set()
                    break
            else:  # "appear"
                # Condition is met if the pixel is found
                if location is not None:
                    self.found_location = location
                    self.condition_met.set()
                    break

            time.sleep(self.check_interval)

    def stop(self):
        self._stop_event.set()

    def wait_for_condition(self, timeout=None):
        """
        Blocks until the pixel has appeared/disappeared (or until timeout).
        Returns True if condition was met, False otherwise.
        """
        if timeout is None:
            # Wait indefinitely with interruptible checks
            while not self.condition_met.is_set() and not self._stop_event.is_set():
                try:
                    time.sleep(0.1)  # Short sleep to allow interruption
                except KeyboardInterrupt:
                    print("Keyboard interrupt detected in PixelMonitor, stopping...")
                    self.stop()
                    return False
        else:
            # Wait with timeout using interruptible approach
            start_time = time.time()
            while not self.condition_met.is_set() and not self._stop_event.is_set():
                if time.time() - start_time >= timeout:
                    return False
                try:
                    time.sleep(0.1)  # Short sleep to allow interruption
                except KeyboardInterrupt:
                    print("Keyboard interrupt detected in PixelMonitor, stopping...")
                    self.stop()
                    return False
        
        return self.condition_met.is_set()
    
    def get_found_location(self):
        """
        Returns the location where the pixel was found, or None if not found.
        """
        return self.found_location
    
    def reset(self):
        """
        Resets the monitor to start looking again.
        """
        self.condition_met.clear()
        self.found_location = None 