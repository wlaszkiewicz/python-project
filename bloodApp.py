import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, font, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
import json
from datetime import datetime
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
        ctk.CTkButton(self, text="Load existing user", command=self.choose_user).pack(pady=20)

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
            return  # If the user frame already exists, do nothing

        self.user_info = self.app.load_user_data()
        if not self.user_info:
            messagebox.showerror("Error", "No user data found. Please create a new user.")
            return

        user_list = list(self.user_info.keys())
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
        app.selected_user = self.user_var.get()
        app.users_info = self.app.load_user_data()
        if app.selected_user in app.users_info:
            self.app.info_frame.user_info = app.load_user_data(app.selected_user)
            self.app.info_frame.populate_user_info()
            self.app.show_frame(self.app.main_frame)
        else:
            messagebox.showerror("Error", "User data not found.")


class InfoFrame(ctk.CTkFrame):
    """
    This class creates a graphical user interface for users to input and manage their personal health information.
    It presents a form layout for various inputs including name, gender, date of birth, weight, height, and diabetes
    type, and calculates the user's Body Mass Index (BMI). The class is designed as a frame to be part of a larger
    application.

    It includes features such as input validations, interactive elements (e.g., calendar for DOB selection),
    and options for saving and retrieving user data.

    :ivar app: Reference to the main application to interact with other components and functionalities.
    :type app: Tkinter or CTk application instance
    :ivar user_info: Dictionary containing the current user's information such as name, gender, DOB, weight,
        height, BMI, etc.
    :type user_info: dict or None
    :ivar name_entry: Input field for the user's name.
    :type name_entry: CTkEntry
    :ivar gender_var: String variable to hold the value of the selected gender radio button.
    :type gender_var: tkinter.StringVar
    :ivar dob_entry: Input field for the user's date of birth.
    :type dob_entry: CTkEntry
    :ivar weight_entry: Input field for the user's weight.
    :type weight_entry: CTkEntry
    :ivar height_entry: Input field for the user's height.
    :type height_entry: CTkEntry
    :ivar bmi_label: Label displaying the calculated BMI.
    :type bmi_label: CTkLabel
    :ivar diabetes_var: String variable to hold the selected type of diabetes from the combo box.
    :type diabetes_var: tkinter.StringVar
    :ivar cal_window: Reference to the popup calendar window for selecting DOB.
    :type cal_window: CTkToplevel or None
    :ivar cal: Calendar widget for date selection in the calendar window.
    :type cal: tkcalendar.Calendar or None
    """
    def __init__(self, app):
        """
        Initializes a form GUI for collecting user-specific information such as name, gender,
        date of birth, weight, height, and diabetes type. The information is used within the
        application to manage user data and related operations.

        :param app: The parent application instance.
        :type app: Any
        :raises ValueError: Raised during value validation if input is invalid.

        Attributes
        ----------
        app : Any
            Reference to the main application instance.
        user_info : Any
            Placeholder to store information entered by the user.
        name_entry : ctk.CTkEntry
            Entry widget for user-provided name.
        gender_var : tk.StringVar
            Variable for storing selected gender option.
        dob_entry : ctk.CTkEntry
            Entry widget for user-provided date of birth.
            Triggers a calendar pop-up when clicked.
        weight_entry : ctk.CTkEntry
            Entry widget for user input weight in kilograms.
            Updates BMI when value changes.
        height_entry : ctk.CTkEntry
            Entry widget for user input height in centimeters.
            Updates BMI when value changes.
        bmi_label : ctk.CTkLabel
            Label to display calculated BMI.
        diabetes_var : tk.StringVar
            Variable for storing selected type of diabetes.
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        self.user_info = None
        form_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        form_frame.pack(pady=50, padx=20)

        ctk.CTkLabel(form_frame, text="Enter your information", font=("Helvetica", 16), text_color="#333333").grid(
            row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(form_frame, text="Name:", text_color="#333333").grid(row=1, column=0, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(form_frame)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)

        ctk.CTkLabel(form_frame, text="Gender:", text_color="#333333").grid(row=2, column=0, pady=5, sticky="e")
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = ctk.CTkFrame(form_frame, fg_color=BG_COLOR)
        gender_frame.grid(row=2, column=1, pady=5, padx=10)
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male",
                           text_color="#333333").pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female",
                           text_color="#333333").pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Other", variable=self.gender_var, value="Other",
                           text_color="#333333").pack(side="left", padx=5)

        ctk.CTkLabel(form_frame, text="Date of Birth:", text_color="#333333").grid(row=3, column=0, pady=5, sticky="e")
        self.dob_entry = ctk.CTkEntry(form_frame)
        self.dob_entry.grid(row=3, column=1, pady=5, padx=10)
        self.dob_entry.bind("<Button-1>", self.open_calendar)

        ctk.CTkLabel(form_frame, text="Weight (kg):", text_color="#333333").grid(row=4, column=0, pady=5, sticky="e")
        self.weight_entry = ctk.CTkEntry(form_frame)
        self.weight_entry.grid(row=4, column=1, pady=5, padx=10)
        self.weight_entry.bind("<KeyRelease>", self.update_bmi)

        ctk.CTkLabel(form_frame, text="Height (cm):", text_color="#333333").grid(row=5, column=0, pady=5, sticky="e")
        self.height_entry = ctk.CTkEntry(form_frame)
        self.height_entry.grid(row=5, column=1, pady=5, padx=10)
        self.height_entry.bind("<KeyRelease>", self.update_bmi)

        self.bmi_label = ctk.CTkLabel(form_frame, text="BMI: ", text_color="#333333")
        self.bmi_label.grid(row=6, column=0, columnspan=2, pady=10)

        diabetes_options = ["Type 1", "Type 2", "Gestational Diabetes", "LADA (Latent autoimmune diabetes in adults)",
                            "MODY (Maturity Onset Diabetes of the Young)", "Neonatal Diabetes",
                            "Cystic Fibrosis-related Diabetes", "Steroid-induced Diabetes", "Other"]
        ctk.CTkLabel(form_frame, text="Diabetes Type:", text_color="#333333").grid(row=7, column=0, pady=5, sticky="e")
        self.diabetes_var = tk.StringVar(value=diabetes_options[0])
        ctk.CTkComboBox(form_frame, values=diabetes_options, variable=self.diabetes_var, text_color="#333333").grid(
            row=7, column=1, pady=5, padx=10)

        ctk.CTkButton(form_frame, text="Save Information", command=self.save_user_info, text_color="#333333").grid(
            row=8, column=0, columnspan=2, pady=20)

        ctk.CTkButton(form_frame, text="Go Back", command=lambda: app.show_frame(app.welcome_frame),
                      text_color="#333333").grid(
            row=9, column=0, columnspan=2, pady=20)

    def populate_user_info(self):
        """
        Populates user information into the user input fields in the UI.

        This function retrieves the user details from the `user_info` attribute and
        updates the corresponding fields in the user interface. It uses default values
        where applicable if certain details are not found.

        :raises AttributeError: If any of the input fields or the `user_info`
            dictionary is not properly initialized before calling this method.

        """
        if self.user_info:  # If user data is found
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.app.selected_user)
            self.gender_var.set(self.user_info.get("gender", "Male"))
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, self.user_info.get("dob", ""))
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, self.user_info.get("weight", ""))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, self.user_info.get("height", ""))
            self.diabetes_var.set(self.user_info.get("diabetes_type", "Type 1"))
            self.update_bmi()


    def open_calendar(self, event):
        """
        Opens a pop-up calendar window for selecting a date of birth. The calendar's
        date selection is restricted to dates up to today's date. The calendar window
        is dynamically resizable and remains always on top of other windows.

        The calendar pop-up features:
        - A bold custom font for the calendar title
        - Dynamically resizable layout
        - A 'Select' button beneath the calendar to confirm date selection

        :param event: The triggering event object
        :type event: Any

        :return: None
        """
        self.cal_window = ctk.CTkToplevel(self.app.root)
        self.cal_window.title("Select Date of Birth")
        self.cal_window.geometry("300x300")
        self.cal_window.config(bg=BG_COLOR)
        self.cal_window.attributes('-topmost', True)  # Always on top

        # Configure the window to adjust dynamically
        self.cal_window.rowconfigure(0, weight=1)
        self.cal_window.columnconfigure(0, weight=1)

        # Get today's date
        today = datetime.now().date()

        # Custom font for the calendar's title
        title_font = font.Font(size=16, weight='bold')

        self.cal = Calendar(
            self.cal_window,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            year=2000,
            month=1,
            day=1,
            maxdate=today,
        )
        # Adjust title font
        self.cal["font"] = title_font

        self.cal.grid(row=0, column=0, sticky='nsew')  # Fill both vertically and horizontally

        # Add the button and place it below the calendar
        button = ctk.CTkButton(self.cal_window, text="Select", command=self.select_date)
        button.grid(row=1, column=0, pady=20)

    def select_date(self):
        """
        Selects a date from the calendar widget and applies it to the date of birth
        entry field. This method clears any existing input in the date of birth entry,
        inserts the selected date from the calendar, and then closes the calendar
        window.

        :return: None
        """
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, self.cal.get_date())
        self.cal_window.destroy()

    def update_bmi(self, event=None):
        """
        Updates the Body Mass Index (BMI) based on weight and height values inputted
        by the user. Converts the height from centimeters to meters and calculates
        BMI using the formula weight divided by the square of height. If invalid
        inputs are provided, the BMI label is cleared.

        :param event: GUI event triggering the BMI update. Defaults to None.
        :type event: object or None
        :return: None
        """
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            bmi = weight / (height ** 2)
            self.bmi_label.configure(text=f"BMI: {bmi:.2f}")
        except ValueError:
            self.bmi_label.configure(text="BMI: ")

    def save_user_info(self):
        """
        Saves user information from the input fields to the application data.

        This method collects user information including name, date of birth, weight,
        height, gender, and diabetes type from input fields. It calculates the user's
        age and BMI (Body Mass Index). The calculated data along with other collected
        information is then added to the application's user records and persisted by
        saving the data. If an error occurs (e.g., invalid or missing input data),
        relevant error messages will be displayed.

        :raises ValueError: Raised if the entered weight or height is invalid.
        :param self: Represents the instance of the class to access enclosed properties.
        :return: None
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        dob = self.dob_entry.get()
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            bmi = weight / (height ** 2)
            self.bmi_label.configure(text=f"BMI: {bmi:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")
            return

        self.app.users_info[name] = {
            "gender": self.gender_var.get(),
            "dob": dob,
            "age": age,
            "weight": weight,
            "height": height * 100,
            "bmi": bmi,
            "diabetes_type": self.diabetes_var.get()
        }

        self.app.save_user_data(self.app.users_info)
        messagebox.showinfo("Info", "User information saved successfully!")
        self.app.show_frame(self.app.main_frame)


