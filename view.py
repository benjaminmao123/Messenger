from tkinter import messagebox


class View:
    def __init__(self):
        self.__current_window = None
        self.current_open_windows = []

    def execute(self):
        self.__current_window.mainloop()

    def set_current_window(self, window):
        self.__current_window = window
        self.current_open_windows.append(self.__current_window)

    def get_current_window(self):
        return self.__current_window

    def destroy_current_window(self):
        self.current_open_windows.remove(self.__current_window)
        self.__current_window.destroy()
        self.__current_window = None

    def create_messagebox(self, title, text):
        messagebox.showinfo(title, text)


