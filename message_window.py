import tkinter
from tkinter import ttk


class MessageWindow(tkinter.Tk):
    def __init__(self, action, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.__action = action
        self.resizable(False, False)
        self.__center_window()
        self.__start()
        self.top_frame.message_list.configure(font="calibri, 12")

    def __center_window(self):
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('+%d+%d' % (x, y))

    def __start(self):
        self.current_user_messaging = tkinter.Label(self, text="Currently Messaging:")
        self.current_user_messaging.pack(side="top", fill="x", pady=2)

        self.__container = tkinter.Frame(self)
        self.__container.pack(fill="both", expand=True)

        self.top_frame = TopFrame(self.__container, self.__action)
        self.top_frame.pack(side="top", fill="both", expand=True)

        self.bottom_frame = BottomFrame(self.__container, self.__action)
        self.bottom_frame.pack(side="top", fill="both", expand=True)

        self.bind("<Return>", self.__action.on_send_message_button_click)
        self.protocol("WM_DELETE_WINDOW", self.__action.on_close)


class TopFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.message_list = tkinter.Text(self, width=72, height=10)
        self.message_list.grid_columnconfigure(0, weight=1)
        self.message_list.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.message_list.tag_config("sender", background="grey", foreground="blue", font="calibri 12 bold")
        self.message_list.tag_config("recipient", foreground="red", font="calibri 12 bold")

        self.scrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.message_list.yview)
        self.scrollbar.grid(row=0, column=5, sticky="nsew", padx=2, pady=2)
        self.message_list.config(yscrollcommand=self.scrollbar.set)


class BottomFrame(tkinter.Frame):
    def __init__(self, parent, action):
        tkinter.Frame.__init__(self, parent)
        self.__action = action
        self.__start()

    def __start(self):
        self.current_message = tkinter.Label(self, text="Current Message:")
        self.current_message.pack(side="top", fill="x", pady=2)

        self.message = tkinter.Text(self, width=72, height=5)
        self.message.pack(side="top", fill="both", padx=2, pady=2, expand=True)

        self.send_message_button = ttk.Button(
            self,
            text="Send Message",
            command=self.__action.on_send_message_button_click
        )
        self.send_message_button.pack(side="top", fill="both", padx=2, pady=2)

