class ChangePasswordWindowActions:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__key = None

    def on_change_password_window(self, key, window):
        self.__key = key
        self.__view.set_window(self.__key, window, self)
        self.focus_window()

    def on_change_password_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        current_password = window.top_frame.current_password_entry.get()
        new_password = window.top_frame.new_password_entry.get()

        if len(current_password) <= 0 or len(new_password) <= 0:
            self.__view.create_messagebox("Change Password", "Error: Password must be at least 1 character")
        else:
            if not self.__model.change_password(current_password, new_password):
                self.__view.create_messagebox("Change Password", "Error: Invalid login information")
            else:
                self.__view.create_messagebox("Change Password", "Success: Successfully changed password")
                self.__view.destroy_window(self.__key)

    def on_close(self):
        self.__view.destroy_window(self.__key)

    def focus_window(self):
        window = self.__view.get_window(self.__key)[0]
        window.lift()
        window.focus_force()

