import unittest
from zabcombain import zabmodule

class TestMethod(unittest.TestCase):
    """docstring for TestMethod."""
    def __init__(self):
        super(TestMethod, self).__init__()

    def setUp(self):
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
        {'hostid': '442','main': '1','type': '4','ip': '127.0.0.4'},
        ]
        self.assertEqual(zabmodule.checkingList(self.TESTLIST2), res)
        self.assertEqual(zabmodule.changeInterfaceList(self.TESTLIST1), [{'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'}])

    def testPingFromOS(self):
        l = len(zabmodule.pingFromOS(None).decode().splitlines())
        self.assertEqual(l,0)
        l = len(zabmodule.pingFromOS(self.iphost).decode().splitlines())
        self.assertEqual(l,8)
