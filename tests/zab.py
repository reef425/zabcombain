from zabmodule import *

hosts = []


for i in range(10):
    host = initHost()
    ifs = [{'ip':'127.0.0.1'},{'ip':'localhost'},{'ip':'192.168.56.101'}]
    host.update([("name",'twigl_'+str(i))])
    host.update([("ip",'localhost')])
    host.update([('interfaces',ifs)])
    hosts.append(host)
# pr = PingRuner_()
# pr.run(hosts)

pingresult = None

def do_end():
    print('task -- end')

def iface_work(item):
    res = pingFromOS(item['ip']).decode()
    item.update([('res',res)])

def host_work(item):
    print(item.get("name"))
    ifacesTasks = TaskRuner()
    ifacesTasks.items = item['interfaces']
    ifacesTasks.do_work = iface_work
    ifacesTasks.run()


runHosts = TaskRuner()
runHosts.items = hosts
runHosts.do_work = host_work
runHosts.do_end =do_end
runHosts.run()

for host in hosts:
    print(host['name'])
    for item in host['interfaces']:
        print(item['res'])
