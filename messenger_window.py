import tkinter
from tkinter import ttk


class MessengerWindow(tkinter.Tk):
    def __init__(self, action, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__action = action
        self.minsize(360, 480)
        self.title("Messenger")
        self.__center_window()
        self.__start()

    def __center_window(self):
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('+%d+%d' % (x, y))

    def __start(self):
        self.username_label = tkinter.Label(self, text="Username:")
        self.username_label.pack(side="top", fill="x", pady=2)

        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)
        self.__container.grid_columnconfigure(0, weight=1)
        self.__container.grid_columnconfigure(1, weight=1)
        self.__container.grid_columnconfigure(2, weight=1)
        self.__container.grid_rowconfigure(0, weight=1)

        self.left_frame = LeftFrame(self.__container, self.__action)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.middle_frame = MiddleFrame(self.__container, self.__action)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame = RightFrame(self.__container, self.__action)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.__action.on_close)


class LeftFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.search_label = tkinter.Label(self, text="Search for User:")
        self.search_label.pack(side="top", fill="x", pady=2)

        self.search_entry = ttk.Entry(self, justify="center")
        self.search_entry.pack(side="top", fill="x", padx=2, pady=2)

        self.search_entry.bind(
            "<Return>",
            self.__action.on_search_button_click
        )

        self.search_button = ttk.Button(
            self,
            text="Search",
            command=self.__action.on_search_button_click
        )
        self.search_button.pack(side="top", fill="both", padx=2, pady=2)

        self.found_user_label = tkinter.Label(self, text="Found User:")
        self.found_user_label.pack(side="top", fill="x", padx=2, pady=2)

        self.found_user_list = tkinter.Listbox(self, justify="center", selectmode=tkinter.SINGLE)
        self.found_user_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.found_user_list.bind(
            "<Double-Button-1>",
            self.__action.on_message_user_button_click
        )

        self.found_user_list_menu = tkinter.Menu(self, tearoff=0)
        self.found_user_list_menu.add_command(
            label="Send Friend Request",
            command=self.__action.on_send_friend_request_button_click
        )
        self.found_user_list.bind(
            "<Button-3>",
            self.__found_user_list_popup
        )

        self.send_friend_request_button = ttk.Button(
            self,
            text="Send Friend Request",
            command=self.__action.on_send_friend_request_button_click
        )
        self.send_friend_request_button.pack(side="top", fill="both", padx=2, pady=2)

        self.change_password_button = ttk.Button(
            self,
            text="Change Password",
            command=self.__action.on_change_password_button_click
        )
        self.change_password_button.pack(side="top", fill="both", padx=2, pady=2)

        self.logout_button = ttk.Button(
            self,
            text="Logout",
            command=self.__action.on_logout_button_click
        )
        self.logout_button.pack(side="top", fill="both", padx=2, pady=2)

    def __found_user_list_popup(self, event):
        try:
            self.found_user_list_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.found_user_list_menu.grab_release()


class MiddleFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.friends_label = tkinter.Label(self, text="Friends:")
        self.friends_label.pack(side="top", fill="x", pady=2)

        self.friends_list = tkinter.Listbox(self, justify="center", selectmode=tkinter.SINGLE)
        self.friends_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.friends_list.bind(
            "<Double-Button-1>",
            self.__action.on_message_user_button_click
        )

        self.friends_list_menu = tkinter.Menu(self, tearoff=0)
        self.friends_list_menu.add_command(
            label="Message User",
            command=self.__action.on_message_user_button_click
        )
        self.friends_list_menu.add_command(
            label="Delete User",
            command=self.__action.on_delete_user_button_click
        )
        self.friends_list.bind(
            "<Button-3>",
            self.__friends_list_popup
        )

        self.message_user_button = ttk.Button(
            self,
            text="Message User",
            command=self.__action.on_message_user_button_click
        )
        self.message_user_button.pack(side="top", fill="both", padx=2, pady=2)

        self.delete_user_button = ttk.Button(
            self,
            text="Delete User",
            command=self.__action.on_delete_user_button_click
        )
        self.delete_user_button.pack(side="top", fill="both", padx=2, pady=2)

    def __friends_list_popup(self, event):
        try:
            self.friends_list_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.friends_list_menu.grab_release()


class RightFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.friend_requests_label = tkinter.Label(self, text="Friend Requests:")
        self.friend_requests_label.pack(side="top", fill="x", pady=2)

        self.friend_request_list = tkinter.Listbox(self, justify="center", selectmode=tkinter.SINGLE)
        self.friend_request_list.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.friend_request_list.bind(
            "<Double-Button-1>",
            self.__action.on_accept_friend_request_button_click
        )

        self.friend_request_list_menu = tkinter.Menu(self, tearoff=0)
        self.friend_request_list_menu.add_command(
            label="Accept Request",
            command=self.__action.on_accept_friend_request_button_click
        )
        self.friend_request_list_menu.add_command(
            label="Decline Request",
            command=self.__action.on_decline_friend_request_button_click
        )
        self.friend_request_list.bind(
            "<Button-3>",
            self.__friend_request_list_popup
        )

        self.accept_request_button = ttk.Button(
            self,
            text="Accept Request",
            command=self.__action.on_accept_friend_request_button_click
        )
        self.accept_request_button.pack(side="top", fill="both", padx=2, pady=2)

        self.decline_request_button = ttk.Button(
            self,
            text="Decline Request",
            command=self.__action.on_decline_friend_request_button_click
        )
        self.decline_request_button.pack(side="top", fill="both", padx=2, pady=2)

    def __friend_request_list_popup(self, event):
        try:
            self.friend_request_list_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.friend_request_list_menu.grab_release()




