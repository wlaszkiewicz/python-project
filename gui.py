import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar

# Initialize the root window using CustomTkinter
root = ctk.CTk()
root.title("Blood Glucose Monitor")
root.geometry("900x700")  # window size
root.config(bg="#F0F4F8") # background color

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')  # set the position

# Global variables for file and canvas
data_file = None
canvas = None
user_info = {}

# Set up custom font and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Function to load the file
def load_file():
    global data_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data_file = file_path
        messagebox.showinfo("File Loaded", "Dataset loaded successfully!")

# Function to create the graph
def make_graph():
    global data_file, canvas

    if data_file is None:
        messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
        return

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    data = pd.read_csv(data_file)

    if 'Date' in data.columns and 'Time' in data.columns and 'Blood Glucose Level (mg/dL)' in data.columns:
        data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

        peak_indices = data['Blood Glucose Level (mg/dL)'].nlargest(3).index
        peak_datetimes = data.loc[peak_indices, 'Datetime']
        peak_values = data.loc[peak_indices, 'Blood Glucose Level (mg/dL)']

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['Datetime'], data['Blood Glucose Level (mg/dL)'], marker='o', label='Blood Glucose Level')

        ax.scatter(peak_datetimes, peak_values, color='red', label='Peaks', zorder=5)
        ax.set_title('Blood Sugar Monitoring', fontsize=16)
        ax.set_xlabel('Datetime', fontsize=12)
        ax.set_ylabel('Blood Glucose Level (mg/dL)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack(pady=20)
        canvas.draw()

    else:
        messagebox.showerror("Error", "The dataset does not have the required columns ('Date', 'Time', 'Blood Glucose Level (mg/dL)').")

def open_user_info_window():
    # Create a new window for user information
    user_window = ctk.CTkToplevel(root)
    user_window.title("Enter Your Information")
    user_window.geometry("400x500")
    user_window.config(bg="#F0F4F8")

    center_window(user_window, 400, 700)

    ctk.CTkLabel(user_window, text="Enter your information", font=("Helvetica", 14),text_color="#333333", bg_color="#F0F4F8").pack(pady=20)

    # Gender Selection
    gender_label = ctk.CTkLabel(user_window, text="Select Gender",text_color="#333333", bg_color="#F0F4F8")
    gender_label.pack(pady=10)

    gender_var = tk.StringVar(value="Male")
    gender_male = ctk.CTkRadioButton(user_window, text="Male", variable=gender_var, value="Male",text_color="#333333", bg_color="#F0F4F8")
    gender_female = ctk.CTkRadioButton(user_window, text="Female", variable=gender_var, value="Female",text_color="#333333", bg_color="#F0F4F8")
    gender_other = ctk.CTkRadioButton(user_window, text="Other", variable=gender_var, value="Other",text_color="#333333", bg_color="#F0F4F8")

    gender_male.pack(pady=5)
    gender_female.pack(pady=5)
    gender_other.pack(pady=5)

    # Age Selection using Spinbox
    age_label = ctk.CTkLabel(user_window, text="Select Age",text_color="#333333", bg_color="#F0F4F8")
    age_label.pack(pady=10)
    age_spinbox = tk.Spinbox(user_window, from_=18, to=100, width=5)
    age_spinbox.pack(pady=5)

    # Date of Birth Selection using Calendar
    dob_label = ctk.CTkLabel(user_window, text="Select Date of Birth",text_color="#333333", bg_color="#F0F4F8")
    dob_label.pack(pady=10)
    cal = Calendar(user_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    # Diabetes Type Selection using ComboBox
    diabetes_label = ctk.CTkLabel(user_window, text="Select Type of Diabetes",text_color="#333333", bg_color="#F0F4F8")
    diabetes_label.pack(pady=10)
    diabetes_options = ["Type 1", "Type 2", "Gestational Diabetes", "Other"]
    diabetes_var = tk.StringVar(value=diabetes_options[0])
    diabetes_combobox = ctk.CTkComboBox(user_window, values=diabetes_options, variable=diabetes_var,text_color="#333333", bg_color="#F0F4F8")
    diabetes_combobox.pack(pady=10)

    def save_user_info():
        user_info["gender"] = gender_var.get()
        user_info["age"] = age_spinbox.get()
        user_info["dob"] = cal.get_date()
        user_info["diabetes_type"] = diabetes_var.get()
        messagebox.showinfo("Info", "Your information has been saved successfully!")
        user_window.destroy()

    save_button = ctk.CTkButton(user_window, text="Save Information", command=save_user_info,text_color="#333333", bg_color="#F0F4F8")
    save_button.pack(pady=20)

def initialize_gui():
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    label = ctk.CTkLabel(frame, text="Blood Glucose Monitoring", font=("Arial", 18))
    label.pack(pady=20)

    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(pady=20)

    button_load = ctk.CTkButton(button_frame, text="Choose Dataset/File", width=20, command=load_file)
    button_load.grid(row=0, column=0, padx=10, pady=10)

    button_graph = ctk.CTkButton(button_frame, text="Create Graph", width=20, command=make_graph)
    button_graph.grid(row=0, column=1, padx=10, pady=10)

    button_user_info = ctk.CTkButton(button_frame, text="Enter Your Information", width=20, command=open_user_info_window)
    button_user_info.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    center_window(root, 900, 700)

    root.mainloop()

if __name__ == "__main__":
    initialize_gui()
