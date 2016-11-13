import urllib.request
import sys
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import (QPainter, QPixmap)
from PyQt5.QtCore import QSize


class ImageButton(QAbstractButton):
    def __init__(self, name, url, parent=None):
        super(ImageButton, self).__init__(parent)
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.pixmap = pixmap
        self.name = name

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return QSize(100, 100)

    def getName(self):
        return self.name
