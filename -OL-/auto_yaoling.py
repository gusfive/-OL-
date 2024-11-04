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

keyboard = Controller()
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
    time.sleep(0.1)  # 增加等待时间确保窗口激活

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


def click_button_in_window(image_path, window_title="MuMuPlayer", timeout=5, click_delay=0.3):
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


def findcharacter(char):
    if find_and_return(char):
        click_button_in_window(char,timeout=3)
    else:
        click_button_in_window('images/manchoosedown.png', timeout=3, click_delay=0.2)
        click_button_in_window(char, timeout=3)


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

def moveAndCollectNew(duration=5):
    click_inxy(812, 218)
    click_inxy(812, 218)
    keyboard.press('q')
    keyboard.press('d')
    time.sleep(duration)
    keyboard.release('q')
    keyboard.release('d')
    print("已停止点击")

def goto():
    find_and_click_until_stop("images/ytly.png", "images/shijieditu.png")
    find_and_click_until_stop("images/zwt.png", "images/ytly.png")
    click_button_in_window("images/yl-backhome.png",timeout=3)
    find_and_click_until_stop("images/djkbqygb.png", "images/kssq.png")
    click_button_in_window("images/djkbqygb.png")

def catchYaoLing(type, findtime=3):
    click_button_in_window("images/byzj.png")
    click_button_in_window("images/yl_chooseup.png")
    if type in ["images/yl-qg.png", "images/yl-fs.png", "images/yl-sc.png", "images/yl-cj.png"]:
        drag_inxy(176, 395, 0, 50, 0.2)
        time.sleep(1)
    find_and_click_until_stop("images/yl_chooseup.png", click_image_path=type)
    click_button_in_window("images/yl-enter.png")
    for i in range(findtime):
        click_button_in_window("images/jxsj.png", click_delay=0.5, timeout=2)
        find_and_click_until_stop("images/catchsize.png", "images/jxsj.png", timeout=20)
        time.sleep(1)
        clickon(185, 489, 2)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        clickon(86, 496, 1.5)
        moveAndCollect(185, 489, 886, 115, 5)
        clickon(185, 489, 1)
        clickon(86, 496, 0.3)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        clickon(86, 496, 1.5)
        moveAndCollect(185, 489, 886, 115, 5)
        clickon(185, 489, 2.5)
        for i in range(14):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        clickon(86, 496, 0.5)
        moveAndCollect(185, 489, 886, 115, 5)
        find_and_click_until_stop("images/xuanshangyes.png","images/yl-exit.png")
        click_button_in_window("images/xuanshangyes.png")
    click_button_in_window("images/back-enter.png")
    find_and_click_until_stop("images/yl-enter.png","images/yl-exit.png",timeout=15)
    find_and_click_until_stop("images/hunzha.png", "images/yl-backhome.png",click_delay=1, timeout=15)
    find_and_click_until_stop("images/hunzha.png","images/ytly.png",timeout=15,click_delay=4)


def firstRelease():
    click_button_in_window("images/byzj.png")
    click_button_in_window("images/yl-enter.png")
    find_and_click_until_stop("images/catchsize.png", "images/jxsj.png", timeout=20)
    time.sleep(1)
    clickon(185, 489, 1.1)
    for i in range(5):
        click_inxy(843, 482)
    click_button_in_window("images/guangan.png", click_delay=0.3)
    clickon(86, 496, 0.8)
    moveAndCollectNew(2)
    find_and_click_until_stop("images/xuanshangyes.png", "images/yl-exit.png")
    find_and_click_until_stop("images/back-enter.png", "images/xuanshangyes.png",timeout=10)
    click_button_in_window("images/back-enter.png")
    find_and_click_until_stop("images/yl-enter.png", "images/yl-exit.png", timeout=15)
    find_and_click_until_stop("images/hunzha.png", "images/yl-backhome.png", click_delay=1, timeout=15)
    find_and_click_until_stop("images/plfs.png","images/hunzha.png",timeout=15)
    find_and_click_until_stop("images/ylSelectAll.png","images/plfs.png",click_delay=1,timeout=15)
    click_button_in_window("images/ylSelectAll.png",timeout=1)
    find_and_click_until_stop("images/nonotice.png","images/qrfs.png",click_delay=1,timeout=15)
    find_and_click_until_stop("images/notice_yes.png","images/nonotice.png",click_delay=1)
    click_button_in_window("images/freeConfirm.png", timeout=5)
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png",click_delay=1.5,timeout=15)


