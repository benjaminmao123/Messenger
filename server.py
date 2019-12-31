import socket
import mysql.connector
import sys
import threading
import struct
import queue


class User:
    def __init__(self, conn):
        self.conn = conn


class Server:
    def __init__(self):
        self.client_username_conn = {}
        self.client_conn_username = {}
        self.__init_socket()

        self.port = 8888
        self.host = ""

        self.__bind()

        self.sock.listen()
        print("Listening")

        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="dragons",
                database="MessengerDB"
            )
            print("Connected to database")
        except mysql.connector.errors:
            print("Failed to connect to database")
            sys.exit()

        self.cursor = self.db.cursor(buffered=True)

    def __init_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Socket Created")
        except socket.error:
            print("Failed to create socket")
            sys.exit()

    def __bind(self):
        try:
            self.sock.bind((self.host, self.port))
            print("Bind Completed")
        except socket.error:
            print("Bind Failed")
            sys.exit()

    def __receive(self, conn, data):
        while True:
            try:
                message = ""
                size = struct.unpack("i", conn.recv(struct.calcsize("i")))[0]

                while len(message) < size:
                    message_chunk = conn.recv(size - len(message)).decode()
                    message += message_chunk

                if message is not None and len(message) > 0:
                    data.put(message)

                    if message == "exit":
                        return
            except:
                data.put("force_exit")
                conn.close()

    def __send(self, conn, data):
        conn.send(struct.pack("i", len(data)) + data.encode())

    def __login(self, conn, data):
        username = data.get()
        password = data.get()

        query = "SELECT Username, Password " \
                "FROM Users " \
                "WHERE Username = %s AND Password = %s"
        self.cursor.execute(query, (username, password, ))
        result = self.cursor.fetchone()

        if result != 0 and result is not None:
            self.__send(conn, "true")
            return username, password
        else:
            self.__send(conn, "false")

        return None, None

    def __register(self, conn, data):
        username = data.get()
        password = data.get()

        query = "SELECT Username " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (username, ))
        result = self.cursor.fetchone()

        if result == 0 or result is None:
            query = "INSERT INTO Users(Username, Password) " \
                    "VALUES(%s, %s)"
            self.cursor.execute(query, (username, password, ))
            self.db.commit()
            self.__send(conn, "true")
        else:
            self.__send(conn, "false")

    def __search_user(self, conn, data, current_username):
        username = data.get()

        if username != current_username:
            query = "SELECT Username " \
                    "FROM Users " \
                    "WHERE Username = %s"
            self.cursor.execute(query, (username, ))
            result = self.cursor.fetchone()

            if result != 0 and result is not None:
                self.__send(conn, "true")
                self.__send(conn, result[0])
            else:
                self.__send(conn, "false")
        else:
            self.__send(conn, "false")

    def __send_friend_request(self, conn, data, current_username):
        username = data.get()

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        current_user_id = self.cursor.fetchone()[0]

        self.cursor.execute(query, (username, ))
        user_id = self.cursor.fetchone()[0]

        query = "SELECT To_UserID " \
                "FROM FriendRequest " \
                "WHERE (From_UserID = %s AND To_UserID = %s) OR (From_UserID = %s AND To_UserID = %s)"
        self.cursor.execute(query, (current_user_id, user_id, user_id, current_user_id, ))
        result = self.cursor.fetchone()

        if result == 0 or result is None:
            query = "SELECT *" \
                    "FROM Friends " \
                    "WHERE (UserID_A = %s AND UserID_B = %s) OR (UserID_A = %s AND UserID_B = %s)"
            self.cursor.execute(query, (current_user_id, user_id, user_id, current_user_id, ))
            result = self.cursor.fetchone()

            if result == 0 or result is None:
                query = "INSERT INTO FriendRequest(From_UserID, To_UserID) " \
                        "VALUES(%s, %s)"
                self.cursor.execute(query, (current_user_id, user_id))
                self.db.commit()
                self.__send(conn, "true")
            else:
                self.__send(conn, "false")
        else:
            self.__send(conn, "false")

    def __send_friend_request_list(self, conn, current_username):
        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        current_user_id = self.cursor.fetchone()[0]

        query = "SELECT Username " \
                "FROM Users " \
                "WHERE UserID IN " \
                "(SELECT From_UserID " \
                "FROM FriendRequest " \
                "WHERE To_UserID = %s)"
        self.cursor.execute(query, (current_user_id, ))
        result = self.cursor.fetchall()

        for row in result:
            for username in row:
                self.__send(conn, username)

        self.__send(conn, "true")

    def __accept_friend_request(self, data, current_username):
        username = data.get()

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        id_a = self.cursor.fetchall()[0][0]

        self.cursor.execute(query, (username, ))
        id_b = self.cursor.fetchall()[0][0]

        query = "INSERT INTO Friends(UserID_A, UserID_B) " \
                "VALUES(%s, %s)"
        self.cursor.execute(query, (id_a, id_b, ))
        self.cursor.execute(query, (id_b, id_a, ))
        self.db.commit()

        query = "SELECT FriendRequestID " \
                "FROM FriendRequest " \
                "WHERE From_UserID = %s AND To_UserID = %s"
        self.cursor.execute(query, (id_a, id_b, ))
        result = self.cursor.fetchone()

        query = "DELETE FROM FriendRequest " \
                "WHERE From_UserID = %s and To_UserID = %s"

        if result != 0 and result is not None:
            self.cursor.execute(query, (id_a, id_b, ))
            self.db.commit()
        else:
            self.cursor.execute(query, (id_b, id_a, ))
            self.db.commit()

    def __decline_friend_request(self, data, current_username):
        username = data.get()

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (username, ))
        from_id = self.cursor.fetchone()[0]

        self.cursor.execute(query, (current_username, ))
        to_id = self.cursor.fetchone()[0]

        query = "DELETE FROM FriendRequest " \
                "WHERE From_UserID = %s AND To_UserID = %s"
        self.cursor.execute(query, (from_id, to_id, ))
        self.db.commit()

    def __send_friends_list(self, conn, current_username):
        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        current_user_id = self.cursor.fetchone()[0]

        query = "SELECT Username " \
                "FROM Users " \
                "WHERE UserID IN " \
                "(SELECT UserID_B " \
                "FROM Friends " \
                "WHERE UserID_A = %s)"
        self.cursor.execute(query, (current_user_id, ))
        result = self.cursor.fetchall()

        for row in result:
            for username in row:
                self.__send(conn, username)

        self.__send(conn, "true")

    def __change_password(self, conn, data, current_username, current_password):
        old_password = data.get()
        new_password = data.get()

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        result = self.cursor.fetchone()[0]

        if current_password == old_password:
            query = "UPDATE Users " \
                    "SET Password = %s " \
                    "WHERE UserID = %s"
            self.cursor.execute(query, (new_password, result, ))
            self.db.commit()
            self.__send(conn, "true")

            return new_password

        self.__send(conn, "false")

        return None

    def __get_username(self, conn, current_username):
        self.__send(conn, current_username)

    def __exit(self, conn):
        self.__send(conn, "exit")
        conn.close()

    def __message_user(self, conn, data, current_username):
        recipient_username = data.get()
        text = data.get()
        text = current_username + ": " + text

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s"
        self.cursor.execute(query, (current_username, ))
        sender_id = self.cursor.fetchone()[0]

        self.cursor.execute(query, (recipient_username, ))
        recipient_id = self.cursor.fetchone()[0]

        query = "INSERT INTO Messages(SenderID, RecipientID, Message) " \
                "VALUES(%s, %s, %s)"
        self.cursor.execute(query, (sender_id, recipient_id, text, ))
        self.db.commit()

        self.__send(conn, "new_message")
        self.__send(conn, text)

        recipient_conn = self.client_username_conn.get(recipient_username)

        if recipient_conn is not None:
            message = "new_message"
            recipient_conn.send(struct.pack("i", len(message)) + message.encode())
            recipient_conn.send(struct.pack("i", len(text)) + text.encode())

    def __send_messages(self, conn, data, current_username):
        other_username = data.get()

        query = "SELECT UserID " \
                "FROM Users " \
                "WHERE Username = %s OR Username = %s"
        self.cursor.execute(query, (current_username, other_username, ))
        result = self.cursor.fetchall()

        query = "SELECT Message " \
                "FROM Messages " \
                "WHERE (SenderID = %s AND RecipientID = %s) OR (SenderID = %s AND RecipientID = %s) " \
                "ORDER BY MessageID ASC"
        self.cursor.execute(query, (result[0][0], result[1][0], result[1][0], result[0][0], ))
        result = self.cursor.fetchall()

        for row in result:
            for message in row:
                self.__send(conn, message)

        self.__send(conn, "true")

    def __client_thread(self, conn, data):
        while True:
            current_username = None

            while True:
                choice = data.get()

                if choice == "login":
                    current_username, current_password = self.__login(conn, data)

                    if current_username is not None and current_password is not None:
                        self.client_username_conn[current_username] = conn
                        self.client_conn_username[conn] = current_username
                        break
                elif choice == "register":
                    self.__register(conn, data)
                elif choice == "exit":
                    self.client_username_conn.pop(current_username, None)
                    self.client_conn_username.pop(conn, None)
                    self.__exit(conn)
                    return
                elif choice == "force_exit":
                    self.client_username_conn.pop(current_username, None)
                    self.client_conn_username.pop(conn, None)
                    return

            while True:
                choice = data.get()

                if choice == "search_user":
                    self.__search_user(conn, data, current_username)
                elif choice == "send_friend_request":
                    self.__send_friend_request(conn, data, current_username)
                elif choice == "get_friend_request_list":
                    self.__send_friend_request_list(conn, current_username)
                elif choice == "accept_friend_request":
                    self.__accept_friend_request(data, current_username)
                elif choice == "decline_friend_request":
                    self.__decline_friend_request(data, current_username)
                elif choice == "get_friends_list":
                    self.__send_friends_list(conn, current_username)
                elif choice == "change_password":
                    result = self.__change_password(conn, data, current_username, current_password)

                    if result is not None:
                        current_password = result
                elif choice == "get_username":
                    self.__get_username(conn, current_username)
                elif choice == "logout":
                    self.client_conn_username[current_username] = None
                    self.client_username_conn[conn] = None
                    break
                elif choice == "message_user":
                    self.__message_user(conn, data, current_username)
                elif choice == "get_messages":
                    self.__send_messages(conn, data, current_username)
                elif choice == "exit":
                    self.client_username_conn.pop(current_username, None)
                    self.client_conn_username.pop(conn, None)
                    self.__exit(conn)
                    return
                elif choice == "force_exit":
                    self.client_username_conn.pop(current_username, None)
                    self.client_conn_username.pop(conn, None)
                    return

    def execute(self):
        while True:
            conn, addr = self.sock.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            data = queue.Queue()

            t1 = threading.Thread(target=self.__client_thread, args=(conn, data, ))
            t1.start()
            t2 = threading.Thread(target=self.__receive, args=(conn, data, ))
            t2.start()

        self.sock.close()


if __name__ == "__main__":
    server = Server()
    server.execute()
