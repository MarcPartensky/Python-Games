from myconnection import Server, getIP
import time
from mybody import Body

print(getIP())
IP = "172.16.0.39."

t0 = time.time()
duration = 10

PORT = 1237

s = Server(IP, PORT)

while time.time() - t0 < duration:
    s.update()
    print(s.requests)
    print(time.time() - t0)

del s
