import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal with Scrollbar")
        self.root.geometry("700x500")

        # Create a Frame to hold the Text widget and scrollbar
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget for terminal-like output
        self.output_text = tk.Text(self.frame, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar and connect it to the Text widget
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=self.scrollbar.set)

        # Create a button to trigger output (for demonstration)
        self.button = ttk.Button(root, text="Print", command=self.display_output)
        self.button.pack()

    def display_output(self):
        # Simulate terminal output
        new_output = "Hello, world!\n"
        self.output_text.insert(tk.END, new_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
