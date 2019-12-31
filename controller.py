import model
import view
import login_register_window
import login_window_actions
import messenger_window_actions
import change_password_window_actions
import message_window_actions


class Controller:
    def __init__(self):
        self.__model = model.Model()
        self.__view = view.View()
        self.login_window_actions = login_window_actions.LoginWindowActions(
            self.__model,
            self.__view,
            self
        )
        self.messenger_window_actions = messenger_window_actions.MessengerWindowActions(
            self.__model,
            self.__view,
            self
        )
        self.change_password_window_actions = change_password_window_actions.ChangePasswordWindowActions(
            self.__model,
            self.__view,
            self
        )
        self.message_window_actions = message_window_actions.MessageWindowActions(
            self.__model,
            self.__view,
            self
        )

    def execute(self):
        self.__view.set_current_window(login_register_window.LoginRegisterWindow(self))
        self.__view.execute()



