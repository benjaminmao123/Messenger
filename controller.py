import model
import view
import login_register_window
import login_register_window_actions


class Controller:
    def __init__(self):
        self.__model = model.Model()
        self.__view = view.View()

    def execute(self):
        key = "login_window"
        action = login_register_window_actions.LoginRegisterWindowActions(self.__model, self.__view)
        window = login_register_window.LoginRegisterWindow(action)
        action.on_login_register_window(key, window)

        self.__view.execute(key)



