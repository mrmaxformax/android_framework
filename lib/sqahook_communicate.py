import re as regx
import random
import websocket
from connection import *
from test_framework.soak import *

class SQAHookConnection(object):
    def __init__(self, p_ip):
        self.ip = p_ip
        self.port = '7681'
        self.url = 'ws://' + self.ip + ':' + self.port + '/devtool-protocol'

    def returnPrm(self, p_val):
        val = p_val
        if type(val) is not bool:
            if type(val) is dict:
                prm = val
            elif type(val) is int:
                prm = {'index': val}
            elif type(val) is (list and tuple):
                if len(val) == 2:
                    prm = {'key': val[1], 'value': val[0]}
                else:
                    prm = {'assetId': val[0], 'playFrom': val[1], 'channelId': val[2]}
            elif len(val) > 60:
                prm = {'assetId': val}
            elif regx.match(r'^[\d{1,}|[a-z]+\d+\w+', val):
                prm = {'channelId': val}
            else:
                prm = {'key': val}
        else:
            if val is False:
                prm = {'SendBacklog': False}
            elif val is True:
                prm = {'SendBacklog': True}
        return prm

    def run(self, cmd=None, prm=None):
        if prm is None:
            prm = ''
        rprm = self.returnPrm(prm)
        try:
            time.sleep(1)
            ws = websocket.create_connection(self.url, timeout=60)
        except Exception, e:
            error = ['WEB SERVICE TIMED OUT Socket Connection Issue', self.ip]
            print 'WEB SERVICE TIMED OUT Connection Time Out Device:  ' + self.ip
            get_screenshot(self.ip)
            sys.exit(0)
        try:
            indexID = random.randint(0, 100)
            url_dict = {'params': rprm, 'id': indexID, 'command': cmd}
            send = json.dumps(url_dict)
            ws.send(send)
            returnVal = ws.recv()
        except Exception, e:
            error = ['WEB SERVICE TIMED OUT Socket Connection Issue', self.ip]
            print 'WEB SERVICE CONNECTION FAILED ' + e.message
            get_screenshot(self.ip)
            sys.exit(0)
        try:
            ws.close()
        except Exception, e:
            print 'Web Service was not closed ' + e.message
        return returnVal