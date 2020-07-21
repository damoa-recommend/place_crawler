from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from QLed import QLed

from PyQt5 import QtCore
from PyQt5 import uic

ApplicationMainForm = uic.loadUiType("main.ui")[0]
StatDisplayForm = uic.loadUiType("statDisplay.ui")[0]

class DisplayStatWidget(QWidget, StatDisplayForm):
  def __init__(self, parent=None, **kwargs):
    QWidget.__init__(self, parent=parent)
    self.setupUi(self)
    self.naver_led_layout = QVBoxLayout(self.naver_led_widget)
    self.kakao_led_layout = QVBoxLayout(self.kakao_led_widget)
    self.google_led_layout = QVBoxLayout(self.google_led_widget)

    self.naver_led=QLed(self, onColour=QLed.Red, shape=QLed.Circle)
    self.kakao_led=QLed(self, onColour=QLed.Green, shape=QLed.Circle)
    self.google_led=QLed(self, onColour=QLed.Red, shape=QLed.Circle)
    
    self.naver_led.value=False
    self.kakao_led.value=False
    self.google_led.value=False

    self.naver_led_layout.addWidget(self.naver_led)
    self.kakao_led_layout.addWidget(self.kakao_led)
    self.google_led_layout.addWidget(self.google_led)

  def toggle(self):
    self.naver_led.value = not self.naver_led.value
    self.kakao_led.value = not self.kakao_led.value
    self.google_led.value = not self.google_led.value

class Application(QMainWindow, ApplicationMainForm):
  def __init__(self ,parent=None, **kwargs):
    super().__init__()
    self.setupUi(self)

    self.display_layout = QVBoxLayout(self.stat_display_widget)
    self.display_Widget = DisplayStatWidget(self)
    self.display_layout.addWidget(self.display_Widget)

    self.start_btn.clicked.connect(self.crawler)

  def crawler(self):
    self.display_Widget.toggle()

if __name__=="__main__":
    from sys import argv, exit
    
    a=QApplication(argv)
    w=Application()
    w.show()
    exit(a.exec_())