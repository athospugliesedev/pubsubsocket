import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.topics = {}
        self.lock = threading.Lock()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Servidor escutando em {self.host}:{self.port}...")

        while True:
            client_socket, address = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_type = client_socket.recv(1024).decode()
        if client_type == "publisher":
            self.handle_publisher(client_socket)
        elif client_type == "subscriber":
            self.handle_subscriber(client_socket)
        client_socket.close()

    def handle_publisher(self, publisher_socket):
        topic = publisher_socket.recv(1024).decode()
        self.add_topic(topic)
        print(f"Novo publicador conectado: {topic}")

        while True:
            message = publisher_socket.recv(1024).decode()
            if not message:
                break
            print(f"Mensagem recebida de {topic}: {message}")
            self.store_message(topic, message)

    def handle_subscriber(self, subscriber_socket):
        topic = subscriber_socket.recv(1024).decode()
        self.add_topic(topic)
        print(f"Novo assinante conectado: {topic}")

        self.send_last_message(subscriber_socket, topic)

    def add_topic(self, topic):
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []

    def store_message(self, topic, message):
        with self.lock:
            self.topics[topic].append(message)

    def send_last_message(self, subscriber_socket, topic):
        with self.lock:
            if topic in self.topics and self.topics[topic]:
                last_message = self.topics[topic][-1]
                subscriber_socket.send(last_message.encode())

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    server = Server("localhost", 5000)
    server.start()
