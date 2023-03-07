import winotify


class Notification(winotify.Notification):
    def __init__(self, title, message_list):
        super().__init__(
            app_id="Conu",
            title=title,
            msg="\n".join(f"• {message}" for message in message_list),
            icon=str()
        )