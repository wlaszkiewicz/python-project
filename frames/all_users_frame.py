import customtkinter as ctk
from tkinter import messagebox
from graph_generator import GraphGenerator
import colors as c

class AllUsersFrame(ctk.CTkFrame):
    """Frame for displaying analysis of all users.

    Attributes:
        app: The main application instance.
        graph_generator: Instance of GraphGenerator for generating graphs.
        user_data: Dictionary containing user data.
        bmi_data: Dictionary containing BMI and diabetes type data for users.
        users: List of user identifiers.
        bmis: List of BMI values for users.
        diabetes_types: List of diabetes types for users.

    Args:
        app: The main application instance.
    """
    def __init__(self, app):
        """Initializes the AllUsersFrame.

        Args:
            app: The main application instance.
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.graph_generator = GraphGenerator(app)
        self.place(relwidth=1, relheight=1)

        button_style = {
            "corner_radius": 10,
            "height": 30,
            "font": ("Arial", 14),
            "fg_color": c.LIGHT_BLUE,
            "hover_color": c.BLUE_ANOTHER,
            "text_color": "white"
        }
        ctk.CTkLabel(self, text="All Users Analysis", font=("Arial", 20, "bold"), text_color="#2d3436").pack(pady=20)
        ctk.CTkButton(self, text="Show BMI of All Users", **button_style, command=self.show_bmi_all_users).pack(pady=20)
        ctk.CTkButton(self, text="Show Average BMI by Diabetes Type", **button_style, command=self.show_avg_bmi_by_type).pack(pady=20)
        ctk.CTkButton(self, text="Show Diabetes Type Distribution by Age", **button_style, command=self.show_age_distribution_by_type).pack(pady=20)
        ctk.CTkButton(self, text="Show Diabetes Type Distribution by Gender", **button_style, command=self.show_gender_distribution_by_type).pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=self.go_back, fg_color=c.LIGHTER_BLUE, hover_color="#5a8bbf", text_color="white", corner_radius=10, width=150).pack(pady=20)

    def analyze_all_users(self):
        """Analyzes all users' data for BMI and diabetes type."""
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
        """Displays the BMI of all users."""
        self.analyze_all_users()
        if not self.bmi_data:
            return
        self.graph_generator.show_bmi_all_users(self.users, self.bmis)

    def show_avg_bmi_by_type(self):
        """Displays the average BMI by diabetes type."""
        self.analyze_all_users()
        if not self.bmi_data:
            return

        diabetes_type_bmi = {}
        for user, (bmi, diabetes_type) in self.bmi_data.items():
            if diabetes_type not in diabetes_type_bmi:
                diabetes_type_bmi[diabetes_type] = []
            diabetes_type_bmi[diabetes_type].append(bmi)

        avg_bmi_per_type = {dtype: sum(bmis) / len(bmis) for dtype, bmis in diabetes_type_bmi.items()}
        self.graph_generator.show_avg_bmi_by_type(avg_bmi_per_type)

    def show_gender_distribution_by_type(self):
        """Displays the distribution of diabetes types by gender."""
        self.analyze_all_users()
        if not self.user_data:
            return

        gender_data = {dtype: [] for dtype in set(self.diabetes_types)}
        for user, data in self.user_data.items():
            if 'gender' in data and 'diabetes_type' in data:
                gender_data[data['diabetes_type']].append(data['gender'])

        self.graph_generator.show_gender_distribution_by_type(gender_data)

    def show_age_distribution_by_type(self):
        """Displays the distribution of diabetes types by age."""
        self.analyze_all_users()
        if not self.user_data:
            return

        age_data = {dtype: [] for dtype in set(self.diabetes_types)}
        for user, data in self.user_data.items():
            if 'age' in data and 'diabetes_type' in data:
                age_data[data['diabetes_type']].append(data['age'])

        self.graph_generator.show_age_distribution_by_type(age_data)

    def go_back(self):
        """Navigates back to the welcome frame. Hides user frame and clears user info."""
        self.app.show_frame(self.app.welcome_frame)
        self.app.welcome_frame.hide_user_frame()
        self.app.info_frame.clear_user_info()