def selectLife(img="images/hunzha.png",image="images/0000.png"):
    count = 0
    health = cv2.imread(image)
    free = cv2.imread("images/free.png", cv2.IMREAD_GRAYSCALE)
    click_button_in_window(img, click_delay=1)
    for row in range(4):
        for line in range(8):
            x = line * 80 + 180
            y = row * 85 + 175
            while True:
                time.sleep(0.1)
                find_and_clickxy_until_stop("images/free.png",x,y,click_delay=0.3,timeout=2)
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
                    click_inxy(34, 217)
                    break
                else:
                    click_button_in_window("images/free.png",)
                    click_inxy(34, 217)
    print(f"筛选完成，1200以上总数：{count}")
    return count


def catchAndSelect(type,num):
    click_button_in_window("images/byzj.png")
    click_button_in_window("images/yl_chooseup.png",click_delay=0.5)
    if type in ["images/yl-qg.png", "images/yl-fs.png", "images/yl-sc.png", "images/yl-cj.png"]:
        drag_inxy(176, 395, 0, 50, 0.2)
        time.sleep(2)
    find_and_click_until_stop("images/yl_chooseup.png", click_image_path=type)
    click_button_in_window("images/yl-enter.png")
    while True:
        click_button_in_window("images/jxsj.png", click_delay=0.5, timeout=2)
        find_and_click_until_stop("images/catchsize.png", "images/jxsj.png", timeout=20)
        time.sleep(1)
        clickon(185, 489, 1)
        for i in range(3):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        clickon(86, 496, 0.8)
        moveAndCollectNew(2)
        clickon(185, 489, 1)
        clickon(86, 496, 0.05)
        for i in range(3):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        clickon(86, 496, 0.8)
        moveAndCollectNew(3)
        clickon(185, 489, 1)
        for i in range(5):
            click_inxy(843, 482)
        click_button_in_window("images/guangan.png", click_delay=0.3)
        moveAndCollectNew(3)
        count = selectLife("images/hunzha-in.png", "images/0000.png")
        if count >= num:
            for i in range(count-num):
                time.sleep(0.3)
                click_inxy(180, 175)
                click_button_in_window("images/free.png", click_delay=0.5)
                click_inxy(180, 175)
            break
        click_button_in_window("images/yl-backhome.png")
        find_and_click_until_stop("images/xuanshangyes.png", "images/yl-exit.png")
        click_button_in_window("images/xuanshangyes.png")
    click_button_in_window("images/yl-backhome.png")
    find_and_click_until_stop("images/xuanshangyes.png", "images/yl-exit.png")
    click_button_in_window("images/xuanshangyes.png")
    click_button_in_window("images/back-enter.png")
    find_and_click_until_stop("images/yl-enter.png", "images/yl-exit.png", timeout=15)
    find_and_click_until_stop("images/hunzha.png", "images/yl-backhome.png", click_delay=1, timeout=15)
    find_and_click_until_stop("images/hunzha.png", "images/ytly.png", timeout=15, click_delay=4)


def fushen(type, num):
    catchAndSelect(type,num)
    click_button_in_window("images/hunzha.png", click_delay=0.3)
    find_and_click_until_stop("images/ylSelectAll.png", "images/relives.png",click_delay=0.5)
    click_button_in_window("images/ylSelectAll.png")
    find_and_click_until_stop("images/freeConfirm.png","images/confirmRelive.png")
    click_button_in_window("images/freeConfirm.png")
    click_button_in_window("images/backHZ.png")
    find_and_click_until_stop("images/zwt.png","images/yl-backhome.png")


def makesoul(num):
    find_and_click_until_stop("images/oneLevelCreation.png", "images/zwt.png", click_delay=0.5)
    find_and_click_until_stop("images/fsll.png", "images/oneLevelCreation.png", click_delay=0.5)
    click_button_in_window("images/fsll.png", timeout=2)
    for i in range(num - 1):
        click_inxy(610, 367)
        time.sleep(0.1)
    click_inxy(531, 490)
    time.sleep(1)
    click_inxy(280, 490)
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png", timeout=20, click_delay=1)


