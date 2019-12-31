import tkinter


class ChangePasswordWindow(tkinter.Tk):
    def __init__(self, controller, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__controller = controller
        self.resizable(False, False)
        self.title("Change Password")
        self.__start()

    def __start(self):
        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)

        self.top_frame = TopFrame(self.__container, self.__controller)
        self.top_frame.pack(side="top", fill="both")

        self.bottom_frame = BottomFrame(self.__container, self.__controller)
        self.bottom_frame.pack(side="top", fill="both")

        self.protocol("WM_DELETE_WINDOW", self.__controller.change_password_window_actions.on_close)


class TopFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.current_password_label = tkinter.Label(self, text="Current Password:")
        self.current_password_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.current_password_entry = tkinter.Entry(self)
        self.current_password_entry.grid(row=0, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)

        self.new_password_label = tkinter.Label(self, text="New Password:")
        self.new_password_label.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.new_password_entry = tkinter.Entry(self)
        self.new_password_entry.grid(row=1, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)


class BottomFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.change_password_button = tkinter.Button(
            self,
            text="Change Password",
            command=self.__controller.change_password_window_actions.on_change_password_button_click
        )
        self.change_password_button.pack(side="top", fill="both", padx=2, pady=2)

