from collections import deque
import socket
import select
import pickle

def getIP():
    return socket.gethostname()

IP = getIP()
PORT = 1235

class Server:
    """Create a socket server that can receive requests and send results
    with socket."""

    def __init__(self, ip, port, max_sockets=10):
        # We don't want people to access our ip, and we suppose the ip constant.
        self._ip = ip
        self._port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self._ip, self._port))
        self.connection.listen(max_sockets)
        self.clients = [self.connection]
        self.data = None
        self.message = None
        self.requests = deque([])
        self.open = True

    def main(self):
        while self.open:
            self.update()

    def update(self):
        read_clients, write_clients, exception_clients = select.select(self.clients, self.clients, self.clients)
        self.readEach(read_clients)
        self.writeEach(write_clients, self.message)
        self.checkEach(exception_clients)

    def readEach(self, clients):
        """Read the request of the clients."""
        for client in clients:
            if client == self.connection:
                self.accept(client)
            else:
                self.read(client)

    def writeEach(self, clients, message):
        """Write to each client."""
        if message is not None:
            for client in clients:
                self.write(client, message)
            self.message = None


    def checkEach(self, clients):
        """Check for any error for each client, and remove them from the list of clients if there is."""
        for client in clients:
            self.clients.remove(client)
            del self.clients[client]

    def accept(self, client):
        """Accept a new client."""
        client_socket, client_address = client.accept()
        self.clients.append(client_socket)

    def read(self, client):
        """"Receive a request sent by a client."""
        result = client.recv(1024)
        if result:
            result = pickle.loads(result)
            if result:
                self.requests.append(result)

    def write(self, client, message):
        """Send the result of the server to the socket of a client."""
        client.send(pickle.dumps(message))

    def __del__(self):
        """Close all connections."""
        print("closing server connection")
        self.closeEach(self.clients)
        self.close()

    def closeEach(self, clients):
        """Close the connection of each client."""
        for client in clients:
            client.close()

    def close(self):
        """Close the main connection of the server."""
        self.connection.close()


class Client:
    """Create a socket client that can send request and receive results to the
    server with socket."""

    def __init__(self, ip, port):
        # We don't want people to access our ip, and we suppose the ip constant.
        self._ip = ip
        self._port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self._ip, self._port))
        self.connection.setblocking(False)
        self.results = deque([])

    def send(self, request):
        """Send the inputs of the server."""
        self.connection.send(pickle.dumps(request))

    def receive(self):
        """Receive the results of the requests."""
        result = self.connection.recv(1024)
        if result:
            result = pickle.loads(result)
            if result:
                self.results.append(result)

    def __del__(self):
        """Close all connections."""
        print("closing client connection")
        self.close()

    def close(self):
        """Close the main connection with the server."""
        self.connection.close()



if __name__ == "__main__":
    s = Server(PORT)
    c1 = Client(IP, PORT)
    c2 = Client(IP, PORT)
    s.update()
    print("Clients number:", len(s.clients))

    c1.send("slt")
    s.update()
    c2.send("hola")
    s.update()
    print(s.requests)

    s.data = "wesh"
    s.update()
    c1.receive()
    c2.receive()
    print(c1.results, c2.results)

    del s, c1, c2
    print("Deleted connections and released ports.")
