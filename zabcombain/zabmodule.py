import time
from threading import Thread
from subprocess import Popen,PIPE
from os import name as osname
import queue



def initHost():
    return {'hostid': '',
            'host': '',
            'name': '',
            'description': '',
            'pingresult':'',
            'groups': [{'groupid': '', 'name': '', 'internal': '', 'flags': ''}],
            'interfaces': [{'interfaceid': '',
                            'hostid': '',
                            'main': '',
                            'type': '',
                            'useip': '',
                            'ip': '',
                            'dns': '',
                            'port': '',
                            'bulk': ''}]}

def initHostsFromData(data):
    hosts = []
    for line in data:
        i=0
        if hosts == []:
            host = initHost()
            host.update([("name",line[0]),("issues",[{"issue":line[1],"agetime":line[2]}])])
            hosts.append(host)
        else:
            for item in hosts:
                if item.get("name")==line[0]:
                    item.get("issues").append({"issue":line[1],"agetime":line[2]})
                    i+=1
            if i==0:
                host = initHost()
                host.update([("name",line[0]),("issues",[{"issue":line[1],"agetime":line[2]}])])
                hosts.append(host)
                i=0
    return hosts

def getApi(hostname,login=None,password=None):
        if not login:
             return "non login",None
        if not password:
             return "non password",None
        from pyzabbix import ZabbixAPI, ZabbixAPIException
        zapi = None
        try:
            zapi = ZabbixAPI(server = hostname)
        except Exception as e:
            return str(e),None
        try:
            zapi.login(login,password)
        except Exception as e:
            return str(e),None
        return "server connect",zapi

def initHostsFromServer(api,hosts):
    output=["hostid","host","name","description","groups","interfaces"]
    hostnames = []
    for host in hosts:
        hostnames.append(host.get("name"))
    for item in api.host.get(output=output,filter={"name":hostnames},selectInterfaces="extend",selectGroups="extend"):
        for host in hosts:
            if host.get("name")==item.get("name"):
                host.update(item.items())

def getItems(text):
    if text:
        for line in text.split("\n"):
            items = line.split("\t")
            if len(items)!=1:
                yield items


def runRemoteServerScript(api,host):
    if api is None:
        print('api is None')
    if host is None:
        print('host is None')
    result = None
    try:
        result = api.script.execute(hostid=host.get("hostid"),scriptid="1")
    except Exception as err:
        print(err)
    finally:
        if result is None:
            result = {'value':'get not data'}
    host.update([('pingresult',result.get('value'))])

def pingFromOS(ip):
    if ip is None:
        return b"ip is None"
    if ip=='':
        return b'ip is empty'
    if osname == "nt":
        pcArg=['ping','-n','3',ip]
    else:
        pcArg=['ping','-c','3',ip]
    proc = Popen(pcArg,stdout=PIPE)
    out = proc.stdout.readlines()
    res = b""
    for row in out:
        res+=row
    proc.stdout.close()
    return res

class TaskRuner():
    def __init__(self):
        self.tasks = queue.Queue()
        self.threads = []
        self.items = None

    def do_start(self):
        pass

    def do_work(self,*args, **kwargs):
        pass

    def do_end(self):
        pass

    def worker(self):
        while True:
            item = self.tasks.get()
            if item is None:
                break
            self.do_work(item)
            self.tasks.task_done()

    def run(self):
        self.do_start()
        for i in range(len(self.items)):
            t = Thread(target=self.worker)
            t.start()
            self.threads.append(t)

        for item in self.items:
            self.tasks.put(item)

        # block until all tasks are done
        self.tasks.join()

        # stop workers
        for i in range(len(self.items)):
            self.tasks.put(None)
        for t in self.threads:
            t.join()
        self.do_end()

def pingRuner(api,hosts):

    def iface_work(item):
        res = pingFromOS(item['ip'])
        if osname == "nt":
            res = res.decode("cp866")
        else:
            res = res.decode()
        item.update([('res',res)])

    def host_work(item):
        runRemoteServerScript(api,item)
        ifacesTasks = TaskRuner()
        ifacesTasks.items = item['interfaces']
        ifacesTasks.do_work = iface_work
        ifacesTasks.run()


    runHosts = TaskRuner()
    runHosts.items = hosts
    runHosts.do_work = host_work
    runHosts.run()
