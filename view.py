from tkinter import messagebox


class View:
    def __init__(self):
        self.__active_windows = {}

    def execute(self, key):
        window = self.__active_windows.get(key)[0]
        window.mainloop()

    def set_window(self, key, window, action):
        self.__active_windows[key] = window, action

    def get_window(self, key):
        return self.__active_windows.get(key)

    def destroy_window(self, key):
        window = self.__active_windows.get(key)[0]
        window.destroy()

        self.__active_windows.pop(key, (None, None))

    def window_exists(self, key):
        if self.__active_windows.get(key) is None:
            return False

        return True

    def create_messagebox(self, title, text):
        messagebox.showinfo(title, text)
