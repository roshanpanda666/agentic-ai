import pyautogui


while True:
    x, y = pyautogui.position()
    print(f"Cursor position → ({x}, {y})")
