from PIL import ImageGrab
import cv2
import pyautogui
import pygetwindow as gw
import time
import os
from pynput.keyboard import Key, Controller

# keyboard = Controller()
# 右键185，489
# 左键86，496
# 速度大概320/s
def clickon(x, y, duration, window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(0.2)  # 增加等待时间确保窗口激活

    # 将相对于窗口的坐标转换为屏幕的绝对坐标
    screen_x = window.left + x
    screen_y = window.top + y

    # 在屏幕的绝对坐标位置点击
    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.mouseDown()
    time.sleep(duration)
    pyautogui.mouseUp()
    print(f"已长按")

def click_inxy(x, y, window_title="MuMuPlayer"):
    # 获取指定窗口
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"未找到窗口: {window_title}")
        return

    window = windows[0]

    # 激活窗口
    window.activate()
    time.sleep(0.2)  # 增加等待时间确保窗口激活

    # 将相对于窗口的坐标转换为屏幕的绝对坐标
    screen_x = window.left + x
    screen_y = window.top + y

    # 在屏幕的绝对坐标位置点击
    pyautogui.click(screen_x, screen_y)
    print(f"已在窗口 {window_title} 内的坐标 ({x}, {y}) 处点击")

# def keyon(x,y,key,duration=1,window_title="MuMuPlayer"):
#     click_inxy(x,y)
#     keyboard = Controller()
#     keyboard.press(key)
#     time.sleep(duration)
#     keyboard.release(key)
#     print(f"已长按")

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

