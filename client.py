from tkinter import *
from tkinter import messagebox
import sys
import time
import threading
import socket  
import re


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
    
def connectButtonPressed():
    global peerRecvPort
    global peerSendPort
    global bListen
    global bShouldConnect
    global peerIp
    try:
        peerRecvPort = int(recvPortsInputBox.get())
        if(not (peerRecvPort > 1024 and peerRecvPort < 65536)):
            messagebox.showinfo("Error", "Invalid recieve port info!")
            peerRecvPort = 0
    except ValueError:
        peerRecvPort = 0
        messagebox.showinfo("Error", "Invalid recieve port info!")
        
    try:
        peerSendPort = int(sendPortsInputBox.get())
        if(not (peerSendPort > 1024 and peerSendPort < 65536)):
            messagebox.showinfo("Error", "Invalid send port info!")
            peerSendPort = 0        
    except ValueError:
        peerSendPort = 0
        messagebox.showinfo("Error", "Invalid send port info!")      
    if(not peerRecvPort == 0 and not peerSendPort == 0):
        if(bConnect.get() == 1):
            bListen = False
        else:
            bListen = True
        bShouldConnect = True
        connectionWindow.destroy()
        
def fillInDefaults():
    if(bConnect.get() == 1):
        sendPortsInputBox.delete(0, END)
        sendPortsInputBox.insert(END, "12345")
        recvPortsInputBox.delete(0, END)
        recvPortsInputBox.insert(END, "12346")
    else:
        sendPortsInputBox.delete(0, END)
        sendPortsInputBox.insert(END, "12346")
        recvPortsInputBox.delete(0, END)
        recvPortsInputBox.insert(END, "12345")    
        
def incomingMessages():
    global bShouldReadIncomingMessages
    global message
    global bUpdateDisplayBox
    global bPeerDisconnected
    while(bShouldReadIncomingMessages):
        message = peerRecv.recv(3072)
        bUpdateDisplayBox = True
        if(message.decode('utf-8') == "c10s3c0nn"):
            bPeerDisconnected = True
            
def ServerCheckboxChanged():
    if(isServer.get() == 1):
        sendPortsInputBox.config(state='disabled')
        recvPortsInputBox.config(state='disabled')
    else:
        sendPortsInputBox.config(state='normal')
        recvPortsInputBox.config(state='normal')        
bShouldReadIncomingMessages = True
bPeerDisconnected = True
bUpdateDisplayBox = False
bIsWindowOpen = True
bListen = False
message = ''
peerSendPort = 0
peerRecvPort = 0
bShouldConnect = False
peerIp = '192.168.1.13'
selfIp = '192.168.1.13'
users = [] 
userInfo = []

connectionWindow = Tk()
connectionWindow.resizable(width=False, height=False)
connectionWindow.geometry('{}x{}'.format(300, 120))
isServer = IntVar(0)
isServer.set(-1)
bConnect = IntVar(0)
bConnect.set(-1)

connectionInfoFrame = Frame(connectionWindow)
connectionInfoLabels = Frame(connectionInfoFrame)
connectionOptionsFrame = Frame(connectionWindow)
listenOrConnectFrame = Frame(connectionWindow)

listenOrConnectFrame.pack(side=BOTTOM)
connectionOptionsFrame.pack(side=RIGHT)
connectionInfoFrame.pack(side=LEFT)
connectionInfoLabels.pack(side=LEFT)


serverCheckBox = Checkbutton(connectionOptionsFrame, text = "Server", variable = isServer, onvalue = 1, offvalue = 0, command=ServerCheckboxChanged)
serverCheckBox.pack(side=TOP, anchor=W)
peerCheckBox = Checkbutton(connectionOptionsFrame, text = "Peer", variable = isServer, onvalue = 0, offvalue = 1, comman=ServerCheckboxChanged)
peerCheckBox.pack(side=TOP, anchor=W)

connectCheckBox = Checkbutton(listenOrConnectFrame, text = "Connect", variable = bConnect, onvalue=1, offvalue=0, command=fillInDefaults)
connectCheckBox.pack(side=LEFT)
recvCheckBox = Checkbutton(listenOrConnectFrame, text = "Receive", variable = bConnect, onvalue=0, offvalue=1, command=fillInDefaults)
recvCheckBox.pack(side=RIGHT)
recvCheckBox.select()

connectButton = Button(connectionOptionsFrame, text ="Connect", command = connectButtonPressed)
connectButton.pack(side=BOTTOM)

ipLabel = Label(connectionInfoLabels, text="IP: ")
ipLabel.pack(side=TOP)
sendPortLabel = Label(connectionInfoLabels, text="Send Port: ")
sendPortLabel.pack(side=BOTTOM)
recvPortLabel = Label(connectionInfoLabels, text="Receive Port: ")
recvPortLabel.pack(side=BOTTOM)

ipInputBox = Entry(connectionInfoFrame)
ipInputBox.pack(side=TOP, fill='x')
sendPortsInputBox = Entry(connectionInfoFrame, width=6)
sendPortsInputBox.pack(side=BOTTOM)
recvPortsInputBox = Entry(connectionInfoFrame, width=6)
recvPortsInputBox.pack(side=BOTTOM)

fillInDefaults()
connectionWindow.mainloop()

if(not bShouldConnect):
    print("Connection failed!")
    sys.exit()
    
if(isServer.get() == 1):   
    socketForServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
    host = socket.gethostname() 
    port = 45555                
        
    socketForServer.connect((host, port))
    
    buffer = socketForServer.recv(1024).decode('utf-8') 
    
    user = ""
    keepAdding = False
    bUserInfoCompleted = False
    
    for i in range(0,len(buffer)):
        if(buffer[i] == "("):
            keepAdding = True
        if(buffer[i] == ")"):
            keepAdding = False
            bUserInfoCompleted = True
        if(keepAdding):
            user += buffer[i+1]
            
        if(bUserInfoCompleted):
            user = user[:-1]
            users.append(user)
            user = ""
            keepAdding = False
            bUserInfoCompleted = False  
            
    for i in range(0, len(users)):
        strToProcess = users[i]
        userInfo.append([])        
        #print(strToProcess)
        for j in range(0, 3):
            userInfo[i].append(re.findall("\'(.*?)\'",strToProcess)[j])
    
    print(userInfo)
    peerSendPort = 12345
    peerRecvPort = 12346
        
    socketForServer.close()
    

    #choice = input("Peer To Peer Chat \n\t(C)to connect \n\t(L)to listen\n")

    #if(choice == "C" or choice == "c"):
        #peerSendPort= 12345       
        #peerRecvPort = 12346
        #bListen = False
        #break

    #elif(choice == "L" or choice == 'l'):
        #peerSendPort= 12346      
        #peerRecvPort = 12345
        #bListen = True
        #break
    


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
            messageDisplay.config(state=NORMAL)
            messageDisplay.insert(END, "\nDisconnected....", "errorTextStyle")
            messageDisplay.config(state=DISABLED) 
            bUpdateDisplayBox = False
            
        message = message.decode('utf-8')
        if(not message == "c10s3c0nn"):
            messageDisplay.config(state=NORMAL)
            messageDisplay.insert(END, message)
            messageDisplay.config(state=DISABLED)
            bUpdateDisplayBox = False
             
