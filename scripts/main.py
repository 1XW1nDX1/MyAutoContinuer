import time
from datetime import datetime, timedelta

import pyautogui
import pyperclip
import pygetwindow as gw
import win32gui
import win32con
import win32com.client

# ===== 配置 =====

TARGET_TIME = "02:57:00"  # 目标时间，格式为 HH:MM:SS
MESSAGE = "继续"
WINDOW_TITLE = "ChatGPT"

pyautogui.FAILSAFE = True


def activate_window(window):
    hwnd = window._hWnd

    if not win32gui.IsWindow(hwnd):
        return False

    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")

        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)

    except Exception as e:
        print(f"窗口激活失败：{e}")
        return False

    return win32gui.GetForegroundWindow() == hwnd


def send_message():
    windows = [
        w for w in gw.getWindowsWithTitle(WINDOW_TITLE)
        if w.visible
    ]

    if not windows:
        print("未找到 ChatGPT 窗口")
        return False

    window = windows[0]

    if not activate_window(window):
        print("ChatGPT 未获得焦点，停止发送")
        return False

    # 计算输入框位置
    x = window.left + window.width // 2
    y = window.top + window.height - 120

    # 确认焦点仍然正确
    if win32gui.GetForegroundWindow() != window._hWnd:
        print("焦点发生变化，停止发送")
        return False

    pyautogui.click(x, y)
    time.sleep(0.3)

    pyperclip.copy(MESSAGE)
    pyautogui.hotkey("ctrl", "v")

    time.sleep(0.3)
    pyautogui.press("enter")

    print(f"[{datetime.now():%H:%M:%S}] 已执行发送操作：{MESSAGE}")
    return True


def wait_until(target_time):
    now = datetime.now()
    hour, minute, second = map(int, target_time.split(":"))

    target = now.replace(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=0
    )

    # 如果今天已经过了目标时间，则等到明天
    if target <= now:
        target += timedelta(days=1)

    print(f"计划执行时间：{target:%Y-%m-%d %H:%M:%S}")

    while True:
        remaining = (target - datetime.now()).total_seconds()

        if remaining <= 0:
            break

        time.sleep(min(remaining, 0.5))


if __name__ == "__main__":
    wait_until(TARGET_TIME)
    send_message()