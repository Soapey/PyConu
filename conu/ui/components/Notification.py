import tkinter as tk
import threading
from enum import Enum


class NotificationColour(Enum):

    SUCCESS = "#74c69d"
    ERROR = "#FF0000"


class Notification:
    def __init__(
        self, title, message_items, bg_color: NotificationColour, duration=3000
    ):
        self.title = title
        self.message_items = message_items
        self.bg_color = bg_color.value
        self.duration = duration

    def show(self):
        message = "\n".join([f"• {m}" for m in self.message_items])

        def show_notification():
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry("+{}+{}".format(root.winfo_screenwidth(), 0))
            root.configure(bg=self.bg_color)

            # Create title label
            title_label = tk.Label(
                root,
                text=self.title,
                fg="white",
                bg=self.bg_color,
                font=("Arial", 14, "bold"),
            )
            title_label.pack(side="top", fill="x")

            # Create message label
            message_label = tk.Label(
                root, text=message, fg="white", bg=self.bg_color, font=("Arial", 12)
            )
            message_label.pack(side="top", fill="x")

            # Resize window to fit contents
            root.update_idletasks()
            width = root.winfo_reqwidth()
            height = root.winfo_reqheight()
            x = root.winfo_screenwidth() - width
            y = 0
            root.geometry("{}x{}+{}+{}".format(width, height, x, y))

            # Set timeout to close notification after duration
            root.after(self.duration, root.destroy)

            root.mainloop()

        # Run show_notification function in a separate thread
        t = threading.Thread(target=show_notification)
        t.start()
