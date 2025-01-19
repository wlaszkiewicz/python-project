from CustomThresholdDialog import CustomThresholdDialog
from WelcomeFrame import WelcomeFrame
from InfoFrame import InfoFrame
from MainFrame import MainFrame
import customtkinter as ctk
from tkinter import filedialog, messagebox, font, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv


BG_COLOR = "#dbdbdb"
low_threshold = None
high_threshold = None

class App:
    """
    Manages the GUI and functionality of a Blood Glucose Monitor application. The class facilitates user interaction,
    data visualization, and insights generation based on loaded blood glucose level data.

    This application is designed to assist users in monitoring and analyzing blood glucose levels. By providing options
    to load data, generate graphical representations, and analyze patterns, it aims to enhance the user's understanding
    of their glucose trends and assist in making informed decisions.

    :ivar root: The root window of the application.
    :type root: tkinter.Tk
    :ivar data_file: The file path of the loaded dataset, initialized to None.
    :type data_file: Optional[str]
    :ivar canvas: Canvas used for plotting figures, initialized to None.
    :type canvas: Optional[Canvas]
    :ivar users_info: Dictionary storing information about multiple users.
    :type users_info: dict
    :ivar selected_user: Current selected user for interaction, initialized to None.
    :type selected_user: Optional[str]
    :ivar user_data_file: File path to the storage of user information in JSON format.
    :type user_data_file: str
    :ivar welcome_frame: The welcome frame of the GUI.
    :type welcome_frame: WelcomeFrame
    :ivar info_frame: The information frame of the GUI.
    :type info_frame: InfoFrame
    :ivar main_frame: The main frame of the GUI.
    :type main_frame: MainFrame
    """
    def __init__(self, root):
        """
        This class initializes and manages the main application window for the Blood
        Glucose Monitor application. It sets up the application interface, including
        appearance, frames, and user-specific data handling. It serves as the parent
        window and interacts with various frames to manage user navigation and actions.

        :param root: The Tkinter root widget that serves as the main container for the
            application.
        :type root: tkinter.Tk
        """
        self.root = root
        self.root.title("Blood Glucose Monitor")
        self.root.geometry("900x700")
        self.root.config(bg=BG_COLOR)  # Light background
        self.data_file = None
        self.canvas = None
        self.users_info = {}
        self.selected_user = None
        self.user_data_file = "user_info.json"
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.welcome_frame = WelcomeFrame(self)
        self.info_frame = InfoFrame(self)
        self.main_frame = MainFrame(self)

        self.show_frame(self.welcome_frame)

    def show_frame(self, frame):
        """
        Raises the specified frame to the top of the display stack, essentially
        making it the visible frame in a Tkinter application. This method is
        used to switch between different frames or views defined in the
        application. Each frame is managed by the Tkinter toolkit and identified
        using its reference.

        :param frame: The frame object to bring to the foreground. The frame
            should be a valid Tkinter widget that supports the `tkraise`
            method.
        :return: None
        """
        frame.tkraise()

    def center_window(self, width, height):
        """
        Centers the application window on the user's screen based on the provided
        width and height. The method calculates the positional offsets required to
        place the window in the center of the screen.

        :param width: Width of the application window in pixels.
        :type width: int
        :param height: Height of the application window in pixels.
        :type height: int
        :return: None
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def load_file(self):
        """
        Opens a file dialog to select a CSV file and loads the selected file path. If a file is chosen,
        it sets the file path to the `data_file` attribute and displays a success message.

        :raises FileNotFoundError: if no file is selected or the operation is canceled

        :return: None
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], parent=self.root)
        if file_path:
            self.data_file = file_path
            messagebox.showinfo("File Loaded", "Dataset loaded successfully!")

    def make_graph_levels_over_time(self):
        """
        Generates and displays a graph for visualizing blood glucose levels over time. The graph includes annotations for the top
        peak values and their corresponding timestamps. The user can optionally save the graph to a PDF file.

        :raises tkinter.messagebox.showerror: Raises an error dialog if no dataset is loaded or if the dataset does not contain
            the required columns ('Date', 'Time', 'Blood Glucose Level (mg/dL)').

        :param self.data_file: str
            Path to the dataset file in CSV format to be loaded and visualized.
        :param self.root: tkinter.Tk
            The root window instance for the application.

        :return: None
        """
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return

        data = pd.read_csv(self.data_file)
        if 'Date' in data.columns and 'Time' in data.columns and 'Blood Glucose Level (mg/dL)' in data.columns:
            data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
            peak_indices = data['Blood Glucose Level (mg/dL)'].nlargest(3).index
            peak_datetimes = data.loc[peak_indices, 'Datetime']
            peak_values = data.loc[peak_indices, 'Blood Glucose Level (mg/dL)']

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data['Datetime'], data['Blood Glucose Level (mg/dL)'], marker='o', label='Blood Glucose Level')
            ax.scatter(peak_datetimes, peak_values, color='red', label='Peaks', zorder=5)

            # Adjust font size here
            ax.set_title('Blood Sugar Monitoring', fontsize=20)  # Increase title font size
            ax.set_xlabel('Datetime', fontsize=16)  # Increase xlabel font size
            ax.set_ylabel('Blood Glucose Level (mg/dL)', fontsize=16)  # Increase ylabel font size

            # Increase tick font size
            ax.tick_params(axis='x', rotation=45, labelsize=14)  # Increase x-axis tick font size
            ax.tick_params(axis='y', labelsize=14)  # Increase y-axis tick font size

            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(fontsize=14)  # Increase legend font size
            fig.tight_layout()

            graph_window = ctk.CTkToplevel(self.root)
            graph_window.title("Blood Glucose Graph")
            graph_window.attributes('-topmost', True)
            graph_window.config(bg=BG_COLOR)
            graph_window.geometry("800x600")

            canvas = FigureCanvasTkAgg(fig, graph_window)
            canvas.get_tk_widget().pack(fill='both', expand=True, pady=(5, 50))
            canvas.draw()

            def save_graph():
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], parent=self.root)
                if file_path:
                    fig.savefig(file_path)
                    messagebox.showinfo("Success", "Graph saved successfully!")

            save_button = ctk.CTkButton(graph_window, text="Save Graph", command=save_graph)
            save_button.pack(pady=10)
        else:
            messagebox.showerror("Error",
                                 "The dataset does not have the required columns ('Date', 'Time', 'Blood Glucose Level (mg/dL)').")


    #graph levels depending on the meal
    def make_graph_levels_meal(self):
        """
        Creates a bar graph displaying blood glucose levels corresponding to meals. It uses a
        dataset provided as a CSV file to generate the visualization and displays the graph
        in a new window with options to save the graph as a PDF file. The function ensures that
        the required dataset columns are available before proceeding, and displays appropriate
        error messages otherwise.

        :param self: Instance of the class where this function is defined. Expects the following
            attributes to be present:
            - self.data_file: The file path to the dataset (string) or None.
            - self.root: The root widget for the graphical user interface.
        :return: None
        :raises: Displays an error message box if no dataset is loaded or if the columns
            'Meal' and 'Blood Glucose Level (mg/dL)' are missing in the dataset.
        """
        if self.data_file is None:
            messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
            return

        data = pd.read_csv(self.data_file)
        if 'Meal' in data.columns and 'Blood Glucose Level (mg/dL)' in data.columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(data['Meal'], data['Blood Glucose Level (mg/dL)'], color='skyblue', edgecolor='black', alpha=0.7)
            ax.set_title('Blood Sugar Monitoring', fontsize=20)
            ax.set_xlabel('Meal', fontsize=16)
            ax.set_ylabel('Blood Glucose Level (mg/dL)', fontsize=16)

            ax.tick_params(axis='x', rotation=45, labelsize=14)
            ax.tick_params(axis='y', labelsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)
            fig.tight_layout()

            graph_window = ctk.CTkToplevel(self.root)
            graph_window.title("Blood Glucose Graph")
            graph_window.attributes('-topmost', True)
            graph_window.config(bg=BG_COLOR)
            graph_window.geometry("800x600")

            canvas = FigureCanvasTkAgg(fig, graph_window)
            canvas.get_tk_widget().pack(fill='both', expand=True, pady=(5, 50))
            canvas.draw()

            def save_graph():
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], parent=self.root)
                if file_path:
                    fig.savefig(file_path)
                    messagebox.showinfo("Success", "Graph saved successfully!")

            save_button = ctk.CTkButton(graph_window, text="Save Graph", command=save_graph)
            save_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "The dataset does not have the required columns ('Meal', 'Blood Glucose Level (mg/dL)').")

    def generate_insights(self):
        """
        Generates insights from the loaded blood glucose dataset and displays them
        in a new interactive window. The function processes the data to provide
        descriptive statistics, categorization, time in target ranges, daily averages,
        and averages across different periods of the day. The results are dynamically
        displayed in a detailed insights window.

        This function requires a CSV dataset containing blood glucose level data
        along with associated meal information and timestamp details. If the dataset
        is missing or incomplete, the user will be prompted for correction. Threshold
        values for blood glucose levels need to be specified for categorization. The
        results include calculated metrics, patterns, and categorizations that facilitate
        better understanding of blood glucose behavior and management.

        :raises Exception: If the dataset is not loaded or is missing required columns.
        :raises FileNotFoundError: When the dataset file is not available.

        :param self: Instance of the current class containing dataset file path
            and root for dynamic UI modifications.
        :return: None
        """
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

            # Thresholds
            if not low_threshold or not high_threshold:
                threshold_dialog = CustomThresholdDialog(self.root, "Set Thresholds", low_initial=70, high_initial=180)
                thresholds = threshold_dialog.show()
                if not thresholds:
                    return # If the user cancels the dialog
                low_threshold, high_threshold = thresholds

            # Categorize glucose levels
            data['Category'] = pd.cut(data['Blood Glucose Level (mg/dL)'], bins=[0, low_threshold, high_threshold, float('inf')],labels=['Low', 'Normal', 'High'])

            # Calculate time in each category
            category_counts = data['Category'].value_counts(normalize=True) * 100

            # Detect patterns
            data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
            data.set_index('Datetime', inplace=True)
            daily_avg = data['Blood Glucose Level (mg/dL)'].resample('D').mean()

            # Detect morning averages
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


            # Insights Window
            insights_window = ctk.CTkToplevel(self.root)
            insights_window.title("Blood Glucose Insights")
            insights_window.attributes('-topmost', True)
            insights_window.geometry("600x600")

            # Frame
            insights_frame = ctk.CTkScrollableFrame(insights_window, fg_color="#FFFFFF", width=780, height=500)
            insights_frame.pack(pady=10, padx=10)

            # Section: Meal Stats
            ctk.CTkLabel(insights_frame, text="Meal Statistics", font=("Arial", 16, "bold")).pack(pady=10)

            # Create a container frame to center the table
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

            # Section: Time in Range
            ctk.CTkLabel(insights_frame, text="Time in Range", font=("Arial", 16, "bold")).pack(pady=10)
            for category, percentage in category_counts.items():
                ctk.CTkLabel(insights_frame, text=f"Time in {category}: {percentage:.2f}%", font=("Arial", 12)).pack(
                    pady=5)

            # Section: Daily Averages
            ctk.CTkLabel(insights_frame, text="Daily Averages", font=("Arial", 16, "bold")).pack(pady=10)
            for date, avg in daily_avg.items():
                ctk.CTkLabel(insights_frame, text=f"{date.date()}: {avg:.2f} mg/dL", font=("Arial", 12)).pack(pady=2)

            # Section: Morning Averages
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
                # Prepare export path
                export_path = filedialog.asksaveasfile(mode="w", defaultextension=".csv",
                                                       filetypes=[("CSV Files", "*.csv")], parent=self.root)
                if export_path:
                    # Prepare data for export
                    export_data = []

                    # Add Meal Statistics
                    export_data.append(["Meal Statistics"])
                    export_data.append(['Meal', 'Mean', 'Std Dev', 'Min', 'Max', 'Count', 'Range'])
                    for meal, stats in meal_stats.iterrows():
                        export_data.append(
                            [meal, stats['mean'], stats['std'], stats['min'], stats['max'], stats['count'],
                             stats['range']])

                    # Add blank row
                    export_data.append([])

                    # Add Time in Range
                    export_data.append(["Time in Range"])
                    export_data.append(['Category', 'Percentage (%)'])
                    for category, percentage in category_counts.items():
                        export_data.append([category, round(percentage, 2)])

                    # Add blank row
                    export_data.append([])

                    # Add Daily Averages
                    export_data.append(["Daily Averages"])
                    export_data.append(['Date', 'Average Glucose (mg/dL)'])
                    for date, avg in daily_avg.items():
                        export_data.append([date.date(), round(avg, 2)])

                    # Add blank row
                    export_data.append([])

                    # Add Morning Averages
                    export_data.append(["Morning Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["06:00-09:00", round(morning_avg, 2)])

                    # Add Noon Averages
                    export_data.append(["Noon Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["09:00-12:00", round(noon_avg, 2)])

                    # Add Afternoon Averages
                    export_data.append(["Afternoon Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["12:00-18:00", round(afternoon_avg, 2)])

                    # Add Evening Averages
                    export_data.append(["Evening Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["18:00-21:00", round(evening_avg, 2)])

                    # Add Night Averages
                    export_data.append(["Night Average"])
                    export_data.append(['Time Period', 'Average Glucose (mg/dL)'])
                    export_data.append(["21:00-06:00", round(night_avg, 2)])


                    # Export to CSV
                    with open(export_path.name, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(export_data)

                    # Show success message
                    messagebox.showinfo("Export Successful", f"Insights exported to {export_path.name}.")

            ctk.CTkButton(insights_window, text="Export to CSV", command=export_insights).pack(pady=10)

        else:
            messagebox.showerror("Error",
                                 "The dataset does not have the required columns ('Meal', 'Blood Glucose Level (mg/dL)').")

    def save_user_data(self, new_data):
        """
        Saves the updated user data by merging it with the previously saved data. Updates the local
        data storage file with the combined result. Displays an error message if the operation fails.

        :param new_data: Dictionary containing new user data to be added or updated in the existing
            data storage.
        :type new_data: dict
        :return: None
        :rtype: None
        """
        try:
            data = self.load_user_data()
            data.update(new_data)
            with open(self.user_data_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user information: {e}")

    def load_user_data(self, username=None):
        """
        Loads user data from a specified JSON file. If a username is provided, retrieves
        data specific to that user. Otherwise, returns the entire data set. If the file does
        not exist or cannot be read as valid JSON, an empty dictionary is returned for all
        users or None for a specific user.

        :param username: The username of the specific user for whom to load data. Defaults to None.
        :type username: Optional[str]
        :return: A dictionary containing user-specific data if username is provided,
                 all users' data if username is None, or None if username data is not found.
        :rtype: Union[dict, None]
        :raises FileNotFoundError: If the specified file does not exist.
        :raises json.JSONDecodeError: If the file contains invalid JSON content.
        """
        try:
            with open(self.user_data_file, "r") as file:
                data = json.load(file)
                if username:
                    return data.get(username, {})
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if not username else None