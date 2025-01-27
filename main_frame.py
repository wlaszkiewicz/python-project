import csv
from tkinter import messagebox, filedialog
import customtkinter as ctk
import pandas as pd
from custom_threshold_dialog import CustomThresholdDialog
import colors as c
from graph_generator import GraphGenerator

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
        global low_threshold, high_threshold
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return

        data = pd.read_csv(self.data_file)
        if 'Meal' in data.columns and 'Blood Glucose Level (mg/dL)' in data.columns:
            meal_groups = data.groupby('Meal')['Blood Glucose Level (mg/dL)']
            meal_stats = meal_groups.agg(['mean', 'std', 'min', 'max', 'count'])
            meal_stats['range'] = meal_stats['max'] - meal_stats['min']
            meal_stats = meal_stats.round(2)

            if not low_threshold or not high_threshold:
                threshold_dialog = CustomThresholdDialog(self.app.root, "Set Thresholds", low_initial=70, high_initial=180)
                thresholds = threshold_dialog.show()
                if not thresholds:
                    return
                low_threshold, high_threshold = thresholds

            data['Category'] = pd.cut(data['Blood Glucose Level (mg/dL)'],
                                      bins=[0, low_threshold, high_threshold, float('inf')],
                                      labels=['Low', 'Normal', 'High'])

            category_counts = data['Category'].value_counts(normalize=True) * 100

            data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
            data.set_index('Datetime', inplace=True)
            daily_avg = data['Blood Glucose Level (mg/dL)'].resample('D').mean()

            morning_data = data.between_time('06:00', '09:00')
            morning_avg = morning_data['Blood Glucose Level (mg/dL)'].mean()

            noon_data = data.between_time('09:00', '12:00')
            noon_avg = noon_data['Blood Glucose Level (mg/dL)'].mean()

            afternoon_data = data.between_time('12:00', '18:00')
            afternoon_avg = afternoon_data['Blood Glucose Level (mg/dL)'].mean()

            evening_data = data.between_time('18:00', '21:00')
            evening_avg = evening_data['Blood Glucose Level (mg/dL)'].mean()

            night_data = data.between_time('21:00', '06:00')
            night_avg = night_data['Blood Glucose Level (mg/dL)'].mean()

            insights_window = ctk.CTkToplevel(self.app.root)
            insights_window.title("Blood Glucose Insights")
            insights_window.attributes('-topmost', True)
            insights_window.geometry("600x600")

            insights_frame = ctk.CTkScrollableFrame(insights_window, fg_color="#FFFFFF", width=780, height=500)
            insights_frame.pack(pady=10, padx=10)

            ctk.CTkLabel(insights_frame, text="Meal Statistics", font=("Arial", 16, "bold")).pack(pady=10)

            meal_stats_container = ctk.CTkFrame(insights_frame, fg_color="#FFFFFF")
            meal_stats_container.pack(pady=5)

            meal_stats_frame = ctk.CTkFrame(meal_stats_container, fg_color="#F9F9F9")
            meal_stats_frame.pack(padx=10, pady=5)

            headers = ['Meal', 'Mean', 'Std Dev', 'Min', 'Max', 'Count', 'Range']
            for col, header in enumerate(headers):
                ctk.CTkLabel(meal_stats_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10,
                                                                                             sticky="ew")

            for i, (meal, stats) in enumerate(meal_stats.iterrows(), 1):
                ctk.CTkLabel(meal_stats_frame, text=meal).grid(row=i, column=0, padx=10, sticky="ew")
                for col, value in enumerate(stats):
                    ctk.CTkLabel(meal_stats_frame, text=value).grid(row=i, column=col + 1, padx=10, sticky="ew")

            ctk.CTkLabel(insights_frame, text="Time in Range", font=("Arial", 16, "bold")).pack(pady=10)
            for category, percentage in category_counts.items():
                ctk.CTkLabel(insights_frame, text=f"Time in {category}: {percentage:.2f}%", font=("Arial", 12)).pack(
                    pady=5)

            ctk.CTkLabel(insights_frame, text="Daily Averages", font=("Arial", 16, "bold")).pack(pady=10)
            for date, avg in daily_avg.items():
                ctk.CTkLabel(insights_frame, text=f"{date.date()}: {avg:.2f} mg/dL", font=("Arial", 12)).pack(pady=2)

            ctk.CTkLabel(insights_frame, text=f"Average Morning Level: {morning_avg:.2f} mg/dL",
                         font=("Arial", 14, "bold"), text_color="green").pack(pady=10)
            ctk.CTkLabel(insights_frame, text=f"Average Noon Level: {noon_avg:.2f} mg/dL",
                         font=("Arial", 14, "bold"), text_color="green").pack(pady=10)
            ctk.CTkLabel(insights_frame, text=f"Average Afternoon Level: {afternoon_avg:.2f} mg/dL",
                         font=("Arial", 14, "bold"), text_color="green").pack(pady=10)
            ctk.CTkLabel(insights_frame, text=f"Average Evening Level: {evening_avg:.2f} mg/dL",
                         font=("Arial", 14, "bold"), text_color="green").pack(pady=10)
            ctk.CTkLabel(insights_frame, text=f"Average Night Level: {night_avg:.2f} mg/dL",
                         font=("Arial", 14, "bold"), text_color="green").pack(pady=10)

            def export_insights():
                """Exports insights to a CSV file."""
                export_path = filedialog.asksaveasfile(mode="w", defaultextension=".csv",
                                                       filetypes=[("CSV Files", "*.csv")], parent=self.app.root)
                if export_path:
                    export_data = [["Meal Statistics"], ['Meal', 'Mean', 'Std Dev', 'Min', 'Max', 'Count', 'Range']]

                    for meal, stats in meal_stats.iterrows():
                        export_data.append(
                            [meal, stats['mean'], stats['std'], stats['min'], stats['max'], stats['count'],
                             stats['range']])

                    export_data.append([])

                    export_data.append(["Time in Range"])
                    export_data.append(['Category', 'Percentage (%)'])
                    for category, percentage in category_counts.items():
                        export_data.append([category, round(percentage, 2)])

                    export_data.append([])

                    export_data.append(["Daily Averages"])
                    export_data.append(['Date', 'Average Glucose (mg/dL)'])
                    for date, avg in daily_avg.items():
                        export_data.append([date.date(), round(avg, 2)])

                    export_data.append([])

                    export_data.append(["Morning Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["06:00-09:00", round(morning_avg, 2)])

                    export_data.append(["Noon Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["09:00-12:00", round(noon_avg, 2)])

                    export_data.append(["Afternoon Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["12:00-18:00", round(afternoon_avg, 2)])

                    export_data.append(["Evening Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["18:00-21:00", round(evening_avg, 2)])

                    export_data.append(["Night Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["21:00-06:00", round(night_avg, 2)])

                    with open(export_path.name, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(export_data)

                    messagebox.showinfo("Export Successful", f"Insights exported to {export_path.name}.")

            ctk.CTkButton(insights_window, text="Export to CSV", command=export_insights).pack(pady=10)

        else:
            messagebox.showerror("Error",
                                 "The dataset does not have the required columns ('Meal', 'Blood Glucose Level (mg/dL)').")

    def populate_user_data(self):
        """Populates user data in the welcome label."""
        self.welcome_label.configure(text=f"Welcome, {self.selected_user}!")

