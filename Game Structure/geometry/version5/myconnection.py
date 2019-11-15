from collections import deque
import socket
import select
import pickle


def getIP():
    return socket.gethostname()


IP_CLIENT = "172.16.0.39."
IP_SERVER = getIP()
PORT = 1234


class Server:
    """Create a socket server that can receive requests and send results
    with socket."""

    def __init__(self, ip, port, max_clients=10, header_length=10):
        """Create a server using the ip and port and optional max_socket."""
        # We don't want people to access our ip, and we suppose the ip constant.
        self._ip = ip
        self._port = port
        self.header_length = header_length
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self._ip, self._port))
        self.connection.listen(max_clients)
        self.clients = [self.connection]
        self.data = None
        self.message = None
        self.queue = deque([])
        self.open = True

    def loop(self):
        """Main loop of the server which only updates it while it is open."""
        while self.open:
            self.update()

    def update(self):
        """Update the server to receive, write and check the sockets of the clients."""
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
                self.receive(client)

    def writeEach(self, clients, message):
        """Write to each client."""
        if message is not None:
            for client in clients:
                self.send(client, message)
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

    def receive(self, client):
        """"Receive a request sent by a client."""
        message_length = int(client.recv(self.header_length).decode("utf-8").strip())
        message = pickle.loads(client.recv(message_length))
        i = self.clients.index(client)
        self.queue.append({i: message})

    def send(self, client, message):
        """Send a message to a client."""
        message = pickle.dumps(message)
        header = f"{len(message):<{self.header_length}}".encode("utf-8")
        client.send(header + message)

    def sendAll(self, message):
        """Send a message to all clients."""
        for client in self.clients:
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

    def __init__(self, ip, port, header_length=10):
        # We don't want people to access our ip, and we suppose the ip constant.
        """Create a client which connects to a server using its ip and port."""
        self._ip = ip
        self._port = port
        self.header_length = header_length
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self._ip, self._port))
        self.connection.setblocking(False)
        self.queue = deque([])

    def send(self, message):
        """Send a message to the server"""
        message = pickle.dumps(message)
        header = f"{len(message):<{self.header_length}}".encode("utf-8")
        self.connection.send(header + message)

    def receive(self):
        """"Receive a message from the server."""
        m = self.connection.recv(self.header_length)
        message_length = int(m.decode("utf-8").strip())
        message = pickle.loads(self.connection.recv(message_length))
        self.queue.append(message)

    def __del__(self):
        """Close all connections."""
        print("closing client connection")
        self.close()

    def close(self):
        """Close the main connection with the server."""
        self.connection.close()


if __name__ == "__main__":
    s = Server(IP_CLIENT, PORT)
    c1 = Client(IP_CLIENT, PORT)
    c2 = Client(IP_CLIENT, PORT)
    s.update()
    print("Clients number:", len(s.clients))

    c1.send("slt")
    c2.send("hola")
    c1.send("slt encore")
    s.update()
    s.update()
    s.update()
    print("server queue:", s.queue)

    s.message = "wesh"
    s.update()
    c1.receive()
    c2.receive()
    print("client queues:",c1.queue, c2.queue)

    del s, c1, c2
    print("Deleted connections and released ports.")
