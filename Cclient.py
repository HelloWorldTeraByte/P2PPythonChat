from tkinter import *
import threading
import socket              

peerIp = '192.168.1.11'
selfIp = '192.168.1.11'
peerSendPort= 12346       
peerRecvPort = 12345

peerSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSend.bind((selfIp, peerSendPort))     

peerRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peerRecv.connect((peerIp, peerRecvPort))
print("Connected to: ", peerIp)
print("Waiting for reply .. \n")
peerSend.listen(1)
peer, peerAddr = peerSend.accept()

while True:
    print(peerRecv.recv(1024))
    message = str(input(": "))
    peer.send(message.encode(encoding='utf_8'))

peerSend.close()              
peerRecv.close()
