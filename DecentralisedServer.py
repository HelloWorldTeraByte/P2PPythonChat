import socket

userInfo = "[('awesomedude99', , '192.168.1.13', '12346', '12345'), ('yeahIdance','192.168.1.13', '12345', '12346'), , ('soWhatmate','192.168.1.13', '13456', '23456')]"

sockForClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
port = 45555               
sockForClient.bind((host, port))      

sockForClient.listen(5)

##while True:s
##   c, addr = sockForClient.accept()
##   for i in range(0, 4):
##      dataToSend = str(userInfo[i])
##      data +' "\n"
##      print("{} {}".format(i, dataToSend))
##      c.send(str.encode(dataToSend))
##   c.close()
   
while True:
   c, addr = sockForClient.accept()    
   #c.send(str.encode(str(len(userInfo))))
   dataToSend = userInfo
   dataToSend += "\n"
   #print("{}".format( dataToSend))
   c.send(str.encode(dataToSend))
   c.close()      
