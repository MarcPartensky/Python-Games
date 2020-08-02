from collections import deque
import socket
import select
import pickle



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# IP_CLIENT = "172.16.0.39."
# IP_SERVER = getIP()
IP = get_ip()
PORT = 1234

HEADER_LENGTH = 10


class Server:
    """Create a socket server that can receive requests and send results
    with socket."""

    def __init__(self, ip, port, max_clients=10, header_length=HEADER_LENGTH):
        """Create a server using the ip and port and optional max_socket."""
        # We don't want people to access our ip, and we suppose the ip constant.
        self._ip = ip
        self._port = port
        self.header_length = header_length
        self.data = None
        self.message = None
        self.queue = deque([])

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self._ip, self._port))
        self.connection.listen(max_clients)
        self.clients = [self.connection]
        self.open = True

    def main(self):
        """Main loop of the server which only updates it while it is open."""
        while self.open:
            self.update()

    def update(self):
        """Update the server to receive, write and check the sockets of the clients."""
        read_clients, write_clients, exception_clients = select.select(self.clients, self.clients, self.clients)
        try:
            self.readEach(read_clients)
            self.writeEach(write_clients, self.message)
        except:
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
        return len(clients) == 0

    def accept(self, client):
        """Accept a new client."""
        client_socket, client_address = client.accept()
        self.clients.append(client_socket)

    def receive(self, client):
        """"Receive a request sent by a client."""
        m = client.recv(self.header_length)
        message_length = int(m.decode("utf-8").strip())
        message = pickle.loads(client.recv(message_length))
        self.queue.append((client, message))

    def sendForSure(self, client, message, max_attempts=10):
        attempts = 0
        sent = False
        while not sent and attempts < max_attempts:
            try:
                self.send(client, message)
                sent = True
            except:
                attempts += 1
        if not sent:
            print("The message: {} could not be sent after {} attempts.".format(message, max_attempts))

    def send(self, client, message):
        """Send a message to a client."""
        bytes_message = pickle.dumps(message)
        bytes_header = f"{len(bytes_message):<{self.header_length}}".encode("utf-8")
        client.send(bytes_header + bytes_message)

    def sendAll(self, message):
        """Send a message to all clients."""
        for client in self.clients:
            self.send(client, message)

    def sendAllForSure(self, message):
        """Send a message to all clients."""
        for client in self.clients:
            self.sendForSure(client, message)

    def __del__(self):
        """Close all connections."""
        try:
            self.closeEach(self.clients)  # We also close the connections of the computers connected.
            self.close()
            print("Closed server connection.")
        except:
            raise Warning("Failed to close client connection.")

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

    def __init__(self, ip, port, header_length=HEADER_LENGTH):
        # We don't want people to access our ip, and we suppose the ip constant.
        """Create a client which connects to a server using its ip and port."""
        self._ip = ip
        self._port = port
        self.header_length = header_length

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self._ip, self._port))
        self.connection.setblocking(False)
        self.queue = deque([])

    def sendForSure(self, message, max_attempts=10):
        attempts = 0
        sent = False
        while not sent and attempts < max_attempts:
            try:
                self.send(message)
                sent = True
            except:
                attempts += 1

    def send(self, message):
        """Send a message to the server"""
        bytes_message = pickle.dumps(message)
        bytes_header = f"{len(bytes_message):<{self.header_length}}".encode("utf-8")
        self.connection.send(bytes_header + bytes_message)

    def receive(self):
        """"Receive a message from the server."""
        m = self.connection.recv(self.header_length)
        message_length = int(m.decode("utf-8").strip())
        message = pickle.loads(self.connection.recv(message_length))
        self.queue.append(message)

    def __del__(self):
        """Close all connections."""
        try:
            self.close()
            print("Closed client connection.")
        except:
            raise Warning("Failed to close client connection.")

    def close(self):
        """Close the main connection with the server."""
        self.connection.close()

    def getIp(self):
        """Ip is readable but not writable.."""
        return self._ip

    def getPort(self):
        return self._port

    ip = property(getIp)
    port = property(getPort)


if __name__ == "__main__":
    s = Server(IP, PORT)
    c1 = Client(IP, PORT)
    c2 = Client(IP, PORT)
    s.update()
    print("Clients number:", len(s.clients))
    from myasteroidgame import AsteroidGame # We can send whatever we want

    c1.send("slt")
    c2.send("hola")
    c1.send(AsteroidGame)
    s.update()
    s.update()
    s.update()
    print("server queue:", s.queue)

    s.message = AsteroidGame
    s.update()
    c1.receive()
    c2.receive()
    print("client queues:", c1.queue, c2.queue)

    del s, c1, c2
    print("Deleted connections and released ports.")
