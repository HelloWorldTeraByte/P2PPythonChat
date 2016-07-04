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
        #peer.send(message.encode(encoding='utf_8'))
        peer.send(str.encode(message))
        messageDisplay.config(state=NORMAL)
        messageDisplay.insert(END, message, "sendTextStyle")
        messageDisplay.config(state=DISABLED)
        
def closeConnections():
    peer.send(str.encode("0"))
    peer.close()              
    peerRecv.close()
    
def onEnterButtonPressed(event):
    if(not inputEntryBox.get == ''):
        sendToPeerButton()
        
def onClose():
    global bShouldReadIncomingMessages
    global bIsWindowOpen
    global bUpdateDisplayBox
    bUpdateDisplayBox = False
    bShouldReadIncomingMessages = False
    closeConnections()
    bIsWindowOpen = False
    mainWindow.destroy()
    print("Exiting")
    #sys.exit()

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
mainWindow.bind('<Return>', onEnterButtonPressed)
entryFrame = Frame(mainWindow)
entryFrame.pack(side=BOTTOM, fill='x')

messageDisplay = Text(mainWindow, height=30, width=40) 
messageDisplay.pack(expand=True, fill='both')
messageDisplay.tag_configure("sendTextStyle", foreground="green", justify='right')
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

incomingMessagesThread = threading.Thread(target=incomingMessages)
incomingMessagesThread.start()

while bIsWindowOpen:
    mainWindow.update_idletasks()
    mainWindow.update()
    if(bUpdateDisplayBox):
        message = message.decode('utf-8')
        messageDisplay.config(state=NORMAL)
        messageDisplay.insert(END, message)
        messageDisplay.config(state=DISABLED)
        bUpdateDisplayBox = False
