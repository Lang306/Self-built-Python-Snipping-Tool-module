import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QShortcut
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QKeySequence, QImage
from PyQt5.QtCore import Qt, QRect, QTimer
from PIL import ImageGrab
from PyQt5.QtGui import QFont

main_widget = None  # 全局声明主窗口，避免生命周期问题

# 截图窗口类，负责全屏遮罩和区域选择
class ScreenshotWidget(QWidget):
    def __init__(self, bg_pixmap, parent=None):
        super().__init__(parent)
        # 设置无边框窗口，并始终置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置鼠标为十字形
        self.setCursor(Qt.CrossCursor)

        # 获取主屏幕尺寸，窗口全屏
        screen = QApplication.primaryScreen()
        self.screen_geometry = screen.geometry()
        self.setFixedSize(self.screen_geometry.size())

        # 初始化截图起止点和状态
        self.start_pos = None  # 框选起点
        self.end_pos = None    # 框选终点
        self.is_drawing = False  # 是否正在框选

        # 强制窗口全屏显示
        self.setWindowState(Qt.WindowFullScreen)
        self.show()            # 显示窗口
        self.activateWindow()  # 激活窗口
        self.raise_()          # 置顶
        self.setFocus()        # 获取焦点

        self.bg_pixmap = bg_pixmap  # 背景截图，用于显示真实桌面

    # 按下键盘事件处理（如Esc退出截图）
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # 按Esc关闭截图窗口

    # 鼠标左键按下，开始绘制截图区域
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.is_drawing = True
            self.update()  # 触发重绘

    # 鼠标移动，动态更新截图区域
    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_pos = event.pos()
            self.update()  # 触发重绘

    # 鼠标左键释放，结束绘制并保存截图
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
            self.end_pos = event.pos()
            self.save_screenshot()  # 保存截图
            self.close()            # 关闭截图窗口

    # 保存截图到剪贴板
    def save_screenshot(self):
        if self.start_pos is None or self.end_pos is None:
            return
        # 坐标转换为全局坐标
        global_start = self.mapToGlobal(self.start_pos)
        global_end = self.mapToGlobal(self.end_pos)
        rect = QRect(global_start, global_end).normalized()
        if rect.width() < 10 or rect.height() < 10:
            return  # 区域太小不截图
        self.hide()  # 先隐藏遮罩窗口
        QApplication.processEvents()  # 强制刷新界面
        # 用PIL抓屏
        img = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height()))
        img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qimg = QImage(data, img.width, img.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        # 保存到剪贴板
        QApplication.clipboard().setPixmap(pixmap)

    # 绘制遮罩和截图框
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # 先绘制全屏截图作为背景
        if self.bg_pixmap:
            painter.drawPixmap(0, 0, self.bg_pixmap)
        # 绘制半透明黑色遮罩
        painter.setBrush(QColor(0, 0, 0, 160))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        # 绘制红色截图框
        if self.is_drawing and self.start_pos and self.end_pos:
            pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)

    # 关闭截图窗口时，直接退出程序
    def closeEvent(self, event):
        QApplication.quit()
        super().closeEvent(event)

# 截图预览窗口类
class ImageViewer(QWidget):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowTitle("截图预览")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)  # 图片自适应窗口
        self.resize(pixmap.width(), pixmap.height())
        self.show()

# 启动截图流程：隐藏主窗口，延迟后弹出截图窗口
def start_capture():
    main_widget.hide()
    QTimer.singleShot(800, grab_and_show_screenshot_widget)  # 延迟800ms，体验更好

# 抓取全屏截图并弹出遮罩窗口
def grab_and_show_screenshot_widget():
    global screenshot_widget
    # 抓取全屏图片并转为QPixmap
    img = ImageGrab.grab()
    img = img.convert("RGB")
    data = img.tobytes("raw", "RGB")
    qimg = QImage(data, img.width, img.height, QImage.Format_RGB888)
    bg_pixmap = QPixmap.fromImage(qimg)
    # 弹出遮罩窗口，等待用户选择区域，区域选择和保存到剪贴板在ScreenshotWidget中完成
    screenshot_widget = ScreenshotWidget(bg_pixmap)
    screenshot_widget.showFullScreen()

# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建主窗口
    main_widget = QWidget()
    main_widget.setWindowTitle("截图工具")
    main_widget.resize(800, 600)  # 设置主窗口大小
    label = QLabel("按下 Ctrl+2 开始截图,鼠标左键框选区域，自动提取保存到剪贴板，请注意：图片格式为png，玩的开心", main_widget)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)  # 启用自动换行
    label.setGeometry(50, 200, 700, 200)  # 居中显示，宽度适中
    # 设置字体和大小
    font = QFont("微软雅黑", 20)  # 字体和字号
    label.setFont(font)
    main_widget.show()
    # 设置快捷键Ctrl+2启动截图
    shortcut = QShortcut(QKeySequence("Ctrl+2"), main_widget)
    shortcut.activated.connect(start_capture)
    print("截图工具已启动，按下 Ctrl+2 开始截图...")
    sys.exit(app.exec_())