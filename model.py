import client
import queue


class Model:
    def __init__(self):
        self.client = client.Client()

    def login(self, username, password):
        message = "login"

        self.client.send(message)
        self.client.send(username)
        self.client.send(password)

        if self.client.data.get() == "true":
            return True

        return False

    def register(self, username, password):
        message = "register"

        self.client.send(message)
        self.client.send(username)
        self.client.send(password)

        if self.client.data.get() == "true":
            return True

        return False

    def search_user(self, username):
        message = "search_user"

        self.client.send(message)
        self.client.send(username)

        if self.client.data.get() == "true":
            return self.client.data.get()

        return None

    def send_friend_request(self, username):
        message = "send_friend_request"

        self.client.send(message)
        self.client.send(username)

        if self.client.data.get() == "true":
            return True

        return False

    def get_friend_requests(self):
        message = "get_friend_request_list"

        self.client.send(message)
        friend_request_list = []

        while True:
            try:
                data = self.client.data.get_nowait()

                if data == "true":
                    break

                friend_request_list.append(data)
            except queue.Empty:
                pass

        return friend_request_list

    def accept_friend_request(self, username):
        message = "accept_friend_request"

        self.client.send(message)
        self.client.send(username)

    def decline_friend_request(self, username):
        message = "decline_friend_request"

        self.client.send(message)
        self.client.send(username)

    def get_friends_list(self):
        message = "get_friends_list"

        self.client.send(message)

        friends_list = []

        while True:
            try:
                data = self.client.data.get_nowait()

                if data == "true":
                    break

                friends_list.append(data)
            except queue.Empty:
                pass

        return friends_list

    def change_password(self, current_password, new_password):
        message = "change_password"

        self.client.send(message)
        self.client.send(current_password)
        self.client.send(new_password)

        if self.client.data.get() == "true":
            return True

        return False

    def get_username(self):
        message = "get_username"

        self.client.send(message)

        return self.client.data.get()

    def logout(self):
        message = "logout"

        self.client.send(message)

    def exit(self):
        message = "exit"

        self.client.send(message)

    def message_user(self, username, text):
        message = "message_user"

        self.client.send(message)
        self.client.send(username)
        self.client.send(text)

    def get_messages(self, username):
        message = "get_messages"

        self.client.send(message)
        self.client.send(username)

        messages = []

        while True:
            try:
                data = self.client.data.get_nowait()

                if data == "true":
                    break

                messages.append(data)
            except queue.Empty:
                pass

        return messages

    def get_most_recent_message(self):
        try:
            data = self.client.data.get_nowait()

            if data == "new_message":
                return self.client.data.get()

        except queue.Empty:
            pass


