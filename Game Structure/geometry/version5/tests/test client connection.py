from myconnection import Client, getIP

IP = "172.16.0.39."
#IP = "MacBook-Pro-de-Olivier.local"
PORT = 1237

c = Client(IP, PORT)
c.send("je fais un test")

del c
