from wx import Window,Notebook,Panel,StaticText,TextCtrl,Button,Frame,App,BoxSizer,CheckBox,Icon,ComboBox
from wx import EVT_BUTTON,TE_MULTILINE,TE_READONLY,TE_PASSWORD,EXPAND, BITMAP_TYPE_ICO, EVT_COMBOBOX
from zabcombain.zabmodule import getApi,PingRuner,initHost, initHostsFromData, initHostsFromServer
from threading import Thread
from os import getlogin,getcwd,path,environ,name as osname
import configparser

class PageMain(Panel):
    def __init__(self, parent):
        Panel.__init__(self, parent)
        self.loginfield = TextCtrl(self, size =(100,25), pos =(10,10))
        self.passfield = TextCtrl(self, value="", size = (100,25), style = TE_PASSWORD, pos =(10,40))
        self.loginfield.SetValue(getlogin())
        self.passfield.SetValue("")
        self.loginButton = Button(self, size =(100,25), label="login", pos =(10,70))
        self.versionButton = Button(self, size =(100,25), label="version",  pos =(10,100))
        self.settingButton = Button(self, size =(100,25), label="setting",  pos =(10,130))
        self.logfield = parent.GetParent().GetParent().logfield
        self.api = None
        self.Bind(EVT_BUTTON, self.OnPressLogin, self.loginButton)
        self.Bind(EVT_BUTTON, self.OnPressGetVersion, self.versionButton)
        self.Bind(EVT_BUTTON, self.OnPressSetting, self.settingButton)

    def OnPressLogin(self,event):
        self.GetParent().GetParent().GetParent().settings.parseSetting()
        hostname = self.GetParent().GetParent().GetParent().settings.hostname
        error,self.api = getApi(hostname, self.loginfield.GetValue(),self.passfield.GetValue())
        self.GetParent().GetParent().GetParent().api = self.api
        self.logfield.SetInsertionPointEnd()
        self.logfield.WriteText(error+"\n")

    def OnPressSetting(self,event):
        win = SettingWindow(self)

    def OnPressGetVersion(self,event):
        if self.api:
            version = self.api.apiinfo.version([])
            self.logfield.SetInsertionPointEnd()
            self.logfield.WriteText("Server v. "+version+"\n")
        else:
            self.logfield.SetInsertionPointEnd()
            self.logfield.WriteText("Не подключены к серверу"+"\n")

