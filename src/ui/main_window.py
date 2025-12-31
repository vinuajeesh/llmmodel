import customtkinter as ctk
import threading
import tkinter as tk
from .chat_frame import ChatFrame
from .sidebar import Sidebar
from backend.controller import AppController

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Local AI Chat")
        self.geometry("1000x600")

        self.controller = AppController()

        # Layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(
            self,
            on_new_chat=self.new_chat,
            on_chat_select=self.load_chat,
            on_model_load=self.load_model,
            on_delete_chat=self.delete_chat,
            width=200
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main Chat Area
        self.chat_area = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.chat_area.grid_rowconfigure(0, weight=1)
        self.chat_area.grid_columnconfigure(0, weight=1)

        self.chat_display = ChatFrame(self.chat_area)
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Input Area
        self.input_frame = ctk.CTkFrame(self.chat_area)
        self.input_frame.grid(row=1, column=0, sticky="ew")

        self.msg_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type a message...")
        self.msg_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message, width=60)
        self.send_btn.pack(side="right")

        # Tools Toggles
        self.tools_frame = ctk.CTkFrame(self.chat_area, height=30)
        self.tools_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))

        self.tool_web = ctk.CTkSwitch(self.tools_frame, text="Web Search")
        self.tool_web.pack(side="left", padx=5)

        self.tool_cmd = ctk.CTkSwitch(self.tools_frame, text="CMD (Risky)")
        self.tool_cmd.pack(side="left", padx=5)

        self.tool_screen = ctk.CTkSwitch(self.tools_frame, text="View Screen")
        self.tool_screen.pack(side="left", padx=5)

        self.tool_net = ctk.CTkSwitch(self.tools_frame, text="Network")
        self.tool_net.pack(side="left", padx=5)

        # Initial Load
        self.refresh_history_list()
        self.new_chat()

    def new_chat(self):
        self.controller.create_new_chat()
        self.chat_display.clear()
        self.refresh_history_list()

    def load_chat(self, conv_id):
        self.controller.set_active_chat(conv_id)
        self.chat_display.clear()
        messages = self.controller.get_chat_history(conv_id)
        for msg in messages:
            self.chat_display.add_message(msg['role'], msg['content'])

    def delete_chat(self, conv_id):
        self.controller.delete_chat(conv_id)
        self.refresh_history_list()
        # If deleted current chat, create new one
        if self.controller.current_conversation_id is None:
            self.new_chat()

    def load_model(self, path):
        # Run in thread to not freeze UI
        def _load():
            success, msg = self.controller.load_model(path)
            self.sidebar.load_btn.configure(text="Loaded" if success else "Error")
            print(msg)

        self.sidebar.load_btn.configure(text="Loading...")
        threading.Thread(target=_load, daemon=True).start()

    def refresh_history_list(self):
        chats = self.controller.get_all_chats()
        self.sidebar.update_history(chats)

    def send_message(self):
        text = self.msg_entry.get()
        if not text.strip():
            return

        self.msg_entry.delete(0, "end")
        self.chat_display.add_message("user", text)

        # Prepare tool flags
        tools = {
            "web": self.tool_web.get() == 1,
            "cmd": self.tool_cmd.get() == 1,
            "screen": self.tool_screen.get() == 1,
            "network": self.tool_net.get() == 1
        }

        # Create placeholder for AI response
        ai_msg_widget = self.chat_display.add_message("assistant", "...")

        def _process():
            response_text = ""
            try:
                for chunk in self.controller.send_message(text, tool_enabled_flags=tools):
                    response_text += chunk
                    # Update UI in main thread safely
                    self.after(0, lambda t=response_text: ai_msg_widget.configure(text=t))
            except Exception as e:
                self.after(0, lambda err=e: ai_msg_widget.configure(text=f"Error: {err}"))

            # Refresh history title if needed (could update title based on first msg)
            self.after(0, self.refresh_history_list)

        threading.Thread(target=_process, daemon=True).start()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
