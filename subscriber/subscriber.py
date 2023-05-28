import socket

class Subscriber:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        self.socket.send("subscriber".encode())

        topic = input("Digite o tópico: ")
        self.socket.send(topic.encode())

        last_message = self.socket.recv(1024).decode()
        if last_message:
            print("Texto mais recente do tópico selecionado:", last_message)

        while True:
            message = self.socket.recv(1024).decode()
            if not message:
                break
            print("Texto recebido:", message)

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    subscriber = Subscriber("localhost", 5000)
    subscriber.start()
