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
    global bIsWindowOpen
    bShouldReadIncomingMessages = False
    peer.close()              
    peerRecv.close()
    bIsWindowOpen = False
    mainWindow.destroy()
    print("Exiting")
    sys.exit()

def incomingMessages():
    global bShouldReadIncomingMessages
    global message
    global bUpdateDisplayBox
    while(bShouldReadIncomingMessages):
        message = peerRecv.recv(1024)
        bUpdateDisplayBox = True

bShouldReadIncomingMessages = True
bUpdateDisplayBox = False
bIsWindowOpen = True
bListen = False
message = ''

while True:
    choice = input("Peer To Peer Chat \n\t(C)to connect \n\t(L)to listen\n")

    if(choice == "C" or choice == "c"):
        peerSendPort= 12345       
        peerRecvPort = 12346
        bListen = False
        break

    elif(choice == "L" or choice == 'l'):
        peerSendPort= 12346      
        peerRecvPort = 12345
        bListen = True
        break

mainWindow= Tk()
mainWindow.protocol("WM_DELETE_WINDOW", onClose)
entryFrame = Frame(mainWindow)
entryFrame.pack(side=BOTTOM)

messageDisplay = Text(mainWindow, height=30, width=40) 
messageDisplay.pack(expand=True, fill='both')

sendButton = Button(entryFrame, text ="Send", command = sendToPeerButton)
sendButton.pack(side=RIGHT)

inputEntryBox = Entry(entryFrame)
inputEntryBox.pack(side=LEFT, expand=True, fill='x')

peerIp = '192.168.1.11'
selfIp = '192.168.1.11'

peerSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSend.bind((selfIp, peerSendPort))     

peerRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if(bListen):
    print("Listening on port: ", peerSendPort)
    peerSend.listen(1)              
    peer, peerAddr = peerSend.accept()    
    print("Connected to ", peerAddr)
    peerRecv.connect((peerIp, peerRecvPort))
else:
    peerRecv.connect((peerIp, peerRecvPort))
    print("Connected to: ", peerIp)
    print("Waiting for reply .. \n")
    peerSend.listen(1)
    peer, peerAddr = peerSend.accept()

incomingMessagesThread = threading.Thread(target=incomingMessages)
incomingMessagesThread.start()

while bIsWindowOpen:
    mainWindow.update_idletasks()
    mainWindow.update()
    if(bUpdateDisplayBox):
        messageDisplay.insert(END, message)
        bUpdateDisplayBox = False
