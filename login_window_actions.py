import messenger_window


class LoginWindowActions:
    def __init__(self, model, view, controller):
        self.__model = model
        self.__view = view
        self.__controller = controller

    def on_login_button_click(self):
        username = self.__view.get_current_window().top_frame.username_entry.get()
        password = self.__view.get_current_window().top_frame.password_entry.get()

        if len(username) <= 0:
            self.__view.create_messagebox("Register", "Error: Username must be at least 1 character")
        elif len(password) <= 0:
            self.__view.create_messagebox("Register", "Error: Password must be at least 1 character")
        else:
            if not self.__model.login(username, password):
                self.__view.create_messagebox("Login", "Error: Invalid login information")
            else:
                self.__view.create_messagebox("Login", "Success: Successfully logged in")
                self.__view.destroy_current_window()
                self.__view.set_current_window(messenger_window.MessengerWindow(self.__controller))
                self.__controller.messenger_window_actions.on_messenger_window()

    def on_register_button_click(self):
        username = self.__view.get_current_window().top_frame.username_entry.get()
        password = self.__view.get_current_window().top_frame.password_entry.get()

        if len(username) <= 0:
            self.__view.create_messagebox("Register", "Error: Username must be at least 1 character")
        elif len(password) <= 0:
            self.__view.create_messagebox("Register", "Error: Password must be at least 1 character")
        else:
            if not self.__model.register(username, password):
                self.__view.create_messagebox("Register", "Error: Username already exists")
            else:
                self.__view.create_messagebox("Register", "Success: Account successfully created")

    def on_close(self):
        self.__model.exit()
        self.__view.destroy_current_window()