def fushenSimple(type, num):
    while True:
        catchYaoLing(type,findtime=1)
        time.sleep(0.2)
        selectLife(image="images/healthAny.png")
        time.sleep(0.2)
        click_button_in_window("images/yl-backhome.png",click_delay=1)
        time.sleep(0.2)
        count = selectLife(image="images/healthAny.png")
        time.sleep(0.2)
        click_button_in_window("images/yl-backhome.png", click_delay=1)
        time.sleep(0.2)
        if count >= num:
            click_button_in_window("images/hunzha.png", click_delay=0.3)
            for i in range(count-num):
                time.sleep(0.5)
                click_inxy(180, 175)
                click_button_in_window("images/free.png", click_delay=0.5)
                click_inxy(180, 175)
            click_button_in_window("images/yl-backhome.png",timeout=1)
            find_and_click_until_stop("images/oneLevelCreation.png", "images/zwt.png", click_delay=0.5)
            find_and_click_until_stop("images/fsll.png", "images/oneLevelCreation.png", click_delay=0.5)
            click_button_in_window("images/fsll.png",timeout=2)
            for i in range(num - 1):
                click_inxy(610, 367)
                time.sleep(0.1)
            click_inxy(531, 490)
            time.sleep(1)
            click_inxy(280, 490)
            find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png", timeout=20,click_delay=1)
            find_and_click_until_stop("images/relives.png", "images/hunzha.png",click_delay=0.5)
            find_and_click_until_stop("images/ylSelectAll.png", "images/relives.png",click_delay=0.5)
            click_button_in_window("images/ylSelectAll.png")
            find_and_click_until_stop("images/freeConfirm.png","images/confirmRelive.png")
            click_button_in_window("images/freeConfirm.png")
            click_button_in_window("images/backHZ.png")
            find_and_click_until_stop("images/zwt.png","images/yl-backhome.png")
            break


def freeTao(image="images/ytxs-hard.png"):
    click_button_in_window(image,click_delay=2)
    find_and_click_until_stop("images/freeConfirm.png","images/zhpq.png",click_delay=0.5,timeout=5)
    click_button_in_window("images/freeConfirm.png")
    find_and_click_until_stop("images/zwt.png","images/yl-backhome.png",click_delay=0.5)


