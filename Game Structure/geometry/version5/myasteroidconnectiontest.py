from myasteroidgameclient import AsteroidClient
from myasteroidgameserver import AsteroidServer

IP = "172.16.0.39."
PORT = 1234

s = AsteroidServer(IP, PORT)
c = AsteroidClient(IP, PORT)

c.client.sendForSure(('events/mousemotion', (628, 125)))

s.update()
print(s.clients)
s.send(s.clients[-1], "test2")

c.client.receive()
print(s.queue)
print(c.client.queue)