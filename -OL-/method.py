import cv2
import numpy as np
from PIL import ImageGrab
import pygetwindow as gw

def xqnum():
    # 定义数字模板
    templates = {}
    for i in range(10):
        template_path = f"images/templates/{i}.png"  # 每个数字的模板图片路径
        templates[str(i)] = cv2.imread(template_path, 0)

    final_result = ""
    while final_result == "":
        # 获取指定窗口
        windows = gw.getWindowsWithTitle("MuMuPlayer")
        if not windows:
            print("未找到窗口: MuMuPlayer")
            return

        window = windows[0]

        # 激活窗口
        window.activate()

        # 获取窗口位置和大小
        x, y, width, height = window.left, window.top, window.width, window.height

        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x + 588, y + 259, x + 715, y + 305))
        # screenshot.save("xq.png")
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)  # 转换为灰度图

        # 预处理目标图片（如二值化）
        _, thresh_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # 模板匹配，支持多个数字
        detected_digits = []  # 存储检测到的数字和位置
        for digit, template in templates.items():
            res = cv2.matchTemplate(thresh_image, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # 匹配阈值
            loc = np.where(res >= threshold)  # 找到匹配区域

            for pt in zip(*loc[::-1]):  # 提取匹配位置
                detected_digits.append((pt[0], digit))  # 存储数字及其位置

        # 去除重复匹配
        detected_digits = sorted(detected_digits, key=lambda x: x[0])  # 按 x 坐标排序
        filtered_digits = []
        prev_x = -999  # 初始化为一个很小的值
        for x, digit in detected_digits:
            if x - prev_x > 10:  # 距离上一个数字的 x 坐标大于 10（根据实际调整）
                filtered_digits.append((x, digit))
                prev_x = x

        # 拼接最终结果
        final_result = "".join([digit for _, digit in filtered_digits])

    print(final_result)

# xqnum()
