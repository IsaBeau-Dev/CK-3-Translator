import io
import os.path
import sys
import customtkinter as ctk
from customtkinter import *
import tkinter as tk
import translator

# Language mapping from display names to ISO 639 codes
LANGUAGES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Simplified Chinese": "zh",
    "Korean": "ko"
}

def list_files(directory):
    """
    Prints all files in the given directory and its subdirectories.
    """
    found_files = False  # Flag to track if any files were found

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".yml"):
                print(os.path.join(root, file))
                found_files = True

    if not found_files:
        print("No files found")

    return found_files

def redirect_print_to_text_widget(text_widget):
    sys.stdout = TextRedirector(text_widget)

class TextRedirector(io.TextIOBase):
    def __init__(self, text_widget, update_interval=100):  # Set a default update interval (in milliseconds)
        self.text_widget = text_widget
        self.update_interval = update_interval
        self.buffer = ""

    def write(self, text):
        # Write to the standard console
        sys.__stdout__.write(text)

    #     # Append to the buffer
    #     self.buffer += text
    #
    #     # Check if it's time to update the Text widget
    #     if len(self.buffer) >= self.update_interval:
    #         self.text_widget.insert(tk.END, self.buffer)
    #         self.text_widget.see(tk.END)  # Scroll to the end
    #         self.buffer = ""  # Clear the buffer
    #
    # def flush(self):
    #     # Flush any remaining content
    #     if self.buffer:
    #         self.text_widget.insert(tk.END, self.buffer)
    #         self.text_widget.see(tk.END)  # Scroll to the end
    #         self.buffer = ""  # Clear the buffer

    #######
        # Write to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Language Translator")
        self.geometry("600x400")  # Set initial window size

        # Create widgets
        self.path_entry = ctk.CTkEntry(self)  # Removed placeholder argument
        self.source_lang_combo = ctk.CTkComboBox(self, values=list(LANGUAGES.keys()),command=self._update_target_langs)
        self.target_lang_combo = ctk.CTkComboBox(self, values=list(LANGUAGES.keys()),command=self._update_source_langs)
        self.translate_button = ctk.CTkButton(self, text="Translate", command=self.translate_text)
        self.mode_switch = ctk.CTkSwitch(self,text="☀", command=self.toggle_mode)
        # Create a Frame to hold the Text widget and scrollbar
        self.frame = ctk.CTkFrame(self)
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, font=("Helvetica", 18))
        # Create a Scrollbar and link it to the Text widget
        self.scrollbar = tk.Scrollbar(self.frame, command=self.text_widget.yview)


        # Set initial values
        self.source_lang_combo.set("English")
        self.target_lang_combo.set("German")

        #Both lists on startup
        selected_source_lang = self.source_lang_combo.get()
        available_target_languages = [lang for lang in LANGUAGES if lang != selected_source_lang]
        self.target_lang_combo.configure(values=available_target_languages)
        # Get the current target language
        target_lang = self.target_lang_combo.get()
        # Create a list of languages that are not equal to the target language
        source_languages = [language for language in LANGUAGES if language != target_lang]
        # Update the values of the source combobox
        self.source_lang_combo.configure(values=source_languages)
        ####


        # Bind the combobox changes to update values
        # self.source_lang_combo.bind("<<ComboboxSelected>>", self._update_target_langs)
        # self.target_lang_combo.bind("<<ComboboxSelected>>", self._update_source_langs)

        # Pack widgets
        self.path_entry.pack(fill="x", padx=20, pady=10)
        self.source_lang_combo.pack(fill="x", padx=20, pady=10)
        self.target_lang_combo.pack(fill="x", padx=20, pady=10)
        self.translate_button.pack(pady=10)
        self.mode_switch.pack(pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y,anchor=tk.E)

        # Configure resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Redirect print output to both the console and the Text widget
        redirect_print_to_text_widget(self.text_widget)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    def _update_target_langs(self,event):
        # Get the current source language
        source_lang = self.source_lang_combo.get()
        # Create a list of languages that are not equal to the source language
        target_languages = [language for language in LANGUAGES if language != source_lang]
        # Update the values of the target combobox
        self.target_lang_combo.configure(values=target_languages)

    def _update_source_langs(self,event):
        # Get the current target language
        target_lang = self.target_lang_combo.get()
        # Create a list of languages that are not equal to the target language
        source_languages = [language for language in LANGUAGES if language != target_lang]
        # Update the values of the source combobox
        self.source_lang_combo.configure(values=source_languages)

    def translate_text(self):
        # Get selected languages
        source_lang = self.source_lang_combo.get()
        target_lang = self.target_lang_combo.get()

        # Convert to ISO 639 codes
        source_code = LANGUAGES.get(source_lang)
        target_code = LANGUAGES.get(target_lang)

        print(f"Source language : {source_code}")
        print(f"Target language : {target_code}")

        path = self.path_entry.get()
        if os.path.exists(path):
            print(f"Path to localization : {path} \n\n")
            if list_files(path):
                # print("Found Valid files")
                # Perform translation based on user input
                # translator.call(source_code,target_code,1,path)
                for i in range(1000):
                    print(i)
                print("Finished")
        else:
            print("No valid path was given")






    def toggle_mode(self):
        # Switch appearance mode (light/dark)
        if self.mode_switch.get():
            set_appearance_mode("dark")
            self.text_widget.configure(bg="black", fg="white")
            self.mode_switch.configure(text ="🌙")  # Moon symbol
        else:
            set_appearance_mode("light")
            self.text_widget.configure(bg="white", fg="black")
            self.mode_switch.configure(text="☀")  # Sun symbol

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()