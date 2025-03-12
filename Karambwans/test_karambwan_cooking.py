import cv2
import numpy as np

def find_color_by_mean(image, target_bgr, tolerance=30):
    """
    Compares the image's average color to the target color.
    Returns True if the Euclidean distance is within tolerance.
    """
    # Compute the mean color over all pixels (ignoring the alpha channel if present)
    mean_color = cv2.mean(image)[:3]  
    mean_color = np.array(mean_color)
    target_bgr = np.array(target_bgr)
    distance = np.linalg.norm(mean_color - target_bgr)
    return distance < tolerance

def on_mouse_click(event, x, y, flags, param):
    """
    Mouse callback that prints a message when a left-click occurs.
    """
    filename = param
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Image '{filename}' clicked!")
        cv2.destroyWindow(filename)

if __name__ == '__main__':
    # List of image filenames (ensure these images are in your working directory)
    image_files = ["Karambwans/burnt_karambwan.png", "Karambwans/cooked_karambwan.png", "Karambwans/raw_karambwan.png"]
    # Define the target color in BGR; here, for example, we are looking for pure red
    target_color = [55, 79, 39]  # BGR for red

    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            print(f"Could not load image: {file}")
            continue

        if find_color_by_mean(img, target_color, tolerance=30):
            print(f"Image '{file}' matched the target color!")
            # Create a window for the image and set the mouse callback (passing filename as parameter)
            cv2.namedWindow(file)
            cv2.setMouseCallback(file, on_mouse_click, param=file)
            cv2.imshow(file, img)
            # Wait indefinitely until a key is pressed or a click event destroys the window
            cv2.waitKey(0)
        else:
            print(f"Image '{file}' did not match the target color.")
    cv2.destroyAllWindows()
