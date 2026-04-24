import pyautogui
import time
import sys
import pygetwindow as gw

# The coordinates you provided
SEARCH_BOX = (246, 111)
MSG_BOX = (894, 685)

def send_whatsapp(contact_name, message):
    print(f"🛡️  Shadow Robot: Initiating WhatsApp Pulse to {contact_name}...")
    
    # 0. Focus WhatsApp Window
    try:
        windows = gw.getWindowsWithTitle('WhatsApp')
        if windows:
            print("🪟  Found WhatsApp window. Bringing to front...")
            whatsapp = windows[0]
            if whatsapp.isMinimized:
                whatsapp.restore()
            whatsapp.activate()
            time.sleep(2) # Increased delay for safety
        else:
            print("⚠️  WhatsApp window not found. Please make sure it's open.")
            return
    except Exception as e:
        print(f"⚠️  Could not focus window: {e}")

    # Fail-safe: Move mouse to top-left corner to abort
    pyautogui.FAILSAFE = True
    
    # 1. Click Search Box (Slow Motion)
    print(f"🛰️  Targeting Search Box at {SEARCH_BOX}...")
    pyautogui.moveTo(SEARCH_BOX[0], SEARCH_BOX[1], duration=1) # Move slowly so you can see!
    pyautogui.click()
    time.sleep(1)
    
    # 2. Type Contact Name and Enter
    print(f"⌨️  Typing contact name: {contact_name}")
    pyautogui.write(contact_name, interval=0.1)
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2) # Wait longer for chat to open

    # 3. Click Message Box (Slow Motion)
    print(f"🛰️  Targeting Message Box at {MSG_BOX}...")
    pyautogui.moveTo(MSG_BOX[0], MSG_BOX[1], duration=1) # Move slowly!
    pyautogui.click()
    time.sleep(1)

    # 4. Type the "Impossible" Message
    print(f"⌨️  Injecting message: {message}")
    pyautogui.write(message, interval=0.05)
    time.sleep(1)
    
    # 5. Send
    pyautogui.press('enter')
    print(f"\n✨ Pulse Delivered. The unthinkable is done.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Please provide: python whatsapp_pulse.py \"Contact Name\" \"Your Message\"")
    else:
        name = sys.argv[1]
        msg = sys.argv[2]
        send_whatsapp(name, msg)
