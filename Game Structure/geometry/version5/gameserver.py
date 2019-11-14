from myconnection import Server
from mygame import Asteroid

IP = "172.16.0.39."
PORT = 1237

class GameServer(Game,Server):
    """Create a multiplayer game."""
    def __init__(self, ip, port):
        """Create a game server using the ip and the port."""
        super().__init__(ip, port)
