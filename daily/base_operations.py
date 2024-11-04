import time
import pyautogui
from pynput.keyboard import Controller
import pygetwindow as gw


class BaseOperations:
    def __init__(self, window_title="MuMuPlayer"):
        self.window_title = window_title
        self.keyboard = Controller()
        
    def click_at(self, x, y, delay=0.1):
        """在指定坐标点击"""
        window = self._get_window()
        if not window:
            return False
            
        screen_x = window.left + x
        screen_y = window.top + y
        pyautogui.click(screen_x, screen_y)
        time.sleep(delay)
        return True
        
    def drag(self, start_x, start_y, offset_x, offset_y, duration=0.5):
        """拖拽操作"""
        window = self._get_window()
        if not window:
            return False
            
        screen_x = window.left + start_x
        screen_y = window.top + start_y
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.dragRel(offset_x, offset_y, duration)
        return True
        
    def find_and_click(self, image_path, timeout=10):
        """查找并点击图像"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._find_image(image_path):
                return True
        return False
        
    def _get_window(self):
        """获取游戏窗口"""
        windows = gw.getWindowsWithTitle(self.window_title)
        if not windows:
            print(f"未找到窗口: {self.window_title}")
            return None
        return windows[0] 