import tkinter


class MessageWindowActions:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__recipient_username = None
        self.__current_username = None
        self.after_id_list = []
        self.__key = None

    def __delete_after(self):
        window = self.__view.get_window(self.__key)[0]

        for after_id in self.after_id_list:
            window.after_cancel(after_id)

    def on_close(self):
        self.__delete_after()

        self.__view.destroy_window(self.__key)

    def focus_window(self):
        window = self.__view.get_window(self.__key)[0]
        window.lift()
        window.focus_force()

    def on_message_window(self, key, window, username):
        self.__key = key
        self.__view.set_window(self.__key, window, self)
        self.focus_window()

        window.current_user_messaging.config(text="Currently Messaging: " + username)

        self.__current_username = self.__model.get_username()
        self.__recipient_username = username

        messages = self.__model.get_messages(self.__recipient_username)

        for message in messages:
            try:
                if message[:len(self.__recipient_username) + 1] == self.__recipient_username + ":":
                    window.top_frame.message_list.configure(state="normal")
                    window.top_frame.message_list.insert("insert", message, "recipient")
                    window.top_frame.message_list.configure(state="disabled")
                else:
                    window.top_frame.message_list.configure(state="normal")
                    window.top_frame.message_list.insert("insert", message, "sender")
                    window.top_frame.message_list.configure(state="disabled")
            except IndexError:
                window.top_frame.message_list.configure(state="normal")
                window.top_frame.message_list.insert("insert", message, "recipient")
                window.top_frame.message_list.configure(state="disabled")

        window.top_frame.message_list.see(tkinter.END)
        window.top_frame.message_list.configure(state="disabled")

        self.on_message()

    def on_send_message_button_click(self, event=None):
        window = self.__view.get_window(self.__key)[0]

        message = window.bottom_frame.message.get("1.0", "end-1c")
        window.bottom_frame.message.delete("1.0", tkinter.END)

        if len(message) > 0:
            self.__model.message_user(self.__recipient_username, message)

    def on_message(self):
        window = self.__view.get_window(self.__key)[0]

        text = self.__model.get_most_recent_message(self.__recipient_username)

        if text != "" and text is not None:
            try:
                if text[:len(self.__recipient_username) + 1] == self.__recipient_username + ":":
                    window.top_frame.message_list.configure(state="normal")
                    window.top_frame.message_list.insert("insert", text, "recipient")
                    window.top_frame.message_list.configure(state="disabled")
                else:
                    window.top_frame.message_list.configure(state="normal")
                    window.top_frame.message_list.insert("insert", text, "sender")
                    window.top_frame.message_list.configure(state="disabled")
            except IndexError:
                window.top_frame.message_list.configure(state="normal")
                window.top_frame.message_list.insert("insert", text, "recipient")
                window.top_frame.message_list.configure(state="disabled")

            window.top_frame.message_list.see(tkinter.END)

        after_id = window.after(
            100,
            self.on_message
        )
        self.after_id_list.append(after_id)

