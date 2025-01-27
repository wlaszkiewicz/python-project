from tkinter import messagebox, filedialog
import pandas as pd
import customtkinter as ctk
import csv
from custom_threshold_dialog import CustomThresholdDialog
import colors as c


class InsightsGenerator:
    """
    Generates insights from the loaded dataset.

    Attributes:
        app (object): The main application instance.
        data_file (str): Path to the loaded dataset file.
        low_threshold (int): The low threshold for blood glucose levels.
        high_threshold (int): The high threshold for blood glucose levels.
    """

    def __init__(self, app):
        """
        Initializes the InsightsGenerator.

        Args:
            app (object): The main application instance.
        """
        self.app = app
        self.data_file = None
        self.low_threshold = None
        self.high_threshold = None

    def load_data(self):
        """
        Loads the dataset from the file.

        Returns:
            DataFrame: The loaded dataset as a pandas DataFrame, or None if no dataset is loaded.
        """
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return None
        return pd.read_csv(self.data_file)

    def set_thresholds(self):
        """
        Sets the low and high thresholds using a custom dialog.

        Returns:
            bool: True if thresholds are set, False otherwise.
        """
        if not self.low_threshold or not self.high_threshold:
            threshold_dialog = CustomThresholdDialog(self.app.root, "Set Thresholds", low_initial=70, high_initial=180)
            thresholds = threshold_dialog.show()
            if not thresholds:
                return False
            self.low_threshold, self.high_threshold = thresholds
        return True

    def generate_meal_stats(self, data):
        """
        Generates meal statistics from the dataset.

        Args:
            data (DataFrame): The dataset as a pandas DataFrame.

        Returns:
            DataFrame: Meal statistics including mean, std, min, max, count, and range.
        """
        meal_groups = data.groupby('Meal')['Blood Glucose Level (mg/dL)']
        meal_stats = meal_groups.agg(['mean', 'std', 'min', 'max', 'count'])
        meal_stats['range'] = meal_stats['max'] - meal_stats['min']
        return meal_stats.round(2)

    def categorize_data(self, data):
        """
        Categorizes the data based on blood glucose levels.

        Args:
            data (DataFrame): The dataset as a pandas DataFrame.

        Returns:
            DataFrame: The dataset with an additional 'Category' column.
        """
        data['Category'] = pd.cut(data['Blood Glucose Level (mg/dL)'],
                                  bins=[0, self.low_threshold, self.high_threshold, float('inf')],
                                  labels=['Low', 'Normal', 'High'])
        return data

    def generate_daily_averages(self, data):
        """
        Generates daily averages of blood glucose levels.

        Args:
            data (DataFrame): The dataset as a pandas DataFrame.

        Returns:
            Series: Daily averages of blood glucose levels.
        """
        data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data.set_index('Datetime', inplace=True)
        return data['Blood Glucose Level (mg/dL)'].resample('D').mean()

    def generate_time_period_averages(self, data):
        """
        Generates averages for different time periods of the day.

        Args:
            data (DataFrame): The dataset as a pandas DataFrame.

        Returns:
            dict: Averages of blood glucose levels for different time periods.
        """
        time_periods = {
            'Morning': ('06:00', '09:00'),
            'Noon': ('09:00', '12:00'),
            'Afternoon': ('12:00', '18:00'),
            'Evening': ('18:00', '21:00'),
            'Night': ('21:00', '06:00')
        }
        averages = {}
        for period, (start, end) in time_periods.items():
            period_data = data.between_time(start, end)
            averages[period] = period_data['Blood Glucose Level (mg/dL)'].mean()
        return averages

    def show_insights(self):
        """
        Displays the insights in a new window.
        """
        data = self.load_data()
        if data is None or 'Meal' not in data.columns or 'Blood Glucose Level (mg/dL)' not in data.columns or 'Notes' not in data.columns:
            messagebox.showerror("Error",
                                 "The dataset does not have the required columns ('Meal', 'Blood Glucose Level (mg/dL)', 'Notes').")
            return

        if not self.set_thresholds():
            return

        meal_stats = self.generate_meal_stats(data)
        data = self.categorize_data(data)
        category_counts = data['Category'].value_counts(normalize=True) * 100
        daily_avg = self.generate_daily_averages(data)
        time_period_averages = self.generate_time_period_averages(data)

        insights_window = ctk.CTkToplevel(self.app.root)
        insights_window.title("Blood Glucose Insights")
        insights_window.attributes('-topmost', True)
        insights_window.geometry("600x600")

        insights_frame = ctk.CTkScrollableFrame(insights_window, fg_color="#FFFFFF", width=780, height=500)
        insights_frame.pack(pady=10, padx=10)

        self.display_meal_stats(insights_frame, meal_stats)
        self.display_category_counts(insights_frame, category_counts)
        self.display_daily_averages(insights_frame, daily_avg)
        self.display_time_period_averages(insights_frame, time_period_averages)
        self.display_extreme_values(insights_frame, data)

        ctk.CTkButton(insights_window, text="Export to CSV",
                      command=lambda: self.export_insights(meal_stats, category_counts, daily_avg,
                                                           time_period_averages)).pack(pady=10)

    def display_meal_stats(self, frame, meal_stats):
        collapsible_frame = CollapsibleFrame(frame, title="Meal Statistics")
        collapsible_frame.pack(pady=15, fill="x")

        meal_stats_container = self.create_background_frame(collapsible_frame.content_frame)
        meal_stats_frame = ctk.CTkFrame(meal_stats_container, fg_color="#F9F9F9")
        meal_stats_frame.pack(padx=10, pady=5, fill="x", expand=True)
        headers = ['Meal', 'Mean', 'Std Dev', 'Min', 'Max', 'Count', 'Range']
        for col, header in enumerate(headers):
            ctk.CTkLabel(meal_stats_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10,
                                                                                         sticky="ew")
        for i, (meal, stats) in enumerate(meal_stats.iterrows(), 1):
            ctk.CTkLabel(meal_stats_frame, text=meal).grid(row=i, column=0, padx=10, sticky="ew")
            for col, value in enumerate(stats):
                ctk.CTkLabel(meal_stats_frame, text=value).grid(row=i, column=col + 1, padx=10, sticky="ew")

    def display_category_counts(self, frame, category_counts):
        collapsible_frame = CollapsibleFrame(frame, title="Time in Range")
        collapsible_frame.pack(pady=15, fill="x")

        category_counts_container = self.create_background_frame(collapsible_frame.content_frame)
        for category, percentage in category_counts.items():
            ctk.CTkLabel(category_counts_container, text=f"Time in {category}: {percentage:.2f}%",
                         font=("Arial", 12)).pack(pady=5)

    def display_daily_averages(self, frame, daily_avg):
        collapsible_frame = CollapsibleFrame(frame, title="Daily Averages")
        collapsible_frame.pack(pady=15, fill="x")

        daily_avg_container = self.create_background_frame(collapsible_frame.content_frame)
        daily_avg_frame = ctk.CTkScrollableFrame(daily_avg_container, fg_color="#F9F9F9", width=500, height=200)
        daily_avg_frame.pack(pady=10)
        for date, avg in daily_avg.items():
            ctk.CTkLabel(daily_avg_frame, text=f"{date.date()}: {avg:.2f} mg/dL", font=("Arial", 12)).pack(pady=2)

    def display_time_period_averages(self, frame, time_period_averages):
        collapsible_frame = CollapsibleFrame(frame, title="Time Period Averages")
        collapsible_frame.pack(pady=15, fill="x")

        time_period_averages_container = self.create_background_frame(collapsible_frame.content_frame)
        for period, avg in time_period_averages.items():
            if avg is not None:
                ctk.CTkLabel(time_period_averages_container, text=f"Average {period} Level: {avg:.2f} mg/dL",
                             font=("Arial", 12)).pack(pady=10)
            else:
                ctk.CTkLabel(time_period_averages_container, text=f"No data available for {period}",
                             font=("Arial", 12)).pack()

    def display_extreme_values(self, frame, data, top_n=5):
        collapsible_frame_high = CollapsibleFrame(frame, title="Highest Blood Sugar Levels")
        collapsible_frame_high.pack(pady=15, fill="x")

        highest_values_container = self.create_background_frame(collapsible_frame_high.content_frame)
        highest_values = data.nlargest(top_n, 'Blood Glucose Level (mg/dL)')
        for _, row in highest_values.iterrows():
            ctk.CTkLabel(highest_values_container,
                         text=f"{row['Date']} {row['Time']}: {row['Blood Glucose Level (mg/dL)']} mg/dL - {row['Notes']}",
                         font=("Arial", 12)).pack(pady=2)

        collapsible_frame_low = CollapsibleFrame(frame, title="Lowest Blood Sugar Levels")
        collapsible_frame_low.pack(pady=15, fill="x")

        lowest_values_container = self.create_background_frame(collapsible_frame_low.content_frame)
        lowest_values = data.nsmallest(top_n, 'Blood Glucose Level (mg/dL)')
        for _, row in lowest_values.iterrows():
            ctk.CTkLabel(lowest_values_container,
                         text=f"{row['Date']} {row['Time']}: {row['Blood Glucose Level (mg/dL)']} mg/dL - {row['Notes']}",
                         font=("Arial", 12)).pack(pady=2)


    def export_insights(self, meal_stats, category_counts, daily_avg, time_period_averages):
        """
        Exports insights to a CSV file.

        Args:
            meal_stats (DataFrame): The meal statistics to export.
            category_counts (Series): The category counts to export.
            daily_avg (Series): The daily averages to export.
            time_period_averages (dict): The time period averages to export.
        """
        export_path = filedialog.asksaveasfile(mode="w", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], parent=self.app.root)
        if export_path:
            export_data = [["Meal Statistics"], ['Meal', 'Mean', 'Std Dev', 'Min', 'Max', 'Count', 'Range']]
            for meal, stats in meal_stats.iterrows():
                export_data.append([meal, stats['mean'], stats['std'], stats['min'], stats['max'], stats['count'], stats['range']])
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
            for period, avg in time_period_averages.items():
                export_data.append([f"{period} Average", round(avg, 2)])
            with open(export_path.name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(export_data)
            messagebox.showinfo("Export Successful", f"Insights exported to {export_path.name}.")

    def create_background_frame(self, parent):
        """
        Creates a white background frame with a fixed width of 400.

        Args:
            parent (CTkFrame): The parent frame to attach the background frame.

        Returns:
            CTkFrame: The created background frame.
        """
        background_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", width=400)
        background_frame.pack(padx=50, pady=5, fill="x", anchor="center")
        return background_frame


class CollapsibleFrame(ctk.CTkFrame):
    def __init__(self, master, title="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title = title
        self.is_collapsed = True

        self.header = ctk.CTkFrame(self, fg_color=c.BG_COLOR)
        self.header.pack(fill="x", expand=True)
        self.header_label = ctk.CTkLabel(self.header, text=self.title, font=("Arial", 16, "bold"), anchor="center",
                                         justify="center")
        self.header_label.pack(side="left", pady=10, expand=True)
        self.toggle_button = ctk.CTkButton(self.header, text="▼", width=2, command=self.toggle, fg_color=c.BG_COLOR,
                                           hover_color=c.BG_COLOR, text_color="black")
        self.toggle_button.pack(side="right", padx=10)

        self.content_frame = ctk.CTkFrame(self, fg_color=c.BG_COLOR)

    def toggle(self):
        if self.is_collapsed:
            self.content_frame.pack(fill="x", expand=True)
            self.toggle_button.configure(text="▲")
        else:
            self.content_frame.pack_forget()
            self.toggle_button.configure(text="▼")
        self.is_collapsed = not self.is_collapsed