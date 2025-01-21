import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AllUsersFrame(ctk.CTkFrame):
    """
    A frame for displaying analysis of all users' BMI data.

    Attributes:
        app (App): The main application instance.
        user_data (dict): Dictionary containing user data.
        bmi_data (dict): Dictionary containing BMI and diabetes type data for users.
        users (list): List of users names.
        bmis (list): List of BMI values.
        diabetes_types (list): List of diabetes types.
    """

    def __init__(self, app):
        """
        Initializes the AllUsersFrame with buttons and labels for analysis.

        Args:
            app (App): The main application instance.
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        ctk.CTkLabel(self, text="All Users Analysis", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Show BMI of All Users", command=self.show_bmi_all_users).pack(pady=20)
        ctk.CTkButton(self, text="Show Average BMI by Diabetes Type", command=self.show_avg_bmi_by_type).pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=lambda: app.show_frame(app.welcome_frame)).pack(pady=20)



    def analyze_all_users(self):
        """
        Analyzes all users' data to extract BMI and diabetes type information.

        Raises:
            messagebox.showerror: If no user data or no BMI/diabetes type data is found.
        """
        self.user_data = self.app.load_user_data()
        if not self.user_data:
            messagebox.showerror("Error", "No user data found.")
            return

        self.bmi_data = {user: (data.get('bmi'), data.get('diabetes_type')) for user, data in self.user_data.items() if
                         'bmi' in data and 'diabetes_type' in data}
        if not self.bmi_data:
            messagebox.showerror("Error", "No BMI or diabetes type data available for users.")
            return

        self.users = list(self.bmi_data.keys())
        self.bmis = [self.bmi_data[user][0] for user in self.users]
        self.diabetes_types = [self.bmi_data[user][1] for user in self.users]


    def show_bmi_all_users(self):
        """
        Displays a plot of BMI values for all users in a new window.

        Raises:
            messagebox.showerror: If no BMI data is available.
        """
        self.analyze_all_users()
        if not self.bmi_data:
            return

        max_bmi = max(self.bmis)
        min_bmi = min(self.bmis)
        max_bmi_user = self.users[self.bmis.index(max_bmi)]
        min_bmi_user = self.users[self.bmis.index(min_bmi)]

        window = tk.Toplevel(self)
        window.title("BMI of All Users")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.users, self.bmis, marker='o', color='#4682B4', label='BMI')  # Darker blue color
        ax.plot(max_bmi_user, max_bmi, marker='o', color='red', label='Highest BMI')
        ax.plot(min_bmi_user, min_bmi, marker='o', color='purple', label='Lowest BMI')
        ax.set_xlabel('Users')
        ax.set_ylabel('BMI')
        ax.set_title('BMI of All Users')
        ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def save_graph():
            self.app.save_graph(fig)

        save_button = ctk.CTkButton(window, text="Save Graph", command=save_graph)
        save_button.pack(pady=10)

        self.app.center_window(window)

    def show_avg_bmi_by_type(self):
        """
        Displays a bar chart of average BMI values by diabetes type in a new window.

        Raises:
            messagebox.showerror: If no BMI data is available.
        """
        self.analyze_all_users()
        if not self.bmi_data:
            return

        diabetes_type_bmi = {}
        for user, (bmi, diabetes_type) in self.bmi_data.items():
            if diabetes_type not in diabetes_type_bmi:
                diabetes_type_bmi[diabetes_type] = []
            diabetes_type_bmi[diabetes_type].append(bmi)

        avg_bmi_per_type = {dtype: sum(bmis) / len(bmis) for dtype, bmis in diabetes_type_bmi.items()}

        window = tk.Toplevel(self)
        window.title("Average BMI for Each Diabetes Type")
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        for i, (dtype, avg_bmi) in enumerate(avg_bmi_per_type.items()):
            dtype_wrapped = dtype.replace(" ", "\n")
            ax.bar(dtype_wrapped, avg_bmi, color=colors[i % len(colors)])
        ax.set_xlabel('Diabetes Type')
        ax.set_ylabel('Average BMI')
        ax.set_title('Average BMI for Each Diabetes Type')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def save_graph():
            self.app.save_graph(fig)

        save_button = ctk.CTkButton(window, text="Save Graph", command=save_graph)
        save_button.pack(pady=10)

        self.app.center_window(window)

    def show_all_users_window(self):
        """
        Displays a window with options to show BMI of all users or average BMI by diabetes type.

        Raises:
            messagebox.showerror: If no BMI data is available.
        """
        self.analyze_all_users()
        if not self.bmi_data:
            return

        window = tk.Toplevel(self)
        window.title("All Users Analysis")
        window.geometry("400x200")
        ctk.CTkButton(window, text="Show BMI of All Users", command=self.show_bmi_all_users).pack(pady=20)
        ctk.CTkButton(window, text="Show Average BMI by Diabetes Type", command=self.show_avg_bmi_by_type).pack(pady=20)

        self.app.center_window(window)