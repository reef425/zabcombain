import unittest
from zabcombain import zabmodule

class TestMethod(unittest.TestCase):
    """docstring for TestMethod."""
    def __init__(self, args):
        super(TestMethod, self).__init__( args)
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
        pass

    def test_checkingList_1(self):
        self.assertEqual(zabmodule.checkingList(self.TESTLIST1)[0], {'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'})

    def test_checkingList_2(self):
        res = [{'hostid': '3425','main': '1','type': '1','ip': '127.0.0.1'},
        {'hostid': '342','main': '1','type': '2','ip': '127.0.0.2'},
        {'hostid': '425','main': '1','type': '3','ip': '127.0.0.3'},
        {'hostid': '442','main': '1','type': '4','ip': '127.0.0.4'},
        ]
        self.assertEqual(zabmodule.checkingList(self.TESTLIST2), res)
