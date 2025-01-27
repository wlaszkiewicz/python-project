import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import json
from all_users_frame import AllUsersFrame
from welcome_frame import WelcomeFrame
from info_frame import InfoFrame
from main_frame import MainFrame
import colors as c

window_width = 600
window_height = 500

class App:
    """Main application class for the Blood Glucose Monitor."""

    def __init__(self, root):
        """
        Initializes the application.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Blood Glucose Monitor")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.config(bg=c.BG_COLOR)
        self.data_file = None
        self.canvas = None
        self.selected_user = None
        self.user_data_file = "user_info.json"
        self.users_info = self.load_user_data()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.welcome_frame = WelcomeFrame(self)
        self.info_frame = InfoFrame(self)
        self.main_frame = MainFrame(self)
        self.all_users_frame = AllUsersFrame(self)

        self.show_frame(self.welcome_frame)

    def show_frame(self, frame):
        """
        Raises the specified frame to the top of the window stack.

        Args:
            frame (ctk.CTkFrame): The frame to be shown.
        """
        frame.tkraise()

    def center_window(self, width, height):
        """
        Centers the application window on the screen.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def load_file(self):
        """Loads a CSV file and sets it as the data file for the application."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], parent=self.root)
        if file_path:
            self.data_file = file_path
            messagebox.showinfo("File Loaded", "Dataset loaded successfully!")

    def load_user_data(self, username=None):
        """
        Loads user data from a JSON file.

        Args:
            username (str, optional): The username to load data for. If None, loads all user data.

        Returns:
            dict: The user data.
        """
        try:
            with open(self.user_data_file, "r") as file:
                data = json.load(file)
                if username:
                    return data.get(username, {})
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if not username else None

    def save_graph(self, fig):
        """
        Saves the given figure as a PDF file.

        Args:
            fig (matplotlib.figure.Figure): The figure to save.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], parent=self.root)
        if file_path:
            fig.savefig(file_path)
            messagebox.showinfo("Success", "Graph saved successfully!")

    def custom_error_dialog(self, title, message):
        """
        Displays a custom error dialog with the given title and message.

        Args:
            title (str): The title of the dialog.
            message (str): The message to display in the dialog.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        tk.Label(dialog, text=message, font=("Arial", 12), fg="red").pack(pady=20)
        tk.Button(dialog, text="OK", command=dialog.destroy, font=("Arial", 12), bg="#3498db", fg="white").pack(pady=10)

    def save_user_data(self, new_data):
        """
        Saves the given user data to a JSON file.

        Args:
            new_data (dict): The new user data to save.
        """
        try:
            data = self.load_user_data()
            data.update(new_data)
            with open(self.user_data_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user information: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    app.center_window(window_width, window_height)
    root.mainloop()