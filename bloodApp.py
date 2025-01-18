import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, font
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from patsy.state import center
from tkcalendar import Calendar
import json
from datetime import datetime

BG_COLOR = "#dbdbdb"

class App:
    def __init__(self, root):
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
        frame.tkraise()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data_file = file_path
            messagebox.showinfo("File Loaded", "Dataset loaded successfully!")

    def make_graph(self):
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
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
                if file_path:
                    fig.savefig(file_path)
                    messagebox.showinfo("Success", "Graph saved successfully!")

            save_button = ctk.CTkButton(graph_window, text="Save Graph", command=save_graph)
            save_button.pack(pady=10)
        else:
            messagebox.showerror("Error",
                                 "The dataset does not have the required columns ('Date', 'Time', 'Blood Glucose Level (mg/dL)').")

    def save_user_data(self, new_data):
        try:
            data = self.load_user_data()
            data.update(new_data)
            with open(self.user_data_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user information: {e}")

    def load_user_data(self, username=None):
        try:
            with open(self.user_data_file, "r") as file:
                data = json.load(file)
                if username:
                    return data.get(username, {})
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if not username else None

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        ctk.CTkLabel(self, text="Welcome to Blood Glucose Monitor", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Create a new user", command=lambda: app.show_frame(app.info_frame)).pack(pady=20)
        ctk.CTkButton(self, text="Load existing user", command=self.choose_user).pack(pady=20)

    def choose_user(self):
        self.user_info = self.app.load_user_data()
        if not self.user_info:
            messagebox.showerror("Error", "No user data found. Please create a new user.")
            return

        user_list = list(self.user_info.keys())
        self.user_var = tk.StringVar(value=user_list[0])
        user_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        user_frame.pack(pady=20)
        ctk.CTkLabel(user_frame, text="Select User:", text_color="#333333").pack(side="left", padx=10)
        ctk.CTkComboBox(user_frame, values=user_list, variable=self.user_var, text_color="#333333").pack(side="left", padx=10)
        ctk.CTkButton(user_frame, text="Select", command=self.load_user_data_for_selected_user, text_color="#333333").pack(side="left", padx=10)

    def load_user_data_for_selected_user(self):
        app.selected_user = self.user_var.get()
        app.users_info = self.app.load_user_data()
        if app.selected_user in app.users_info:
            self.app.info_frame.user_info = app.load_user_data(app.selected_user)
            self.app.info_frame.populate_user_info()
            self.app.show_frame(self.app.main_frame)
        else:
            messagebox.showerror("Error", "User data not found.")


class InfoFrame(ctk.CTkFrame):
    def __init__(self, app):
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
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, self.cal.get_date())
        self.cal_window.destroy()

    def update_bmi(self, event=None):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            bmi = weight / (height ** 2)
            self.bmi_label.configure(text=f"BMI: {bmi:.2f}")
        except ValueError:
            self.bmi_label.configure(text="BMI: ")

    def save_user_info(self):
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
    def __init__(self, app):
        super().__init__(app.root, corner_radius=10)
        self.app = app
        self.place(relwidth=1, relheight=1)
        ctk.CTkLabel(self, text="Blood Glucose Monitoring", font=("Arial", 18)).pack(pady=20)
        button_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="Choose Dataset/File", width=20, command=app.load_file).grid(row=0, column=0,
                                                                                                      padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Create The Blood Sugar Graph", width=20, command=app.make_graph).grid(row=0, column=1,
                                                                                                padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Change My Data", width=20, command=lambda: app.show_frame(app.info_frame)).grid(row=0, column=2,
                                                                                                padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Go Back", width=20, command=lambda: app.show_frame(app.welcome_frame)).grid(row=0, column=3,
                                                                                                padx=10, pady=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    app.center_window(900, 700)
    root.mainloop()