class PageOrder(Panel):
    def __init__(self, parent):
        Panel.__init__(self, parent)
        w,h = self.GetParent().GetSize()
        #  self.logfield вывод логов
        self.logfield = parent.GetParent().GetParent().logfield
        # Zabbix api - self.api
        self.api = None
        # self.flags - флаг завершения фонового процесса self.process
        self.flags = [False]
        # Описание Input рабочей области
        self.inputLabel = StaticText(self,label="Input", pos =(5,5))
        self.inputfield = TextCtrl(self,value="", size = (w-80,160), pos =(5,25),style=TE_MULTILINE)
        self.pasteButton = Button(self, size =(60,25), label="Paste", pos =(w-70,25))
        self.proccButton = Button(self, size =(60,25), label="Proccess", pos =(w-70,55))
        self.inputCheckBox = CheckBox(self,label="Contin.",pos=(w-70,85))
        self.Bind(EVT_BUTTON, self.OnPressPaste, self.pasteButton)
        self.Bind(EVT_BUTTON, self.OnPressProcess, self.proccButton)
        # Описание Output рабочей области
        self.outputLabel = StaticText(self,label="Output", pos =(5,210))
        self.outputfield = TextCtrl(self,value="", size = (w-80,160), pos =(5,230),style=TE_MULTILINE)
        self.copyButton = Button(self, size =(60,25), label="Copy", pos =(w-70,230))
        self.outputCheckBox = CheckBox(self,label="Contin.",pos=(w-70,260))
        self.Bind(EVT_BUTTON, self.OnSelectCopy, self.copyButton)

    def setDataRun(self):
        initHostsFromServer(self.api,self.hosts)
        PingRuner(self.api,self.hosts)
        if not self.outputCheckBox.IsChecked():
            self.outputfield.Clear()
        for host in self.hosts:
            res="{:<9}:{}\n".format("name",host.get("name"))
            res+="{:<9}:{}\n".format("hostname",host.get("host"))
            for issue in host.get("issues"):
                res+="{:<9}:{}\n".format("issue",issue.get("issue"))
                res+="{:<9}:{}\n".format("agetime",issue.get("agetime"))
            self.outputfield.AppendText(res)
            for item in host.get("pingresult"):
                self.outputfield.WriteText(item)
            self.outputfield.AppendText("\n")
        self.flags[0] = False

    def OnPressProcess(self,event):
        self.api = self.GetParent().GetParent().GetParent().api
        if not self.api:
            self.logfield.AppendText("Не подключены к серверу\n")
        else:
            if self.flags[0]:
                self.logfield.AppendText("Подождите идет получение данных\n")
            else:
                self.hosts = initHostsFromData(self.getItems())
                self.logfield.SetInsertionPointEnd()
                self.logfield.WriteText("Hosts = %d\n"%len(self.hosts))
                for i,v in enumerate(self.hosts):
                    self.logfield.WriteText("%d %s\n"%(i+1,v.get("name")))
                self.flags[0] = True
                try:
                    t = Thread(target=self.setDataRun,args="",name="Set data")
                    t.start()
                except Exception as er:
                    print("error start Thread",er)


    def OnPressPaste(self,event):
            if self.inputfield.CanPaste():
                if not self.inputCheckBox.IsChecked():
                    self.inputfield.Clear()
                self.inputfield.Paste()
                self.inputfield.AppendText("\n")
            else:
                self.logfield.AppendText("Буфер обмена пуст\n")

    def OnSelectCopy(self,event):
            if self.outputfield.IsEmpty():
                self.logfield.AppendText("Output пустой\n")
            else:
                if self.outputfield.CanCopy():
                    self.outputfield.Copy()
                    self.logfield.AppendText("Выделенный текст скопирован\n")
                else:
                    self.outputfield.SelectAll()
                    self.outputfield.Copy()
                    self.logfield.AppendText("Весь текст скопирован\n")
                self.outputfield.SelectNone()

    def getItems(self):
        text = self.inputfield.GetValue()
        if text:
            for line in text.split("\n"):
                items = line.split("\t")
                if len(items)!=1:
                    yield items


class PagePing(Panel):
    """docstring forPagePing"""
    def __init__(self, parent):
        Panel.__init__(self, parent)
        w,h = self.GetParent().GetSize()
        #  self.logfield вывод логов
        self.logfield = parent.GetParent().GetParent().logfield
        # Zabbix api - self.api
        self.api = None
        # self.flags - флаг завершения фонового процесса self.process
        self.flags = [False]
        items =["item %d"%(x+1) for x in range(10)]
        self.groupLabel = StaticText(self,label="Groups",pos=(5,5))
        self.selectGroup = ComboBox(self,choices = items,size=(200,25),pos=(5,25))
        self.selectGroup.Disable()
        self.Bind(EVT_COMBOBOX, self.OnSelectGroup,self.selectGroup)
        self.hostLabel = StaticText(self,label="Hosts",pos=(5,55))
        self.selectHost = ComboBox(self,size=(200,25),pos=(5,75))
        self.selectHost.Disable()
        self.Bind(EVT_COMBOBOX, self.OnSelectHost,self.selectHost)
        self.updateButton = Button(self,label="Update",size=(100,25),pos=(210,25))
        self.Bind(EVT_BUTTON, self.OnUpdate, self.updateButton)
        self.pingButton = Button(self,label="Ping",size=(100,25),pos=(5,100))
        self.pingButton.Disable()
        self.Bind(EVT_BUTTON, self.OnPing, self.pingButton)
        self.outputLabel = StaticText(self,label="Output", pos =(5,210))
        self.outputfield = TextCtrl(self,value="", size = (w-80,160), pos =(5,230),style=TE_MULTILINE)
        self.outputfield.Disable()

    def OnUpdate(self,event):
        self.api = self.GetParent().GetParent().GetParent().api
        if not self.api:
            self.logfield.AppendText("Не подключены к серверу\n")
        else:
            self.groups = dict(self.getGroups())
            items = list(self.groups.keys())
            items.sort()
            self.selectGroup.SetItems(items)
            self.selectGroup.Enable()

    def OnSelectGroup(self,event):
        key = self.selectGroup.GetStringSelection()
        self.hosts = dict(self.getHosts(self.groups[key]))
        items = list(self.hosts.keys())
        items.sort()
        self.selectHost.SetItems(items)
        self.selectHost.Enable()

    def OnSelectHost(self,event):
        self.pingButton.Enable()

    def OnPing(self,event):
        if not self.api:
            self.logfield.AppendText("Не подключены к серверу\n")
        else:
            if not self.flags[0]:
                self.flags[0] = True
                try:
                    t = Thread(target=self.worker,args="",name="Set data")
                    t.start()
                except Exception as er:
                    print("error start Thread",er)
            else:
                self.logfield.AppendText("Пождите идет получение данных\n")

    def worker(self):
        key = self.selectHost.GetStringSelection()
        host = initHost()
        host.update(self.hosts[key].items())
        PingRuner(self.api,[host])
        self.outputfield.Enable()
        self.outputfield.Clear()
        res="{:<9}:{}\n".format("name",host.get("name"))
        res+="{:<9}:{}\n".format("hostname",host.get("host"))
        self.outputfield.AppendText(res)
        for item in host.get("pingresult"):
            self.outputfield.WriteText(item)
        self.flags[0] = False

    def getGroups(self):
        for item in self.api.hostgroup.get():
            print(item)
            yield item["name"],item["groupid"]

    def getHosts(self, groupid = None):
        output=["hostid","host","name","description","groups","interfaces"]
        for item in self.api.host.get(groupids=[groupid],filter={"status":"0"},output=output,selectInterfaces="extend"):
            yield item["name"],item

