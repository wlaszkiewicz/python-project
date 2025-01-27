from tkinter import messagebox, filedialog
import customtkinter as ctk
import pandas as pd
import colors as c
from graph_generator import GraphGenerator
from insights_generator import InsightsGenerator


low_threshold = None
high_threshold = None

class MainFrame(ctk.CTkFrame):
    """Main frame for the application.

    Args:
        app: The main application instance.
    """

    def __init__(self, app):
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.data_file = None
        self.place(relwidth=1, relheight=1)
        self.graph_generator = GraphGenerator(app)
        self.insights_generator = InsightsGenerator(app)
        self.selected_user = None

        self.welcome_label = ctk.CTkLabel(
            self, text="", font=("Arial", 24, "bold"), fg_color="transparent"
        )
        self.welcome_label.pack(pady=30)

        dataset_frame = ctk.CTkFrame(self, fg_color=c.BG_COLOR)
        dataset_frame.pack(pady=20, fill="both", expand=True)

        inner_frame = ctk.CTkFrame(dataset_frame, fg_color="transparent")
        inner_frame.pack(expand=True)

        self.select_dataset_button = ctk.CTkButton(
            inner_frame,
            text="Choose Dataset",
            command=self.load_file,
            width=200,
            height=30,
            font=("Arial", 14, "bold"),
            corner_radius=20,
            fg_color=c.BLUE,
            text_color="white",
            hover_color=c.DARK_BLUE,
        )
        self.select_dataset_button.grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            inner_frame,
            text="Change My Data",
            command=lambda: self.app.show_frame(self.app.info_frame),
            width=150,
            height=30,
            font=("Arial", 12),
            corner_radius=20,
            fg_color="white",
            border_width=2,
            border_color=c.BLUE,
            text_color=c.DARK_BLUE,
            hover_color="#b3e5ff",
        ).grid(row=0, column=1, padx=10, pady=10)

        self.dataset_label = ctk.CTkLabel(
            inner_frame,
            text="No dataset selected",
            font=("Arial", 12, "italic"),
            text_color="#6B7280",
        )
        self.dataset_label.grid(row=1, column=0, columnspan=2, pady=10)

        action_frame = ctk.CTkFrame(inner_frame, fg_color=c.BG_COLOR, corner_radius=10)
        action_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), padx=20, sticky="nsew")

        action_label = ctk.CTkLabel(
            action_frame, text="Actions", font=("Arial", 16, "bold"), text_color="#1F2937"
        )
        action_label.grid(row=0, column=0, columnspan=1, pady=(10, 20))

        self.graph_time_button = ctk.CTkButton(
            action_frame,
            text="Blood Glucose Trends Over Time Graph",
            command=self.make_graph_levels_over_time,
            state="disabled",
            hover_color=c.BLUE_ANOTHER,
            fg_color="gray",
            text_color="white",
            width=300,
        )
        self.graph_time_button.grid(row=1, column=0, padx=20, pady=10)

        self.graph_meal_button = ctk.CTkButton(
            action_frame,
            text="Blood Glucose Levels by Meal",
            command=self.make_graph_levels_meal,
            state="disabled",
            hover_color=c.BLUE_ANOTHER,
            fg_color="gray",
            text_color="white",
            width=300,
        )
        self.graph_meal_button.grid(row=2, column=0, padx=20, pady=10)

        self.insights_button = ctk.CTkButton(
            action_frame,
            text="Generate Insights",
            command=self.generate_insights,
            state="disabled",
            hover_color=c.BLUE_ANOTHER,
            fg_color="gray",
            text_color="white",
            width=300,
        )
        self.insights_button.grid(row=3, column=0, padx=20, pady=10)

        self.go_back_button = ctk.CTkButton(
            action_frame,
            text="Go Back",
            command=self.go_back,
            fg_color=c.LIGHTER_BLUE,
            hover_color="#5a8bbf",
            text_color="white",
            corner_radius=10,
            width=150,
        )
        self.go_back_button.grid(row=4, column=0, padx=20, pady=10)

    def load_file(self):
        """Allows the user to load a CSV file and enables buttons."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                pd.read_csv(file_path)
                self.data_file = file_path
                self.dataset_label.configure(text=f"Dataset: {file_path.split('/')[-1]}")
                self.enable_buttons()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {e}")
        else:
            messagebox.showinfo("Info", "No file selected.")

    def enable_buttons(self):
        """Enables buttons for graphing and insights generation."""
        for button in [self.graph_time_button, self.graph_meal_button, self.insights_button]:
            button.configure(state="normal", fg_color=c.LIGHT_BLUE)

    def disable_buttons(self):
        """Disables buttons for graphing and insights generation."""
        for button in [self.graph_time_button, self.graph_meal_button, self.insights_button]:
            button.configure(state="disabled", fg_color="gray")

    def go_back(self):
        """Navigates back to the previous frame."""
        self.app.show_frame(self.app.welcome_frame)
        self.app.welcome_frame.hide_user_frame()
        self.app.info_frame.clear_user_info()
        self.app.info_frame.from_welcome_frame = False
        self.selected_user = None

    def make_graph_levels_over_time(self):
        """Creates a graph of blood glucose levels over time."""
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return
        self.graph_generator.make_graph_levels_over_time(self.data_file)

    def make_graph_levels_meal(self):
        """Creates a bar chart of blood glucose levels by meal."""
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return
        self.graph_generator.make_graph_levels_meal(self.data_file)

    def generate_insights(self):
        """Generates insights from the loaded dataset."""
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return
        self.insights_generator.data_file = self.data_file
        self.insights_generator.show_insights()

    def populate_user_data(self):
        """Populates user data in the welcome label."""
        self.welcome_label.configure(text=f"Welcome, {self.selected_user}!")