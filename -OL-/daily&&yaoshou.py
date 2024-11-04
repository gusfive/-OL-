from PIL import ImageGrab
import cv2
import pyautogui
import pygetwindow as gw
import time
import os
from auto_yaoling import ytlyhard
from auto_yaoling import ytlyhardhard
from auto_yaoling import ytly
from auto_yaoling import catchforweekends
from auto_yaoling import drag_inxy
from auto_yaoling import find_xy
from pynput.keyboard import Key, Controller
import numpy as np
import pyperclip
from datetime import datetime

keyboard = Controller()


def getwin():
    # 获取所有窗口的标题
    titles = gw.getAllTitles()

    # 打印所有窗口的标题
    for title in titles:
        print(title)


def writeinwin(txt):
    pyperclip.copy(txt)
    time.sleep(0.1)  # 增加等待时间确保窗口激活
    with keyboard.pressed(Key.ctrl):
        keyboard.press('v')
        keyboard.release('v')
    time.sleep(0.3)
    click_inxy(150,78)
    click_inxy(150,78)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def drag_inxy(x, y, x1, y1, duration, window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(0.1)  # 增加等待时间确保窗口激活

    # 将相对于窗口的坐标转换为屏幕的绝对坐标
    screen_x = window.left + x
    screen_y = window.top + y

    # 在屏幕的绝对坐标位置拖动
    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.dragRel(x1, y1, duration)
    print(f"已在窗口 {window_title} 内的坐标 ({x}, {y}) 处点击")


def scroll_inxy(x, y, amount=1, delay=0.1, window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(1)  # 增加等待时间确保窗口激活

    # 将相对于窗口的坐标转换为屏幕的绝对坐标
    screen_x = window.left + x
    screen_y = window.top + y

    # 在屏幕的绝对坐标位置点击
    time.sleep(0.5)
    for _ in range(amount):
        pyautogui.moveTo(screen_x, screen_y, 0.25)
        pyautogui.scroll(-1000)
        time.sleep(delay)
    print(f"已滚动")


def find_and_clickxy_until_stop(stop_image_path, x1, y1, window_title="MuMuPlayer", timeout=90, click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(0.1)  # 增加等待时间确保窗口激活

    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    start_time = time.time()
    while True:
        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot_filename = 'window_screenshot.png'
        screenshot.save(screenshot_filename)

        # 加载窗口截图
        window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配查找停止按钮位置
        result_stop = cv2.matchTemplate(window_image, stop_image, cv2.TM_CCOEFF_NORMED)
        min_val_stop, max_val_stop, min_loc_stop, max_loc_stop = cv2.minMaxLoc(result_stop)

        # 设置匹配阈值
        threshold = 0.85
        if max_val_stop >= threshold:
            print(f"找到停止按钮 {stop_image_path}，停止循环")
            break

        # 在窗口内点击按钮位置
        time.sleep(0.1)
        pyautogui.click(x1 + x, y1 + y)

        time.sleep(click_delay)  # 每次循环后的延迟

        # 检查是否超时
        if time.time() - start_time >= timeout:
            print(f"未找到 {stop_image_path}，超时退出")
            break

    # 删除截图文件
    os.remove(screenshot_filename)


def find_and_return(stop_image_path, window_title="MuMuPlayer"):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return
    window = windows[0]
    # 激活窗口
    window.activate()
    time.sleep(0.1)  # 增加等待时间确保窗口激活
    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    # 截取窗口截图
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot_filename = 'window_screenshot.png'
    screenshot.save(screenshot_filename)

    # 加载窗口截图
    window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

    # 使用模板匹配查找停止按钮位置
    result_stop = cv2.matchTemplate(window_image, stop_image, cv2.TM_CCOEFF_NORMED)
    min_val_stop, max_val_stop, min_loc_stop, max_loc_stop = cv2.minMaxLoc(result_stop)

    # 设置匹配阈值
    threshold = 0.85
    if max_val_stop >= threshold:
        return True
    else:
        return False


def find_and_click_until_stop(stop_image_path, click_image_path, window_title="MuMuPlayer", timeout=90,
                              click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)
    click_image = cv2.imread(click_image_path, cv2.IMREAD_GRAYSCALE)
    click_height, click_width = click_image.shape[:2]

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(0.2)  # 增加等待时间确保窗口激活

    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    start_time = time.time()
    while True:
        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot_filename = 'window_screenshot.png'
        screenshot.save(screenshot_filename)

        # 加载窗口截图
        window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配查找停止按钮位置
        result_stop = cv2.matchTemplate(window_image, stop_image, cv2.TM_CCOEFF_NORMED)
        min_val_stop, max_val_stop, min_loc_stop, max_loc_stop = cv2.minMaxLoc(result_stop)

        # 设置匹配阈值
        threshold = 0.85
        if max_val_stop >= threshold:
            print(f"找到停止按钮 {stop_image_path}，停止循环")
            break

        # 使用模板匹配查找点击按钮位置
        result_click = cv2.matchTemplate(window_image, click_image, cv2.TM_CCOEFF_NORMED)
        min_val_click, max_val_click, min_loc_click, max_loc_click = cv2.minMaxLoc(result_click)

        if max_val_click >= threshold:
            button_x, button_y = max_loc_click
            button_x += x + click_width // 2  # 转换为屏幕坐标并调整为中心位置
            button_y += y + click_height // 2

            # 在窗口内点击按钮位置
            time.sleep(0.1)
            pyautogui.click(button_x, button_y)
            print(f"已点击 {click_image_path}")

        time.sleep(click_delay)  # 每次循环后的延迟

        # 检查是否超时
        if time.time() - start_time >= timeout:
            print(f"未找到 {stop_image_path}，超时退出")
            break

    # 删除截图文件
    os.remove(screenshot_filename)


def find_and_clickon_until_stop(stop_image_path, click_image_path, window_title="MuMuPlayer", timeout=60,
                                click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)
    click_image = cv2.imread(click_image_path, cv2.IMREAD_GRAYSCALE)
    click_height, click_width = click_image.shape[:2]

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(2)  # 增加等待时间确保窗口激活

    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    start_time = time.time()
    while True:
        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot_filename = 'window_screenshot.png'
        screenshot.save(screenshot_filename)

        # 加载窗口截图
        window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配查找停止按钮位置
        result_stop = cv2.matchTemplate(window_image, stop_image, cv2.TM_CCOEFF_NORMED)
        min_val_stop, max_val_stop, min_loc_stop, max_loc_stop = cv2.minMaxLoc(result_stop)

        # 设置匹配阈值
        threshold = 0.85
        if max_val_stop >= threshold:
            print(f"找到停止按钮 {stop_image_path}，停止循环")
            break

        # 使用模板匹配查找点击按钮位置
        result_click = cv2.matchTemplate(window_image, click_image, cv2.TM_CCOEFF_NORMED)
        min_val_click, max_val_click, min_loc_click, max_loc_click = cv2.minMaxLoc(result_click)

        if max_val_click >= threshold:
            button_x, button_y = max_loc_click
            button_x += x + click_width // 2  # 转换为屏幕坐标并调整为中心位置
            button_y += y + click_height // 2

            # 在窗口内点击按钮位置
            pyautogui.click(button_x, button_y)
            pyautogui.mouseDown()
            time.sleep(5)
            pyautogui.mouseUp()
            print(f"已点击 {click_image_path}")

        time.sleep(click_delay)  # 每次循环后的延迟

        # 检查是否超时
        if time.time() - start_time >= timeout:
            print(f"未找到 {stop_image_path}，超时退出")
            break

    # 删除截图文件
    os.remove(screenshot_filename)


def click_inxy(x, y, window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(1)  # 增加等待时间确保窗口激活

    # 将相对于窗口的坐标转换为屏幕的绝对坐标
    screen_x = window.left + x
    screen_y = window.top + y

    # 在屏幕的绝对坐标位置点击
    pyautogui.click(screen_x, screen_y)
    print(f"已在窗口 {window_title} 内的坐标 ({x}, {y}) 处点击")


def click_button_in_window2(image_path, window_title="MuMuPlayer", timeout=10):
    # 加载按钮图像
    button_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    button_height, button_width = button_image.shape[:2]

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()

    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    start_time = time.time()

    while time.time() - start_time < timeout:
        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot_filename = 'window_screenshot.png'
        screenshot.save(screenshot_filename)

        # 加载窗口截图
        window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配查找按钮位置
        result = cv2.matchTemplate(window_image, button_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 设置匹配阈值
        threshold = 0.85  # 增加匹配阈值
        if max_val >= threshold:
            button_x, button_y = max_loc
            button_x += x + button_width // 2  # 转换为屏幕坐标并调整为中心位置
            button_y += y + button_height // 2

            # 在窗口内点击按钮位置
            pyautogui.click(button_x, button_y)
            print("已点击 " + image_path)
            break

    if time.time() - start_time >= timeout:
        print("未找到" + image_path + "，超时退出")

    # 删除截图文件
    os.remove(screenshot_filename)


def click_button_in_window(image_path, window_title="MuMuPlayer", timeout=10, click_delay=0.3, max_clicks=6):
    # 加载按钮图像
    button_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    button_height, button_width = button_image.shape[:2]

    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()

    # 获取窗口位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height

    start_time = time.time()
    stop_clicking = False  # 标志变量

    while time.time() - start_time < timeout and not stop_clicking:
        # 截取窗口截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot_filename = 'window_screenshot.png'
        screenshot.save(screenshot_filename)

        # 加载窗口截图
        window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配查找按钮位置
        result = cv2.matchTemplate(window_image, button_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 设置匹配阈值
        threshold = 0.85  # 增加匹配阈值
        if max_val >= threshold:
            button_x, button_y = max_loc
            button_x += x + button_width // 2  # 转换为屏幕坐标并调整为中心位置
            button_y += y + button_height // 2

            # 在窗口内点击按钮位置
            click_count = 0

            while click_count < max_clicks:
                pyautogui.click(button_x, button_y)
                print("已点击 " + image_path)

                # 添加点击后的延迟
                time.sleep(click_delay)

                # 截取窗口截图
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.save(screenshot_filename)

                # 加载窗口截图
                window_image = cv2.imread(screenshot_filename, cv2.IMREAD_GRAYSCALE)

                # 使用模板匹配查找按钮位置
                result = cv2.matchTemplate(window_image, button_image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                if max_val < threshold:
                    print("图标已消失，停止点击")
                    stop_clicking = True  # 设置标志变量
                    break

                click_count += 1

            if click_count >= max_clicks:
                print("达到最大点击次数，停止点击")
                stop_clicking = True  # 设置标志变量

            time.sleep(0.2)  # 每0.5秒检查一次

    if time.time() - start_time >= timeout:
        print("未找到" + image_path + "，超时退出")

    # 删除截图文件
    os.remove(screenshot_filename)


# 进入游戏到大街界面
def start_to_street():
    click_button_in_window('images/startgame.png', timeout=2, click_delay=0.5)
    click_button_in_window('images/gongao.png', timeout=12, click_delay=0.5)
    click_button_in_window('images/huodong.png', timeout=5, click_delay=1)


def jtKls():
    find_and_click_until_stop("images/ytly.png", "images/shijieditu.png")
    find_and_click_until_stop("images/zwt.png", "images/ytly.png")
    click_button_in_window("images/yl-backhome.png", timeout=3)
    find_and_click_until_stop("images/djkbqygb.png", "images/kssq.png",timeout=6)
    click_button_in_window("images/djkbqygb.png")
    time.sleep(0.5)
    drag_inxy(525, 252, -411, 114, 0.8)
    click_inxy(707, 132)
    time.sleep(1)
    click_inxy(523, 197)
    click_inxy(523, 197)
    find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("images/freeConfirm.png")
    find_and_click_until_stop("images/yl-yes.png", "images/together.png", click_delay=0.5, timeout=10)
    click_button_in_window("images/yl-yes.png", click_delay=0.5, timeout=10)
    click_button_in_window("images/door-kssz.png")
    click_button_in_window("images/kssz-yes.png")
    click_button_in_window("images/door-qrpq.png", click_delay=1)
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png",timeout=5)
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/map-exit.png", click_delay=1.5)


def xianbao():
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=10)
    find_and_click_until_stop("images/zl_fb.png.", "images/gerenziliao.png", timeout=5)
    find_and_click_until_stop("images/hqxb.png", "images/zl_fb.png")
    find_and_click_until_stop("images/yj.png", "images/hqxb.png")
    find_and_click_until_stop("images/hdyj.png", "images/yj.png")
    find_and_clickxy_until_stop("images/yjwj.png", x1=304, y1=324, timeout=15)
    click_button_in_window("images/yjwj.png", timeout=5)
    find_and_click_until_stop("images/hdyj.png", "images/xb_exit.png", click_delay=1, timeout=5)
    find_and_clickxy_until_stop("images/yjwj.png", x1=633, y1=295, timeout=15)
    click_button_in_window("images/yjwj.png", timeout=5)
    find_and_click_until_stop("images/hdyj.png", "images/xb_exit.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/fx_exit.png", "images/xbyj_exit.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/caidan.png", "images/fx_exit.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/youjian.png", "images/caidan.png", click_delay=2, timeout=5)


def chushihuaweizhi():
    time.sleep(1)
    click_button_in_window('images/shijieditu.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/penglai.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    # find_and_click_until_stop("images/en.png","images/jss.png")
    # find_and_click_until_stop("images/en_kstz.png","images/en.png")
    # find_and_click_until_stop("images/dashu.png","images/en_kstz.png")
    # click_inxy(812, 218)
    # click_inxy(812, 218)
    # keyboard.press('d')
    # time.sleep(3)
    # keyboard.release('d')
    # start_time = time.time()
    # while time.time() - start_time < 6:
    #     click_button_in_window("images/guangan.png",max_clicks=2)
    #     click_button_in_window("images/dashu.png",max_clicks=2)
    # keyboard.press('d')
    # time.sleep(3)
    # keyboard.release('d')
    # start_time = time.time()
    # while time.time() - start_time < 6:
    #     click_button_in_window("images/guangan.png",max_clicks=2)
    #     click_button_in_window("images/dashu.png",max_clicks=2)
    find_and_click_until_stop("images/youjian.png", "images/huijia.png", click_delay=0.2, timeout=20)


def street_to_xianmeng(nezhai):
    time.sleep(4)
    click_inxy(921, 444)
    time.sleep(4)
    click_inxy(918, 424)
    if nezhai == 1:
        time.sleep(4)
        click_inxy(561,424)
    time.sleep(4)
    click_inxy(450, 330)


def xuanshang():
    if 10 <= datetime.now().hour <= 21:
        drag_inxy(670,386,-200,0,0.5)
        find_and_click_until_stop("images/lianmeng/cxxs.png", "images/lianmeng/xuanshang.png", click_delay=1, timeout=3)
        click_button_in_window("images/lianmeng/cxxs.png",click_delay=0.5, timeout=3)
        click_inxy(150,78)
        writeinwin("三级")
        find_and_click_until_stop("images/yes.png","images/lianmeng/receive.png",timeout=3)
        click_button_in_window("images/yes.png", click_delay=1, timeout=3)
        find_and_click_until_stop("images/yes.png","images/lianmeng/receive.png",timeout=3)
        click_button_in_window("images/yes.png", click_delay=1, timeout=3)
        find_and_click_until_stop("images/lianmeng/xuanshang.png", "images/lianmeng/xs_exit.png", click_delay=1, timeout=3)
        find_and_click_until_stop("images/lianmeng/cxxs.png", "images/lianmeng/xuanshang.png", click_delay=0.5, timeout=3)
        click_button_in_window("images/lianmeng/cxxs.png",click_delay=0.5, timeout=3)
        click_inxy(150,78)
        writeinwin("二级")
        find_and_click_until_stop("images/yes.png","images/lianmeng/receive.png",timeout=3)
        click_button_in_window("images/yes.png", click_delay=1, timeout=3)
        find_and_click_until_stop("images/yes.png","images/lianmeng/receive.png",timeout=3)
        click_button_in_window("images/yes.png", click_delay=1, timeout=3)
        find_and_click_until_stop("images/lianmeng/overview_xs.png", "images/lianmeng/myxs.png", click_delay=0.5, timeout=3)
        for i in range(2):
            find_and_click_until_stop("images/lianmeng/change.png", "images/lianmeng/overview_xs.png", click_delay=0.5, timeout=3)
            find_and_click_until_stop("images/lianmeng/rank2.png", "images/lianmeng/change.png", click_delay=0.5, timeout=3)
            find_and_click_until_stop("images/lianmeng/change_in.png", "images/lianmeng/rank2.png", click_delay=0.5, timeout=3)
            click_button_in_window("images/lianmeng/change_in.png",click_delay=0.5,timeout=3)
            click_button_in_window("images/lianmeng/maxnum.png",click_delay=0.5,timeout=2)
            click_button_in_window("images/lianmeng/sure.png",click_delay=0.5,timeout=2)
            click_button_in_window("images/lianmeng/overview.png",click_delay=0.5,timeout=2)
            click_button_in_window("images/lianmeng/select_exit.png",click_delay=0.5,timeout=4)
        for i in range(2):
            find_and_click_until_stop("images/lianmeng/change.png", "images/lianmeng/overview_xs.png", click_delay=0.5,
                                      timeout=3)
            find_and_click_until_stop("images/lianmeng/rank2.png", "images/lianmeng/change.png", click_delay=0.5, timeout=3)
            find_and_click_until_stop("images/lianmeng/rank3.png", "images/lianmeng/second.png", click_delay=0.5,
                                      timeout=3)
            find_and_click_until_stop("images/lianmeng/change_in.png", "images/lianmeng/rank3.png", click_delay=0.5,
                                      timeout=3)
            click_button_in_window("images/lianmeng/change_in.png", click_delay=0.5, timeout=3)
            click_button_in_window("images/lianmeng/maxnum.png", click_delay=0.5, timeout=2)
            click_button_in_window("images/lianmeng/sure.png", click_delay=0.5, timeout=2)
            click_button_in_window("images/lianmeng/overview.png", click_delay=0.5, timeout=2)
            click_button_in_window("images/lianmeng/select_exit.png",click_delay=0.5,timeout=4)
        click_button_in_window("images/lianmeng/take.png",click_delay=0.5,timeout=2)
        for i in range(4):
            find_and_click_until_stop("images/lianmeng/yes_small.png", "images/lianmeng/give.png",timeout=3)
            click_button_in_window("images/lianmeng/yes_small.png", click_delay=0.5,timeout=3)
        click_button_in_window("images/lianmeng/xs_exit.png",click_delay=0.5,timeout=5)


def lianmeng():
    click_button_in_window('images/jingrulianmeng.png', timeout=2, click_delay=1)
    click_button_in_window("images/moku.png", timeout=2, click_delay=0.2)
    find_and_clickxy_until_stop("images/yes.png", 175, 386, timeout=5)
    click_button_in_window("images/yes.png", timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/moyuan.png", "images/moku_exit.png", click_delay=1, timeout=5)
    click_button_in_window('images/moyuan.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/sxian_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lianyaota.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/liandan.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lianyaota-exit.png', timeout=4, click_delay=0.2)
    click_button_in_window('images/lianyaota-exit2.png', timeout=2, click_delay=0.2)
    # xuanshang()
    find_and_click_until_stop("images/fanhuixianmeng.png", "images/lianmeng/confirm.png", click_delay=0.5, timeout=3)
    click_button_in_window('images/fanhuixianmeng.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/putonjianshe.png", "images/xianmengzhulou.png", timeout=20)
    find_and_click_until_stop("images/yes.png", "images/putonjianshe.png", timeout=10)
    find_and_click_until_stop("images/putonjianshe.png", "images/yes.png", timeout=10)
    find_and_click_until_stop("images/caidan.png", "images/xianmeng-exit.png", timeout=20)


def caidanhuicunzhuang():
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1.5, timeout=20)
    find_and_click_until_stop("images/huicunzhuang.png", "images/shezhi.png")
    find_and_click_until_stop("images/shijieditu.png", "images/huicunzhuang.png")


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
        screenshot = ImageGrab.grab(bbox=(x + 404, y + 224, x + 500, y + 274))
        screenshot.save("xq.png")
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
    final_number = int(final_result)
    print(final_result)
    return final_number


def xianqi():
    click_inxy(818,313)
    time.sleep(2)
    find_and_clickxy_until_stop("images/yes.png", 314, 301)
    time.sleep(0.5)
    num = xqnum()
    while num < 30000:
        click_inxy(632,324)
        num = xqnum()
    click_button_in_window("images/yes.png")
    find_and_click_until_stop("images/shijieditu.png","images/lm_exit.png",click_delay=1,timeout=10)


def saodan():
    # find_and_click_until_stop("images/penglai.png", "images/shijieditu.png")
    # find_and_click_until_stop("images/yes.png", "images/penglai.png")
    # click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    time.sleep(2)
    click_inxy(837, 358)
    click_button_in_window2('images/yes.png', timeout=2)
    time.sleep(4)
    click_inxy(837, 358)
    click_button_in_window2('images/yes.png', timeout=2)
    time.sleep(4)
    click_inxy(837, 358)
    click_button_in_window2('images/yes.png', timeout=2)
    click_button_in_window('images/dan-exit.png', timeout=2, click_delay=0.5)
    # find_and_click_until_stop("images/shijieditu.png", "images/huijia.png")


def saodan170():
    # find_and_click_until_stop("images/penglai.png", "images/shijieditu.png")
    # find_and_click_until_stop("images/yes.png", "images/penglai.png")
    # click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    time.sleep(2)
    click_inxy(647,118)
    click_button_in_window2('images/yes.png', timeout=2)
    time.sleep(4)
    click_inxy(647,118)
    click_button_in_window2('images/yes.png', timeout=2)
    time.sleep(4)
    click_inxy(647,118)
    click_button_in_window2('images/yes.png', timeout=2)
    click_button_in_window('images/dan-exit.png', timeout=2, click_delay=0.5)
    # find_and_click_until_stop("images/shijieditu.png", "images/huijia.png")


def fantianta():
    drag_inxy(298, 383, 0, 200, 0.5)
    find_and_click_until_stop("images/yl-close.png","images/ftt.png")
    find_and_click_until_stop("images/huijia.png","images/yl-close.png")


def jibeixilie():
    find_and_click_until_stop("images/jibeiditu.png", "images/shijieditu.png")
    find_and_click_until_stop("images/jibeiqueding.png", "images/jibeiditu.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/jibeiqueding.png")
    find_and_click_until_stop("images/quanxuan.png", "images/yijiannianya.png")
    click_button_in_window('images/quanxuan.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/nianya.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/huodong.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/ny_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/bingshuangyiji.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/jingru.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yijiansaodang.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/jingdiansaodang.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/saodangxialu.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/saobinqueding.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/digong_exit.png', timeout=2, click_delay=0.2)
    saodan170()
    saodan()
    fantianta()
    click_button_in_window('images/huijia.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/shijieditu.png", "images/huijia.png")


def zudui_ce():
    drag_inxy(480, 50, 0, y1=400, duration=0.2)
    drag_inxy(507, 49, 0, 200, 0.3)
    find_and_click_until_stop("images/dontianwang.png", "images/rainbowbuilding.png", timeout=5)
    find_and_click_until_stop("images/selectRank.png", "images/dontianwang.png", timeout=5)
    click_button_in_window('images/selectRank.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_button_in_window('images/zudui.png', timeout=2, click_delay=0.2)
    time.sleep(0.5)
    find_and_click_until_stop("images/gkdw.png", "images/chuangdui.png")
    time.sleep(0.5)
    click_button_in_window('images/gkdw.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/kaishi.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/guangan.png", "images/kaishi.png")
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(1.8)
    keyboard.release('d')
    keyboard.press('h')
    time.sleep(0.2)
    keyboard.release('h')
    keyboard.press('d')
    time.sleep(3)
    keyboard.release('d')
    click_button_in_window("images/guangan.png")
    find_and_clickon_until_stop("images/choupai.png", "images/guangan.png")
    click_button_in_window('images/choupai.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_inxy(640, 250)
    click_button_in_window('images/backdt.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zd_exit.png", "images/backdt.png")
    find_and_click_until_stop("images/chuangdui.png", "images/zd_exit.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/huijia.png")


def tianting():
    find_and_click_until_stop("images/tianting.png", "images/shijieditu.png")
    find_and_click_until_stop("images/yes.png", "images/tianting.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/yes.png")
    time.sleep(1)
    drag_inxy(277, 359, 0, y1=-300, duration=0.5)
    time.sleep(0.2)
    find_and_click_until_stop("images/moxie.png", "images/lonmengfudi.png", timeout=5, click_delay=1)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/moxie.png", timeout=5, click_delay=1)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5, click_delay=1)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lonmen_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/taotuo.png", "images/moxie.png", timeout=5)
    # find_and_click_until_stop("images/kaishitiaozhan.png", "images/taotuo.png", timeout=5)
    # find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    # click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    # click_button_in_window('images/lonmen_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/wuzhuangguan.png", "images/lm_exit.png", timeout=5)
    find_and_click_until_stop("images/dadian.png", "images/wuzhuangguan.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/dadian.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/houyuan.png", "images/dadian.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/houyuan.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/xiangfang.png", "images/houyuan.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/xiangfang.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/waiyuan.png", "images/xiangfang.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/waiyuan.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/wuzhuang_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window2('images/waiyuan.png', timeout=2)
    find_and_click_until_stop("images/xukong.png", "images/lm_exit.png", timeout=5)
    find_and_click_until_stop("images/zhenwu.png", "images/xukong.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/zhenwu.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/xukon_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/yaohuang.png", "images/zhenwu.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/yaohuang.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/xukon_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/xiuluo.png", "images/yaohuang.png", timeout=5)
    find_and_click_until_stop("images/kaishitiaozhan.png", "images/xiuluo.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/kaishitiaozhan.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/xukon_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window2('images/xiuluo.png', timeout=2)
    click_button_in_window('images/lm_exit.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    # drag_inxy(472, 420, 0, y1=-300, duration=0.5)
    # drag_inxy(472, 420, 0, y1=-300, duration=0.5)
    # click_button_in_window('images/baxian.png', timeout=2, click_delay=0.2)
    # click_button_in_window('images/baxiantiaozhan.png', timeout=2, click_delay=0.2)
    # click_button_in_window('images/addtime.png', timeout=2, click_delay=0.2)
    # click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    # click_button_in_window('images/baxian_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/huijia.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/huijia.png")


def kunlun():
    time.sleep(8)
    click_inxy(812, 218)
    click_inxy(812, 218)
    while True:
        keyboard.press('d')
        keyboard.press('k')
        if find_and_return("images/kls-yxd.png"):
            keyboard.release('d')
            keyboard.release('k')
            click_button_in_window("images/guangan.png")
            click_inxy(812, 218)
            click_inxy(812, 218)
            keyboard.press('a')
            time.sleep(6)
            keyboard.release('a')
            click_inxy(812, 218)
            click_inxy(812, 218)
            keyboard.press('d')
            time.sleep(1)
            keyboard.release('d')
            sec = (find_xy("images/kls-yxd.png") - find_xy("images/chenghao.png")) / 280
            click_inxy(812, 218)
            click_inxy(812, 218)
            keyboard.press('d')
            time.sleep(sec)
            keyboard.release('d')
            break
        elif find_and_return("images/iknow.png"):
            click_button_in_window("images/iknow.png")
            click_inxy(812, 218)
            click_inxy(812, 218)
    time.sleep(8)
    find_and_clickxy_until_stop("images/caidan.png", 812, 218, timeout=20)
    time.sleep(2)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("images/guangan.png", click_delay=1, max_clicks=5)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("images/guangan.png", click_delay=1, max_clicks=5)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("images/guangan.png", click_delay=1, max_clicks=3)
    time.sleep(2)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=10)
    find_and_click_until_stop("images/backmap.png", "images/shezhi.png", click_delay=0.5)
    find_and_click_until_stop("images/ks_exit.png", "images/backmap.png", click_delay=0.5)
    find_and_click_until_stop("images/yijiannianya.png", "images/ks_exit.png")
    click_inxy(300, 250)
    click_inxy(300, 250)
    pyautogui.dragRel(0, -200, duration=0.2)
    click_button_in_window('images/kunlunshan.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/kls-task.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/rewards.png', timeout=6, click_delay=0.2, max_clicks=10)
    click_button_in_window('images/zd_exit.png', timeout=6, click_delay=0.2)
    click_button_in_window('images/lm_exit.png', timeout=6, click_delay=1)
    find_and_click_until_stop("images/youjian.png", "images/huijia.png")


def klDianQuan():
    find_and_click_until_stop("images/ytly.png", "images/shijieditu.png")
    find_and_click_until_stop("images/zwt.png", "images/ytly.png")
    click_button_in_window("images/yl-backhome.png", timeout=3)
    find_and_click_until_stop("images/djkbqygb.png", "images/kssq.png")
    click_button_in_window("images/djkbqygb.png")
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/map-exit.png", click_delay=1)
    # find_and_click_until_stop("images/yes.png", "images/tianting.png")
    # find_and_click_until_stop("images/yijiannianya.png", "images/yes.png")
    # time.sleep(0.5)
    # drag_inxy(218,272,0,y1=-200,duration=0.2)
    # find_and_click_until_stop("images/kls-task.png","images/kunlunshan.png")
    # find_and_clickxy_until_stop("images/yes.png",470,447)
    # find_and_click_until_stop("images/caidan.png","images/yes.png")
    # find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=10)
    # find_and_click_until_stop("images/huicunzhuang.png","images/shezhi.png",click_delay=1, timeout=10)
    # find_and_click_until_stop("images/ks_exit.png","images/huicunzhuang.png")
    find_and_click_until_stop("images/youjian.png", "images/ks_exit.png")
    time.sleep(1)


def yaopu():
    if 10 <= datetime.now().hour <= 23:
        click_button_in_window("images/yaoyuan/yaoji.png",click_delay=0.3,timeout=3)
        click_button_in_window("images/yaoyuan/yaofu.png",click_delay=0.5,timeout=3)
        click_button_in_window("images/yaoyuan/take.png",click_delay=0.5,timeout=3)
        click_button_in_window("images/yaoyuan/yy_exit.png",click_delay=0.5,timeout=2)
        click_button_in_window("images/yaoyuan/give.png",click_delay=0.5,timeout=3)
        click_inxy(350,158)
        click_button_in_window("images/yaoyuan/sure.png",click_delay=0.5,timeout=3)
        time.sleep(1)
        click_inxy(439,274)
        click_inxy(439,274)
        time.sleep(0.5)
        click_inxy(575,308)
        click_inxy(575,308)
        time.sleep(0.5)
        click_inxy(719,366)
        click_inxy(719,366)
        click_button_in_window("images/yaoyuan/yy_exit.png",click_delay=0.5,timeout=2)
        click_button_in_window("images/yaoyuan/exit.png",click_delay=0.5,timeout=2)
        find_and_click_until_stop("images/jiguang.png", "images/yaoyuan/confirm.png", click_delay=1, timeout=3)


def huoyue():
    find_and_click_until_stop("images/jdianrenwu.png", "images/renwu.png", timeout=5)
    find_and_click_until_stop("images/xuanshangrenwu.png", "images/jdianrenwu.png", timeout=5)
    # find_and_click_until_stop("images/fqxs.png", "images/xuanshangrenwu.png", timeout=5)
    # find_and_click_until_stop("images/xuanshangyes.png", "images/lijiwancheng.png", timeout=5)
    # click_button_in_window("images/xuanshangyes.png", timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zhanyaochumo.png", "images/richangrenwu.png", timeout=5)
    find_and_click_until_stop("images/qzzl.png", "images/zhanyaochumo.png", timeout=6, click_delay=2)
    time.sleep(2)
    click_inxy(300, 189)
    pyautogui.dragRel(0, -60, duration=0.2)
    time.sleep(2)
    click_button_in_window('images/xianmengrenwu.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/lijiwancheng.png", "images/task_finish.png")
    click_button_in_window('images/task_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pvp.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/doushouchang.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/tiaozhan.png', timeout=2, click_delay=0.2, max_clicks=1)
    click_button_in_window('images/jiacheng.png', timeout=2, click_delay=0.2)
    click_inxy(440, 280)
    click_inxy(280, 280)
    click_button_in_window('images/buff_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/renshu.png", "images/cw_tiaozhan.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/renshu.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/pvpc.png", "images/lm_exit.png")
    click_button_in_window('images/pvpc.png', timeout=2, click_delay=0.2)
    find_and_clickxy_until_stop("images/guangan.png", 780, 200, timeout=20)
    time.sleep(4)
    click_button_in_window("images/guangan.png")
    keyboard.press('n')
    time.sleep(0.2)
    keyboard.release('n')
    find_and_click_until_stop("images/lm_exit.png", "images/guangan.png", timeout=75)
    find_and_click_until_stop("images/caidan.png", "images/lm_exit.png", timeout=5)
    find_and_click_until_stop("images/shijieditu.png", "images/caidan.png", timeout=5, click_delay=1)
    # klDianQuan()
    find_and_click_until_stop("images/lquyoujian.png", "images/youjian.png")
    click_button_in_window('images/lquyoujian.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yj_exit.png', timeout=2, click_delay=0.2)
    time.sleep(2)
    find_and_click_until_stop("images/zhenlin.png", "images/zhankai.png")
    find_and_click_until_stop("images/peiyang.png", "images/zhenlin.png")
    find_and_click_until_stop("images/niepan.png", "images/peiyang.png")
    find_and_click_until_stop("images/bagua.png", "images/niepan.png")
    find_and_click_until_stop("images/bggj.png", "images/bagua.png")
    find_and_click_until_stop("images/jingjie.png", "images/bggj.png")
    click_button_in_window('images/jingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pljj.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/select_all.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/qdjj.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zhankai.png", "images/suolue.png", timeout=6)
    time.sleep(2)
    click_inxy(546, 400)
    time.sleep(2)
    click_inxy(500, 279)
    click_button_in_window('images/fabaojingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/tjzb.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/xz.png", "images/fbjj.png", click_delay=1)
    click_button_in_window('images/xz.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pljj.png', timeout=2, click_delay=0.2)
    for i in range(2):
        click_button_in_window('images/quxiao.png', timeout=2, click_delay=0.2)
        click_button_in_window('images/select_all.png', timeout=2, click_delay=0.2)
        find_and_click_until_stop("images/yes.png", "images/qdjj.png")
        click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/cw.png", "images/caidan.png", click_delay=1)
    find_and_click_until_stop("images/wyang.png", "images/cw.png", timeout=5)
    find_and_click_until_stop("images/yaoshui.png", "images/wyang.png", timeout=5)
    find_and_click_until_stop("images/djwy.png", "images/yaoshui.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/djwy.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/caidan.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/caidan.png", click_delay=1)


def huoyue_ce():
    find_and_click_until_stop("images/jdianrenwu.png", "images/renwu.png", timeout=5)
    find_and_click_until_stop("images/xuanshangrenwu.png", "images/jdianrenwu.png", timeout=5)
    # find_and_click_until_stop("images/fqxs.png", "images/xuanshangrenwu.png", timeout=5)
    # find_and_click_until_stop("images/xuanshangyes.png", "images/lijiwancheng.png", timeout=5)
    # click_button_in_window("images/xuanshangyes.png", timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zhanyaochumo.png", "images/richangrenwu.png", timeout=5)
    find_and_click_until_stop("images/qzzl.png", "images/zhanyaochumo.png", timeout=6, click_delay=2)
    time.sleep(2)
    click_inxy(300, 189)
    pyautogui.dragRel(0, -60, duration=0.2)
    time.sleep(2)
    click_button_in_window('images/xianmengrenwu.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/lijiwancheng.png", "images/task_finish.png")
    click_button_in_window('images/task_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pvp.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/doushouchang.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/tiaozhan.png', timeout=2, click_delay=0.2, max_clicks=1)
    click_button_in_window('images/jiacheng.png', timeout=2, click_delay=0.2)
    click_inxy(440, 280)
    click_inxy(280, 280)
    click_button_in_window('images/buff_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/renshu.png", "images/cw_tiaozhan.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/renshu.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/pvpc.png", "images/lm_exit.png")
    click_button_in_window('images/pvpc.png', timeout=2, click_delay=0.2)
    find_and_clickxy_until_stop("images/guangan.png", 780, 200, timeout=20)
    time.sleep(4)
    click_button_in_window("images/guangan.png")
    keyboard.press('h')
    time.sleep(0.2)
    keyboard.release('h')
    find_and_click_until_stop("images/lm_exit.png", "images/guangan.png", timeout=75)
    find_and_click_until_stop("images/caidan.png", "images/lm_exit.png", timeout=5)
    find_and_click_until_stop("images/shijieditu.png", "images/caidan.png", timeout=5, click_delay=1)
    # klDianQuan()
    find_and_click_until_stop("images/lquyoujian.png", "images/youjian.png")
    click_button_in_window('images/lquyoujian.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yj_exit.png', timeout=2, click_delay=0.2)
    time.sleep(2)
    find_and_click_until_stop("images/zhenlin.png", "images/zhankai.png")
    find_and_click_until_stop("images/peiyang.png", "images/zhenlin.png")
    find_and_click_until_stop("images/niepan.png", "images/peiyang.png")
    find_and_click_until_stop("images/bagua.png", "images/niepan.png")
    find_and_click_until_stop("images/bggj.png", "images/bagua.png")
    find_and_click_until_stop("images/jingjie.png", "images/bggj.png")
    click_button_in_window('images/jingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pljj.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/select_all.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/qdjj.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zhankai.png", "images/suolue.png", timeout=5)
    time.sleep(2)
    click_inxy(546, 400)
    time.sleep(2)
    click_inxy(500, 279)
    click_button_in_window('images/fabaojingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/tjzb.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/xz.png", "images/fbjj.png", click_delay=1)
    click_button_in_window('images/xz.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/pljj.png', timeout=2, click_delay=0.2)
    for i in range(2):
        click_button_in_window('images/quxiao.png', timeout=2, click_delay=0.2)
        click_button_in_window('images/select_all.png', timeout=2, click_delay=0.2)
        find_and_click_until_stop("images/yes.png", "images/qdjj.png")
        click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/cw.png", "images/caidan.png", click_delay=1)
    find_and_click_until_stop("images/wyang.png", "images/cw.png", timeout=5)
    find_and_click_until_stop("images/yaoshui.png", "images/wyang.png", timeout=5)
    find_and_click_until_stop("images/djwy.png", "images/yaoshui.png", timeout=5)
    find_and_click_until_stop("images/yes.png", "images/djwy.png", timeout=5)
    click_button_in_window('images/yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/caidan.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/caidan.png", click_delay=1)


def richang():
    time.sleep(2)
    find_and_click_until_stop("images/jibeicunzhuang.png", "images/shijieditu.png", timeout=5)
    find_and_click_until_stop("images/jibeiqueding.png", "images/jibeicunzhuang.png", timeout=5)
    find_and_click_until_stop("images/jiguang.png", "images/jibeiqueding.png", timeout=15)
    yaopu()
    time.sleep(0.5)
    find_and_click_until_stop("images/zhaoling.png", "images/jiguang.png", timeout=15)
    click_button_in_window('images/zhaoling.png', timeout=5, click_delay=0.5)
    for i in range(15):
        time.sleep(0.2)
        click_inxy(650, 165)
    click_button_in_window('images/zhaoling_exit.png', timeout=3, click_delay=0.5)
    click_button_in_window2('images/jiguaung_exit.png', timeout=3)
    find_and_click_until_stop("images/ronyuxunzhang.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/ryushangdian.png", "images/ronyuxunzhang.png", timeout=5)
    click_button_in_window('images/ryushangdian.png', timeout=3, click_delay=1)
    time.sleep(1)
    click_inxy(232, 332)
    click_inxy(232, 332)
    time.sleep(0.5)
    click_inxy(232, 332)
    find_and_click_until_stop("images/caidan.png", "images/lm_exit.png", timeout=5)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=15)


def reStart():
    while True:
        click_inxy(x=334, y=-24)
        find_and_click_until_stop("images/startgame.png", "images/zmxyOL.png", click_delay=3)
        time.sleep(5)
        if find_and_return("images/startgame.png"):
            break
    drag_inxy(480, 3, 0, 489, 1)


def findcharacter(char):
    if find_and_return(char):
        click_button_in_window(char, timeout=3)
    else:
        click_button_in_window('images/manchoosedown.png', timeout=3, click_delay=0.2)
        click_button_in_window(char, timeout=3)


def yitiao(image_path,nezhai=0):
    findcharacter(image_path)
    start_to_street()
    jtKls()
    xianbao()
    chushihuaweizhi()
    street_to_xianmeng(nezhai)
    lianmeng()
    caidanhuicunzhuang()
    time.sleep(0.5)
    xianqi()
    jibeixilie()
    tianting()
    huoyue()
    richang()


def yitiao_ce(image_path):
    findcharacter(image_path)
    start_to_street()
    jtKls()
    xianbao()
    chushihuaweizhi()
    street_to_xianmeng(0)
    lianmeng()
    caidanhuicunzhuang()
    xianqi()
    time.sleep(0.5)
    jibeixilie()
    tianting()
    huoyue_ce()
    richang()


def yaoshou(image_path):
    findcharacter(image_path)
    start_to_street()
    find_and_click_until_stop("images/yaoshou.png", "images/tiaozhan.png", timeout=8)
    find_and_click_until_stop("images/ysjr.png", "images/yaoshou.png", timeout=3)
    find_and_click_until_stop("images/bxs.png", "images/ysjr.png", timeout=3)
    find_and_click_until_stop("images/bxs_yes.png", "images/bxs.png", timeout=3, click_delay=1)
    click_button_in_window("images/tzys.png", timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/alldamage.png", "images/shijieditu.png", timeout=10)
    click_inxy(178, 500)
    keyboard.press('d')
    time.sleep(6)
    keyboard.release('d')
    find_and_clickxy_until_stop("images/tuichufuben.png", 660, 505, timeout=30, click_delay=0)
    find_and_click_until_stop("images/youjian.png", "images/tuichufuben.png")
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=10, click_delay=0.5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=5)


# time.sleep(10)

characters = [
    "images/houzi.png",
    "images/tangseng.png",
    "images/bajie.png",
    "images/shaseng.png",
    "images/liuli.png",
    "images/wangzi.png",
    "images/change.png",
    "images/nezhai.png"
]


def yaoshouAll():
    for character in characters:
        yaoshou(character)
    reStart()


def zudui(image_path):
    findcharacter(image_path)
    start_to_street()
    find_and_click_until_stop("images/tianting.png", "images/shijieditu.png")
    find_and_click_until_stop("images/yes.png", "images/tianting.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/yes.png")
    drag_inxy(480, 50, 0, y1=400, duration=0.2)
    drag_inxy(507, 49, 0, 200, 0.3)
    find_and_click_until_stop("images/dontianwang.png", "images/rainbowbuilding.png", timeout=5)
    find_and_click_until_stop("images/selectRank.png", "images/dontianwang.png", timeout=5)
    click_button_in_window('images/selectRank.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_button_in_window('images/zudui.png', timeout=2, click_delay=0.2)
    time.sleep(0.5)
    find_and_click_until_stop("images/gkdw.png", "images/chuangdui.png")
    time.sleep(0.5)
    click_button_in_window('images/gkdw.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/kaishi.png', timeout=2, click_delay=1)
    find_and_click_until_stop("images/guangan.png", "images/kaishi.png",click_delay=1)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(1.8)
    keyboard.release('d')
    keyboard.press('n')
    time.sleep(0.2)
    keyboard.release('n')
    keyboard.press('d')
    time.sleep(3)
    keyboard.release('d')
    click_button_in_window("images/guangan.png")
    find_and_clickon_until_stop("images/choupai.png", "images/guangan.png")
    click_button_in_window('images/choupai.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_inxy(640, 250)
    click_button_in_window('images/backdt.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zd_exit.png", "images/backdt.png")
    find_and_click_until_stop("images/chuangdui.png", "images/zd_exit.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/huijia.png")
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=15)


def zuduiCE():
    findcharacter("images/change.png")
    start_to_street()
    find_and_click_until_stop("images/tianting.png", "images/shijieditu.png")
    find_and_click_until_stop("images/yes.png", "images/tianting.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/yes.png")
    drag_inxy(480, 50, 0, y1=400, duration=0.2)
    drag_inxy(507, 49, 0, 200, 0.3)
    find_and_click_until_stop("images/dontianwang.png", "images/rainbowbuilding.png", timeout=5)
    find_and_click_until_stop("images/selectRank.png", "images/dontianwang.png", timeout=5)
    click_button_in_window('images/selectRank.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_button_in_window('images/zudui.png', timeout=2, click_delay=0.2)
    time.sleep(0.5)
    find_and_click_until_stop("images/gkdw.png", "images/chuangdui.png")
    time.sleep(0.5)
    click_button_in_window('images/gkdw.png', timeout=2, click_delay=0.2)
    click_button_in_window('images/kaishi.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/guangan.png", "images/kaishi.png")
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(1.8)
    keyboard.release('d')
    keyboard.press('h')
    time.sleep(0.2)
    keyboard.release('h')
    keyboard.press('d')
    time.sleep(3)
    keyboard.release('d')
    click_button_in_window("images/guangan.png")
    find_and_clickon_until_stop("images/choupai.png", "images/guangan.png")
    click_button_in_window('images/choupai.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_inxy(640, 250)
    click_button_in_window('images/backdt.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("images/zd_exit.png", "images/backdt.png")
    find_and_click_until_stop("images/chuangdui.png", "images/zd_exit.png")
    find_and_click_until_stop("images/yijiannianya.png", "images/lm_exit.png")
    find_and_click_until_stop("images/youjian.png", "images/huijia.png")
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=15)


def zuduiAll():
    zudui("images/houzi.png")
    zudui("images/tangseng.png")
    zudui("images/bajie.png")
    zudui("images/shaseng.png")
    zudui("images/liuli.png")
    zudui("images/wangzi.png")
    zuduiCE()
    zudui("images/nezhai.png")
    reStart()


def ytlyAll():
    ytlyhardhard("images/houzi.png")
    reStart()
    ytlyhardhard("images/tangseng.png",huo=3)
    reStart()
    ytlyhardhard("images/bajie.png")
    reStart()
    ytlyhardhard("images/shaseng.png")
    reStart()
    ytlyhard("images/liuli.png")
    reStart()
    ytlyhardhard("images/wangzi.png")
    reStart()
    ytlyhardhard("images/change.png")
    reStart()
    ytlyhard("images/nezhai.png")
    reStart()


def dailyAll():
    yitiao("images/houzi.png")
    yitiao("images/tangseng.png")
    yitiao("images/bajie.png")
    yitiao("images/shaseng.png")
    yitiao("images/liuli.png")
    yitiao("images/wangzi.png")
    yitiao_ce("images/change.png")
    yitiao("images/nezhai.png",nezhai=1)
    reStart()


# yaoshouAll()
# zuduiAll()
dailyAll()
ytlyAll()
os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
