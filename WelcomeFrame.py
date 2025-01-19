import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, font, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG_COLOR = "#dbdbdb"
low_threshold = None
high_threshold = None

class WelcomeFrame(ctk.CTkFrame):
    """
    A class used to create the main interface that serves as the entry point
    of the Blood Glucose Monitor application.

    This class initializes the graphical widgets, including labels and buttons,
    and manages navigation to other parts of the application.

    :ivar app: The application instance managing the different frames.
    :type app: BloodGlucoseMonitorApp
    :ivar user_info: Holds user data retrieved from the application when loading
        existing users.
    :type user_info: dict
    :ivar user_var: A tkinter StringVar object that stores the selected user
        from the dropdown menu.
    :type user_var: tkinter.StringVar
    :ivar user_frame: The frame where user-related UI elements are displayed.
    :type user_frame: ctk.CTkFrame or None
    """
    def __init__(self, app):
        """
        A class used to create the main interface that serves as the entry point
        of the Blood Glucose Monitor application.

        This class initializes the graphical widgets, including labels and buttons,
        and manages navigation to other parts of the application.

        :param app: The application instance managing the different frames
        :type app: BloodGlucoseMonitorApp
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        ctk.CTkLabel(self, text="Welcome to Blood Glucose Monitor", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Create a new user", command=lambda: app.show_frame(app.info_frame)).pack(pady=20)
        ctk.CTkButton(self, text="Load existing user/ all users", command=self.choose_user).pack(pady=20)

    def choose_user(self):
        """
        Handles the selection of a user by providing a dropdown menu with a list of available users
        and allowing the user to load their respective data through a selection interface. This
        function ensures the UI component for user selection is created only once and interacts
        with application data to fetch the list of users.

        :raises messagebox.showerror: Raised if no user data is found when attempting to create
            a user selection interface.
        """
        if hasattr(self, 'user_frame') and self.user_frame.winfo_exists():
            return

        self.user_info = self.app.load_user_data()
        if not self.user_info:
            messagebox.showerror("Error", "No user data found. Please create a new user.")
            return

        user_list = list(self.user_info.keys())
        user_list.append("All Users")
        self.user_var = tk.StringVar(value=user_list[0])
        self.user_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.user_frame.pack(pady=20)
        ctk.CTkLabel(self.user_frame, text="Select User:", text_color="#333333").pack(side="left", padx=10)
        ctk.CTkComboBox(self.user_frame, values=user_list, variable=self.user_var, text_color="#333333").pack(
            side="left", padx=10)
        ctk.CTkButton(self.user_frame, text="Select", command=self.load_user_data_for_selected_user,
                      text_color="#333333").pack(side="left", padx=10)

    def load_user_data_for_selected_user(self):
        """
        Loads and processes user data for the selected user to update the information
        frame and show the main application frame. If the selected user's data cannot
        be loaded, an error message is displayed.

        :raises messagebox.Error: If the selected user's data is not found.

        :return: None
        """
        selected_user = self.user_var.get()
        if selected_user == "All Users":
            self.app.show_frame(self.app.all_users_frame)
        else:
            self.app.selected_user = selected_user
            self.app.users_info = self.app.load_user_data()
            if self.app.selected_user in self.app.users_info:
                self.app.info_frame.user_info = self.app.load_user_data(self.app.selected_user)
                self.app.info_frame.populate_user_info()
                self.app.show_frame(self.app.main_frame)
            else:
                messagebox.showerror("Error", "User data not found.")

    def show_all_users_window(self):
        self.analyze_all_users()
        if not self.bmi_data:
            return

        window = tk.Toplevel(self)
        window.title("All Users Analysis")
        window.geometry("400x200")
        ctk.CTkButton(window, text="Show BMI of All Users", command=self.show_bmi_all_users).pack(pady=20)
        ctk.CTkButton(window, text="Show Average BMI by Diabetes Type", command=self.show_avg_bmi_by_type).pack(pady=20)