import customtkinter as ctk

class ChatFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.messages = []

    def add_message(self, role, text):
        # Create a container for the message
        msg_frame = ctk.CTkFrame(self, fg_color="transparent")
        msg_frame.grid(row=len(self.messages), column=0, sticky="ew", pady=5)
        msg_frame.columnconfigure(1, weight=1)

        if role == "user":
            # User message: Align right, different color
            lbl = ctk.CTkLabel(
                msg_frame,
                text=text,
                fg_color=("#3B8ED0", "#1F6AA5"),
                text_color="white",
                corner_radius=10,
                wraplength=400,
                anchor="e",
                justify="left"
            )
            lbl.grid(row=0, column=1, sticky="e", padx=10)
        else:
            # AI message: Align left
            lbl = ctk.CTkLabel(
                msg_frame,
                text=text,
                fg_color=("#DCE4EE", "#2B2B2B"),
                text_color=("black", "white"),
                corner_radius=10,
                wraplength=400,
                anchor="w",
                justify="left"
            )
            lbl.grid(row=0, column=0, sticky="w", padx=10)

        self.messages.append(lbl)
        # Scroll to bottom
        self._parent_canvas.yview_moveto(1.0)

        return lbl

    def update_last_message(self, text):
        if self.messages:
            last_lbl = self.messages[-1]
            last_lbl.configure(text=text)
            self._parent_canvas.yview_moveto(1.0)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.messages = []
