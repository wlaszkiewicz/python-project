import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import datetime
import colors as c

low_threshold = None
high_threshold = None

class InfoFrame(ctk.CTkFrame):
    def __init__(self, app):
        """
        Initializes the InfoFrame.

        Args:
            app: The main application instance.
        """
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        self.user_info = None
        self.from_welcome_frame = True

        form_frame = ctk.CTkFrame(self, fg_color=c.BG_COLOR)
        form_frame.pack(pady=10, padx=20)

        ctk.CTkLabel(
            form_frame,
            text="Enter Your Information",
            font=("Helvetica", 18, "bold"),
            text_color="#2C3E50"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(form_frame, text="Name:", text_color="#333333").grid(row=1, column=0, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your name")
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)

        ctk.CTkLabel(form_frame, text="Gender:", text_color="#333333").grid(row=2, column=0, pady=5, sticky="e")
        self.gender_var = tk.StringVar(value=None)
        gender_frame = ctk.CTkFrame(form_frame, fg_color=c.BG_COLOR)
        gender_frame.grid(row=2, column=1, pady=5, padx=10)
        for gender in ["Male", "Female", "Other"]:
            ctk.CTkRadioButton(
                gender_frame,
                text=gender,
                variable=self.gender_var,
                value=gender,
                text_color="#333333"
            ).pack(side="left", padx=5)

        ctk.CTkLabel(form_frame, text="Date of Birth:", text_color="#333333").grid(row=3, column=0, pady=5, sticky="e")
        self.dob_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD")
        self.dob_entry.grid(row=3, column=1, pady=5, padx=10)
        self.dob_entry.bind("<Button-1>", self.open_calendar)

        ctk.CTkLabel(form_frame, text="Weight (kg):", text_color="#333333").grid(row=4, column=0, pady=5, sticky="e")
        self.weight_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your weight")
        self.weight_entry.grid(row=4, column=1, pady=5, padx=10)
        self.weight_entry.bind("<KeyRelease>", self.update_bmi)

        ctk.CTkLabel(form_frame, text="Height (cm):", text_color="#333333").grid(row=5, column=0, pady=5, sticky="e")
        self.height_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your height")
        self.height_entry.grid(row=5, column=1, pady=5, padx=10)
        self.height_entry.bind("<KeyRelease>", self.update_bmi)

        self.bmi_label = ctk.CTkLabel(
            form_frame,
            text="BMI: ",
            font=("Helvetica", 14, "bold"),
            text_color="#2C3E50"
        )
        self.bmi_label.grid(row=6, column=0, columnspan=2, pady=10)

        diabetes_options = [
            "Type 1", "Type 2", "Gestational Diabetes", "LADA", "MODY",
            "Neonatal Diabetes", "Cystic Fibrosis-related Diabetes", "Steroid-induced Diabetes", "Other"
        ]
        ctk.CTkLabel(form_frame, text="Diabetes Type:", text_color="#333333").grid(row=7, column=0, pady=5, sticky="e")
        self.diabetes_var = tk.StringVar(value="Choose Diabetes Type")
        ctk.CTkComboBox(form_frame, values=diabetes_options, variable=self.diabetes_var).grid(
            row=7, column=1, pady=20,padx=10
        )

        ctk.CTkButton(
            form_frame,
            text="Save Information",
            command=self.save_user_info,
            text_color="white",
            fg_color=c.VIBRANT_BLUE,
            hover_color=c.BLUE,
        ).grid(row=8, column=0, columnspan=2)

        ctk.CTkButton(
            form_frame,
            text="Go Back",
            command=self.go_back,
            text_color="white",
            fg_color=c.LIGHT_BLUE,
            hover_color=c.LIGHTER_BLUE,
        ).grid(row=9, column=0, columnspan=2, pady=10)


    def populate_user_info(self):
        """
        Populates user information into the user input fields in the UI.

        Raises:
            AttributeError: If any of the input fields or the `user_info`
                dictionary is not properly initialized before calling this method.
        """
        if self.user_info:
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
        Opens a pop-up calendar window for selecting a date of birth.

        Args:
            event: The triggering event object.
        """
        self.cal_window = ctk.CTkToplevel(self.app.root)
        self.cal_window.title("Select Date of Birth")
        self.cal_window.geometry("300x300")
        self.cal_window.config(bg=c.BG_COLOR)
        self.cal_window.attributes('-topmost', True)

        self.cal_window.rowconfigure(0, weight=1)
        self.cal_window.columnconfigure(0, weight=1)

        today = datetime.now().date()

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
        self.cal["font"] = title_font

        self.cal.grid(row=0, column=0, sticky='nsew')

        button = ctk.CTkButton(self.cal_window, text="Select", command=self.select_date)
        button.grid(row=1, column=0, pady=20)

    def select_date(self):
        """
        Selects a date from the calendar widget and applies it to the date of birth entry field.
        """
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, self.cal.get_date())
        self.cal_window.destroy()

    def update_bmi(self, event=None):
        """
        Updates the BMI label based on the weight and height entries.

        Args:
            event: The triggering event object (optional).
        """
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100
            bmi = weight / (height ** 2)
            self.bmi_label.configure(text=f"BMI: {bmi:.2f}")
        except ValueError:
            self.bmi_label.configure(text="BMI: ")

    def save_user_info(self):
        """
        Saves the user information and updates the main application data.
        """

        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        if name in self.app.users_info and name != self.app.main_frame.selected_user:
            messagebox.showerror("Error", "User already exists. Please choose a different name.")
            return

        dob = self.dob_entry.get()
        if not dob:
            messagebox.showerror("Error", "Date of birth is required.")
            return
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100
            bmi = weight / (height ** 2)
            self.bmi_label.configure(text=f"BMI: {bmi:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")
            return

        if self.diabetes_var.get() == "Choose Diabetes Type":
            messagebox.showerror("Error", "Please select a diabetes type.")
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

        self.app.main_frame.selected_user = name
        self.app.main_frame.populate_user_data()
        self.app.show_frame(self.app.main_frame)

    def clear_user_info(self):
        """
        Clears all input fields and resets the form, leaving placeholder values intact.
        """
        self.name_entry.delete(0, tk.END)
        self.name_entry.configure(placeholder_text="Enter your name")
        self.gender_var.set("")
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.configure(placeholder_text="YYYY-MM-DD")
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.configure(placeholder_text="Enter your weight")
        self.height_entry.delete(0, tk.END)
        self.height_entry.configure(placeholder_text="Enter your height")
        self.bmi_label.configure(text="BMI: ")
        self.diabetes_var.set("Choose Diabetes Type")

        self.user_info = None

    def go_back(self):
        """
        Navigates back to the previous frame based on the user's information.
        """
        if self.app.selected_user:
            self.app.show_frame(self.app.main_frame)
        else:
            self.app.show_frame(self.app.welcome_frame)
            self.app.welcome_frame.hide_user_frame()

