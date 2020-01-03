import tkinter


class ChangePasswordWindow(tkinter.Tk):
    def __init__(self, action, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__action = action
        self.resizable(False, False)
        self.title("Change Password")
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
        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)

        self.top_frame = TopFrame(self.__container, self.__action)
        self.top_frame.pack(side="top", fill="both")

        self.bottom_frame = BottomFrame(self.__container, self.__action)
        self.bottom_frame.pack(side="top", fill="both")

        self.protocol("WM_DELETE_WINDOW", self.__action.on_close)
        self.bind(
            "<Return>",
            self.__action.on_change_password_button_click
        )


class TopFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.current_password_label = tkinter.Label(self, text="Current Password:")
        self.current_password_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.current_password_entry = tkinter.Entry(self, show="●")
        self.current_password_entry.grid(row=0, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)

        self.new_password_label = tkinter.Label(self, text="New Password:")
        self.new_password_label.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.new_password_entry = tkinter.Entry(self, show="●")
        self.new_password_entry.grid(row=1, column=1, sticky="nsew", ipadx=42, padx=2, pady=2)


class BottomFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.change_password_button = tkinter.Button(
            self,
            text="Change Password",
            command=self.__action.on_change_password_button_click
        )
        self.change_password_button.pack(side="top", fill="both", padx=2, pady=2)

