import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

BG_COLOR = "#dbdbdb"

class CustomThresholdDialog:
    """A custom dialog for setting low and high thresholds for blood glucose analysis.

    Attributes:
        dialog (ctk.CTkToplevel): The top-level dialog window.
        low_threshold (tk.IntVar): Variable for the low threshold value.
        high_threshold (tk.IntVar): Variable for the high threshold value.
        low_entry (ctk.CTkEntry): Entry widget for the low threshold.
        high_entry (ctk.CTkEntry): Entry widget for the high threshold.
        result (tuple): The result containing the low and high thresholds.

    Args:
        root (tk.Tk): The root window of the application.
        title (str): The title of the dialog.
        low_initial (int, optional): The initial value for the low threshold. Defaults to 70.
        high_initial (int, optional): The initial value for the high threshold. Defaults to 180.
    """
    def __init__(self, root, title, low_initial=70, high_initial=180):
        """
        Initializes the CustomThresholdDialog.

        Args:
            root (tk.Tk): The root window of the application.
            title (str): The title of the dialog.
            low_initial (int, optional): The initial value for the low threshold. Defaults to 70.
            high_initial (int, optional): The initial value for the high threshold. Defaults to 180.
        """
        self.dialog = ctk.CTkToplevel(root)
        self.dialog.title(title)
        self.dialog.geometry("300x200")
        self.dialog.config(bg=BG_COLOR)
        self.dialog.resizable(False, False)
        self.dialog.attributes('-topmost', True)  # Always on top
        self.dialog.grab_set()  # Make the dialog modal

        self.low_threshold = tk.IntVar(value=low_initial)
        self.high_threshold = tk.IntVar(value=high_initial)

        ctk.CTkLabel(self.dialog, text="Low Threshold:", font=("Arial", 15), bg_color=BG_COLOR).pack(pady=10)
        self.low_entry = ctk.CTkEntry(self.dialog, font=("Arial", 15), textvariable=self.low_threshold)
        self.low_entry.pack()

        ctk.CTkLabel(self.dialog, text="High Threshold:", font=("Arial", 15), bg_color=BG_COLOR).pack(pady=10)
        self.high_entry = ctk.CTkEntry(self.dialog, font=("Arial", 15), textvariable=self.high_threshold)
        self.high_entry.pack()

        ctk.CTkButton(self.dialog, text="Confirm", command=self.confirm).pack(pady=10)

        self.result = None

    def confirm(self):
        """Confirms the input and closes the dialog."""
        try:
            self.result = (int(self.low_entry.get()), int(self.high_entry.get()))
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter valid integers.")
            return
        self.dialog.destroy()

    def show(self):
        """
        Displays the dialog and waits for user input.

        Returns:
            tuple: A tuple containing the low and high thresholds, or None if the dialog was canceled.
        """
        self.dialog.wait_window()
        return self.result