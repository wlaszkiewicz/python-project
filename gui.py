import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
data_file = None  # Global variable to store the file path
canvas = None  # Global variable to store the plot

def load_file():
    global data_file
    # Open file dialog to select the CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data_file = file_path  # Save the file path for later use

def make_graph():
    global data_file, canvas

    if data_file is None:
        # Show an error message if no file is loaded
        messagebox.showerror("Error", "No dataset loaded. Please choose a file first.")
        return

    # Destroy the previous canvas if it exists
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Load the dataset
    data = pd.read_csv(data_file)

    # Convert 'Date' and 'Time' columns to a single datetime column
    if 'Date' in data.columns and 'Time' in data.columns and 'Blood Glucose Level (mg/dL)' in data.columns:
        data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

        # Identify peak values
        peak_indices = data['Blood Glucose Level (mg/dL)'].nlargest(3).index  # Change 3 to the desired number of peaks
        peak_datetimes = data.loc[peak_indices, 'Datetime']
        peak_values = data.loc[peak_indices, 'Blood Glucose Level (mg/dL)']

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(data['Datetime'], data['Blood Glucose Level (mg/dL)'], marker='o', label='Blood Glucose Level')

        # Highlight peaks in red
        ax.scatter(peak_datetimes, peak_values, color='red', label='Peaks', zorder=5)

        # Adding labels and title
        ax.set_title('Blood Sugar Monitoring', fontsize=14)
        ax.set_xlabel('Datetime', fontsize=12)
        ax.set_ylabel('Blood Glucose Level (mg/dL)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        fig.tight_layout()

        # Embed the plot in the Tkinter app
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack(pady=10, padx=10)
        canvas.draw()
    else:
        messagebox.showerror("Error", "The dataset does not have the required columns ('Date', 'Time', 'Blood Glucose Level (mg/dL)').")


def initialize_gui():
    # Create the main window
    root.title("Diabetes")
    root.geometry("800x600")  # Set the window size to 800x600 pixels

    # Add a label widget
    label = tk.Label(root, text="Hello, Diabetyk!")
    label.pack(pady=20)

    # Add buttons for loading the file and making the graph
    button_load = tk.Button(root, text='Choose the dataset / file', width=25, command=load_file, bg="#73B8F3",
                            activeforeground="black", activebackground="#4190F0", fg="black")
    button_load.pack(pady=10)

    button_graph = tk.Button(root, text='Create Graph', width=25, command=make_graph, bg="#73B8F3",
                             activeforeground="black", activebackground="#4190F0", fg="black")
    button_graph.pack(pady=10)

    # Run the main loop
    root.mainloop()

if __name__ == '__main__':
    initialize_gui()
