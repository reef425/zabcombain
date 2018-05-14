
import sys
from PyQt5.QtWidgets import *
#QInputDialog,
#QLabel,
#QMainWindow,
#QDialog,
#QWidget,
#QLineEdit,
#QDesktopWidget,
#QPlainTextEdit,
#QTabWidget,
#QToolTip,
#QPushButton,
#QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *


from zabmodule import getApi,PingRuner,initHost, initHostsFromData, initHostsFromServer

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

class Page(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # print(self.parentWidget())
        self.parent = self.parentWidget().parentWidget()
        self.settings = self.parentWidget().parentWidget().settings
        self.console  = self.parentWidget().parentWidget().console
        # self.api = None

class PageMain(Page):
    """
    pass vvvTudf88
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.loginfield = QLineEdit(self)
        self.loginfield.setText(getlogin())
        self.loginfield.setGeometry(10,10,100,25)
        self.passfield = QLineEdit('vvvTudf88',self)
        self.passfield.setGeometry(10,40,100,25)
        self.passfield.setEchoMode(2)
        self.loginButton = QPushButton("login",self)
        self.loginButton.setGeometry(10,70,100,25)
        self.loginButton.pressed.connect(self.OnPressLogin)
        self.settingButton = QPushButton("settings",self)
        self.settingButton.setGeometry(10,100,100,25)
        self.settingButton.pressed.connect(self.OnPressSetting)

    def OnPressLogin(self):
        # mz = MockZabbix()
        # getApi = mz.getApi
        self.console.appendPlainText(self.loginfield.text())
        self.console.appendPlainText(self.passfield.text())
        self.console.appendPlainText(self.settings.hostname)
        error,self.parent.api = getApi(self.settings.hostname, self.loginfield.text(),self.passfield.text())
        self.console.appendPlainText(error+"\n")

    def OnPressSetting(self):
        text, ok = QInputDialog.getMultiLineText(self, 'Settings',"Write otions",self.settings.readValue)
        if ok:
            self.settings.saveSetting(str(text))

class WorkerOrder(QThread):
        finished = pyqtSignal(str)
        def __init__(self,parent = None ):
            super(WorkerOrder,self).__init__(parent)

        def setAPI(self,api):
            self.api = api

        def setHosts(self,hosts):
            self.hosts = hosts

        def getDataPing(self):
            initHostsFromServer(self.api,self.hosts)
            PingRuner(self.api,self.hosts)
            for host in self.hosts:
                res="{:<9}:{}\n".format("name",host.get("name"))
                res+="{:<9}:{}\n".format("hostname",host.get("host"))
                for issue in host.get("issues"):
                    res+="{:<9}:{}\n".format("issue",issue.get("issue"))
                    res+="{:<9}:{}\n".format("agetime",issue.get("agetime"))
            for item in host.get("pingresult"):
                res += item.decode()
            return res

        def run(self):
            res = ''
            res = self.getDataPing()
            self.finished.emit(res)

class PageOrder(Page):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        w = self.parentWidget().geometry().width()
        h = self.parentWidget().geometry().height()
        # #  self.console
        # # Zabbix api - self.api
        self.api = None
        # # self.flags - self.process
        # self.flags = [False]
        #  Input
        self.inputLabel = QLabel("Input",self)
        self.inputLabel.move(5,5)
        self.inputField = QPlainTextEdit(self)
        self.inputField.setGeometry(5,25,w-80,160)
        self.pasteButton = QPushButton("Paste",self)
        self.pasteButton.setGeometry(w-70,25,60,25)
        self.proccButton = QPushButton("Proccess",self)
        self.proccButton.setGeometry(w-70,55,60,25)
        self.inputCheckBox =  QCheckBox("Contin.",self)
        self.inputCheckBox.move(w-70,85)
        self.pasteButton.pressed.connect(self.OnPressPaste)
        self.proccButton.pressed.connect(self.OnPressProcess)
        # self.Bind(EVT_BUTTON, self.OnPressPaste, self.pasteButton)
        # self.Bind(EVT_BUTTON, self.OnPressProcess, self.proccButton)
        # Output
        self.outputLabel = QLabel("Output",self)
        self.outputLabel.move(5,210)
        self.outputField = QPlainTextEdit(self)
        self.outputField.setGeometry(5,230,w-80,160)
        self.copyButton = QPushButton("Copy",self)
        self.copyButton.setGeometry(w-70,230,60,25)
        # self.outputCheckBox = QCheckBox("Contin.",self)
        # self.outputCheckBox.move(w-70,260)
        self.copyButton.pressed.connect(self.OnSelectCopy)


    def OnPressPaste(self):
        if self.inputField.canPaste():
            if not self.inputCheckBox.checkState():
                self.inputField.clear()
            self.inputField.paste()
            self.inputField.appendPlainText("\n")
        else:
            self.console.appendPlainText("Buffer is empty\n")




    def OnPressProcess(self):
        if not self.parent.api:
            self.console.appendPlainText("no connection to server\n")
        else:
            try:
                if self.wo.isFinished():
                    self.process()
                else:
                    self.console.appendPlainText("please wait\n")
            except AttributeError:
                self.process()

    def process(self):
        self.hosts = initHostsFromData(self.getItems())
        self.console.appendPlainText("Hosts = %d\n"%len(self.hosts))
        for i,v in enumerate(self.hosts):
            self.console.appendPlainText("%d %s\n"%(i+1,v.get("name")))
        try:
            self.wo = WorkerOrder()
            self.wo.setAPI(self.parent.api)
            self.wo.setHosts(self.hosts)
            self.wo.start()
            self.wo.finished.connect(self.getWorkerResult)
        except Exception as er:
            print("error start Thread",er)

    def getWorkerResult(self,res):
        self.outputField.appendPlainText(res)
        self.outputField.appendPlainText('\n')

    def OnSelectCopy(self):
        if self.outputField.toPlainText()=="":
            self.console.appendPlainText("Output is empty\n")
        else:
            self.outputField.selectAll()
            self.outputField.copy()
            self.console.appendPlainText("all text copied\n")

    def getItems(self):
        text = str(self.inputField.toPlainText())
        if text:
            for line in text.split("\n"):
                items = line.split("\t")
                if len(items)!=1:
                    yield items


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
        # self.panel.addTab(PageMain(),"Order")
        # self.panel.addTab(PageMain(),"Ping")
        # add console
        self.console = QPlainTextEdit(self)
        self.console.setGeometry(5,450,self.width-10,120)
        self.panel = QTabWidget(self)
        self.panel.setGeometry(5,5,self.width-10,440)
        self.panel.addTab(PageMain(self.panel),"Main")
        self.panel.addTab(PageOrder(self.panel),"Oreders")
        self.panel.addTab(Page(self.panel),"Page")
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
