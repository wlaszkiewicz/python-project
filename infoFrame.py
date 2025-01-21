import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, font, simpledialog
from tkcalendar import Calendar
from datetime import datetime


BG_COLOR = "#dbdbdb"
low_threshold = None
high_threshold = None

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