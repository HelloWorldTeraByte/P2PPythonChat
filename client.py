from tkinter import *
import sys
import time
import threading
import socket              

def sendToPeerButton():
    global inputEntryBox
    message = inputEntryBox.get()
    peer.send(message.encode(encoding='utf_8'))

def onClose():
    global bShouldReadIncomingMessages
    bShouldReadIncomingMessages = False
    peer.close()              
    peerRecv.close()
    mainWindow.destroy()
    sys.exit()

def incomingMessages():
    global bShouldReadIncomingMessages
    global messageDisplay
    while(bShouldReadIncomingMessages):
        peersMessage = peerRecv.recv(1024)
        messageDisplay.insert(END, peersMessage)

bShouldReadIncomingMessages = True

mainWindow= Tk()
mainWindow.protocol("WM_DELETE_WINDOW", onClose)
entryFrame = Frame(mainWindow)
entryFrame.pack(side=BOTTOM)

messageDisplay = Text(mainWindow, height=30, width=40) 
messageDisplay.pack(expand=True, fill='both')

sendButton = Button(entryFrame, text ="Send", command = sendToPeerButton)
sendButton.pack(side=RIGHT)

inputEntryBox = Entry(entryFrame)
inputEntryBox.pack(expand=True, fill='x')

if(len(sys.argv) == 2):
    if(sys.argv[1] == 'l' or sys.argv[1] == 'L'):
        peerSendPort= 12345       
        peerRecvPort = 12346
    elif(sys.argv[1] == 'c' or sys.argv[1] == 'C'):
        peerSendPort= 12346      
        peerRecvPort = 12345
    else:
        print("Pass in \n\t(C)to connect \n\t(L)to listen")
        sys.exit()
else:
    print("Pass in \n\t(C)to connect \n\t(L)to listen")
    sys.exit()

peerIp = '192.168.1.11'
selfIp = '192.168.1.11'

peerSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSend.bind((selfIp, peerSendPort))     

peerRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if(len(sys.argv) == 2):
    if(sys.argv[1] == 'l' or sys.argv[1] == 'L'):
        print("Listening on port: ", peerSendPort)
        peerSend.listen(1)              
        peer, peerAddr = peerSend.accept()    
        print("Connected to ", peerAddr)
        peerRecv.connect((peerIp, peerRecvPort))
    elif(sys.argv[1] == 'c' or sys.argv[1] == 'C'):
        peerRecv.connect((peerIp, peerRecvPort))
        print("Connected to: ", peerIp)
        print("Waiting for reply .. \n")
        peerSend.listen(1)
        peer, peerAddr = peerSend.accept()
    else:
        print("Pass in \n\t(C)to connect \n\t(L)to listen")
        sys.exit()
else:
    print("Pass in \n\t(C)to connect \n\t(L)to listen")
    sys.exit()

incomingMessagesThread = threading.Thread(target=incomingMessages)
incomingMessagesThread.start()

mainWindow.mainloop()
