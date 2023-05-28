import socket

class Publisher:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        self.socket.send("publisher".encode())

        topic = input("Tópico: ")
        self.socket.send(topic.encode())

        while True:
            message = input("Texto: ")
            self.socket.send(message.encode())

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    publisher = Publisher("localhost", 5000)
    publisher.start()
