import sys
import socket
import threading
import struct
import queue


class Client:
    def __init__(self):
        self.message = None
        self.__init_socket()

        self.port = 8888
        self.host = "192.168.1.2"
        self.data = queue.Queue()

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
        self.sock.send(struct.pack("i", len(data)) + data.encode())

    def __receive(self):
        while True:
            self.message = ""
            size = struct.unpack("i", self.sock.recv(struct.calcsize("i")))[0]

            while len(self.message) < size:
                message_chunk = self.sock.recv(size - len(self.message)).decode()
                self.message += message_chunk

            if self.message is not None and len(self.message) > 0:
                self.data.put(self.message)

                if self.message == "exit":
                    self.sock.close()
                    return


