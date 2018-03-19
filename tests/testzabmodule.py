import unittest
from unittest.mock import MagicMock
from zabcombain import zabmodule

class TestMethod(unittest.TestCase):
    """docstring for TestMethod."""
    # def __init__(self,args):
    #     super(TestMethod, self).__init__(args)

    def setupApi(self):
        self.api = MagicMock()
        self.api.script = MagicMock()
        self.scriptValue = 'result value'
        self.api.script.execute = MagicMock(return_value={'value':self.scriptValue})


    def setUp(self):
        self.setupApi()
        ###############################
        self.host = zabmodule.initHost()
        ##################################################
        self.lhost = 'localhost'
        self.iphost = '127.0.0.1'
        ##############   add TESTLIST1 ###################
        self.TESTLIST1 = ({'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'},
        {'hostid': '342','main': '1','type': '2','ip': '127.0.0.1'},
        {'hostid': '425','main': '1','type': '3','ip': '127.0.0.1'},
        {'hostid': '442','main': '1','type': '4','ip': '127.0.0.1'},
        {'hostid': '465','main': '0','type': '1','ip': '127.0.0.1'},
        {'hostid': '405','main': '0','type': '2','ip': '127.0.0.1'},
        {'hostid': '135','main': '0','type': '3','ip': '127.0.0.1'},
        {'hostid': '245','main': '0','type': '4','ip': '127.0.0.1'}
        )
        ##############   add TESTLIST2 ###################
        self.TESTLIST2 = ({'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'},
        {'hostid': '342','main': '1','type': '2','ip': '127.0.0.2'},
        {'hostid': '425','main': '1','type': '3','ip': '127.0.0.3'},
        {'hostid': '442','main': '1','type': '4','ip': '127.0.0.4'},
        {'hostid': '465','main': '0','type': '1','ip': '127.0.0.1'},
        {'hostid': '405','main': '0','type': '2','ip': '127.0.0.2'},
        {'hostid': '135','main': '0','type': '3','ip': '127.0.0.3'},
        {'hostid': '245','main': '0','type': '4','ip': '127.0.0.4'}
        )


    def testCheckingList(self):
        self.assertEqual(zabmodule.checkingList(self.TESTLIST1)[0], {'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'})
        res = [{'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'},
        {'hostid': '342','main': '1','type': '2','ip': '127.0.0.2'},
        {'hostid': '425','main': '1','type': '3','ip': '127.0.0.3'},
        {'hostid': '442','main': '1','type': '4','ip': '127.0.0.4'}]
        self.assertEqual(zabmodule.checkingList(self.TESTLIST2), res)

    def testChangeInterfaceList(self):
        self.assertEqual(zabmodule.changeInterfaceList(self.TESTLIST1), [{'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'}])

    @unittest.skip("skip ping from OS")
    def testPingFromOS(self):
        self.assertEqual(zabmodule.pingFromOS(None),b"ip is None")
        self.assertEqual(zabmodule.pingFromOS(""),b"ip is empty")
        l = len(zabmodule.pingFromOS(self.iphost).decode().splitlines())
        self.assertEqual(l,8)

    def testFromRemoteServerScript(self):
        res = zabmodule.runRemoteServerScript(None,self.host)
        self.assertEqual(res,'api is None')
        res = zabmodule.runRemoteServerScript(self.api,None)
        self.assertEqual(res,'host is None')
        res = zabmodule.runRemoteServerScript(self.api,self.host)
        self.assertEqual(self.host.get("pingresult"),[self.scriptValue.encode()])
        self.assertEqual(res,'ok')

    def setupForPingRuner(self):
        self.hosts = []
        interfaces = [
        {'hostid': '1','main': '1','type': '1','ip': '127.0.0.127'},
        {'hostid': '2','main': '0','type': '1','ip': '127.0.0.1'}
        ]
        for i in range(3):
            self.hosts.append(zabmodule.initHost())
        for i,item in enumerate(self.hosts):
            interfaces[0].update([("hostid",str(i))])
            interfaces[0].update([("interfaceid",str(i)+'1')])
            interfaces[1].update([("hostid",str(i))])
            interfaces[1].update([("interfaceid",str(i)+'2')])
            item.update([('interfaces',interfaces),('hostid',str(i)),('host','id-'+str(i))])



    def testFromPingRuner(self):
        self.setupForPingRuner()
        res = zabmodule.PingRuner(None,self.hosts)
        self.assertEqual(res,'api is None')
        res = zabmodule.PingRuner(self.api,None)
        self.assertEqual(res,'hosts is None')
        res = zabmodule.PingRuner(self.api,[])
        self.assertEqual(res,'hosts is empty')
        res = zabmodule.PingRuner(self.api,self.hosts)
        for item in self.hosts:
            res = item['pingresult']
            self.assertEqual(res[0],self.scriptValue.encode())
            l = len(res[1].splitlines())
            self.assertEqual(l,8)
