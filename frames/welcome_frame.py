import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import colors as c

low_threshold = None
high_threshold = None

class WelcomeFrame(ctk.CTkFrame):
    """
    Welcome frame for the application.

    Attributes:
        app (object): The main application instance.
        selected_user (str): The currently selected user.
        user_info (dict): Information about the users.
        user_var (tk.StringVar): Tkinter variable for the selected user.
        user_frame (ctk.CTkFrame): Frame for user selection.

    Args:
        app: The main application instance.

    """
    def __init__(self, app):
        """
        Initializes the WelcomeFrame and sets up the UI components.

        Args:
            app: The main application instance.
        """
        super().__init__(app.root, corner_radius=20, fg_color=c.BG_COLOR)
        self.app = app
        self.selected_user = None
        self.place(relwidth=1, relheight=1)

        # Title Section
        ctk.CTkLabel(
            self,
            text="Welcome to the Blood Glucose Analyzer",
            font=("Arial", 26, "bold"),
            text_color="#2d3436"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self,
            text="Analyze your blood glucose trends, generate insights, and track progress effortlessly.",
            font=("Arial", 14),
            text_color="#636e72",
            wraplength=600,
            justify="center"
        ).pack(pady=(0, 30))

        # Buttons Section
        button_style = {
            "corner_radius": 12,
            "height": 35,
            "font": ("Arial", 14, "bold"),
            "fg_color": c.VIBRANT_BLUE,
            "hover_color": c.BLUE,
            "text_color": "white"
        }
        ctk.CTkButton(
            self, text="Create a New User", **button_style, command=lambda: app.show_frame(app.info_frame)
        ).pack(pady=(10, 10), padx=40)
        ctk.CTkButton(
            self, text="Load Existing Users", **button_style, command=self.choose_user
        ).pack(pady=(10, 10), padx=40)
        ctk.CTkButton(
            self, text="Analysis of All Users", **button_style, command=lambda: app.show_frame(app.all_users_frame)
        ).pack(pady=(10, 20), padx=40)

        # Footer Label
        ctk.CTkLabel(
            self,
            text="Start by creating a user or loading existing data.",
            font=("Arial", 12, "italic"),
            text_color="#636e72"
        ).pack(pady=(20, 10))

    def choose_user(self):
        """
        Displays a dropdown to select an existing user and load their data. Hide the user frame if it is already displayed.
        """
        if hasattr(self, 'user_frame') and self.user_frame.winfo_exists() and self.user_frame.winfo_ismapped():
            return

        self.user_info = self.app.load_user_data()
        if not self.user_info:
            messagebox.showerror("Error", "No user data found. Please create a new user.")
            return

        user_list = list(self.user_info.keys())
        self.user_var = tk.StringVar(value=user_list[0])

        # Create the user frame
        self.user_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=c.BG_COLOR)
        self.user_frame.pack(pady=20)

        ctk.CTkLabel(self.user_frame, text="Select User:", font=("Arial", 12), text_color="#333333").pack(side="left", padx=10)
        ctk.CTkComboBox(self.user_frame, values=user_list, variable=self.user_var, text_color="#333333").pack(side="left", padx=10)
        ctk.CTkButton(
            self.user_frame, text="Select", corner_radius=10, command=self.load_user_data_for_selected_user,
            fg_color="#6c5ce7", hover_color="#5b4bdb", text_color="white"
        ).pack(side="left", padx=10)

    def load_user_data_for_selected_user(self):
        """
        Loads the data for the selected user and navigates to the main frame. Hide the user frame after loading the data.

        Raises:
            KeyError: If the selected user data is not found.
        """
        self.app.info_frame.from_welcome_frame = True
        self.selected_user = self.user_var.get()
        self.app.selected_user = self.selected_user
        self.app.users_info = self.app.load_user_data()
        if self.app.selected_user in self.app.users_info:
            self.app.info_frame.user_info = self.app.load_user_data(self.app.selected_user)
            self.app.info_frame.populate_user_info()
            self.app.main_frame.selected_user = self.app.selected_user
            self.app.main_frame.populate_user_data()
            self.app.show_frame(self.app.main_frame)
        else:
            self.app.custom_error_dialog("Error", "User data not found. Please check the user list and try again.")

    def hide_user_frame(self):
        """
        Hides the user selection frame.
        """
        if hasattr(self, 'user_frame') and self.user_frame.winfo_exists():
            self.user_frame.pack_forget()
        self.selected_user = None
        self.app.selected_user = None
        self.app.info_frame.user_info = None
