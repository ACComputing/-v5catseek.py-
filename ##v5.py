import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
import time
import random
from dataclasses import dataclass


# ==== CatSEEK R1 backend (no files, no API keys, pure software) ====
@dataclass
class CatSEEKConfig:
    name: str = "CatSEEK‑R1‑2B"
    max_tokens: int = 512
    temperature: float = 0.7


class CatSEEKLLM:
    """
    A playful mock of a 2B‑parameter CatSEEK R1 LLM.
    No files, no network, no API keys – just clever Python.
    Generates keyword‑driven responses from a built‑in phrase bank.
    """

    def __init__(self, config: CatSEEKConfig | None = None):
        self.config = config or CatSEEKConfig()
        # Built‑in phrase bank (no external files)
        self.phrases = {
            "greeting": [
                "Meow! How can I assist you today?",
                "Hi there! What's on your mind?",
                "Greetings! I'm ready to help.",
            ],
            "farewell": [
                "Goodbye! Feel free to return anytime.",
                "Take care! If you have more questions, I'm here.",
                "Bye! It was nice chatting with you.",
            ],
            "thanks": [
                "You're welcome! Happy to help.",
                "My pleasure! Anything else?",
                "Glad I could assist!",
            ],
            "name": [
                "I'm CatSEEK R1, a 2B parameter model.",
                "You can call me CatSEEK R1. I'm a distilled 2B model.",
                "I'm your AI assistant, based on CatSEEK architecture.",
            ],
            "capabilities": [
                "I can answer questions, help with writing, explain concepts, and more.",
                "My training covers a wide range of topics up to early 2025.",
                "I'm designed to be helpful, harmless, and honest.",
            ],
            "default": [
                "That's interesting. Could you tell me more?",
                "I see. Let me think about that for a moment.",
                "Hmm, I need a bit more context to give a good answer.",
                "Interesting question! Here's what I think...",
            ],
        }

    def generate(self, prompt: str) -> str:
        """
        Generate a response – entirely local, no I/O.
        Uses keyword matching and random selection from built‑in phrases.
        """
        # Simulate thinking time (varies a bit)
        time.sleep(random.uniform(0.5, 1.2))

        text = prompt.strip().lower()
        if not text:
            return "🐱 CatSEEK R1: Please say something – I'm listening."

        # Keyword‑based routing
        if any(word in text for word in ["hello", "hi", "hey", "greetings"]):
            category = "greeting"
        elif any(word in text for word in ["bye", "goodbye", "see you", "later"]):
            category = "farewell"
        elif any(word in text for word in ["thank", "thanks", "appreciate"]):
            category = "thanks"
        elif any(word in text for word in ["your name", "who are you", "call you"]):
            category = "name"
        elif any(word in text for word in ["what can you do", "capabilities", "help"]):
            category = "capabilities"
        else:
            category = "default"

        # Pick a random phrase from the chosen category
        base = random.choice(self.phrases[category])

        # Sometimes add a bit of "reasoning" trace (optional)
        if random.random() < 0.3:  # 30% chance
            trace = (
                "🧠 Activating 2 of 16 experts via MoE router...\n"
                "   Multi‑Head Latent Attention applied.\n"
                "   Generating response...\n\n"
            )
        else:
            trace = ""

        return f"🐱 CatSEEK R1 (2B, MoE+MLA):\n{trace}{base}"


