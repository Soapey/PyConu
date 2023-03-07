import winotify


class Notification(winotify.Notification):
    def __init__(self, title, message_list):

        if not message_list:
            message = str()
        elif len(message_list) == 1:
            message = message_list[0]
        else:
            message = "\n".join(f"• {message}" for message in message_list)

        super().__init__(
            app_id="Conu",
            title=title,
            msg=message,
            icon=str()
        )