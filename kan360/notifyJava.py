# -*- coding: utf-8 -*-
import socket
import time
from time import localtime

#notifyJava 函数， 和java进程进行通信。java进程接收到信号之后，开始建立lucene索引
def notifyJava():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 6670))
    s.send('10')
    buffer = []
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = ''.join(buffer)
    s.close()
    if data:
        print "the server said:"+data
    else:
        print "failt to receive the server data."
    print time.localtime(time.time())
    
    
#notifyJava()
