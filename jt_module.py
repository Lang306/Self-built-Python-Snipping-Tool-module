# screenshot_module.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt5.QtCore import Qt, QRect, QTimer
from PIL import ImageGrab


# 截图窗口类（与原代码一致，略去重复部分）
class ScreenshotWidget(QWidget):
    def __init__(self, bg_pixmap, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        self.screen_geometry = screen.geometry()
        self.setFixedSize(self.screen_geometry.size())
        self.start_pos = None
        self.end_pos = None
        self.is_drawing = False
        self.setWindowState(Qt.WindowFullScreen)
        self.show()
        self.activateWindow()
        self.raise_()
        self.setFocus()
        self.bg_pixmap = bg_pixmap

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
            self.end_pos = event.pos()
            self.save_screenshot()
            self.close()

    def save_screenshot(self):
        if self.start_pos is None or self.end_pos is None:
            return
        global_start = self.mapToGlobal(self.start_pos)
        global_end = self.mapToGlobal(self.end_pos)
        rect = QRect(global_start, global_end).normalized()
        if rect.width() < 10 or rect.height() < 10:
            return
        self.hide()
        QApplication.processEvents()
        img = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height()))
        img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qimg = QImage(data, img.width, img.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        QApplication.clipboard().setPixmap(pixmap)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.bg_pixmap:
            painter.drawPixmap(0, 0, self.bg_pixmap)
        painter.setBrush(QColor(0, 0, 0, 160))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        if self.is_drawing and self.start_pos and self.end_pos:
            pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)

    def closeEvent(self, event):
        QApplication.quit()
        super().closeEvent(event)


# 全局变量
main_widget = None
screenshot_widget = None


# 启动截图流程
def take_screenshot():
    global main_widget
    app = QApplication(sys.argv)
    main_widget = QWidget()
    main_widget.hide()
    QTimer.singleShot(800, grab_and_show_screenshot_widget)
    sys.exit(app.exec_())


# 抓取全屏截图并弹出遮罩窗口
def grab_and_show_screenshot_widget():
    global screenshot_widget
    img = ImageGrab.grab()
    img = img.convert("RGB")
    data = img.tobytes("raw", "RGB")
    qimg = QImage(data, img.width, img.height, QImage.Format_RGB888)
    bg_pixmap = QPixmap.fromImage(qimg)
    screenshot_widget = ScreenshotWidget(bg_pixmap)
    screenshot_widget.showFullScreen()