def Tao(image="images/ytxs-hard.png"):
    click_button_in_window(image,click_delay=2)
    time.sleep(1)
    click_inxy(238, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("images/shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("images/szConfim.png", click_delay=1, timeout=5)
    time.sleep(1)
    click_inxy(509, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("images/shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("images/szConfim.png", click_delay=1, timeout=5)
    click_button_in_window("images/qrpq.png",click_delay=0.5)
    find_and_click_until_stop("images/zwt.png","images/yl-backhome.png")


def freeYu(image="images/hlc.png"):
    click_button_in_window(image,click_delay=1.5)
    find_and_click_until_stop("images/freeConfirm.png", "images/zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("images/freeConfirm.png")
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png", click_delay=0.5)


def Yu(image="images/hlc.png"):
    click_button_in_window(image,click_delay=1.5)
    time.sleep(1)
    click_inxy(238, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("images/shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("images/szConfim.png", click_delay=1, timeout=5)
    time.sleep(1)
    click_inxy(509, 477)
    time.sleep(1)
    click_inxy(188, 122)
    click_button_in_window("images/shangzheng.png", click_delay=1, timeout=5)
    click_button_in_window("images/szConfim.png", click_delay=1, timeout=5)
    click_button_in_window("images/qrpq.png", click_delay=0.5)
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png")


def freeshgfone():
    drag_inxy(67,406,75,20,0.3)
    time.sleep(2)
    click_button_in_window("images/shgfone.png",timeout=6,click_delay=2)
    click_button_in_window("images/shgfone.png",timeout=3,click_delay=2)
    find_and_click_until_stop("images/sz-exit.png","images/pqsz.png")
    find_and_click_until_stop("images/freeConfirm.png", "images/sz-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("images/freeConfirm.png")
    click_button_in_window("images/sz-exit.png")
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png", click_delay=0.5)
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/ytly.png",click_delay=1)


def shgfone():
    drag_inxy(67, 406, 75, 20, 0.3)
    time.sleep(2)
    click_button_in_window("images/shgfone.png",timeout=6,click_delay=2)
    click_button_in_window("images/shgfone.png",timeout=3,click_delay=2)
    find_and_click_until_stop("images/sz-exit.png","images/pqsz.png")
    click_button_in_window("images/sz-kssz.png")
    find_and_click_until_stop("images/sz-qrpq.png","images/kssz-yes.png")
    time.sleep(1)
    click_button_in_window("images/sz-qrpq.png", click_delay=1)
    click_button_in_window("images/sz-exit.png")
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png")
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/ytly.png",click_delay=1)


def freejtjxone(image="images/jtjxone.png"):
    drag_inxy(525,252,-411,114,0.8)
    click_button_in_window(image,click_delay=1.5)
    click_button_in_window(image,click_delay=1.5)
    time.sleep(0.5)
    click_inxy(130, 241)
    find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("images/freeConfirm.png")
    click_button_in_window("images/door-exit.png")
    time.sleep(1)
    click_inxy(523, 197)
    find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    click_button_in_window("images/freeConfirm.png")
    click_button_in_window("images/door-exit.png")
    # time.sleep(1)
    # click_inxy(887, 140)
    # find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    # click_button_in_window("images/freeConfirm.png")
    # click_button_in_window("images/door-exit.png")
    # time.sleep(1)
    # drag_inxy(634, 441, -600, 0, 0.5)
    # time.sleep(0.5)
    # drag_inxy(634, 441, -600, 0, 0.5)
    # click_inxy(307,177)
    # find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    # click_button_in_window("images/freeConfirm.png")
    # click_button_in_window("images/door-exit.png")
    # click_inxy(699,223)
    # find_and_click_until_stop("images/freeConfirm.png", "images/door-zhpq.png", click_delay=0.5, timeout=5)
    # click_button_in_window("images/freeConfirm.png")
    # click_button_in_window("images/door-exit.png")
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png", click_delay=0.5)
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/ytly.png",click_delay=1)


def jtjxone(image="images/jtjxone.png"):
    drag_inxy(525,252,-411,114,0.8)
    click_button_in_window(image,click_delay=1.5)
    click_button_in_window(image,click_delay=1.5)
    time.sleep(0.5)
    click_inxy(130, 241)
    click_button_in_window("images/door-kssz.png")
    find_and_click_until_stop("images/door-qrpq.png","images/kssz-yes.png")
    time.sleep(1)
    click_button_in_window("images/door-qrpq.png", click_delay=1)
    time.sleep(2)
    click_inxy(523, 197)
    click_button_in_window("images/door-kssz.png")
    find_and_click_until_stop("images/door-qrpq.png","images/kssz-yes.png")
    time.sleep(1)
    click_button_in_window("images/door-qrpq.png", click_delay=1)
    time.sleep(1)
    # click_inxy(887, 140)
    # click_button_in_window("images/door-kssz.png")
    # find_and_click_until_stop("images/door-qrpq.png", "images/kssz-yes.png")
    # time.sleep(1)
    # click_button_in_window("images/door-qrpq.png", click_delay=1)
    # time.sleep(1)
    # drag_inxy(634, 441, -600, 0, 0.5)
    # time.sleep(0.5)
    # drag_inxy(634, 441, -600, 0, 0.5)
    # click_inxy(307,177)
    # click_button_in_window("images/door-kssz.png")
    # find_and_click_until_stop("images/door-qrpq.png", "images/kssz-yes.png")
    # time.sleep(1)
    # click_button_in_window("images/door-qrpq.png", click_delay=1)
    # time.sleep(1)
    # click_inxy(699,223)
    # click_button_in_window("images/door-kssz.png")
    # find_and_click_until_stop("images/door-qrpq.png", "images/kssz-yes.png")
    # time.sleep(1)
    # click_button_in_window("images/door-qrpq.png", click_delay=1)
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png",click_delay=1)
    click_button_in_window("images/yl-close.png")
    click_button_in_window("images/ytly.png",click_delay=1)


def freeyllt():
    find_and_click_until_stop("images/ckyl.png", "images/yllt.png", click_delay=0.5)
    click_button_in_window("images/ckyl.png", timeout=5)
    click_button_in_window("images/yl-qx.png")
    find_and_click_until_stop("images/ylSelectAll.png", "images/plfs.png", click_delay=0.5)
    click_button_in_window("images/ylSelectAll.png", timeout=5)
    find_and_click_until_stop("images/freeConfirm.png", "images/qrfs.png", click_delay=0.5)
    click_button_in_window("images/freeConfirm.png", timeout=5)
    find_and_click_until_stop("images/yl-backhome.png", "images/yllt_exit.png")
    find_and_click_until_stop("images/zwt.png", "images/yl-backhome.png")


def ytlyhard(image_path):
    findcharacter(image_path)
    click_button_in_window('images/startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('images/gongao.png', timeout=10, click_delay=2)
    click_button_in_window('images/huodong.png', timeout=3, click_delay=2)
    goto()
    freeYu("images/hlc-hard.png")
    freeTao("images/ytxs.png")
    freejtjxone("images/jtjxone-hardhard.png")
    freeshgfone()
    freeyllt()
    firstRelease()
    makesoul(74)
    fushen("images/yl-cj.png",2)
    fushen("images/yl-cd.png",2)
    fushen("images/yl-sg.png",16)
    fushen("images/yl-sh.png",6)
    fushen("images/yl-lq.png",6)
    fushen("images/yl-qg.png",6)
    fushen("images/yl-fs.png",6)
    fushen("images/yl-sc.png",6)
    fushen("images/yl-by.png",10)
    fushen("images/yl-by.png",10)
    fushen("images/yl-fd.png",4)
    Tao("images/ytxs.png")
    shgfone()
    jtjxone("images/jtjxone-hardhard.png")
    Yu("images/hlc-hard.png")
    click_button_in_window("images/yl-close.png",click_delay=1)
    click_button_in_window("images/map-exit.png",click_delay=1)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=20)


def ytly(image_path):
    findcharacter(image_path)
    click_button_in_window('images/startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('images/gongao.png', timeout=10, click_delay=2)
    click_button_in_window('images/huodong.png', timeout=3, click_delay=2)
    goto()
    freeYu()
    freeTao()
    freejtjxone()
    freeshgfone()
    freeyllt()
    firstRelease()
    makesoul(39)
    fushen("images/yl-cj.png",1)
    fushen("images/yl-cd.png",1)
    fushen("images/yl-sg.png",8)
    fushen("images/yl-sh.png",4)
    fushen("images/yl-lq.png",4)
    fushen("images/yl-qg.png",9)
    fushen("images/yl-fs.png",9)
    fushen("images/yl-sc.png",9)
    fushen("images/yl-by.png",11)
    Tao()
    Yu()
    shgfone()
    jtjxone()
    click_button_in_window("images/yl-close.png", click_delay=1)
    click_button_in_window("images/map-exit.png", click_delay=1)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=20)


def ytlyhardhard(image_path,yu=2,tao=2,huo=2,jtjx=4,dan=2):
    findcharacter(image_path)
    click_button_in_window('images/startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('images/gongao.png', timeout=10, click_delay=2)
    click_button_in_window('images/huodong.png', timeout=3, click_delay=2)
    goto()
    freeYu()
    freeTao()
    freejtjxone("images/jtjxone.png")
    freeshgfone()
    freeyllt()
    firstRelease()
    makesoul(tao*2+yu*2+huo*10+jtjx*4+4*dan)
    fushen("images/yl-cj.png", tao)
    fushen("images/yl-cd.png", yu)
    fushen("images/yl-sg.png", 4*huo+2*dan)
    fushen("images/yl-sh.png", 2*huo)
    fushen("images/yl-lq.png", 2*huo)
    fushen("images/yl-qg.png", jtjx)
    fushen("images/yl-fs.png", jtjx)
    fushen("images/yl-sc.png", jtjx)
    fushen("images/yl-by.png", tao+yu+2*huo+jtjx)
    fushen("images/yl-fd.png",dan*2)
    Tao()
    shgfone()
    jtjxone("images/jtjxone.png")
    Yu()
    click_button_in_window("images/yl-close.png",click_delay=1)
    click_button_in_window("images/map-exit.png",click_delay=1)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=20)


def catchforweekends(image_path):
    click_button_in_window('images/manchoosedown.png', timeout=8, click_delay=0.2)
    click_button_in_window(image_path, timeout=5, click_delay=0.2)
    click_button_in_window('images/startgame.png', timeout=5, click_delay=0.2)
    click_button_in_window('images/gongao.png', timeout=10, click_delay=2)
    click_button_in_window('images/huodong.png', timeout=3, click_delay=2)
    goto()
    firstRelease()
    makesoul(29)
    fushen("images/yl-cj.png",2,1)
    fushen("images/yl-cd.png",2,1)
    fushen("images/yl-sg.png",8,3)
    fushen("images/yl-sh.png",4,2)
    fushen("images/yl-lq.png",4,2)
    fushen("images/yl-qg.png",8,3)
    fushen("images/yl-fs.png",8,3)
    fushen("images/yl-sc.png",8,3)
    fushen("images/yl-by.png",14,3)
    click_button_in_window("images/yl-close.png",click_delay=1)
    click_button_in_window("images/map-exit.png",click_delay=1)
    find_and_click_until_stop("images/shezhi.png", "images/caidan.png", click_delay=1, timeout=5)
    find_and_click_until_stop("images/kaishijiemian.png", "images/shezhi.png", timeout=5)
    find_and_click_until_stop("images/ks_exit.png", "images/kaishijiemian.png", timeout=5)
    find_and_click_until_stop("images/startgame.png", "images/ks_exit.png", timeout=20)
