import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, font, simpledialog


BG_COLOR = "#dbdbdb"
low_threshold = None
high_threshold = None

class CustomThresholdDialog:
    """
    This class provides a custom threshold dialog for setting low and high
    threshold values in a graphical user interface. The dialog is modal, always
    stays on top, and ensures valid integer inputs for the thresholds.

    The dialog is initialized with a parent window, a title, and optional
    initial values for the thresholds. It allows users to input low and high
    threshold values through entry fields and confirms the values upon
    interaction with a button.

    Attributes are used to store the initial values, graphical components, and
    the resulting thresholds while structuring the dialog.

    :ivar low_threshold: Initial value of the low threshold, bindable to entry field.
    :type low_threshold: tkinter.IntVar
    :ivar high_threshold: Initial value of the high threshold, bindable to entry field.
    :type high_threshold: tkinter.IntVar
    :ivar result: Tuple containing the low and high threshold values entered by the user,
                  None if the dialog is canceled or invalid values are provided.
    :type result: tuple or None
    :ivar dialog: The tkinter dialog window object associated with this threshold dialog.
    :type dialog: ctk.CTkToplevel
    :ivar low_entry: Entry widget for user input of the low threshold value.
    :type low_entry: ctk.CTkEntry
    :ivar high_entry: Entry widget for user input of the high threshold value.
    :type high_entry: ctk.CTkEntry
    """
    def __init__(self, root, title, low_initial=70, high_initial=180):
        """
        Initializes a threshold dialog window that allows the user to input and adjust
        low and high threshold values. The dialog uses a modern custom Tkinter-based
        appearance and is modal to prevent user interaction with the main window until the
        dialog is closed.

        The dialog includes input fields for setting the low and high thresholds, labels
        to identify the fields, and a confirm button. The initial values for the thresholds
        can be specified through the constructor.

        :param root: The parent Tkinter widget or Tk instance. This determines the parent
                     of the dialog.
        :param title: The title of the dialog window.
        :param low_initial: The initial value for the low threshold. This is optional
                            and defaults to 70.
        :param high_initial: The initial value for the high threshold. This is optional
                             and defaults to 180.
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

        # Add labels and entry fields
        ctk.CTkLabel(self.dialog, text="Low Threshold:", font=("Arial", 15), bg_color=BG_COLOR).pack(pady=10)
        self.low_entry = ctk.CTkEntry(self.dialog, font=("Arial", 15), textvariable=self.low_threshold)
        self.low_entry.pack()

        ctk.CTkLabel(self.dialog, text="High Threshold:", font=("Arial", 15), bg_color=BG_COLOR).pack(pady=10)
        self.high_entry = ctk.CTkEntry(self.dialog, font=("Arial", 15), textvariable=self.high_threshold)
        self.high_entry.pack()

        # Add confirm button
        ctk.CTkButton(self.dialog, text="Confirm", command=self.confirm).pack(pady=10)

        # Initialize result
        self.result = None

    def confirm(self):
        """
        Retrieves and validates user input from dialog entries and closes the dialog.

        The `confirm` method is used to gather input from the user, convert the
        retrieved values into integers, handles potential errors for invalid
        entries, and subsequently closes the dialog window if the inputs are
        valid.

        :raises ValueError: Raised when the user inputs are not valid integers,
            resulting in a message box displaying an error notification to the
            user.

        :return: None
        """
        # Retrieve the entered values and close the dialog
        try:
            self.result = (int(self.low_entry.get()), int(self.high_entry.get()))
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter valid integers.")
            return
        self.dialog.destroy()

    def show(self):
        """
        Represents a method for waiting for a dialog window to close and retrieving its result.

        This method is intended for use in cases where a dialog window is displayed, and
        execution must pause until the user interacts with the dialog. Once the dialog is
        closed, the result of the interaction will be returned.

        :return: The result of the interaction with the dialog window.
        :rtype: Any
        """
        self.dialog.wait_window()
        return self.result