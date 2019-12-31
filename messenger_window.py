import tkinter


class MessengerWindow(tkinter.Tk):
    def __init__(self, controller, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__controller = controller
        self.minsize(360, 480)
        self.title("Messenger")
        self.__start()

    def __start(self):
        self.username_label = tkinter.Label(self, text="Username:")
        self.username_label.pack(side="top", fill="x", pady=2)

        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)
        self.__container.grid_columnconfigure(0, weight=1)
        self.__container.grid_columnconfigure(1, weight=1)
        self.__container.grid_columnconfigure(2, weight=1)
        self.__container.grid_rowconfigure(0, weight=1)

        self.left_frame = LeftFrame(self.__container, self.__controller)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.middle_frame = MiddleFrame(self.__container, self.__controller)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame = RightFrame(self.__container, self.__controller)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.__controller.messenger_window_actions.on_close)


class LeftFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.search_label = tkinter.Label(self, text="Search for User:")
        self.search_label.pack(side="top", fill="x", pady=2)

        self.search_entry = tkinter.Entry(self, justify="center")
        self.search_entry.pack(side="top", fill="x", padx=2, pady=2)

        self.search_button = tkinter.Button(
            self,
            text="Search",
            command=self.__controller.messenger_window_actions.on_search_button_click
        )
        self.search_button.pack(side="top", fill="both", padx=2, pady=2)

        self.found_user_label = tkinter.Label(self, text="Found User:")
        self.found_user_label.pack(side="top", fill="x", padx=2, pady=2)

        self.found_user_list = tkinter.Listbox(self, justify="center", selectmode=tkinter.SINGLE)
        self.found_user_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.send_friend_request_button = tkinter.Button(
            self,
            text="Send Friend Request",
            command=self.__controller.messenger_window_actions.on_send_friend_request_button_click
        )
        self.send_friend_request_button.pack(side="top", fill="both", padx=2, pady=2)

        self.change_password_button = tkinter.Button(
            self,
            text="Change Password",
            command=self.__controller.messenger_window_actions.on_change_password_button_click
        )
        self.change_password_button.pack(side="top", fill="both", padx=2, pady=2)

        self.logout_button = tkinter.Button(
            self,
            text="Logout",
            command=self.__controller.messenger_window_actions.on_logout_button_click
        )
        self.logout_button.pack(side="top", fill="both", padx=2, pady=2)


class MiddleFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.friends_label = tkinter.Label(self, text="Friends:")
        self.friends_label.pack(side="top", fill="x", pady=2)

        self.friends_list = tkinter.Listbox(self, selectmode=tkinter.SINGLE)
        self.friends_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.message_user_button = tkinter.Button(
            self,
            text="Message User",
            command=self.__controller.messenger_window_actions.on_message_user_button_click
        )
        self.message_user_button.pack(side="top", fill="both", padx=2, pady=2)


class RightFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.friend_requests_label = tkinter.Label(self, text="Friend Requests:")
        self.friend_requests_label.pack(side="top", fill="x", pady=2)

        self.friend_request_list = tkinter.Listbox(self, justify="center", selectmode=tkinter.SINGLE)
        self.friend_request_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.accept_request_button = tkinter.Button(
            self,
            text="Accept Request",
            command=self.__controller.messenger_window_actions.on_accept_friend_request_button_click
        )
        self.accept_request_button.pack(side="top", fill="both", padx=2, pady=2)

        self.decline_request_button = tkinter.Button(
            self,
            text="Decline Request",
            command=self.__controller.messenger_window_actions.on_decline_friend_request_button_click
        )
        self.decline_request_button.pack(side="top", fill="both", padx=2, pady=2)





