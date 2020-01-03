import client


class Model:
    def __init__(self):
        self.client = client.Client()

    def login(self, username, password):
        message = "login"

        self.client.send(message)
        self.client.send(username)
        self.client.send(password)

        while True:
            try:
                if self.client.data[0] == "true":
                    self.client.data.popleft()
                    return True
                else:
                    self.client.data.popleft()
                    return False
            except IndexError:
                pass

    def register(self, username, password):
        message = "register"

        self.client.send(message)
        self.client.send(username)
        self.client.send(password)

        while True:
            try:
                if self.client.data[0] == "true":
                    self.client.data.popleft()
                    return True
                else:
                    self.client.data.popleft()
                    return False
            except IndexError:
                pass

    def search_user(self, username):
        message = "search_user"

        self.client.send(message)
        self.client.send(username)

        users = []

        while True:
            try:
                data = self.client.data[0]

                if data == "true":
                    self.client.data.popleft()
                    return users

                if data[0:12] == "search_user:":
                    users.append(data[12:])
                    self.client.data.popleft()
            except IndexError:
                pass

        return users

    def send_friend_request(self, username):
        message = "send_friend_request"

        self.client.send(message)
        self.client.send(username)

        while True:
            try:
                if self.client.data[0] == "true":
                    self.client.data.popleft()
                    return True
            except IndexError:
                pass

        return False

    def get_friend_requests(self):
        message = "get_friend_request_list"

        self.client.send(message)
        friend_request_list = []

        while True:
            try:
                data = self.client.data[0]

                if data == "true":
                    self.client.data.popleft()
                    break

                if data[0:15] == "friend_request:":
                    friend_request_list.append(data[15:])
                    self.client.data.popleft()
            except IndexError:
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
                data = self.client.data[0]

                if data == "true":
                    self.client.data.popleft()
                    return friends_list

                if data[0:13] == "friends_list:":
                    friends_list.append(data[13:])
                    self.client.data.popleft()
            except IndexError:
                pass

    def change_password(self, current_password, new_password):
        message = "change_password"

        self.client.send(message)
        self.client.send(current_password)
        self.client.send(new_password)

        while True:
            try:
                if self.client.data[0] == "true":
                    self.client.data.popleft()
                    return True
                else:
                    self.client.data.pop()
                    return False
            except IndexError:
                pass

    def get_username(self):
        message = "get_username"

        self.client.send(message)

        while True:
            try:
                data = self.client.data[0]
                self.client.data.popleft()
                return data
            except IndexError:
                pass

    def logout(self):
        message = "logout"

        self.client.send(message)

    def exit(self):
        message = "exit"

        self.client.send(message)

    def message_user(self, username, text):
        if text != "\n":
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
                data = self.client.data[0]

                if data == "true":
                    self.client.data.popleft()
                    return messages

                if data[0:8] == "message:":
                    messages.append(data[8:])
                    self.client.data.popleft()
            except IndexError:
                pass

        return messages

    def get_most_recent_message(self, recipient):
        try:
            data = self.client.data[0]

            if data[0:12 + len(recipient) + 1] == "new_message:" + recipient + ":":
                self.client.data.popleft()
                return data[12 + len(recipient) + 1:]
        except IndexError:
            return ""

    def get_most_recent_change(self):
        try:
            data = self.client.data[0]

            if data[0:11] == "new_friend:":
                self.client.data.popleft()
                return data[11:], "", ""
            elif data[0:19] == "new_friend_request:":
                self.client.data.popleft()
                return "", data[19:], ""
            elif data == "delete_friend":
                self.client.data.popleft()
                return "", "", "true"
        except IndexError:
            return "", "", ""

        return "", "", ""

    def delete_friend(self, username):
        message = "delete_friend"

        self.client.send(message)
        self.client.send(username)
