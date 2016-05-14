from tkinter import *
import threading
import socket              

peerIp = '192.168.1.11'
selfIp = '192.168.1.11'
peerSendPort= 12345       
peerRecvPort = 12346

peerSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSend.bind((selfIp, peerSendPort))     

peerRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Listening on port: ", peerSendPort)
peerSend.listen(1)              
peer, peerAddr = peerSend.accept()    
print("Connected to ", peerAddr)
peerRecv.connect((peerIp, peerRecvPort))

while True:
    message = str(input(": "))
    if(message == "q"):
        break
    peer.send(message.encode(encoding='utf_8'))
    print(peerRecv.recv(1024))

peerSend.close()              
peerRecv.close()
