import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_new_chat, on_chat_select, on_model_load, on_delete_chat, **kwargs):
        super().__init__(master, **kwargs)
        self.on_new_chat = on_new_chat
        self.on_chat_select = on_chat_select
        self.on_model_load = on_model_load
        self.on_delete_chat = on_delete_chat

        # Title
        self.logo_label = ctk.CTkLabel(self, text="AI Assistant", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # New Chat Button
        self.new_chat_btn = ctk.CTkButton(self, text="New Chat", command=self.on_new_chat)
        self.new_chat_btn.grid(row=1, column=0, padx=20, pady=10)

        # Model Loader
        self.model_frame = ctk.CTkFrame(self)
        self.model_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.model_path_entry = ctk.CTkEntry(self.model_frame, placeholder_text="Path to .gguf")
        self.model_path_entry.pack(side="top", fill="x", padx=5, pady=5)

        self.load_btn = ctk.CTkButton(self.model_frame, text="Load Model", command=self._load_model_handler, width=80)
        self.load_btn.pack(side="top", pady=5)

        # History List (Scrollable)
        self.history_frame = ctk.CTkScrollableFrame(self, label_text="History")
        self.history_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(3, weight=1)

    def _load_model_handler(self):
        path = self.model_path_entry.get()
        if path:
            self.on_model_load(path)

    def update_history(self, conversations):
        # Clear existing
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for conv in conversations:
            c_id, title, _ = conv

            # Container for chat item
            item_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)

            # Button for selecting chat
            btn = ctk.CTkButton(
                item_frame,
                text=title,
                command=lambda cid=c_id: self.on_chat_select(cid),
                fg_color="transparent",
                border_width=1,
                text_color=("gray10", "#DCE4EE"),
                anchor="w",
                width=140
            )
            btn.pack(side="left", fill="x", expand=True)

            # Delete button (small 'X')
            del_btn = ctk.CTkButton(
                item_frame,
                text="X",
                command=lambda cid=c_id: self.on_delete_chat(cid),
                width=30,
                fg_color="#CC0000",
                hover_color="#AA0000"
            )
            del_btn.pack(side="right", padx=(2,0))
