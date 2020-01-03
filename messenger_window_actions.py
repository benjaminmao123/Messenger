import tkinter
import change_password_window
import login_register_window
import message_window
import change_password_window_actions
import login_register_window_actions
import message_window_actions


class MessengerWindowActions:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.after_id_list = []
        self.__key = None

    def on_search_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        username = window.left_frame.search_entry.get()

        if len(username) > 0 and username is not None:
            result = self.__model.search_user(username)

            if result is not None:
                window.left_frame.found_user_list.delete(0, tkinter.END)

                for user in result:
                    window.left_frame.found_user_list.insert(tkinter.END, user)

    def on_send_friend_request_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        selection = window.left_frame.found_user_list.curselection()

        if selection:
            username = window.left_frame.found_user_list.get(
                            window.left_frame.found_user_list.curselection()
                        )

            if not self.__model.send_friend_request(username):
                self.__view.create_messagebox("Send Friend Request", "Error: Request has already been sent")

    def on_friend_request(self):
        window = self.__view.get_window(self.__key)[0]

        username = self.__model.get_most_recent_friend_request()
        window.right_frame.friend_request_list.insert(tkinter.END, username)

        after_id = window.after(
            100,
            self.on_friend_request
        )
        self.after_id_list.append(after_id)

    def on_messenger_window(self, key, window):
        self.__key = key
        self.__view.set_window(self.__key, window, self)

        result = self.__model.get_friends_list()

        for username in result:
            window.middle_frame.friends_list.insert(tkinter.END, username)

        result = self.__model.get_friend_requests()

        for username in result:
            window.right_frame.friend_request_list.insert(tkinter.END, username)

        username = self.__model.get_username()

        window.username_label.config(text="Username: " + username)

        self.on_ui_change()

    def on_accept_friend_request_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        selection = window.right_frame.friend_request_list.curselection()

        if selection:
            username = window.right_frame.friend_request_list.get(
                            window.right_frame.friend_request_list.curselection()
                       )

            window.right_frame.friend_request_list.delete(
                window.right_frame.friend_request_list.curselection()
            )

            self.__model.accept_friend_request(username)
            window.middle_frame.friends_list.insert(tkinter.END, username)

    def on_decline_friend_request_button_click(self):
        window = self.__view.get_window(self.__key)[0]

        selection = window.right_frame.friend_request_list.curselection()

        if selection:
            username = window.right_frame.friend_request_list.get(
                            window.right_frame.friend_request_list.curselection()
                       )

            window.right_frame.friend_request_list.delete(
                window.right_frame.friend_request_list.curselection()
            )

            self.__model.decline_friend_request(username)

    def on_ui_change(self):
        window = self.__view.get_window(self.__key)[0]

        result = self.__model.get_most_recent_change()

        if result[0] != "":
            window.middle_frame.friends_list.insert(tkinter.END, result[0])
        elif result[1] != "":
            window.right_frame.friend_request_list.insert(tkinter.END, result[1])
        elif result[2] != "":
            result = self.__model.get_friends_list()

            window.middle_frame.friends_list.delete(0, tkinter.END)

            for user in result:
                window.right_frame.friend_request_list.insert(tkinter.END, user)

        after_id = window.after(
            100,
            self.on_ui_change
        )
        self.after_id_list.append(after_id)

    def on_change_password_button_click(self):
        key = "change_password_window"

        if self.__view.window_exists(key):
            action = change_password_window_actions.ChangePasswordWindowActions(
                self.__model,
                self.__view
            )
            window = change_password_window.ChangePasswordWindow(action)
            action.on_change_password_window(key, window)

    def on_logout_button_click(self):
        self.__model.logout()

        self.__delete_after()

        self.__view.destroy_window(self.__key)

        key = "login_window"
        action = login_register_window_actions.LoginRegisterWindowActions(
            self.__model,
            self.__view
        )
        window = login_register_window.LoginRegisterWindow(action)
        action.on_login_register_window(key, window)

    def on_close(self):
        self.__delete_after()

        self.__model.exit()
        self.__view.destroy_window(self.__key)

    def on_message_user_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        selection_friends = window.middle_frame.friends_list.curselection()
        selection_found_user = window.left_frame.found_user_list.curselection()

        if selection_friends:
            username = window.middle_frame.friends_list.get(
                            window.middle_frame.friends_list.curselection()
                       )

            key = "message_window_" + username

            if self.__view.window_exists(key):
                action = self.__view.get_window(key)[1]
                action.focus_window()
            else:
                action = message_window_actions.MessageWindowActions(
                    self.__model,
                    self.__view
                )
                window = message_window.MessageWindow(action)
                action.on_message_window(key, window, username)

        if selection_found_user:
            username = window.left_frame.found_user_list.get(
                window.left_frame.found_user_list.curselection()
            )

            key = "message_window_" + username

            if self.__view.window_exists(key):
                action = self.__view.get_window(key)[1]
                action.focus_window()
            else:
                action = message_window_actions.MessageWindowActions(
                    self.__model,
                    self.__view
                )
                window = message_window.MessageWindow(action)
                action.on_message_window(key, window, username)

    def on_delete_user_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        selection = window.middle_frame.friends_list.curselection()

        if selection:
            username = window.middle_frame.friends_list.get(
                window.middle_frame.friends_list.curselection()
            )

            self.__model.delete_friend(username)
            window.middle_frame.friends_list.delete(selection)

    def __delete_after(self):
        window = self.__view.get_window(self.__key)[0]

        for after_id in self.after_id_list:
            window.after_cancel(after_id)

    def focus_window(self):
        window = self.__view.get_window(self.__key)[0]
        window.lift()
        window.focus_force()


