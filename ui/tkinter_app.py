import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
from config import Config
from src.agent.graph import AskFileAIAgent
from typing import Dict
import pyttsx3

# ==========================
#   DARK MODE COLORS
# ==========================
BG_MAIN = "#1e1e1e"
BG_CARD = "#363535"
BG_SIDEBAR = "#161616"
BTN_BG = "#3a3a3a"
BTN_ACCENT = "#4CAF50"
TEXT = "#ffffff"


def rounded_button(parent, text, command, bg=BTN_BG, fg="white"):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        relief="flat",
        bd=0,
        activebackground="#555555",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=7
    )
    return btn

class AskFileAIGUI:
    """Modern Dark UI for AskFileAI"""

    def __init__(self, root):
        self.root = root
        self.root.title("AskFileAI - Local File Question Answering")
        self.root.geometry("1000x720")
        self.root.configure(bg=BG_MAIN)

        self.config = Config()
        self.agent = AskFileAIAgent(self.config)
        self.current_file = None
        self._create_layout()
        
        self.is_speaking = False
        self.stop_flag = False

    # ==========================
    #        LAYOUT
    # ==========================
    def _create_layout(self):

        # ---------------------------
        # SIDEBAR
        # ---------------------------
        sidebar = tk.Frame(self.root, width=200, bg=BG_SIDEBAR)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        logo = tk.Label(
            sidebar,
            text="AskFileAI",
            bg=BG_SIDEBAR,
            fg=TEXT,
            font=("Segoe UI", 20, "bold"),
            pady=20
        )
        logo.pack()

        tk.Label(
            sidebar,
            text="AI File Assistant",
            bg=BG_SIDEBAR,
            fg="#bbbbbb",
            font=("Segoe UI", 10)
        ).pack()

        # BUTTONS IN SIDEBAR
        # COPY + READ BUTTONS MOVED TO SIDEBAR
        rounded_button(sidebar, "📋 Copy Answer", self._copy_answer, bg="#6c5ce7").pack(pady=10, fill=tk.X, padx=20)
        #rounded_button(sidebar, "🔊 Read Aloud", self._read_answer_aloud, bg="#0984e3").pack(pady=5, fill=tk.X, padx=20)
        rounded_button(sidebar, "🔊 Read Aloud", self._toggle_read_aloud).pack(pady=5, fill=tk.X, padx=20)


        # DOWNLOAD & CLEAR STORE
        rounded_button(sidebar, "⬇ Download Answer", self._download_answer, bg="#8e44ad").pack(pady=15, fill=tk.X, padx=20)
        rounded_button(sidebar, "🧹 Clear Vector Store", self._clear_store, bg="#d43f3a").pack(pady=5, fill=tk.X, padx=20)

        # ---------------------------
        # MAIN WORK AREA
        # ---------------------------
        main = tk.Frame(self.root, bg=BG_MAIN)
        main.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # ---------------------------
        # FILE PATH + BROWSE BUTTON
        # ---------------------------
        
        file_section = tk.Frame(main, bg=BG_MAIN)
        file_section.pack(fill=tk.X)
        
        # Label (this stays packed)
        tk.Label(file_section, text="Selected File:", fg=TEXT, bg=BG_MAIN).pack(anchor=tk.W)
        
        # A dedicated GRID frame inside file_section
        file_row = tk.Frame(file_section, bg=BG_MAIN)
        file_row.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        
        file_entry = tk.Entry(
            file_row,
            textvariable=self.file_path_var,
            font=("Segoe UI", 10),
            bg=BG_CARD,
            fg=TEXT,
            relief="flat"
        )
        file_entry.grid(row=0, column=0, sticky="we", padx=(0, 10))
        
        browse_btn = rounded_button(file_row, "📂 Browse", self._browse_file, bg="#3498db")
        browse_btn.grid(row=0, column=1, sticky="e")
        
        file_row.columnconfigure(0, weight=1)



        # QUESTION
        tk.Label(main, text="Your Question:", fg=TEXT, bg=BG_MAIN).pack(anchor=tk.W)
        self.question_text = tk.Text(main, height=3, font=("Segoe UI", 10), bg=BG_CARD, fg=TEXT, relief="flat")
        self.question_text.pack(fill=tk.X, pady=5)

        rounded_button(main, "Ask Question 🤖", self._ask_question, bg=BTN_ACCENT).pack(pady=5)
        
        # ---------------------------
        # COPY & AUDIO BUTTONS
        # ---------------------------
        # Row of center action buttons
        action_row = tk.Frame(main, bg=BG_MAIN)
        action_row.pack(pady=5)

        # LOADING BAR
        self.progress = ttk.Progressbar(main, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=5)
        self.progress.stop()

        # ANSWER BOX
        tk.Label(main, text="Answer:", fg=TEXT, bg=BG_MAIN).pack(anchor=tk.W)
        self.answer_text = scrolledtext.ScrolledText(
            main,
            font=("Segoe UI", 10),
            bg=BG_CARD,
            fg=TEXT,
            relief="flat"
        )
        self.answer_text.pack(expand=True, fill=tk.BOTH, pady=5)

    # =================================================
    #   FUNCTIONALITY
    # =================================================

    def _download_answer(self):
        answer = self.answer_text.get("1.0", tk.END).strip()
        if not answer:
            messagebox.showerror("Error", "No answer to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(answer)
            messagebox.showinfo("Saved", "Answer downloaded successfully!")

    def _browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_file = file_path
            self.file_path_var.set(file_path)

    def _ask_question(self):
        """Process question in separate thread"""
        file_path = self.file_path_var.get().strip()
        question = self.question_text.get("1.0", tk.END).strip()

        if not file_path:
            messagebox.showerror("Error", "Select a file first!")
            return

        if not question:
            messagebox.showerror("Error", "Enter a question!")
            return

        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", "Processing your question...")

        self.progress.start(10)

        thread = threading.Thread(target=self._process_question, args=(file_path, question))
        thread.daemon = True
        thread.start()

    def _process_question(self, file_path, question):
        try:
            result = self.agent.ask(file_path, question)
            self.root.after(0, lambda: self._display_answer(result))
        except Exception as e:
            self.root.after(0, lambda: self._display_error(str(e)))

    def _display_answer(self, result):
        self.progress.stop() 
        self.answer_text.delete("1.0", tk.END) #
        self.answer_text.insert("1.0", f"📝 Great question here is your answer:\n\n{result['answer']}")

    def _display_error(self, error):
        self.progress.stop()
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", f"❌ Error: {error}")

    def _clear_store(self):
        try:
            self.agent.vector_store.clear_collection()
            messagebox.showinfo("Cleared", "Vector Store cleaned successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _copy_answer(self):
     answer = self.answer_text.get("1.0", tk.END).strip()
     if answer:
         self.root.clipboard_clear()
         self.root.clipboard_append(answer)
         messagebox.showinfo("Copied", "Answer copied to clipboard!")

    import pyttsx3
    import threading
    import time
    def _toggle_read_aloud(self):
        """Toggle between start and stop"""
        if not self.is_speaking:
            self._start_reading()
        else:
            self._stop_reading()
       
    def _start_reading(self):
        """Start reading aloud"""
        text = self.answer_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "No answer to read aloud.")
            return
    
        self.is_speaking = True
        self.stop_flag = False
    
        # Create a FRESH engine every time
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)
    
        threading.Thread(target=self._tts_thread, args=(text,), daemon=True).start()
      
    def _stop_reading(self):
        """Stop reading aloud instantly"""
        self.stop_flag = True
        self.is_speaking = False
    
        if hasattr(self, "engine") and self.engine is not None:
            try:
                self.engine.stop()
            except:
                pass
      
    def _tts_thread(self, text):
        """Thread that supports stopping mid-sentence"""
        for sentence in text.split(". "):
            if self.stop_flag:
                break
            
            try:
                self.engine.say(sentence)
                self.engine.runAndWait()
            except:
                break
    
        self.is_speaking = False
    

def main():
    """Main entry point"""
    root = tk.Tk()
    app = AskFileAIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

