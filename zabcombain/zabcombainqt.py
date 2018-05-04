
import sys
from PyQt5.QtWidgets import (QWidget,QDesktopWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont

# from zabcombain.zabmodule import getApi,PingRuner,initHost, initHostsFromData, initHostsFromServer

from threading import Thread,Lock

from os import getlogin,getcwd,path,environ,name as osname
import configparser


class Settings():
    def __init__(self):
        self.defaultValue = "[server]\nhost = http://127.0.0.1/zabbix\n"
        if osname == "nt":
            self.home = path.join("c:\\",environ["HOMEPATH"])
        else:
            self.home = environ["HOME"]
        self.here = path.join(self.home,".zabcombain")
        self.hostname = None
        self.readSetting()

    def readSetting(self):
        if path.exists(self.here):
            with open(self.here,"r") as f:
                self.readValue = f.read()
        else:
            self.readValue=self.defaultValue
            with open(self.here,"w") as f:
                f.write(self.defaultValue)
        self.parseSetting()

    def saveSetting(self,value):
        if self.readValue != value:
            with open(self.here,"w") as f:
                f.write(value)
            self.readValue = value

    def parseSetting(self):
        config = configparser.ConfigParser()
        config.read(self.here)
        self.hostname = config["server"]["host"]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.width = 600
        self.height = 600
        self.resize(self.width,self.height)
        QToolTip.setFont(QFont('SansSerif',10))

        self.setToolTip("This is <b>QWidget<b> widget")

        self.center()
        self.setWindowTitle('Zabcombain')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    # Next, create an application object.
    # QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)
    # Show it.
    frame = MainWindow()
    # Start the event loop.
    sys.exit(app.exec_())
