from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from subprocess import Popen,PIPE
import sys


lock = QReadWriteLock()

class Worker(QThread):
    finished = pyqtSignal(str)
    def __init__(self,parent = None ):
        super(Worker,self).__init__(parent)

    def setIP(self,ip):
        self.ip = ip

    def pingFromOS(self,ip):
        if ip is None:
            return b"ip is None"
        if ip=='':
            return b'ip is empty'
        pcArg=['ping','-c','9',ip]
        proc = Popen(pcArg,stdout=PIPE)
        out = proc.stdout.readlines()
        res = b""
        for row in out:
            res+=row
        proc.stdout.close()
        return res.decode()


    def run(self):
        res  = self.pingFromOS(self.ip)
        self.finished.emit(res)



class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.initUI()

    def initUI(self):
        self.width = 600
        self.height = 600
        self.resize(self.width,self.height)
        self.center()
        self.ipField = QLineEdit(self)
        self.ipField.setText('127.1.1.0')
        self.ipField.setGeometry(10,10,100,25)
        self.button = QPushButton("ping",self)
        self.button.setGeometry(120,10,100,25)
        self.button.clicked.connect(self.onPressPing)
        self.console = QPlainTextEdit(self)
        self.console.setGeometry(5,50,self.width-10,self.height-60)
        self.setWindowTitle('Ping from os')
        self.show()

    def onPressPing(self):
        self.w = Worker()
        self.w.setIP(self.ipField.text())
        self.w.start()
        self.w.finished.connect(self.OnPing)


    def OnPing(self,res):
        self.console.appendPlainText(res)

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
