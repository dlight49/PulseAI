import pyautogui
import time

print("🛡️  Shadow Robot Eyes are ACTIVE.")
print("Move your mouse to any button or spot on the screen.")
print("Press Ctrl+C to stop.")
print("--------------------------------------------------")

try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {str(x).rjust(4)} Y: {str(y).rjust(4)}"
        print(position_str, end="")
        print("\b" * len(position_str), end="", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n✅ Eyes closed.")
