import webbrowser
import time
import pyautogui

def open_amazon_gui(product: str):
    try:
        print(f"🛒 Rose: Opening Amazon and searching for {product}...")

        # Open Amazon in default browser
        webbrowser.open("https://www.amazon.in")
        time.sleep(5)  # wait for page to fully load

        # 🎯 Step 1: Move cursor to initial neutral point (like bottom-left corner)
        pyautogui.moveTo(100, 800, )

        # 🎯 Step 2: Move cursor to the Amazon search bar (coords must be adjusted for your screen)
        # 👉 Run pyautogui.position() to get exact x, y when hovering search bar
        pyautogui.moveTo(600, 200,)  # example coords
        pyautogui.click()
 
        # 🎯 Step 3: Type product name
        pyautogui.typewrite(product)
        pyautogui.press("enter")
        time.sleep(3)

        pyautogui.scroll(-300)
        pyautogui.moveTo(1017,411)
        time.sleep(2)
        pyautogui.click()

        time.sleep(4)
        pyautogui.scroll(-300)
        pyautogui.moveTo(1566,783)
        time.sleep(2)
        pyautogui.click()


        return f"🛒 Searching Amazon for {product}..."
    except Exception as e:
        return f"⚠️ PyAutoGUI failed: {e}"

# Example run
if __name__=="__main__":
    product_name = " mechanical keyboard"
    result = open_amazon_gui(product_name)
    print(result)