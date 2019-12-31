import tkinter
import change_password_window
import login_register_window
import message_window


class MessengerWindowActions:
    def __init__(self, model, view, controller):
        self.__model = model
        self.__view = view
        self.__controller = controller
        self.after_id_list = []

    def on_search_button_click(self):
        username = self.__view.get_current_window().left_frame.search_entry.get()

        if len(username) > 0 and username is not None:
            result = self.__model.search_user(username)

            if result is not None:
                self.__view.get_current_window().left_frame.found_user_list.delete(0, tkinter.END)
                self.__view.get_current_window().left_frame.found_user_list.insert(tkinter.END, result)

    def on_send_friend_request_button_click(self):
        selection = self.__view.get_current_window().left_frame.found_user_list.curselection()

        if selection:
            username = self.__view.get_current_window().left_frame.found_user_list.get(
                            self.__view.get_current_window().left_frame.found_user_list.curselection()
                        )

            if not self.__model.send_friend_request(username):
                self.__view.create_messagebox("Send Friend Request", "Error: Request has already been sent")

    def on_friend_request(self):
        result = self.__model.get_friend_requests()

        self.__view.get_current_window().right_frame.friend_request_list.delete(0, tkinter.END)

        for username in result:
            self.__view.get_current_window().right_frame.friend_request_list.insert(tkinter.END, username)

        after_id = self.__view.get_current_window().after(
            5000,
            self.__controller.messenger_window_actions.on_friend_request
        )

        self.after_id_list.append(after_id)

    def on_messenger_window(self):
        self.on_friend_request()
        self.on_friends_list()

        username = self.__model.get_username()
        self.__view.get_current_window().username_label.config(text="Username: " + username)

    def on_accept_friend_request_button_click(self):
        selection = self.__view.get_current_window().right_frame.friend_request_list.curselection()

        if selection:
            username = self.__view.get_current_window().right_frame.friend_request_list.get(
                            self.__view.get_current_window().right_frame.friend_request_list.curselection()
                       )

            self.__view.get_current_window().right_frame.friend_request_list.delete(
                self.__view.get_current_window().right_frame.friend_request_list.curselection()
            )

            self.__model.accept_friend_request(username)
            self.__view.get_current_window().middle_frame.friends_list.insert(tkinter.END, username)

    def on_decline_friend_request_button_click(self):
        selection = self.__view.get_current_window().right_frame.friend_request_list.curselection()

        if selection:
            username = self.__view.get_current_window().right_frame.friend_request_list.get(
                            self.__view.get_current_window().right_frame.friend_request_list.curselection()
                       )

            self.__view.get_current_window().right_frame.friend_request_list.delete(
                self.__view.get_current_window().right_frame.friend_request_list.curselection()
            )

            self.__model.decline_friend_request(username)

    def on_friends_list(self):
        result = self.__model.get_friends_list()

        self.__view.get_current_window().middle_frame.friends_list.delete(0, tkinter.END)

        for username in result:
            self.__view.get_current_window().middle_frame.friends_list.insert(tkinter.END, username)

        after_id = self.__view.get_current_window().after(
            5000,
            self.__controller.messenger_window_actions.on_friends_list
        )

        self.after_id_list.append(after_id)

    def on_change_password_button_click(self):
        for after_id in self.after_id_list:
            self.__view.get_current_window().after_cancel(after_id)

        self.__view.destroy_current_window()
        self.__view.set_current_window(change_password_window.ChangePasswordWindow(self.__controller))

    def on_logout_button_click(self):
        self.__model.logout()

        for after_id in self.after_id_list:
            self.__view.get_current_window().after_cancel(after_id)

        self.__view.destroy_current_window()
        self.__view.set_current_window(login_register_window.LoginRegisterWindow(self.__controller))

    def on_close(self):
        for after_id in self.after_id_list:
            self.__view.get_current_window().after_cancel(after_id)

        self.__controller.login_window_actions.on_close()

    def on_message_user_button_click(self):
        selection = self.__view.get_current_window().middle_frame.friends_list.curselection()

        if selection:
            username = self.__view.get_current_window().middle_frame.friends_list.get(
                            self.__view.get_current_window().middle_frame.friends_list.curselection()
                       )

            for after_id in self.after_id_list:
                self.__view.get_current_window().after_cancel(after_id)

            self.__view.destroy_current_window()
            self.__view.set_current_window(message_window.MessageWindow(self.__controller))
            self.__controller.message_window_actions.on_message_window(username)





