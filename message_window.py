import tkinter


class MessageWindow(tkinter.Tk):
    def __init__(self, controller, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__controller = controller
        self.minsize(480, 360)
        self.resizable(False, False)
        self.__start()

    def __start(self):
        self.current_user_messaging = tkinter.Label(self, text="Currently Messaging:")
        self.current_user_messaging.pack(side="top", fill="x", pady=2)

        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)

        self.top_frame = TopFrame(self.__container, self.__controller)
        self.top_frame.pack(side="top", fill="both", expand=True)

        self.bottom_frame = BottomFrame(self.__container, self.__controller)
        self.bottom_frame.pack(side="top", fill="both", expand=True)

        self.bind("<Return>", self.__controller.message_window_actions.on_send_message_button_click)
        self.protocol("WM_DELETE_WINDOW", self.__controller.message_window_actions.on_close)


class TopFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.message_list = tkinter.Listbox(self, width=108, height=10)
        self.message_list.grid_columnconfigure(0, weight=1)
        self.message_list.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.scrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.message_list.yview)
        self.scrollbar.grid(row=0, column=5, sticky="nsew", padx=2, pady=2)
        self.message_list.config(yscrollcommand=self.scrollbar.set)


class BottomFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.__controller = controller
        self.__start()

    def __start(self):
        self.current_message = tkinter.Label(self, text="Current Message:")
        self.current_message.pack(side="top", fill="x", pady=2)

        self.message = tkinter.Text(self, height=5)
        self.message.pack(side="top", fill="both", padx=2, pady=2, expand=True)

        self.send_message_button = tkinter.Button(
            self,
            text="Send Message",
            command=self.__controller.message_window_actions.on_send_message_button_click
        )
        self.send_message_button.pack(side="top", fill="both", padx=2, pady=2)

