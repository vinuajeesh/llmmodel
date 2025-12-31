from .memory import MemoryManager
from .tools import SystemTools
from .model_engine import ModelEngine
import datetime
import threading
import time

class AppController:
    def __init__(self):
        self.memory = MemoryManager()
        self.engine = ModelEngine()
        self.current_conversation_id = None
        self._start_reminder_checker()

    def _start_reminder_checker(self):
        self.checker_thread = threading.Thread(target=self._check_reminders, daemon=True)
        self.checker_thread.start()

    def _check_reminders(self):
        while True:
            try:
                reminders = self.memory.get_pending_reminders()
                for r in reminders:
                    r_id, msg, r_time = r
                    # Trigger notification (simple print/callback for now)
                    print(f"REMINDER: {msg} at {r_time}")
                    self.memory.mark_reminder_complete(r_id)
            except Exception:
                pass
            time.sleep(10)

    def load_model(self, path):
        return self.engine.load_model(path)

    def create_new_chat(self):
        self.current_conversation_id = self.memory.create_conversation(f"Chat {datetime.datetime.now().strftime('%H:%M')}")
        return self.current_conversation_id

    def get_chat_history(self, conv_id):
        return self.memory.get_messages(conv_id)

    def get_all_chats(self):
        return self.memory.get_conversations()

    def set_active_chat(self, conv_id):
        self.current_conversation_id = conv_id

    def delete_chat(self, conv_id):
        self.memory.delete_conversation(conv_id)
        if self.current_conversation_id == conv_id:
            self.current_conversation_id = None

    def send_message(self, user_text, tool_enabled_flags=None):
        """
        tool_enabled_flags: dict {'web': bool, 'cmd': bool, 'screen': bool, 'network': bool}
        """
        if self.current_conversation_id is None:
            self.create_new_chat()

        self.memory.add_message(self.current_conversation_id, "user", user_text)

        # 1. Check for simple tool triggers (in a real advanced LLM, this would be an agent loop)
        # We will do simple keyword detection or LLM decision here.
        # For robustness, we will inject tool outputs into the system prompt or message history
        # if the user asks for it.

        system_context = [f"Current Date/Time: {SystemTools.get_current_time()}"]

        # Simple heuristic for tool usage if enabled
        if tool_enabled_flags:
            if tool_enabled_flags.get('web') and "search" in user_text.lower():
                res = SystemTools.search_web(user_text)
                system_context.append(f"Web Search Results: {res}")

            if tool_enabled_flags.get('screen') and ("screen" in user_text.lower() or "look" in user_text.lower()):
                # We can't actually feed the image to a text GGUF easily unless it's multimodal (Llava).
                # We will just acknowledge we took a screenshot.
                res = SystemTools.take_screenshot()
                system_context.append(f"System: {res}")

            if tool_enabled_flags.get('network') and "network" in user_text.lower():
                res = SystemTools.scan_network()
                system_context.append(f"Network Scan: {res}")

            if tool_enabled_flags.get('cmd') and "cmd" in user_text.lower() and "run" in user_text.lower():
                # Extract command roughly (very unsafe/imprecise)
                # Heuristic: assume everything after "run command" or "run cmd" is the command.
                # Example: "please run cmd echo hello" -> "echo hello"
                import re
                match = re.search(r"(run cmd|run command)\s+(.*)", user_text, re.IGNORECASE)
                if match:
                    cmd_to_run = match.group(2).strip()
                    res = SystemTools.execute_cmd(cmd_to_run)
                    system_context.append(f"Command Execution Result:\n{res}")

        # Check for reminder setting
        # Simple heuristic: "remind me to [message] in [X] [seconds|minutes|hours]"
        import re
        remind_match = re.search(r"remind me to (.+) in (\d+)\s*(seconds?|minutes?|hours?)", user_text, re.IGNORECASE)
        if remind_match:
            msg = remind_match.group(1).strip()
            amount = int(remind_match.group(2))
            unit = remind_match.group(3).lower()

            delta = 0
            if "second" in unit:
                delta = amount
            elif "minute" in unit:
                delta = amount * 60
            elif "hour" in unit:
                delta = amount * 3600

            reminder_time = datetime.datetime.now() + datetime.timedelta(seconds=delta)
            self.memory.add_reminder(msg, reminder_time.isoformat())
            system_context.append(f"System: Reminder set for '{msg}' at {reminder_time.strftime('%H:%M:%S')}.")

        # Add long term memories
        memories = self.memory.get_memories()
        if memories:
            system_context.append("Long-term Memories:\n" + "\n".join(memories))

        system_prompt = "\n".join(system_context)
        system_prompt += "\nYou are a helpful AI assistant on a Windows PC."

        # Get history
        history = self.memory.get_messages(self.current_conversation_id)
        # Filter history to just role/content
        clean_history = [{"role": m["role"], "content": m["content"]} for m in history]

        # Generator
        response_text = ""
        for chunk in self.engine.generate_response(clean_history, system_prompt=system_prompt):
            response_text += chunk
            yield chunk

        # Save AI response
        self.memory.add_message(self.current_conversation_id, "assistant", response_text)

        # Post-processing: Check if user asked to remember something
        if "remember" in user_text.lower():
            # A simple way to extract what to remember. ideally use an extraction LLM call.
            # We'll just save the user's text for now.
            self.memory.add_memory(user_text)
