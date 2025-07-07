# main_tray_app.py

import pystray
from PIL import Image as PILImage
from pystray import MenuItem as item
import keyboard
import threading
import sys
import os

# 导入我们自己写的截图模块
import jt_module

# 托盘点击事件：退出
def on_quit(icon, item):
    icon.stop()

# 创建系统托盘图标
def create_icon():
    image_path = "icon.png"
    if not os.path.exists(image_path):
        # 如果没有图标就用默认的空白图
        image = PILImage.new('RGB', (64, 64), color='blue')
    else:
        image = PILImage.open(image_path)
    menu = (item('退出', on_quit),)
    icon = pystray.Icon("screenshot_tool", image, "截图工具", menu)
    return icon

# 在子线程中启动 PyQt 的截图功能
def trigger_screenshot():
    thread = threading.Thread(target=jt_module.take_screenshot)
    thread.start()

# 主程序入口
if __name__ == "__main__":
    # 设置快捷键 Ctrl+2
    keyboard.add_hotkey('ctrl+2', trigger_screenshot)

    # 创建托盘图标
    icon = create_icon()

    # 运行托盘程序
    print("截图工具已启动，按 Ctrl+2 开始截图...")
    icon.run()