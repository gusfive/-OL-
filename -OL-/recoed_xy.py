import pygetwindow as gw
import time
from pynput import mouse

def get_click_position(window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(2)  # 增加等待时间确保窗口激活

    print("请在窗口内点击任意位置...")

    def on_click(x, y, button, pressed):
        if pressed:
            # 计算点击位置相对于窗口的坐标
            relative_x = x - window.left
            relative_y = y - window.top
            print(f"点击位置在窗口内的坐标: ({relative_x-200}, {relative_y-20})")
            print(f"点击位置绝对坐标: ({x}, {y})")
            print(f"窗口坐标: ({window.left}, {window.top})")
            return False  # 停止监听

    # 监听鼠标点击事件
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

# 示例调用
get_click_position()

(688, 133)