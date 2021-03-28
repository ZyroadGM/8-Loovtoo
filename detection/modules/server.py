import socket
import threading
import time

class server:
    def __init__(self, port=5050):
        self.format = 'utf-8'
        self.header = 64
        self.local_address = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.local_address, self.port))
        self.disconnect_message = '*DISCONNECT'
        self.get_header_message = '*HEADER'
        self.event = 0
        self.message = ''
        self.clients = []
        self.waiting = False

    def get_feedback(self, connection, address, message_size):
        self.event = None
        message = connection.recv(message_size).decode(self.format)
        if message:
            print('[{}] {}'.format(address[0], message))
            self.event = message

    def assign_data(self, data):
        self.message = str('{} \r'.format(data)).encode(self.format)

    def handle_client(self, connection, address):
        connected = True
        past_message = ''
        print('[NEW CONNECTION] "{}" has connected'.format(address[0]))
        """client_message_size = connection.recv(self.header).decode(self.format)
        if client_message_size:
            client_message_size = int(client_message_size)"""
        while connected:
            if self.message != '' and self.message != past_message:
                connection.send(self.message)
                past_message = self.message
                print(self.message)
            if self.event is not None:
                if self.event == self.disconnect_message:
                    connected = False
                    print('[{}] Disconnected from the server'.format(address[0]))
                elif self.event == self.get_header_message:
                    connection.send()
                """thread = threading.Thread(target=self.get_feedback, args=(connection, address, client_message_size))
                thread.start()"""
        connection.close()
        print('[{}] Disconnected from the server'.format(address[0]))
        return False

    def get_clients(self):
        return self.clients

    def gdklg(self):
        client_connection, client_address = self.server.accept()
        thread = threading.Thread(target=self.handle_client, args=(client_connection, client_address))
        thread.start()
        self.clients.append(client_address)

    def main(self):
        self.server.listen()
        print('[LISTENING] listening on "{}"'.format(self.local_address))
        while True:
            thread = threading.Thread(target=self.gdklg)
            thread.start()

def start():
    server_transmitter = server()
    thread = threading.Thread(target=server_transmitter.main)
    thread.start()
    while True:
        with open(r'C:\Users\Henri\PycharmProjects\ImageProcessing\detection\data\error.txt', 'r') as r:
            server_message = r.read()
        server_transmitter.assign_data(server_message)


if __name__ == '__main__':
    start()