# ==== GUI app (CatSEEK R1 themed) ====
class CatSEEKChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CatSEEK R1 · 2B Chat")
        self.geometry("900x600")
        self.minsize(600, 400)

        # Optional modern ttk theme
        try:
            self.style = ttk.Style(self)
            if "clam" in self.style.theme_names():
                self.style.theme_use("clam")
        except Exception:
            pass

        self.configure(bg="#020617")

        # Backend LLM – pure software, no files/keys
        self.llm = CatSEEKLLM()
        self._current_thread: threading.Thread | None = None

        self._build_layout()

    def _build_layout(self):
        # Header bar
        header = tk.Frame(self, bg="#020617", height=48)
        header.pack(side=tk.TOP, fill=tk.X)

        title_label = tk.Label(
            header,
            text="CatSEEK R1",
            fg="#e5e7eb",
            bg="#020617",
            font=("Segoe UI", 14, "bold"),
        )
        title_label.pack(side=tk.LEFT, padx=14, pady=(10, 6))

        model_pill = tk.Label(
            header,
            text="2B (MoE + MLA) · pure software mock",
            fg="#e5e7eb",
            bg="#111827",
            font=("Segoe UI", 9),
            padx=10,
            pady=3,
        )
        model_pill.pack(side=tk.LEFT, padx=(8, 0), pady=(12, 6))

        clear_btn = tk.Button(
            header,
            text="Clear chat",
            command=self._clear_chat,
            bg="#020617",
            fg="#9ca3af",
            activebackground="#111827",
            activeforeground="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=2,
        )
        clear_btn.pack(side=tk.RIGHT, padx=14, pady=(10, 6))

        # Chat area
        main_frame = tk.Frame(self, bg="#020617")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=(2, 4))

        self.chat_box = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#020617",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True)

        # Input area
        input_container = tk.Frame(self, bg="#020617")
        input_container.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=(4, 12))

        input_frame = tk.Frame(input_container, bg="#020617")
        input_frame.pack(side=tk.TOP, fill=tk.X)

        self.input_text = tk.Text(
            input_frame,
            height=3,
            bg="#020617",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 4), pady=4)
        self.input_text.bind("<Return>", self._on_enter_pressed)

        buttons_frame = tk.Frame(input_frame, bg="#020617")
        buttons_frame.pack(side=tk.RIGHT, padx=(4, 0), pady=4)

        stop_btn = tk.Button(
            buttons_frame,
            text="Stop",
            command=self._stop_response,
            bg="#111827",
            fg="#e5e7eb",
            activebackground="#1f2937",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        stop_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))

        send_btn = tk.Button(
            buttons_frame,
            text="Send",
            command=self._on_send_click,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        send_btn.pack(side=tk.TOP, fill=tk.X)

        hint_label = tk.Label(
            input_container,
            text="🐱 Pure software · No files, no API keys · Keyword‑driven responses",
            fg="#6b7280",
            bg="#020617",
            font=("Segoe UI", 8),
            anchor="w",
        )
        hint_label.pack(side=tk.TOP, fill=tk.X, padx=(4, 4), pady=(2, 0))

        # Initial message
        self._append_message(
            "system",
            "Welcome to CatSEEK R1 (2B).\n"
            "This is a pure‑software mock – responses vary based on your input.\n"
            "Type below and press Enter (Shift+Enter for newline).",
        )

        self.after(200, lambda: self.input_text.focus_set())

    # ==== Chat helpers ====
    def _append_message(self, sender: str, message: str):
        self.chat_box.config(state=tk.NORMAL)

        if sender == "user":
            label = "You"
            tag = "user"
        elif sender == "assistant":
            label = "CatSEEK R1"
            tag = "assistant"
        else:
            label = ""
            tag = "system"

        if self.chat_box.index("end-1c") != "1.0":
            self.chat_box.insert(tk.END, "\n")

        if label:
            self.chat_box.insert(tk.END, f"{label}:\n", (f"{tag}_label",))
        self.chat_box.insert(tk.END, message + "\n", (tag,))

        self.chat_box.tag_config(
            "user_label",
            foreground="#a5b4fc",
            font=("Segoe UI", 9, "bold"),
        )
        self.chat_box.tag_config(
            "assistant_label",
            foreground="#6ee7b7",
            font=("Segoe UI", 9, "bold"),
        )
        self.chat_box.tag_config(
            "user",
            foreground="#e5e7eb",
            font=("Segoe UI", 10),
        )
        self.chat_box.tag_config(
            "assistant",
            foreground="#d1fae5",
            font=("Segoe UI", 10),
        )
        self.chat_box.tag_config(
            "system",
            foreground="#9ca3af",
            font=("Segoe UI", 9, "italic"),
        )

        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def _on_enter_pressed(self, event):
        # Shift+Enter for newline, Enter to send
        if event.state & 0x0001:
            return
        self._on_send_click()
        return "break"

    def _on_send_click(self):
        user_text = self.input_text.get("1.0", tk.END).strip()
        if not user_text:
            return

        self.input_text.delete("1.0", tk.END)
        self._append_message("user", user_text)

        if self._current_thread and self._current_thread.is_alive():
            return

        self._current_thread = threading.Thread(
            target=self._handle_llm_response,
            args=(user_text,),
            daemon=True,
        )
        self._current_thread.start()

    def _handle_llm_response(self, user_text: str):
        try:
            reply = self.llm.generate(user_text)
        except Exception as e:
            reply = f"(CatSEEK R1 backend error: {e})"

        # Make sure UI update happens in main thread
        self.after(0, lambda: self._append_message("assistant", reply))

    def _clear_chat(self):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete("1.0", tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def _stop_response(self):
        # No hard thread cancel; in a real backend you could use a stop token.
        pass


if __name__ == "__main__":
    app = CatSEEKChatApp()
    app.mainloop()
