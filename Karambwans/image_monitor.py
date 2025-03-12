import threading
import time

class ImageMonitor(threading.Thread):
    """
    Monitors a given region for an image to either 'appear' or 'disappear'
    using the ScreenInteractor's CV2-based image search.

    Usage example:
      im = ImageMonitor(screen_interactor, "path/to/image.png",
                        region="bag", confidence=0.9,
                        check_interval=1.0, wait_for="disappear")
      im.start()
      if im.wait_for_condition(timeout=60):
          print("Image condition met (disappeared)!")
      else:
          print("Timeout waiting for image to disappear.")
      im.stop()
    """
    def __init__(self, screen_interactor, image_path,
                 region=None, confidence=0.98, check_interval=1.0,
                 wait_for="disappear"):
        """
        :param screen_interactor: An instance of ScreenInteractor
        :param image_path: Path to the image file to look for
        :param region: Region label (str) or tuple (x, y, w, h)
        :param confidence: Matching threshold
        :param check_interval: How often (in seconds) to check
        :param wait_for: "appear" or "disappear"
        """
        super().__init__(daemon=True)
        self.si = screen_interactor
        self.image_path = image_path
        self.region = region
        self.confidence = confidence
        self.check_interval = check_interval
        self.wait_for = wait_for.lower().strip()
        self._stop_event = threading.Event()
        self.condition_met = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Use the CV2-based finder from ScreenInteractor
            location = self.si.find_image_cv2(self.image_path, region=self.region, threshold=self.confidence)
            
            if self.wait_for == "disappear":
                # Condition is met if the image is no longer found
                if location is None:
                    self.condition_met.set()
                    break
            else:  # "appear"
                # Condition is met if the image is found
                if location is not None:
                    self.condition_met.set()
                    break

            time.sleep(self.check_interval)

    def stop(self):
        self._stop_event.set()

    def wait_for_condition(self, timeout=None):
        """
        Blocks until the image has appeared/disappeared (or until timeout).
        Returns True if condition was met, False otherwise.
        """
        return self.condition_met.wait(timeout)
