import messenger_window
import tkinter


class MessageWindowActions:
    def __init__(self, model, view, controller):
        self.__model = model
        self.__view = view
        self.__controller = controller
        self.__recipient_username = None
        self.after_id_list = []

    def on_close(self):
        username = self.__model.get_username()

        for after_id in self.after_id_list:
            self.__view.get_current_window().after_cancel(after_id)

        self.__view.destroy_current_window()
        self.__view.set_current_window(messenger_window.MessengerWindow(self.__controller, username))
        self.__controller.messenger_window_actions.on_friend_request()
        self.__controller.messenger_window_actions.on_friends_list()

    def on_message_window(self, username):
        self.__recipient_username = username
        self.__view.get_current_window().current_user_messaging.config(text="Currently Messaging: " + username)
        messages = self.__model.get_messages(self.__recipient_username)

        for message in messages:
            self.__view.get_current_window().top_frame.message_list.insert(tkinter.END, message)

        self.on_message()

    def on_send_message_button_click(self, event=None):
        message = self.__view.get_current_window().bottom_frame.message.get("1.0", "end-1c")
        self.__view.get_current_window().bottom_frame.message.delete("1.0", tkinter.END)

        if len(message) > 0:
            self.__model.message_user(self.__recipient_username, message)

    def on_message(self):
        text = self.__model.get_most_recent_message()

        if text is not None:
            self.__view.get_current_window().top_frame.message_list.insert(tkinter.END, text)

        after_id = self.__view.get_current_window().after(
            100,
            self.__controller.message_window_actions.on_message
        )

        self.after_id_list.append(after_id)
        self.__view.get_current_window().top_frame.message_list.see(tkinter.END)