def find_xy(image,window_title="MuMuPlayer"):
    # 加载称号图像（彩色）
    chenghao_image = cv2.imread(image)
    chenghao_height, chenghao_width = chenghao_image.shape[:2]

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

    # 截取窗口截图
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot_filename = 'window_screenshot.png'
    screenshot.save(screenshot_filename)

    # 加载窗口截图（彩色）
    window_image = cv2.imread(screenshot_filename)

    # 使用彩色模板匹配查找称号位置
    result = cv2.matchTemplate(window_image, chenghao_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 设置匹配阈值
    threshold = 0.8  # 增加匹配阈值

    if max_val >= threshold:
        # 获取匹配位置的中心点
        center_x = max_loc[0] + chenghao_width // 2
        center_y = max_loc[1] + chenghao_height // 2
        print(f"称号图标位置: ({center_x}, {center_y})")
        return center_x
    else:
        print("未找到匹配的称号图标")
        return None

def find_and_click_until_stop(stop_image_path, click_image_path, window_title="MuMuPlayer", timeout=5, click_delay=0.5):
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

        # 使用模板匹配查找点击按钮位置
        result_click = cv2.matchTemplate(window_image, click_image, cv2.TM_CCOEFF_NORMED)
        min_val_click, max_val_click, min_loc_click, max_loc_click = cv2.minMaxLoc(result_click)

        if max_val_click >= threshold:
            button_x, button_y = max_loc_click
            button_x += x + click_width // 2  # 转换为屏幕坐标并调整为中心位置
            button_y += y + click_height // 2

            # 在窗口内点击按钮位置
            pyautogui.click(button_x, button_y)
            print(f"已点击 {click_image_path}")

        time.sleep(click_delay)  # 每次循环后的延迟

        # 检查是否超时
        if time.time() - start_time >= timeout:
            print(f"未找到 {stop_image_path}，超时退出")
            break

    # 删除截图文件
    os.remove(screenshot_filename)

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

def click_button_in_window(image_path, window_title="MuMuPlayer", timeout=5, click_delay=0.1):
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
            max_clicks = 3
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

def moveAndCollect(x, y, x1, y1, duration=5, window_title="MuMuPlayer"):
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

    # 在屏幕的绝对坐标位置点击
    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.mouseDown()
    start_time = time.time()
    while time.time() - start_time < duration:
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.click(x1 + window.left, y1 + window.top)
        pyautogui.click(x1 + window.left, y1 + window.top)
    print("已停止点击")

def goto():
    find_and_click_until_stop("ytly.png", "shijieditu.png")
    find_and_click_until_stop("zwt.png", "ytly.png")
    click_button_in_window("yl-backhome.png",timeout=3)
    find_and_click_until_stop("djkbqygb.png", "kssq.png")
    click_button_in_window("djkbqygb.png")

def catchYaoLing(type, findtime=3):
    click_button_in_window("byzj.png")
    click_button_in_window("yl_chooseup.png")
    if type in ["yl-qg.png", "yl-fs.png", "yl-sc.png", "yl-cj.png"]:
        drag_inxy(176, 395, 0, 50, 0.2)
        time.sleep(1)
    find_and_click_until_stop("yl_chooseup.png", click_image_path=type)
    click_button_in_window("yl-enter.png")
    for i in range(findtime):
        click_button_in_window("jxsj.png", click_delay=0.5, timeout=2)
        find_and_click_until_stop("catchsize.png", "jxsj.png", timeout=20)
        time.sleep(1)
        clickon(185, 489, 2)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("guangan.png", click_delay=0.3)
        clickon(86, 496, 1.5)
        moveAndCollect(185, 489, 886, 115, 5)
        clickon(185, 489, 1)
        clickon(86, 496, 0.3)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("guangan.png", click_delay=0.3)
        clickon(86, 496, 1.5)
        moveAndCollect(185, 489, 886, 115, 5)
        clickon(185, 489, 2.5)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("guangan.png", click_delay=0.3)
        clickon(86, 496, 0.5)
        moveAndCollect(185, 489, 886, 115, 5)
        find_and_click_until_stop("xuanshangyes.png","yl-exit.png")
        click_button_in_window("xuanshangyes.png")
    click_button_in_window("back-enter.png")
    find_and_click_until_stop("yl-enter.png","yl-exit.png",timeout=15)
    find_and_click_until_stop("hunzha.png", "yl-backhome.png",click_delay=1, timeout=15)
    find_and_click_until_stop("hunzha.png","ytly.png",timeout=15,click_delay=4)


def firstRelease():
    click_button_in_window("byzj.png")
    click_button_in_window("yl-enter.png")
    find_and_click_until_stop("catchsize.png", "jxsj.png", timeout=20)
    time.sleep(1)
    clickon(185, 489, 2)
    for i in range(10):
        click_inxy(843, 482)
    click_button_in_window("guangan.png", click_delay=0.3)
    clickon(86, 496, 1.5)
    moveAndCollect(185, 489, 886, 115, 5)
    find_and_click_until_stop("xuanshangyes.png", "yl-exit.png")
    find_and_click_until_stop("back-enter.png", "xuanshangyes.png",timeout=10)
    click_button_in_window("back-enter.png")
    find_and_click_until_stop("yl-enter.png", "yl-exit.png", timeout=15)
    find_and_click_until_stop("hunzha.png", "yl-backhome.png", click_delay=1, timeout=15)
    find_and_click_until_stop("plfs.png","hunzha.png",timeout=15)
    find_and_click_until_stop("ylSelectAll.png","plfs.png",click_delay=1,timeout=15)
    click_button_in_window("ylSelectAll.png",timeout=1)
    find_and_click_until_stop("nonotice.png","qrfs.png",click_delay=1,timeout=15)
    click_button_in_window("nonotice.png",timeout=5,click_delay=0.5)
    click_button_in_window("freeConfirm.png", timeout=5)
    find_and_click_until_stop("zwt.png", "yl-backhome.png",click_delay=1.5,timeout=15)

def selectLife(image="2000.png"):
    count = 0
    health = cv2.imread(image)
    free = cv2.imread("free.png", cv2.IMREAD_GRAYSCALE)
    click_button_in_window("hunzha.png", click_delay=1)
    for row in range(4):
        for line in range(8):
            x = line * 80 + 180
            y = row * 85 + 175
            while True:
                time.sleep(0.2)
                find_and_clickxy_until_stop("free.png",x,y,click_delay=0.5,timeout=2)
                # 获取指定窗口
                windows = gw.getWindowsWithTitle("MuMuPlayer")
                if not windows:
                    print(f"未找到窗口")
                    return
                window = windows[0]
                screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
                screenshot_filename = 'window_screenshot.png'
                screenshot.save(screenshot_filename)
                window_image = cv2.imread(screenshot_filename)
                window_image_gray = cv2.cvtColor(window_image, cv2.COLOR_BGR2GRAY)
                window_image_eq = cv2.equalizeHist(window_image_gray)

                result_common = cv2.matchTemplate(window_image, health, cv2.TM_CCOEFF_NORMED)
                min_val_stop, max_val_stop, min_loc_stop, max_loc_stop = cv2.minMaxLoc(result_common)
                result_stop = cv2.matchTemplate(window_image_eq, free, cv2.TM_CCOEFF_NORMED)
                minval_stop, maxval_stop, minloc_stop, maxloc_stop = cv2.minMaxLoc(result_stop)

                if not maxval_stop >= 0.7:
                    print("格子为空，停止遍历。")
                    print(f"筛选完成，1200以上总数：{count}")
                    return count

                # 设置匹配阈值
                threshold = 0.93
                if max_val_stop >= threshold:
                    count += 1
                    print(f"2200,下一个")
                    time.sleep(0.2)
                    click_inxy(34, 217)
                    break
                else:
                    time.sleep(0.2)
                    click_button_in_window("free.png",)
                    time.sleep(0.2)
                    click_inxy(34, 217)
    print(f"筛选完成，1200以上总数：{count}")
    return count

def fushen(type, num,findtime):
    while True:
        catchYaoLing(type,findtime)
        time.sleep(0.2)
        selectLife()
        time.sleep(0.2)
        click_button_in_window("yl-backhome.png",click_delay=1)
        time.sleep(0.2)
        count = selectLife()
        time.sleep(0.2)
        click_button_in_window("yl-backhome.png", click_delay=1)
        time.sleep(0.2)
        if count >= num:
            click_button_in_window("hunzha.png", click_delay=0.3)
            for i in range(count-num):
                time.sleep(0.5)
                click_inxy(180, 175)
                click_button_in_window("free.png", click_delay=0.5)
                click_inxy(180, 175)
            find_and_click_until_stop("ylSelectAll.png", "relives.png",click_delay=0.5)
            click_button_in_window("ylSelectAll.png")
            find_and_click_until_stop("freeConfirm.png","confirmRelive.png")
            click_button_in_window("freeConfirm.png")
            click_button_in_window("backHZ.png")
            find_and_click_until_stop("zwt.png","yl-backhome.png")
            break

def makesoul(num):
    find_and_click_until_stop("oneLevelCreation.png", "zwt.png", click_delay=0.5)
    find_and_click_until_stop("fsll.png", "oneLevelCreation.png", click_delay=0.5)
    click_button_in_window("fsll.png", timeout=2)
    for i in range(num - 1):
        click_inxy(610, 367)
        time.sleep(0.1)
    click_inxy(531, 490)
    time.sleep(1)
    click_inxy(280, 490)
    find_and_click_until_stop("zwt.png", "yl-backhome.png", timeout=20, click_delay=1)


def fushenSimple(type, num):
    while True:
        catchYaoLing(type,findtime=1)
        time.sleep(0.2)
        selectLife(image="healthAny.png")
        time.sleep(0.2)
        click_button_in_window("yl-backhome.png",click_delay=1)
        time.sleep(0.2)
        count = selectLife(image="healthAny.png")
        time.sleep(0.2)
        click_button_in_window("yl-backhome.png", click_delay=1)
        time.sleep(0.2)
        if count >= num:
            click_button_in_window("hunzha.png", click_delay=0.3)
            for i in range(count-num):
                time.sleep(0.5)
                click_inxy(180, 175)
                click_button_in_window("free.png", click_delay=0.5)
                click_inxy(180, 175)
            click_button_in_window("yl-backhome.png",timeout=1)
            find_and_click_until_stop("oneLevelCreation.png", "zwt.png", click_delay=0.5)
            find_and_click_until_stop("fsll.png", "oneLevelCreation.png", click_delay=0.5)
            click_button_in_window("fsll.png",timeout=2)
            for i in range(num - 1):
                click_inxy(610, 367)
                time.sleep(0.1)
            click_inxy(531, 490)
            time.sleep(1)
            click_inxy(280, 490)
            find_and_click_until_stop("zwt.png", "yl-backhome.png", timeout=20,click_delay=1)
            find_and_click_until_stop("relives.png", "hunzha.png",click_delay=0.5)
            find_and_click_until_stop("ylSelectAll.png", "relives.png",click_delay=0.5)
            click_button_in_window("ylSelectAll.png")
            find_and_click_until_stop("freeConfirm.png","confirmRelive.png")
            click_button_in_window("freeConfirm.png")
            click_button_in_window("backHZ.png")
            find_and_click_until_stop("zwt.png","yl-backhome.png")
            break

def freeTao():
    click_button_in_window("ytxs.png")
    find_and_click_until_stop("freeConfirm.png","zhpq.png",click_delay=0.5,timeout=5)
    click_button_in_window("freeConfirm.png")
    find_and_click_until_stop("zwt.png","yl-backhome.png",click_delay=0.5)

def Tao():
    click_button_in_window("ytxs.png")
    time.sleep(1)
    click_inxy(238, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("szConfim.png", click_delay=1, timeout=5)
    time.sleep(1)
    click_inxy(509, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("szConfim.png", click_delay=1, timeout=5)
    click_button_in_window("qrpq.png",click_delay=0.5)
    find_and_click_until_stop("zwt.png","yl-backhome.png")

def freeYu():
    click_button_in_window("hlc.png")
    find_and_click_until_stop("freeConfirm.png", "zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("freeConfirm.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png", click_delay=0.5)

def Yu():
    click_button_in_window("hlc.png")
    click_button_in_window("kssz.png")
    click_button_in_window("qrpq.png", click_delay=0.5)
    find_and_click_until_stop("zwt.png", "yl-backhome.png")

def freeshgfone():
    drag_inxy(67,406,75,20,0.3)
    time.sleep(2)
    click_button_in_window("shgfone.png",timeout=6,click_delay=1)
    find_and_click_until_stop("sz-exit.png","pqsz.png")
    find_and_click_until_stop("freeConfirm.png", "sz-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("freeConfirm.png")
    click_button_in_window("sz-exit.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png", click_delay=0.5)
    click_button_in_window("yl-close.png")
    click_button_in_window("ytly.png",click_delay=1)

def shgfone():
    drag_inxy(67, 406, 75, 20, 0.3)
    time.sleep(2)
    click_button_in_window("shgfone.png",timeout=6,click_delay=1)
    find_and_click_until_stop("sz-exit.png","pqsz.png")
    click_button_in_window("sz-kssz.png")
    click_button_in_window("sz-qrpq.png", click_delay=1)
    click_button_in_window("sz-exit.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png")
    click_button_in_window("yl-close.png")
    click_button_in_window("ytly.png",click_delay=1)

def freejtjxone():
    drag_inxy(525,252,-411,114,0.8)
    click_button_in_window("jtjxone.png")
    time.sleep(0.5)
    click_inxy(130, 241)
    find_and_click_until_stop("freeConfirm.png", "door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("freeConfirm.png")
    click_button_in_window("door-exit.png")
    time.sleep(1)
    click_inxy(523, 197)
    find_and_click_until_stop("freeConfirm.png", "door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("freeConfirm.png")
    click_button_in_window("door-exit.png")
    time.sleep(1)
    click_inxy(887, 140)
    find_and_click_until_stop("freeConfirm.png", "door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("freeConfirm.png")
    click_button_in_window("door-exit.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png", click_delay=0.5)
    click_button_in_window("yl-close.png")
    click_button_in_window("ytly.png",click_delay=1)

def jtjxone():
    drag_inxy(525,252,-411,114,0.8)
    click_button_in_window("jtjxone.png")
    time.sleep(0.5)
    click_inxy(130, 241)
    click_button_in_window("door-kssz.png")
    click_button_in_window("door-qrpq.png", click_delay=1)
    click_button_in_window("door-exit.png")
    time.sleep(1)
    click_inxy(523, 197)
    click_button_in_window("door-kssz.png")
    click_button_in_window("door-qrpq.png", click_delay=1)
    click_button_in_window("door-exit.png")
    time.sleep(1)
    click_inxy(887, 140)
    click_button_in_window("door-kssz.png")
    click_button_in_window("door-qrpq.png", click_delay=1)
    click_button_in_window("door-exit.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png")
    click_button_in_window("yl-close.png")
    click_button_in_window("ytly.png",click_delay=1)

def freeyllt():
    find_and_click_until_stop("ckyl.png", "yllt.png", click_delay=0.5)
    click_button_in_window("ckyl.png", timeout=5)
    click_button_in_window("yl-qx.png")
    find_and_click_until_stop("ylSelectAll.png", "plfs.png", click_delay=0.5)
    click_button_in_window("ylSelectAll.png", timeout=5)
    find_and_click_until_stop("freeConfirm.png", "qrfs.png", click_delay=0.5)
    click_button_in_window("freeConfirm.png", timeout=5)
    find_and_click_until_stop("yl-backhome.png", "yllt_exit.png")
    find_and_click_until_stop("zwt.png", "yl-backhome.png")

def ytlyhard(image_path):
    click_button_in_window('manchoosedown.png', timeout=8, click_delay=0.2)
    click_button_in_window(image_path, timeout=5, click_delay=0.2)
    click_button_in_window('startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('gongao.png', timeout=10, click_delay=2)
    click_button_in_window('huodong.png', timeout=3, click_delay=2)
    goto()
    freeYu()
    freeTao()
    freejtjxone()
    freeshgfone()
    freeyllt()
    firstRelease()
    makesoul(29)
    fushen("yl-cj.png",1,1)
    fushen("yl-cd.png",1,1)
    fushen("yl-sg.png",4,2)
    fushen("yl-sh.png",2,1)
    fushen("yl-lq.png",2,1)
    fushen("yl-qg.png",4,2)
    fushen("yl-fs.png",4,2)
    fushen("yl-sc.png",4,2)
    fushen("yl-by.png",7,2)
    Tao()
    shgfone()
    jtjxone()
    Yu() 
    click_button_in_window("yl-close.png",click_delay=1)
    click_button_in_window("map-exit.png",click_delay=1)
    find_and_click_until_stop("shezhi.png", "caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("kaishijiemian.png", "shezhi.png", timeout=5)
    find_and_click_until_stop("ks_exit.png", "kaishijiemian.png", timeout=5)
    find_and_click_until_stop("startgame.png", "ks_exit.png", timeout=20)

def ytly(image_path):
    click_button_in_window('manchoosedown.png', timeout=8, click_delay=0.2)
    click_button_in_window(image_path, timeout=5, click_delay=0.2)
    click_button_in_window('startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('gongao.png', timeout=20, click_delay=2)
    click_button_in_window('huodong.png', timeout=3, click_delay=2)
    goto()
    freeYu()
    freeTao()
    freejtjxone()
    freeshgfone()
    freeyllt()
    firstRelease()
    fushenSimple("yl-cj.png",6)
    fushenSimple("yl-cd.png",6)
    fushenSimple("yl-sg.png",6)
    fushenSimple("yl-sg.png",6)
    fushenSimple("yl-sh.png",6)
    fushenSimple("yl-lq.png",6)
    fushenSimple("yl-qg.png",8)
    fushenSimple("yl-fs.png",8)
    fushenSimple("yl-sc.png",8)
    fushenSimple("yl-by.png",12)
    fushenSimple("yl-by.png",12)
    Tao()
    shgfone()
    jtjxone()
    Yu()
    click_button_in_window("yl-close.png",click_delay=1)
    click_button_in_window("map-exit.png",click_delay=1)
    find_and_click_until_stop("shezhi.png", "caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("kaishijiemian.png", "shezhi.png", timeout=5)
    find_and_click_until_stop("ks_exit.png", "kaishijiemian.png", timeout=5)
    find_and_click_until_stop("startgame.png", "ks_exit.png", timeout=20)

