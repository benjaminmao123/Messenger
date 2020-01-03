import messenger_window
import messenger_window_actions


class LoginRegisterWindowActions:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__key = None

    def on_login_register_window(self, key, window):
        self.__key = key
        self.__view.set_window(self.__key, window, self)

    def on_login_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        username = window.top_frame.username_entry.get()
        password = window.top_frame.password_entry.get()

        if len(username) <= 0:
            self.__view.create_messagebox("Register", "Error: Username must be at least 1 character")
        elif len(password) <= 0:
            self.__view.create_messagebox("Register", "Error: Password must be at least 1 character")
        else:
            if not self.__model.login(username, password):
                self.__view.create_messagebox("Login", "Error: Invalid login information")
            else:
                self.__view.create_messagebox("Login", "Success: Successfully logged in")
                self.__view.destroy_window(self.__key)

                key = "messenger_window"
                action = messenger_window_actions.MessengerWindowActions(self.__model, self.__view)
                window = messenger_window.MessengerWindow(action)
                action.on_messenger_window(key, window)

    def on_register_button_click(self):
        window = self.__view.get_window(self.__key)[0]

        username = window.top_frame.username_entry.get()
        password = window.top_frame.password_entry.get()

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
        self.__view.destroy_window(self.__key)

    def focus_window(self):
        window = self.__view.get_window(self.__key)[0]
        window.lift()
        window.focus_force()