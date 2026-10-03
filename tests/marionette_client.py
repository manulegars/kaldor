import json
import socket
import time

class Marionette:
    def __init__(self):
        self.s=socket.create_connection(('127.0.0.1',2828));self.i=0;self.receive()
    def receive(self):
        length=b''
        while not length.endswith(b':'): length+=self.s.recv(1)
        body=b''
        while len(body)<int(length[:-1]): body+=self.s.recv(int(length[:-1])-len(body))
        return json.loads(body)
    def command(self,name,args=None):
        self.i+=1;data=json.dumps([0,self.i,name,args or {}]).encode();self.s.sendall(str(len(data)).encode()+b':'+data)
        result=self.receive()
        if result[2]:raise RuntimeError(result[2])
        return result[3]
    def js(self,script):return self.command('WebDriver:ExecuteScript',{'script':script,'args':[],'newSandbox':False})['value']
    def wait(self,condition,timeout=12):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            if self.js('return '+condition):return
            time.sleep(.08)
        raise AssertionError('Délai dépassé : '+condition)
