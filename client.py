import sys
import socket
import threading
import struct
import collections
import configparser


class Client:
    def __init__(self):
        self.message = None
        self.__init_socket()

        parser = configparser.ConfigParser()
        parser.read("client_settings.ini")

        self.port = int(parser.get("client", "port"))
        self.host = parser.get("client", "host")

        self.data = collections.deque()

        self.__connect()

        t1 = threading.Thread(target=self.__receive)
        t1.start()

    def __init_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Created Socket")
        except socket.error:
            print("Failed to create socket")
            sys.exit()

    def __connect(self):
        self.sock.connect((self.host, self.port))
        print("Connected")

    def send(self, data):
        try:
            self.sock.send(struct.pack("i", len(data)) + data.encode())
        except socket.error:
            self.sock.close()

    def __receive(self):
        while True:
            try:
                self.message = ""
                size = struct.unpack("i", self.sock.recv(struct.calcsize("i")))[0]

                while len(self.message) < size:
                    message_chunk = self.sock.recv(size - len(self.message)).decode()
                    self.message += message_chunk

                if self.message is not None and len(self.message) > 0:
                    self.data.append(self.message)

                    if self.message == "exit":
                        self.sock.close()
                        return
            except socket.error:
                self.sock.close()


