import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .zabmodule import *
from os import path, environ, name as osname
import configparser
from datetime import datetime


def get_login():
    name = ''
    if osname == "nt":
        name = environ['username']
    else:
        name = environ['LOGNAME']
    return name


class Page(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = self.parentWidget().parentWidget()
        self.settings = self.parentWidget().parentWidget().settings
        self.console = self.parentWidget().parentWidget().console

    def consoleLog(self, text):
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.console.appendPlainText(dt + ' ' + text)


class PageMain(Page):
    """
    docstring PageMain
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_field = QtWidgets.QLineEdit(self)
        self.login_field.setText(get_login())
        self.pass_field = QtWidgets.QLineEdit(self)
        self.pass_field.setEchoMode(2)
        self.loginButton = QtWidgets.QPushButton('login', self)
        self.loginButton.clicked.connect(self.OnPressLogin)
        self.settingButton = QtWidgets.QPushButton('settings', self)
        self.settingButton.clicked.connect(self.OnPressSetting)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout)
        self.vlayout.addWidget(self.login_field, Qt.AlignTop, Qt.AlignLeft)
        self.vlayout.addWidget(self.pass_field, Qt.AlignTop, Qt.AlignLeft)
        self.vlayout.addWidget(self.loginButton, Qt.AlignTop, Qt.AlignLeft)
        self.vlayout.addWidget(self.settingButton, Qt.AlignTop, Qt.AlignLeft)
        self.vlayout.addSpacing(100)

    def OnPressLogin(self):
        error, self.parent.api = getApi(self.settings.hostname, self.login_field.text(), self.pass_field.text())
        self.consoleLog(error)

    def OnPressSetting(self):
        text, ok = QtWidgets.QInputDialog.getMultiLineText(self, 'Settings', 'Write otions', self.settings.readValue)
        if ok:
            self.settings.saveSetting(str(text))
            self.settings.readSetting()


class WorkerOrder(QThread):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerOrder, self).__init__(parent)

    def setAPI(self, api):
        self.api = api

    def setHosts(self, hosts):
        self.hosts = hosts

    def getDataPing(self):
        initHostsFromServer(self.api, self.hosts)
        pingRuner(self.api, self.hosts)
        res = ''
        for host in self.hosts:
            res += '{:<9}:{}\n'.format('name', host.get('name'))
            res += '{:<9}:{}\n'.format('hostname', host.get('host'))
            if host.setdefault('issues', False):
                for issue in host.get('issues'):
                    res += '{:<9}:{}\n'.format('issue', issue.get('issue'))
                    res += '{:<9}:{}\n'.format('agetime', issue.get('agetime'))
            res += '\nZABBIX PING RESULT\n\n'
            res += host['pingresult']
            res += '\nINTERFACES PING RESULT\n\n'
            for item in host['interfaces']:
                res += item['res']
                res += '\n'
        return res

    def run(self):
        self.finished.emit(self.getDataPing())


class PageOrder(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Zabbix api - self.api
        self.api = None

        self.inputLabel = QtWidgets.QLabel('Input', self)
        self.inputField = QtWidgets.QPlainTextEdit(self)
        self.pasteButton = QtWidgets.QPushButton('Paste', self)
        self.proccButton = QtWidgets.QPushButton('Proccess', self)
        self.inputCheckBox = QtWidgets.QCheckBox('Contin.', self)
        self.glayuot = QtWidgets.QGridLayout()
        self.setLayout(self.glayuot)

        self.pasteButton.clicked.connect(self.OnPressPaste)
        self.proccButton.clicked.connect(self.OnPressProcess)
        # Output
        self.outputLabel = QtWidgets.QLabel('Output', self)
        self.outputField = QtWidgets.QPlainTextEdit(self)
        self.copyButton = QtWidgets.QPushButton('Copy', self)
        self.copyButton.clicked.connect(self.OnSelectCopy)

        self.glayuot.addWidget(self.inputLabel, 1, 1, 1, 1)
        self.glayuot.addWidget(self.inputField, 2, 1, 1, 1)

        self.vlayuot = QtWidgets.QVBoxLayout()
        self.vlayuot.addWidget(self.pasteButton)
        self.vlayuot.addWidget(self.proccButton)
        self.vlayuot.addWidget(self.inputCheckBox)

        self.glayuot.addLayout(self.vlayuot, 2, 2, Qt.AlignTop)
        self.glayuot.addWidget(self.outputLabel, 3, 1, 1, 1)
        self.glayuot.addWidget(self.outputField, 4, 1, 1, 1)
        self.glayuot.addWidget(self.copyButton, 4, 2, 1, 1, Qt.AlignTop)

    def OnPressPaste(self):
        if self.inputField.canPaste():
            if not self.inputCheckBox.checkState():
                self.inputField.clear()
            self.inputField.paste()
            self.inputField.appendPlainText('\n')
        else:
            self.consoleLog('Buffer is empty')

    def OnPressProcess(self):
        if not self.parent.api:
            self.consoleLog('no connection to server')
        else:
            try:
                if self.wo.isFinished():
                    self.process()
                else:
                    self.consoleLog('please wait')
            except AttributeError:
                self.process()

    def process(self):
        self.hosts = initHostsFromData(self.getItems())
        self.consoleLog('Order process')
        self.consoleLog('Hosts = %d' % len(self.hosts))
        for i, v in enumerate(self.hosts):
            self.consoleLog('%d %s' % (i + 1, v.get('name')))
        try:
            self.wo = WorkerOrder()
            self.wo.setAPI(self.parent.api)
            self.wo.setHosts(self.hosts)
            self.wo.start()
            self.wo.finished.connect(self.getWorkerResult)
        except Exception as er:
            print('error start Thread', er)

    def getWorkerResult(self, res):
        self.outputField.clear()
        self.outputField.appendPlainText(res)

    def OnSelectCopy(self):
        if self.outputField.toPlainText() == '':
            self.consoleLog('Output is empty')
        else:
            self.outputField.selectAll()
            self.outputField.copy()
            self.consoleLog('all text copied')

    def getItems(self):
        text = str(self.inputField.toPlainText())
        if text:
            for line in text.split('\n'):
                items = line.split('\t')
                if len(items) != 1:
                    yield items


class PagePing(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.glayuot = QtWidgets.QGridLayout()
        self.setLayout(self.glayuot)

        self.groupLb = QtWidgets.QLabel('Groups', self)
        self.selectGroup = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.selectGroup.setSizePolicy(sizePolicy)
        self.selectGroup.setMinimumWidth(200)
        self.selectGroup.setEnabled(False)
        self.selectGroup.currentIndexChanged.connect(self.OnSelectGroup)
        self.hostLb = QtWidgets.QLabel('Hosts', self)
        self.selectHost = QtWidgets.QComboBox(self)
        self.selectHost.setEnabled(False)
        self.selectHost.currentIndexChanged.connect(self.OnSelectHost)
        self.selectHost.setSizePolicy(sizePolicy)
        self.selectHost.setMinimumWidth(200)
        # update button
        self.updateBtn = QtWidgets.QPushButton('Update', self)
        self.updateBtn.clicked.connect(self.onPressUpdate)
        # ping button
        self.pingButton = QtWidgets.QPushButton('Ping', self)
        self.pingButton.setEnabled(False)
        self.pingButton.clicked.connect(self.OnPressPing)
        # output field
        self.outputLb = QtWidgets.QLabel('Output', self)
        self.outputField = QtWidgets.QPlainTextEdit(self)

        self.glayuot.addWidget(self.groupLb, 0, 0, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.selectGroup, 1, 0, 1, 2, Qt.AlignLeft)
        self.glayuot.addWidget(self.updateBtn, 1, 1, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.hostLb, 2, 0, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.selectHost, 3, 0, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.pingButton, 4, 0, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.outputLb, 5, 0, 1, 1, Qt.AlignLeft)
        self.glayuot.addWidget(self.outputField, 6, 0, 1, 5)

    def onPressUpdate(self):
        if not self.parent.api:
            self.consoleLog('no connection to server')
        else:
            self.groups = dict(self.getGroups())
            items = list(self.groups.keys())
            items.sort()
            self.selectGroup.addItems(items)
            self.selectGroup.setEnabled(True)

    def getGroups(self):
        for item in self.parent.api.hostgroup.get():
            yield item['name'], item['groupid']

    def getHosts(self, groupid=None):
        output = ['hostid', 'host', 'name', 'description', 'groups', 'interfaces']
        for item in self.parent.api.host.get(groupids=[groupid], filter={'status': '0'}, output=output,
                                             selectInterfaces='extend'):
            yield item['name'], item

    def OnSelectGroup(self, index):
        key = self.selectGroup.currentText()
        self.hosts = dict(self.getHosts(self.groups[key]))
        items = list(self.hosts.keys())
        items.sort()
        self.selectHost.clear()
        self.selectHost.addItems(items)
        self.selectHost.setEnabled(True)

    def OnSelectHost(self, index):
        self.pingButton.setEnabled(True)

    def OnPressPing(self):
        if not self.parent.api:
            self.consoleLog('no connection to server')
        else:
            try:
                if self.wo.isFinished():
                    self.process()
                else:
                    self.consoleLog('please wait')
            except AttributeError:
                self.process()

    def process(self):
        key = self.selectHost.currentText()
        host = initHost()
        host.update(self.hosts[key].items())
        self.consoleLog('Ping for ' + host.get('name'))
        try:
            self.wo = WorkerOrder()
            self.wo.setAPI(self.parent.api)
            self.wo.setHosts([host])
            self.wo.start()
            self.wo.finished.connect(self.getWorkerResult)
        except Exception as er:
            print('error start Thread', er)

    def getWorkerResult(self, res):
        self.outputField.clear()
        self.outputField.appendPlainText(res)


class Settings(object):
    def __init__(self):
        self.defaultValue = '[server]\nhost = http://127.0.0.1/zabbix\n'
        if osname == 'nt':
            self.home = path.join('c:\\', environ['HOMEPATH'])
        else:
            self.home = environ['HOME']
        self.here = path.join(self.home, '.zabcombain')
        self.hostname = None
        self.readSetting()

    def readSetting(self):
        if path.exists(self.here):
            with open(self.here, 'r') as f:
                self.readValue = f.read()
        else:
            self.readValue = self.defaultValue
            with open(self.here, 'w') as f:
                f.write(self.defaultValue)
        self.parse_setting()

    def saveSetting(self, value):
        if self.readValue != value:
            with open(self.here, 'w') as f:
                f.write(value)
            self.readValue = value

    def parse_setting(self):
        config = configparser.ConfigParser()
        config.read(self.here)
        self.hostname = config['server']['host']


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.api = None
        self.initUI()

    def initUI(self):
        self.width = 640
        self.height = 480
        self.resize(self.width, self.height)
        self.setMinimumSize(360, 400)
        QtWidgets.QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Zabcombain')

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.settings = Settings()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.console = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.console.setSizePolicy(sizePolicy)
        self.console.setMaximumHeight(150)

        self.panel = QtWidgets.QTabWidget(self.centralwidget)
        self.centralwidget.console = self.console

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.addWidget(self.panel)
        self.vlayout.addWidget(self.console)
        self.centralwidget.setLayout(self.vlayout)

        self.panel.addTab(PageMain(self.panel), 'Main')
        self.panel.addTab(PageOrder(self.panel), 'Oreders')
        self.panel.addTab(PagePing(self.panel), 'Ping')

        self.center()
        here = path.abspath(path.dirname(__file__))
        here = path.split(here)[0]
        icon_file = path.join(here, 'data', 'favicon.ico')
        icon = QIcon(path.abspath(icon_file))

        self.setWindowIcon(icon)
        self.setWindowTitle('Zabcombain')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    # Next, create an application object.
    QtWidgets.QApplication.setDesktopSettingsAware(False)
    app = QtWidgets.QApplication(sys.argv)
    # Show it.
    frame = MainWindow(None)
    # Start the event loop.
    sys.exit(app.exec_())
