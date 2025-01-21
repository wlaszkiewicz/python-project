import customtkinter as ctk

BG_COLOR = "#dbdbdb"
low_threshold = None
high_threshold = None

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