class MainFrame(ctk.CTkFrame):
    """
    MainFrame Class.

    Represents the main frame of the Blood Glucose Monitoring application. This frame
    serves as the central interface for users to select actions such as choosing a
    dataset/file, navigating to other frames, visualizing data trends, and generating
    insights. It includes buttons organized in a structured layout, grouped into
    functional categories.

    :ivar app: Reference to the main application instance that contains the root
        window and necessary methods for frame navigation, data loading, graph
        generation, and analytics functionality.
    :type app: Application
    """
    def __init__(self, app):
        """
        Represents a UI for Blood Glucose Monitoring using custom widgets and layout. This
        widget is initialized with a parent application and contains buttons for various
        functionalities like loading datasets, viewing graphs, and generating insights.

        This widget is designed to occupy the entire parent frame and includes labels and
        buttons arranged in two rows. The first row provides options for file operations and
        navigation, while the second row includes buttons for graph generation and insights analysis.

        :param app: The parent application containing references to shared resources and
            methods like navigation and data handling.
        :type app: Application
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        ctk.CTkLabel(self, text="Blood Glucose Monitoring", font=("Arial", 18)).pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        button_frame.pack(pady=20)

        # First row: Choose Dataset/File, Change My Data, Go Back
        ctk.CTkButton(button_frame, text="Choose Dataset/File", width=20, command=app.load_file).grid(row=0, column=0,
                                                                                                      padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Change My Data", width=20,
                      command=lambda: app.show_frame(app.info_frame)).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Go Back", width=20, command=lambda: app.show_frame(app.welcome_frame)).grid(
            row=0, column=2, padx=10, pady=10)

        # Second row: Graph buttons in a column
        ctk.CTkButton(button_frame, text="Blood Glucose Trends Over Timer Graph", width=20,
                      command=app.make_graph_levels_over_time).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Blood Glucose Levels Depending on the Meal", width=20,
                      command=app.make_graph_levels_meal).grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Generate Insights", width=20, command=app.generate_insights).grid(row=3, column=0, columnspan=3, padx=10, pady=10)


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

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    app.center_window(900, 700)
    root.mainloop()