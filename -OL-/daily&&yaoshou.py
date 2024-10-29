from PIL import ImageGrab
import cv2
import pyautogui
import pygetwindow as gw
import time
import os
from auto_yaoling import ytly
from auto_yaoling import drag_inxy
from auto_yaoling import find_xy
from pynput.keyboard import Key, Controller

keyboard = Controller()
def getwin():
    # 获取所有窗口的标题
    titles = gw.getAllTitles()

    # 打印所有窗口的标题
    for title in titles:
        print(title)


def scroll_inxy(x,y,amount=1,delay=0.1,window_title="MuMuPlayer"):
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
        pyautogui.moveTo(screen_x,screen_y,0.25)
        pyautogui.scroll(-1000)
        time.sleep(delay)
    print(f"已滚动")

def find_and_clickxy_until_stop(stop_image_path, x1,y1, window_title="MuMuPlayer", timeout=90, click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)
    stop_height, stop_width = stop_image.shape[:2]

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
        pyautogui.click(x1+x, y1+y)

        time.sleep(click_delay)  # 每次循环后的延迟

        # 检查是否超时
        if time.time() - start_time >= timeout:
            print(f"未找到 {stop_image_path}，超时退出")
            break

    # 删除截图文件
    os.remove(screenshot_filename)

def find_and_return(stop_image_path,  window_title="MuMuPlayer"):
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

def find_and_click_until_stop(stop_image_path, click_image_path, window_title="MuMuPlayer", timeout=90, click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)
    click_image = cv2.imread(click_image_path, cv2.IMREAD_GRAYSCALE)
    stop_height, stop_width = stop_image.shape[:2]
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

def find_and_clickon_until_stop(stop_image_path, click_image_path, window_title="MuMuPlayer", timeout=60, click_delay=0.5):
    # 加载图像
    stop_image = cv2.imread(stop_image_path, cv2.IMREAD_GRAYSCALE)
    click_image = cv2.imread(click_image_path, cv2.IMREAD_GRAYSCALE)
    stop_height, stop_width = stop_image.shape[:2]
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

def click_inxy(x,y,window_title="MuMuPlayer"):
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

def click_button_in_window2(image_path, window_title="MuMuPlayer", timeout=10, click_delay=0.1):
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

def click_button_in_window(image_path, window_title="MuMuPlayer", timeout=10, click_delay=0.1,max_clicks = 6):
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

    while time.time() - start_time < timeout  and not stop_clicking:
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
        print("未找到"+image_path+"，超时退出")

    # 删除截图文件
    os.remove(screenshot_filename)

def click_button_in_window(image_path, window_title="MuMuPlayer", timeout=10, click_delay=0.1,max_clicks = 6):
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

    while time.time() - start_time < timeout  and not stop_clicking:
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
        print("未找到"+image_path+"，超时退出")

    # 删除截图文件
    os.remove(screenshot_filename)

# 进入游戏到大街界面
def start_to_street():
    click_button_in_window('startgame.png', timeout=2, click_delay=0.5)
    click_button_in_window('gongao.png', timeout=12, click_delay=0.5)
    click_button_in_window('huodong.png', timeout=5, click_delay=1)

def chushihuaweizhi():
    time.sleep(1)
    click_button_in_window('shijieditu.png', timeout=2, click_delay=0.2)
    click_button_in_window('penglai.png', timeout=2, click_delay=0.2)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("youjian.png","huijia.png",click_delay=0.2,timeout=20)

def street_to_xianmeng():
    time.sleep(4)
    click_inxy(921,444)
    time.sleep(4)
    click_inxy(918,424)
    time.sleep(4)
    click_inxy(450,330)

