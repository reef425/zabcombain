import time
from threading import Thread
from subprocess import Popen,PIPE
from os import name as osname



def initHost():
    return {'hostid': '',
            'host': '',
            'name': '',
            'description': '',
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
             return "Non login",None
        if not password:
             return "Non password",None
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
        return "Server connect",zapi

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

def getScript(api,host,count):
    if host.setdefault("pingresult",True):
        host.update([("pingresult",[])])
    result = ""
    try:
         result= api.script.execute(hostid=host.get("hostid"),scriptid="1")
    except Exception as err:
        print(err)
    # print("res ",result)
    host.get("pingresult").append(result.get("value").encode())
    count.append(0)

def pingOS(api,host,count):
    if host.setdefault("pingresult",True):
        host.update([("pingresult",[])])
    pcArg="-n 3"
    for iface in host.get("interfaces"):
        if iface.get("main")=="0":
            proc = Popen("ping %s %s"%(pcArg,iface.get("ip")),shell=True,stdout=PIPE)
            out = proc.stdout.readlines()
            res = b""
            for row in out:
                res+=row
            if osname == "nt":
                host.get("pingresult").append(res.decode("cp866"))
            else:
                host.get("pingresult").append(res.decode())
    count.append(0)

def PingRuner(api,hosts):
    # print("Start ping")
    count =[]
    ifaceCount = 0
    hostCount=0
    for host in hosts:
        hostCount+=1
        if hostCount==15:
            hostCount=0
            # print("Many requests, 20 second timeout")
            time.sleep(20)
        ifaceCount+=len(host.get("interfaces"))
        try:
            t = Thread(target=getScript,args=[api,host,count],name=host.get("hostid"))
            t.start()
        except Exception as er:
            print("error start Thread",er)
        if len(host.get("interfaces"))>1:
            for iface in host.get("interfaces"):
                try:
                    t = Thread(target=pingOS,args=[api,host,count],name=host.get("hostid")+"-os")
                    t.start()
                except Exception as er:
                    print("error start Thread")
        time.sleep(1)
    while True:
        if ifaceCount==len(count):
            break
    # print("End work ping runner!")
