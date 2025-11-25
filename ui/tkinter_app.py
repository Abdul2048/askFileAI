import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
from config import Config
from src.agent.graph import AskFileAIAgent
from typing import Dict

class AskFileAIGUI:
    """Tkinter GUI for AskFileAI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AskFileAI - Local Intelligent File Q&A")
        self.root.geometry("900x700")
        
        self.config = Config()
        self.agent = AskFileAIAgent(self.config)
        self.current_file = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create GUI widgets"""
        header = tk.Label(
            self.root,
            text="AskFileAI - Ask Questions About Your Files",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)
        
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(file_frame, text="File Path:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            width=60,
            font=("Arial", 10)
        )
        file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(
            file_frame,
            text="Browse",
            command=self._browse_file,
            bg="#3498db",
            fg="white",
            font=("Arial", 10)
        )
        browse_btn.pack(side=tk.LEFT)
        
        question_frame = tk.Frame(self.root, pady=10)
        question_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(question_frame, text="Your Question:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.question_text = tk.Text(
            question_frame,
            height=3,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.question_text.pack(fill=tk.X, pady=5)
        
        ask_btn = tk.Button(
            question_frame,
            text="Ask Question",
            command=self._ask_question,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=5
        )
        ask_btn.pack()
        
        answer_frame = tk.Frame(self.root, pady=10)
        answer_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(answer_frame, text="Answer:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.answer_text = scrolledtext.ScrolledText(
            answer_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg="#ecf0f1"
        )
        self.answer_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        clear_btn = tk.Button(
            self.root,
            text="Clear Vector Store",
            command=self._clear_store,
            bg="#e74c3c",
            fg="white"
        )
        clear_btn.pack(side=tk.BOTTOM, pady=5)
    
    def _browse_file(self):
        """Open file browser"""
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All supported files", "*.pdf *.docx *.doc *.txt *.md *.csv *.xlsx *.xls *.py *.cpp *.java *.js *.png *.jpg"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx *.doc"),
                ("Text files", "*.txt *.md"),
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("Code files", "*.py *.cpp *.java *.js"),
                ("Images", "*.png *.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.current_file = file_path
    
    def _ask_question(self):
        """Process question in separate thread"""
        file_path = self.file_path_var.get().strip()
        question = self.question_text.get("1.0", tk.END).strip()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not question:
            messagebox.showerror("Error", "Please enter a question!")
            return
        
        self.status_var.set("Processing... This may take a moment.")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", "Processing your question...\n\nThis includes:\n- Loading the file\n- Chunking text\n- Generating embeddings\n- Storing in vector DB\n- Retrieving relevant content\n- Generating answer\n\nPlease wait...")
        
        thread = threading.Thread(target=self._process_question, args=(file_path, question))
        thread.daemon = True
        thread.start()
    
    def _process_question(self, file_path: str, question: str):
        """Process question with agent"""
        try:
            result = self.agent.ask(file_path, question)
            
            self.root.after(0, self._display_answer, result)
        except Exception as e:
            self.root.after(0, self._display_error, str(e))
    
    def _display_answer(self, result: Dict):
        """Display answer in GUI"""
        self.answer_text.delete("1.0", tk.END)
        
        if result["error"]:
            self.answer_text.insert("1.0", f"❌ Error: {result['error']}")
            self.status_var.set("Error occurred")
        else:
            answer_display = f"📝 Good question here is your answer:\n\n{result['answer']}\n\n"
            answer_display += f"{'='*80}\n\n"
            #answer_display += f"📚 Retrieved Context ({len(result['retrieved_docs'])} chunks):\n\n"
            
          #  for i, doc in enumerate(result['retrieved_docs']):
          #      answer_display += f"[Chunk {i+1}] (Relevance: {1 - doc.get('distance', 0):.2f})\n"
          #      answer_display += f"{doc['text'][:300]}...\n\n"
            
            self.answer_text.insert("1.0", answer_display)
            self.status_var.set("Answer generated successfully")
    
    def _display_error(self, error: str):
        """Display error message"""
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", f"❌ Error: {error}")
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", error)
    
    def _clear_store(self): 
        """Clear vector store"""
        if messagebox.askyesno("Confirm", "Clear all stored vectors?"):
            try:
                self.agent.vector_store.clear_collection()
                messagebox.showinfo("Success", "Vector store cleared!")
                self.status_var.set("Vector store cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AskFileAIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
