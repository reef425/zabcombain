import time
from threading import Thread
from subprocess import Popen,PIPE
from os import name as osname



def initHost():
    return {'hostid': '',
            'host': '',
            'name': '',
            'description': '',
            'pingresult':[],
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

def getScript(api,host,count):
    runRemoteServerScript(api,host)
    count.append(0)

def runRemoteServerScript(api,host):
    result = None
    try:
        result = api.script.execute(hostid=host.get("hostid"),scriptid="1")
    except Exception as err:
        print(err)
    host.get("pingresult").append(result.get("value").encode())

def pingFromOS(ip):
    if osname == "nt":
        pcArg=['ping','-n','3',ip]
    else:
        pcArg=['ping','-c','3',ip]
    proc = Popen(pcArg,stdout=PIPE)
    out = proc.stdout.readlines()
    res = b""
    for row in out:
        res+=row
    return res

def pingFromIface(api,host,ip,count):
    res = pingFromOS(ip)
    if osname == "nt":
        res = res.decode("cp866")
    else:
        res = res.decode()
    host.get("pingresult").append(res)
    count.append(0)

def sortByType(iface):
    return iface['type']



def checkingList(interfaces):
    result = []
    result.append(interfaces[0])
    flag = 1
    for iface in interfaces:
        for res in result:
            if iface['ip']==res['ip']:
                    flag =0
        if flag:
            result.append(iface)
        flag = 1
    return result

def changeInterfaceList(interfaces):
    mainifaces = []
    result = []
    for iface in interfaces:
        if iface['main']=='1':
            iface['main']=='0'
            mainifaces.append(iface)
        else:
            result.append(iface)
    if len(mainifaces)>0:
        mainifaces.sort(key= sortByType)
    mainifaces[0]['main'] = '1'
    return checkingList(mainifaces + result)

def PingRuner(api,hosts):
    count =[]
    ifaceCount = 0
    hostCount=0
    for host in hosts:
        hostCount+=1
        if hostCount==15:
            hostCount=0
            time.sleep(20)
        host.update([("interfaces",changeInterfaceList(host.get("interfaces")))])
        ifaceCount = ifaceCount + len(host.get("interfaces"))
        try:
            t = Thread(target=getScript,args=[api,host,count],name=host.get("hostid"))
            t.start()
        except Exception as er:
            print("error start Thread",er)
        if len(host.get("interfaces"))>1:
            for iface in host.get("interfaces"):
                if iface["main"]=="0":
                    try:
                        t = Thread(target=pingFromIface,args=[api,host,iface["ip"],count],name=iface["interfaceid"])
                        t.start()
                    except Exception as er:
                        print("error start Thread")
                time.sleep(1)
        time.sleep(2)
    while True:
        if ifaceCount==len(count):
            break
