from tkinter import *
import threading
import socket              

def updateWindow(window):
    window.update_idletasks()
    window.update()

def sendToPeerButton():
    pass

def onClose():
    peer.close()              
    peerRecv.close()
    mainWindow.destroy()

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

#mainWindow.mainloop()

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
    updateWindow(mainWindow)


