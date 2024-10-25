from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

# 按住 'd' 键
keyboard.press('d')
time.sleep(5)  # 持续按住 5 秒
# 松开 'd' 键
keyboard.release('d')