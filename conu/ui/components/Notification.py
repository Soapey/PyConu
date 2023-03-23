from tkinter import Tk, Label, Button
from helpers import darken_color


class Notification:
    def __init__(self, title, messages, bg_color, font_color):

        self.title = title
        self.messages = messages
        self.bg_color = bg_color
        self.font_color = font_color

    def show(self):
        root = Tk()
        root.overrideredirect(True)

        # Create a label with the title and messages
        message = "\n".join(self.messages)
        label = Label(
            root,
            text=f"{self.title}\n\n{message}",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.font_color,
            padx=10,
            pady=20,
            justify="left",
            wraplength=400,
        )
        label.pack()

        # Create a button with "X" symbol to close the window
        close_button_width = 20
        close_button_height = 20
        button_bg_color_rgb = darken_color(self.bg_color, 30)
        button_bg_color = f"#{button_bg_color_rgb[0]:02x}{button_bg_color_rgb[1]:02x}{button_bg_color_rgb[2]:02x}"
        close_button = Button(
            root,
            text="X",
            bg=button_bg_color,
            fg=self.font_color,
            font=("Arial", 12),
            relief="flat",
            borderwidth=0,
            command=root.destroy,
            cursor="hand2",
        )

        # Center the window and set the title
        root.title(self.title)
        root.update_idletasks()
        x = 0
        y = 0
        root.geometry(f"+{x}+{y}")
        root_width = root.winfo_width()
        close_button.place(
            x=root_width - close_button_width,
            y=0,
            width=close_button_width,
            height=close_button_height,
        )

        # Set the duration and close the window after the specified time
        root.after(int(len(self.messages) * 1000), root.destroy)
        root.mainloop()


class ErrorNotification(Notification):
    def __init__(self, title, messages):
        super().__init__(title, messages, "#e63946", "ffffff")


class SuccessNotification(Notification):
    def __init__(self, title, messages):
        super().__init__(title, messages, "#c7f9cc", "000000")
