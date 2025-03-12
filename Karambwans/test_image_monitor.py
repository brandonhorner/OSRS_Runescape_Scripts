import time
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor

def test_bag_monitor(wait_for="disappear", timeout=64):
    """
    Monitors the bag region for the raw karambwan image.
    
    :param wait_for: Either "appear" or "disappear" to indicate which condition to monitor.
    :param timeout: Timeout in seconds to wait for the condition.
    """
    si = ScreenInteractor()
    
    print(f"Monitoring bag region for raw karambwans to {wait_for} (timeout: {timeout}s).")
    print("Make sure your game client is visible and the bag region is as expected.")
    
    # Create the monitor for the raw karambwan image in the bag region.
    monitor = ImageMonitor(
        screen_interactor=si,
        image_path="Karambwans/raw_karambwan.png",
        region="bag",  # using the 'bag' area from get_scan_area()
        confidence=0.98,
        check_interval=1.0,
        wait_for=wait_for
    )
    
    monitor.start()
    print("Started image monitor. Waiting for condition...")
    
    condition_met = monitor.wait_for_condition(timeout=timeout)
    if condition_met:
        print(f"Condition met: Raw karambwans have {wait_for}ed from the bag.")
    else:
        print("Timeout reached: Condition not met.")
    
    monitor.stop()

if __name__ == "__main__":
    # You can change "disappear" to "appear" for testing if you want to detect when raw karambwans show up.
    test_bag_monitor(wait_for="disappear", timeout=64)