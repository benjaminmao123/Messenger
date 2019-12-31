import tkinter


class LoginRegisterWindow(tkinter.Tk):
    def __init__(self, controller, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__controller = controller
        self.resizable(False, False)
        self.title("Login")
        self.__start()

    def __start(self):
        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)

        self.top_frame = TopFrame(self.__container, self.__controller)
        self.top_frame.pack(side="top", fill="both")

        self.bottom_frame = BottomFrame(self.__container, self.__controller)
        self.bottom_frame.pack(side="top", fill="both")

        self.protocol("WM_DELETE_WINDOW", self.__controller.login_window_actions.on_close)


class TopFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.username_label = tkinter.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.username_entry = tkinter.Entry(self)
        self.username_entry.grid(row=0, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)

        self.password_label = tkinter.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.password_entry = tkinter.Entry(self, show="●")
        self.password_entry.grid(row=1, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)


class BottomFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.login_button = tkinter.Button(
            self,
            text="Login",
            command=self.__controller.login_window_actions.on_login_button_click
        )
        self.login_button.pack(side="top", fill="both", padx=2, pady=2)

        self.register_button = tkinter.Button(
            self,
            text="Register",
            command=self.__controller.login_window_actions.on_register_button_click
        )
        self.register_button.pack(side="top", fill="both", padx=2, pady=2)
