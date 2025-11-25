"""
main.py - Entry point for AskFileAI
Launches the Tkinter GUI
"""

from ui.tkinter_app import AskFileAIGUI
import tkinter as tk


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AskFileAIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
