import mss
import cv2
import numpy as np
import pyautogui
import easyocr
import time

# Initialize OCR reader (English by default)
reader = easyocr.Reader(['en'])

def find_and_click_button(button_text: str, wait: float = 2.0):
    """
    Detects a button by its text on screen and clicks it.
    :param button_text: Text to search on screen (e.g. "Buy Now")
    :param wait: Seconds to wait before action
    """
    time.sleep(wait)  # Give some buffer (e.g., wait for page load)

    # 1. Capture screen
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # 2. OCR detection
    results = reader.readtext(frame)

    found_coords = None
    for (bbox, text, prob) in results:
        if button_text.lower() in text.lower() and prob > 0.6:
            # bbox = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            (x_min, y_min) = bbox[0]
            (x_max, y_max) = bbox[2]
            cx, cy = int((x_min + x_max) / 2), int((y_min + y_max) / 2)
            found_coords = (cx, cy)
            break

    # 3. Move & click if found
    if found_coords:
        print(f"🎯 Found '{button_text}' at {found_coords}, clicking...")
        pyautogui.moveTo(found_coords[0], found_coords[1], duration=0.5)
        pyautogui.click()
        return True
    else:
        print(f"⚠️ Could not find '{button_text}' on screen.")
        return False


# Example usage
if __name__ == "__main__":
    print("🖥️ Looking for button...")
    success = find_and_click_button("Buy Now", wait=4)

    if success:
        print("✅ Button clicked successfully!")
    else:
        print("❌ Button not found.")
