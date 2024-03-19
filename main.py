import io
import sys
import customtkinter as ctk
from customtkinter import *
import tkinter as tk

# Language mapping from display names to ISO 639 codes
LANGUAGES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Simplified Chinese": "zh",
    "Korean": "ko"
}

def redirect_print_to_text_widget(text_widget):
    sys.stdout = TextRedirector(text_widget)

class TextRedirector(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Write to the standard console
        sys.__stdout__.write(text)

        # Write to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end


class CustomSwitch(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.switch_state = tk.BooleanVar(value=False)

        # Create moon and sun labels
        self.moon_label = tk.Label(self, text="🌙", font=("Arial", 12))
        self.sun_label = tk.Label(self, text="☀️", font=("Arial", 12))

        # Create switch button
        self.switch_button = tk.Checkbutton(self, variable=self.switch_state, command=self.toggle_switch)

        # Pack labels and button
        self.moon_label.pack(side="left")
        self.switch_button.pack(side="left")
        self.sun_label.pack(side="left")

    def toggle_switch(self):
        # Update labels based on switch state
        if self.switch_state.get():
            self.moon_label.config(foreground="gray")
            self.sun_label.config(foreground="yellow")
        else:
            self.moon_label.config(foreground="yellow")
            self.sun_label.config(foreground="gray")

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

        # Ensure different source and target languages
        if source_lang == target_lang:
            print("Source and target languages must be different.")
            return

        # Convert to ISO 639 codes
        source_code = LANGUAGES.get(source_lang)
        target_code = LANGUAGES.get(target_lang)

        print(f"Source language (ISO code): {source_code}")
        print(f"Target language (ISO code): {target_code}")

        # Perform translation based on user input

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