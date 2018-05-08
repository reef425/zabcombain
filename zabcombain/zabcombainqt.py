
import sys
from PyQt5.QtWidgets import (QInputDialog,QMainWindow,QDialog,QWidget,QLineEdit, QDesktopWidget,QTextEdit, QTabWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5 import Qt

# from zabmodule import getApi,PingRuner,initHost, initHostsFromData, initHostsFromServer

from threading import Thread,Lock

from os import getlogin,getcwd,path,environ,name as osname
import configparser
from unittest.mock import MagicMock

class MockZabbix():

    def __init__(self):
        pass

    def getlogin(self):
        return "reef"

    def getApi(self,*args,**kwargs):
        return "connect",self

class PageMain(QWidget):
    def __init__(self,*args,**kwargs):
        """
        for test
        """
        super().__init__(*args,**kwargs)
        self.loginfield = QLineEdit(self)
        self.loginfield.setText(getlogin())
        self.loginfield.setGeometry(10,10,100,25)
        self.passfield = QLineEdit(self)
        self.passfield.setGeometry(10,40,100,25)
        self.passfield.setEchoMode(2)
        self.loginButton = QPushButton("login",self)
        self.loginButton.setGeometry(10,70,100,25)
        self.loginButton.pressed.connect(self.OnPressLogin)
        self.settingButton = QPushButton("settings",self)
        self.settingButton.setGeometry(10,100,100,25)
        self.settingButton.pressed.connect(self.OnPressSetting)

    def OnPressLogin(self):
        mz = MockZabbix()
        getApi = mz.getApi
        parent = self.parentWidget().parentWidget().parentWidget()
        parent.console.append(self.loginfield.text())
        parent.console.append(self.passfield.text())
        parent.console.append(parent.settings.hostname)
        error,self.api = getApi(parent.settings.hostname, self.loginfield.text(),self.passfield.text())
        parent.console.append(error+"\n")

    def OnPressSetting(self):
        parent = self.parentWidget().parentWidget().parentWidget()
        text, ok = QInputDialog.getMultiLineText(self, 'Settings',"Write otions",parent.settings.readValue)
        if ok:
            parent.settings.saveSetting(str(text))






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

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.api = None
        self.settings = Settings()
        self.initUI()

    def initUI(self):
        self.width = 600
        self.height = 600
        self.resize(self.width,self.height)
        QToolTip.setFont(QFont('SansSerif',10))

        self.setToolTip("This is <b>QWidget<b> widget")
        # add panel
        self.panel = QTabWidget(self)
        self.panel.setGeometry(5,5,self.width-10,440)
        self.panel.addTab(PageMain(self),"Main")
        # self.panel.addTab(PageMain(),"Order")
        # self.panel.addTab(PageMain(),"Ping")
        # add console
        self.console = QTextEdit(self)
        self.console.setGeometry(5,450,self.width-10,120)
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
    QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)
    # Show it.
    frame = MainWindow()
    # Start the event loop.
    sys.exit(app.exec_())
