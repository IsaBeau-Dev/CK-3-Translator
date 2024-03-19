import tkinter as tk
import sys

class CTkTerminalWidget(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(state=tk.DISABLED)  # Disable direct editing
        self.bind("<KeyPress>", self.handle_keypress)
        self.buffer = ""

    def handle_keypress(self, event):
        if event.keysym == "Return":
            # Handle user input (e.g., execute a command)
            user_input = self.buffer.strip()
            self.insert(tk.END, f"\n> {user_input}\n")
            self.buffer = ""

            # Simulate command execution (replace with your actual logic)
            self.execute_command(user_input)

            # Scroll to the end
            self.see(tk.END)
        else:
            self.buffer += event.char

    def execute_command(self, command):
        # Simulate command execution (replace with your actual logic)
        if command.lower() == "hello":
            self.insert(tk.END, "Hello, world!\n")
        else:
            self.insert(tk.END, f"Unknown command: {command}\n")

    def flush(self):
        pass  # No need to flush anything

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CustomTkinter Terminal")

    terminal = CTkTerminalWidget(root, wrap=tk.WORD)
    terminal.pack(fill=tk.BOTH, expand=True)

    # Redirect stdout to the terminal
    sys.stdout = terminal

    root.mainloop()
