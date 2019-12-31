import messenger_window


class ChangePasswordWindowActions:
    def __init__(self, model, view, controller):
        self.__model = model
        self.__view = view
        self.__controller = controller

    def on_change_password_button_click(self):
        current_password = self.__view.get_current_window().top_frame.current_password_entry.get()
        new_password = self.__view.get_current_window().top_frame.new_password_entry.get()

        if len(current_password) <= 0 or len(new_password) <= 0:
            self.__view.create_messagebox("Change Password", "Error: Password must be at least 1 character")
        else:
            if not self.__model.change_password(current_password, new_password):
                self.__view.create_messagebox("Change Password", "Error: Invalid login information")
            else:
                username = self.__model.get_username()

                self.__view.create_messagebox("Change Password", "Success: Successfully changed password")
                self.__view.destroy_current_window()
                self.__view.set_current_window(messenger_window.MessengerWindow(self.__controller, username))
                self.__controller.messenger_window_actions.on_messenger_window()

    def on_close(self):
        username = self.__model.get_username()

        self.__view.destroy_current_window()
        self.__view.set_current_window(messenger_window.MessengerWindow(self.__controller, username))
        self.__controller.messenger_window_actions.on_messenger_window()