class Settings():
    def __init__(self):
        self.defaultValue = "[server]\nhost = 127.0.0.1/zabbix\n"
        if osname == "nt":
            self.home = environ["HOMEPATH"]
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
        # self.textField.SetValue(self.readValue)

    def saveSetting(self,value):
        if self.readValue != value:
            with open(self.here,"w") as f:
                f.write(value)
            self.readValue = value

    def parseSetting(self):
        config = configparser.ConfigParser()
        config.read(self.here)
        self.hostname = config["server"]["host"]

class SettingWindow(Frame):
    """docstring for SettingWindow."""
    def __init__(self, parent):
        width = 300
        height = 300
        Frame.__init__(self,parent,title= "Settings",size=(width, height))
        # super(SettingWindow, self).__init__(parrent)
        self.textField = TextCtrl(self,pos = (5,5),size=(width-20,height-80),style=TE_MULTILINE)
        self.buttonOk= Button(self,label = "Ok",pos = (5,height-60),size=(80,25) )
        self.buttonCancel = Button(self,label = "Cancel",pos = (90,height-60), size=(80,25))
        self.Bind(EVT_BUTTON, self.OnOK, self.buttonOk)
        self.Bind(EVT_BUTTON, self.OnCANCEL, self.buttonCancel)
        self.settings = self.GetParent().GetParent().GetParent().GetParent().settings
        self.textField.SetValue(self.settings.readValue)
        self.Show()
        # self.logfield = self.GetParent.logfield()

    def OnOK(self,event):
        value = self.textField.GetValue()
        self.settings.saveSetting(value)
        self.Close()

    def OnCANCEL(self,event):
        self.Close()

class MainWindow(Frame):
    def __init__(self, parent, title):
        self.width = 600
        self.height = 600
        Frame.__init__(self, parent, title=title, size=(self.width, self.height))
        here = path.abspath(path.dirname(__file__))
        here = path.split(here)[0]
        icon_file = path.join(here,"data","favicon.ico")
        self.SetIcon(Icon(path.abspath(icon_file),BITMAP_TYPE_ICO))
        self.api = None
        self.settings = Settings()
        self.logfield = TextCtrl(self, size =(self.width-30,100),style=TE_MULTILINE+TE_READONLY, pos =(5,450))
        self.panel = Panel(self,size = (self.width-30,440),pos=(5,5))
        self.notebook = Notebook(self.panel,size = (self.width-30,440))
        self.main = PageMain(self.notebook)
        self.order = PageOrder(self.notebook)
        self.ping = PagePing(self.notebook)
        self.notebook.AddPage(self.main, "Main")
        self.notebook.AddPage(self.order, "Order")
        self.notebook.AddPage(self.ping, "Ping")
        self.Show()


if __name__ == '__main__':
    # Next, create an application object.
    app = App()
    # Show it.
    frame = MainWindow(None, "ZabCombain")
    # Start the event loop.
    app.MainLoop()