def lianmeng():
    click_button_in_window('jingrulianmeng.png', timeout=2, click_delay=0.2)
    click_button_in_window('moyuan.png', timeout=2, click_delay=0.2)
    click_button_in_window('sxian_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('lianyaota.png', timeout=2, click_delay=0.2)
    click_button_in_window('liandan.png', timeout=2, click_delay=0.2)
    click_button_in_window('lianyaota-exit.png', timeout=4, click_delay=0.2)
    click_button_in_window('lianyaota-exit2.png', timeout=2, click_delay=0.2)
    click_button_in_window('fanhuixianmeng.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("putonjianshe.png","xianmengzhulou.png",timeout=20)
    find_and_click_until_stop("yes.png","putonjianshe.png",timeout=10)
    find_and_click_until_stop("putonjianshe.png","yes.png",timeout=10)
    find_and_click_until_stop("caidan.png","xianmeng-exit.png",timeout=20)

def caidanhuicunzhuang():
    find_and_click_until_stop("shezhi.png","caidan.png",click_delay=1.5,timeout=20)
    find_and_click_until_stop("huicunzhuang.png","shezhi.png")
    find_and_click_until_stop("shijieditu.png","huicunzhuang.png")

def jibeixilie():
    find_and_click_until_stop("jibeiditu.png","shijieditu.png")
    find_and_click_until_stop("jibeiqueding.png","jibeiditu.png")
    find_and_click_until_stop("yijiannianya.png","jibeiqueding.png")
    find_and_click_until_stop("quanxuan.png","yijiannianya.png")
    click_button_in_window('quanxuan.png', timeout=2, click_delay=0.2)
    click_button_in_window('nianya.png', timeout=2, click_delay=0.2)
    click_button_in_window('huodong.png', timeout=2, click_delay=0.2)
    click_button_in_window('ny_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('bingshuangyiji.png', timeout=2, click_delay=0.2)
    click_button_in_window('jingru.png', timeout=2, click_delay=0.2)
    click_button_in_window('yijiansaodang.png', timeout=2, click_delay=0.2)
    click_button_in_window('jingdiansaodang.png', timeout=2, click_delay=0.2)
    click_button_in_window('saodangxialu.png', timeout=2, click_delay=0.2)
    click_button_in_window('saobinqueding.png', timeout=2, click_delay=0.2)
    click_button_in_window('digong_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('huijia.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("shijieditu.png","huijia.png")

def saodan():
    find_and_click_until_stop("penglai.png","shijieditu.png")
    find_and_click_until_stop("yes.png","penglai.png")
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    time.sleep(8)
    click_inxy(695,159)
    click_button_in_window2('yes.png', timeout=2, click_delay=0.2)
    time.sleep(4)
    click_inxy(695,159)
    click_button_in_window2('yes.png', timeout=2, click_delay=0.2)
    time.sleep(4)
    click_inxy(695,159)
    click_button_in_window2('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('huodong.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("shijieditu.png","huijia.png")

def tianting():
    find_and_click_until_stop("tianting.png","shijieditu.png")
    find_and_click_until_stop("yes.png","tianting.png")
    find_and_click_until_stop("yijiannianya.png","yes.png")
    time.sleep(1)
    drag_inxy(277,359,0,y1=-300,duration=0.5)
    time.sleep(0.2)
    find_and_click_until_stop("moxie.png","lonmengfudi.png",timeout=5,click_delay=1)
    find_and_click_until_stop("kaishitiaozhan.png","moxie.png",timeout=5,click_delay=1)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5,click_delay=1)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('lonmen_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("taotuo.png","moxie.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","taotuo.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('lonmen_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("wuzhuangguan.png","lm_exit.png",timeout=5)
    find_and_click_until_stop("dadian.png","wuzhuangguan.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","dadian.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("houyuan.png","dadian.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","houyuan.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("xiangfang.png","houyuan.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","xiangfang.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('wuzhuang_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("waiyuan.png","xiangfang.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","waiyuan.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('wuzhuang_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window2('waiyuan.png', timeout=2, click_delay=1)
    find_and_click_until_stop("xukong.png","lm_exit.png",timeout=5)
    find_and_click_until_stop("zhenwu.png","xukong.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","zhenwu.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('xukon_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("yaohuang.png","zhenwu.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","yaohuang.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('xukon_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("xiuluo.png","yaohuang.png",timeout=5)
    find_and_click_until_stop("kaishitiaozhan.png","xiuluo.png",timeout=5)
    find_and_click_until_stop("yes.png","kaishitiaozhan.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('xukon_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window2('xiuluo.png', timeout=2, click_delay=0.2)
    click_button_in_window('lm_exit.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    drag_inxy(472, 420, 0, y1=-300, duration=0.5)
    drag_inxy(472, 420, 0, y1=-300, duration=0.5)
    click_button_in_window('baxian.png', timeout=2, click_delay=0.2)
    click_button_in_window('baxiantiaozhan.png', timeout=2, click_delay=0.2)
    click_button_in_window('addtime.png', timeout=2, click_delay=0.2)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('baxian_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("huijia.png","lm_exit.png")
    find_and_click_until_stop("renwu.png","huijia.png",timeout=5)

def kunlun():
    time.sleep(8)
    click_inxy(812, 218)
    click_inxy(812, 218)
    while True:
        keyboard.press('d')
        keyboard.press('k')
        if find_and_return("kls-yxd.png"):
            keyboard.release('d')
            keyboard.release('k')
            click_button_in_window("guangan.png")
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
            sec = (find_xy("kls-yxd.png") - find_xy("chenghao.png")) / 280
            click_inxy(812,218)
            click_inxy(812,218)
            keyboard.press('d')
            time.sleep(sec)
            keyboard.release('d')
            break
        elif find_and_return("iknow.png"):
            click_button_in_window("iknow.png")
            click_inxy(812, 218)
            click_inxy(812, 218)
    time.sleep(8)
    find_and_clickxy_until_stop("caidan.png",812,218,timeout=20)
    time.sleep(2)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("guangan.png",click_delay=1,max_clicks=5)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("guangan.png",click_delay=1,max_clicks=5)
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('d')
    time.sleep(5)
    keyboard.release('d')
    click_button_in_window("guangan.png",click_delay=1,max_clicks=3)
    time.sleep(2)
    find_and_click_until_stop("shezhi.png","caidan.png",click_delay=1,timeout=10)
    find_and_click_until_stop("backmap.png","shezhi.png",click_delay=0.5)
    find_and_click_until_stop("ks_exit.png","backmap.png",click_delay=0.5)
    find_and_click_until_stop("yijiannianya.png","ks_exit.png")
    click_inxy(300, 250)
    click_inxy(300, 250)
    pyautogui.dragRel(0, -200, duration=0.2)
    click_button_in_window('kunlunshan.png', timeout=2, click_delay=0.2)
    click_button_in_window('kls-task.png', timeout=2, click_delay=0.2)
    click_button_in_window('rewards.png', timeout=6, click_delay=0.2,max_clicks=10)
    click_button_in_window('zd_exit.png', timeout=6, click_delay=0.2)
    click_button_in_window('lm_exit.png', timeout=6, click_delay=1)
    find_and_click_until_stop("youjian.png","huijia.png")

def huoyue():
    find_and_click_until_stop("jdianrenwu.png","renwu.png",timeout=5)
    find_and_click_until_stop("xuanshangrenwu.png","jdianrenwu.png",timeout=5)
    find_and_click_until_stop("fqxs.png","xuanshangrenwu.png",timeout=5)
    find_and_click_until_stop("xuanshangyes.png","lijiwancheng.png",timeout=5)
    click_button_in_window("xuanshangyes.png", timeout=2, click_delay=0.2)
    find_and_click_until_stop("zhanyaochumo.png","richangrenwu.png",timeout=5)
    find_and_click_until_stop("qzzl.png","zhanyaochumo.png",timeout=5)
    time.sleep(2)
    click_inxy(300,189)
    pyautogui.dragRel(0, -60, duration=0.2)
    time.sleep(2)
    click_button_in_window('xianmengrenwu.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("lijiwancheng.png","task_finish.png")
    click_button_in_window('task_exit.png', timeout=2, click_delay=0.2)
    click_button_in_window('pvp.png', timeout=2, click_delay=0.2)
    click_button_in_window('doushouchang.png', timeout=2, click_delay=0.2)
    click_button_in_window('tiaozhan.png', timeout=2, click_delay=0.2,max_clicks=1)
    click_button_in_window('jiacheng.png', timeout=2, click_delay=0.2)
    click_inxy(440, 280)
    click_button_in_window('buff_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("renshu.png","cw_tiaozhan.png",timeout=5)
    find_and_click_until_stop("yes.png","renshu.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("pvpc.png","lm_exit.png")
    click_button_in_window('pvpc.png', timeout=2, click_delay=0.2)
    find_and_clickxy_until_stop("guangan.png",780,200,timeout=20)
    find_and_click_until_stop("lm_exit.png","guangan.png",timeout=75)
    find_and_click_until_stop("caidan.png","lm_exit.png",timeout=5)
    find_and_click_until_stop("shijieditu.png","caidan.png",timeout=5,click_delay=1)
    find_and_click_until_stop("tianting.png","shijieditu.png",timeout=5)
    find_and_click_until_stop("yes.png","tianting.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    time.sleep(10)
    click_inxy(300, 250)
    pyautogui.dragRel(0, 160, duration=0.2)
    find_and_click_until_stop("dontianwang.png","rainbowbuilding.png",timeout=5)
    find_and_click_until_stop("selectRank.png","dontianwang.png",timeout=5)
    click_button_in_window('selectRank.png', timeout=2, click_delay=0.2)
    click_button_in_window('zudui.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("gkdw.png","chuangdui.png")
    click_button_in_window('gkdw.png', timeout=2, click_delay=0.2)
    click_button_in_window('kaishi.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("guangan.png","kaishi.png")
    time.sleep(3)
    click_inxy(166,480)
    pyautogui.mouseDown(duration=5)
    time.sleep(8)
    find_and_clickon_until_stop("choupai.png","move_right.png")
    click_button_in_window('choupai.png', timeout=2, click_delay=0.2)
    time.sleep(1)
    click_inxy(640,250)
    click_button_in_window('backdt.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("zd_exit.png","backdt.png")
    find_and_click_until_stop("chuangdui.png","zd_exit.png")
    find_and_click_until_stop("yijiannianya.png","lm_exit.png")
    time.sleep(1)
    click_inxy(300, 250)
    find_and_click_until_stop("youjian.png","huijia.png")
    find_and_click_until_stop("lquyoujian.png","youjian.png")
    click_button_in_window('lquyoujian.png', timeout=2, click_delay=0.2)
    click_button_in_window('yj_exit.png', timeout=2, click_delay=0.2)
    time.sleep(2)
    find_and_click_until_stop("zhenlin.png","zhankai.png")
    find_and_click_until_stop("peiyang.png","zhenlin.png")
    find_and_click_until_stop("niepan.png","peiyang.png")
    find_and_click_until_stop("bagua.png","niepan.png")
    find_and_click_until_stop("bggj.png","bagua.png")
    find_and_click_until_stop("jingjie.png","bggj.png")
    click_button_in_window('jingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('pljj.png', timeout=2, click_delay=0.2)
    click_button_in_window('select_all.png', timeout=2, click_delay=0.2)
    click_button_in_window('qdjj.png', timeout=2, click_delay=0.2)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("zhankai.png","suolue.png",timeout=5)
    time.sleep(2)
    click_inxy(546,400)
    time.sleep(2)
    click_inxy(500,279)
    click_button_in_window('fabaojingjie.png', timeout=2, click_delay=0.2)
    click_button_in_window('tjzb.png', timeout=2, click_delay=0.2)
    click_button_in_window('fbjj.png', timeout=2, click_delay=0.2)
    click_button_in_window('xz.png', timeout=2, click_delay=0.2)
    click_button_in_window('pljj.png', timeout=2, click_delay=0.2)
    for i in range(10):
        click_button_in_window('quxiao.png', timeout=2, click_delay=0.2)
        click_button_in_window('select_all.png', timeout=2, click_delay=0.2)
        find_and_click_until_stop("yes.png","qdjj.png")
        click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    click_button_in_window('lm_exit.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("cw.png","caidan.png",click_delay=1)
    find_and_click_until_stop("wyang.png","cw.png",timeout=5)
    find_and_click_until_stop("yaoshui.png","wyang.png",timeout=5)
    find_and_click_until_stop("djwy.png","yaoshui.png",timeout=5)
    find_and_click_until_stop("yes.png","djwy.png",timeout=5)
    click_button_in_window('yes.png', timeout=2, click_delay=0.2)
    find_and_click_until_stop("caidan.png","lm_exit.png")
    find_and_click_until_stop("youjian.png","caidan.png",click_delay=1)

def richang():
    time.sleep(2)
    find_and_click_until_stop("jibeicunzhuang.png","shijieditu.png",timeout=5)
    find_and_click_until_stop("jibeiqueding.png","jibeicunzhuang.png",timeout=5)
    find_and_click_until_stop("jiguang.png","jibeiqueding.png",timeout=15)
    find_and_click_until_stop("zhaoling.png","jiguang.png",timeout=15)
    click_button_in_window('zhaoling.png', timeout=5, click_delay=0.5)
    for i in range(15):
        time.sleep(0.2)
        click_inxy(650, 165)
    click_button_in_window('zhaoling_exit.png', timeout=3, click_delay=0.5)
    click_button_in_window2('jiguaung_exit.png', timeout=3, click_delay=1)
    find_and_click_until_stop("ronyuxunzhang.png","caidan.png",click_delay=1,timeout=5)
    find_and_click_until_stop("ryushangdian.png","ronyuxunzhang.png",timeout=5)
    click_button_in_window('ryushangdian.png', timeout=3, click_delay=1)
    time.sleep(1)
    click_inxy(232,332)
    click_inxy(232,332)
    time.sleep(0.5)
    click_inxy(232,332)
    find_and_click_until_stop("caidan.png","lm_exit.png",timeout=5)
    find_and_click_until_stop("shezhi.png","caidan.png",click_delay=1,timeout=5)
    find_and_click_until_stop("kaishijiemian.png","shezhi.png",timeout=5)
    find_and_click_until_stop("ks_exit.png","kaishijiemian.png",timeout=5)
    find_and_click_until_stop("startgame.png","ks_exit.png",timeout=15)

def yitiao(image_path):
    click_button_in_window('manchoosedown.png', timeout=5, click_delay=0.2)
    click_button_in_window(image_path, timeout=5, click_delay=0.2)
    start_to_street()
    chushihuaweizhi()
    street_to_xianmeng()
    lianmeng()
    caidanhuicunzhuang()
    jibeixilie()
    saodan()
    tianting()
    huoyue()
    richang()

def yaoshou(image_path):
    click_button_in_window('manchoosedown.png', timeout=2, click_delay=0.2)
    click_button_in_window(image_path, timeout=2, click_delay=0.2)
    start_to_street()
    find_and_click_until_stop("yaoshou.png","tiaozhan.png",timeout=8)
    find_and_click_until_stop("ysjr.png","yaoshou.png",timeout=3)
    find_and_click_until_stop("bxs.png","ysjr.png",timeout=3)
    find_and_click_until_stop("bxs_yes.png","bxs.png",timeout=3,click_delay=1)
    click_button_in_window("tzys.png",timeout=2,click_delay=0.2)
    find_and_click_until_stop("alldamage.png","shijieditu.png",timeout=10)
    click_inxy(178, 500)
    keyboard.press('d')
    time.sleep(6)
    keyboard.release('d')
    find_and_clickxy_until_stop("tuichufuben.png", 660, 505, timeout=30, click_delay=0)
    find_and_click_until_stop("youjian.png","tuichufuben.png")
    find_and_click_until_stop("shezhi.png", "caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("kaishijiemian.png", "shezhi.png", timeout=10,click_delay=0.5)
    find_and_click_until_stop("ks_exit.png", "kaishijiemian.png", timeout=5)
    find_and_click_until_stop("startgame.png", "ks_exit.png", timeout=5)

yitiao("liuli.png")
yitiao("wangzi.png")
yitiao("bajie.png")
yitiao("change.png")
yitiao("shaseng.png")
yitiao("houzi.png")
yitiao("tangseng.png")


# yaoshou("liuli.png")
# yaoshou("tangseng.png")
# yaoshou("houzi.png")
# yaoshou("change.png")
# yaoshou("nezhai.png")
# yaoshou("bajie.png")
# yaoshou("shaseng.png")
# yaoshou("wangzi.png")


