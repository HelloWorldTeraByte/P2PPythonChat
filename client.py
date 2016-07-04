from tkinter import *
import sys
import time
import threading
import socket              

def sendToPeerButton():
    message = inputEntryBox.get()
    if(not message == ''):
        inputEntryBox.delete(0, END)
        message += "\n"
        peer.send(str.encode(message))
        messageDisplay.config(state=NORMAL)
        messageDisplay.insert(END, message, "sendTextStyle")
        messageDisplay.config(state=DISABLED)
    
def onEnterButtonPressed(event):
    if(not inputEntryBox.get == ''):
        sendToPeerButton()
        
def onClose():
    global bShouldReadIncomingMessages
    global bIsWindowOpen
    global bUpdateDisplayBox
    peer.send(str.encode("c10s3c0nn"))
    bUpdateDisplayBox = False
    bShouldReadIncomingMessages = False
    bIsWindowOpen = False
    mainWindow.destroy()
    print("Exiting")

def incomingMessages():
    global bShouldReadIncomingMessages
    global message
    global bUpdateDisplayBox
    global bPeerDisconnected
    while(bShouldReadIncomingMessages):
        message = peerRecv.recv(1024)
        bUpdateDisplayBox = True
        if(message.decode('utf-8') == "c10s3c0nn"):
            bPeerDisconnected = True

bShouldReadIncomingMessages = True
bPeerDisconnected = True
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
mainWindow.bind('<Return>', onEnterButtonPressed)
entryFrame = Frame(mainWindow)
entryFrame.pack(side=BOTTOM, fill='x')

messageDisplay = Text(mainWindow, height=30, width=40) 
messageDisplay.pack(expand=True, fill='both')
messageDisplay.tag_configure("sendTextStyle", foreground="green", justify='right')
messageDisplay.tag_configure("errorTextStyle", foreground="red", justify='center')
messageDisplay.config(state=DISABLED)

sendButton = Button(entryFrame, text ="Send", command = sendToPeerButton)
sendButton.pack(side=RIGHT)

inputEntryBox = Entry(entryFrame)
inputEntryBox.pack(side=LEFT, expand=True, fill='x')

peerIp = '192.168.1.13'
selfIp = '192.168.1.13'

peerSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    peerSend.bind((selfIp, peerSendPort))
except socket.error as e:
    print(str(e))

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
    
bPeerDisconnected = False

incomingMessagesThread = threading.Thread(target=incomingMessages)
incomingMessagesThread.start()

while bIsWindowOpen:
    mainWindow.update_idletasks()
    mainWindow.update()
        
    if(bUpdateDisplayBox):
        if(bPeerDisconnected):
            #messageDisplay.config(state=NORMAL)
            messageDisplay.insert(END, "\nDisconnected....", "errorTextStyle")
            #messageDisplay.config(state=DISABLED) 
            bUpdateDisplayBox = False
            
        message = message.decode('utf-8')
        if(not message == "c10s3c0nn"):
            messageDisplay.config(state=NORMAL)
            messageDisplay.insert(END, message)
            messageDisplay.config(state=DISABLED)
            bUpdateDisplayBox = False
             
