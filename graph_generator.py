import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import messagebox, filedialog
import colors as c
import tkinter as tk

class GraphGenerator:
    def __init__(self, app):
        """
        Initializes the GraphGenerator.

        Args:
            app: The main application instance.
        """
        self.app = app

    def make_graph_levels_over_time(self, data_file):
        """
        Creates a graph of blood glucose levels over time.

        Args:
            data_file: The path to the CSV file containing the data.
        """
        data = pd.read_csv(data_file)
        if {"Date", "Time", "Blood Glucose Level (mg/dL)"}.issubset(data.columns):
            data["Datetime"] = pd.to_datetime(data["Date"] + " " + data["Time"])
            peaks = data["Blood Glucose Level (mg/dL)"].nlargest(3)
            peak_indices = peaks.index
            peak_datetimes = data.loc[peak_indices, "Datetime"]
            peak_values = data.loc[peak_indices, "Blood Glucose Level (mg/dL)"]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data["Datetime"], data["Blood Glucose Level (mg/dL)"], label="Glucose Levels", marker="o")
            ax.scatter(peak_datetimes, peak_values, color="red", label="Peaks", zorder=5)

            ax.set_title("Blood Glucose Monitoring", fontsize=20)
            ax.set_xlabel("Datetime", fontsize=16)
            ax.set_ylabel("Blood Glucose Level (mg/dL)", fontsize=16)
            ax.tick_params(axis="x", rotation=45, labelsize=12)
            ax.tick_params(axis="y", labelsize=12)
            ax.legend(fontsize=14)
            ax.grid(alpha=0.7, linestyle="--")

            self.display_graph_window(fig)
        else:
            messagebox.showerror(
                "Error", "Dataset must include 'Date', 'Time', and 'Blood Glucose Level (mg/dL)' columns."
            )

    def make_graph_levels_meal(self, data_file):
        """
        Creates a bar chart of blood glucose levels by meal.

        Args:
            data_file: The path to the CSV file containing the data.
        """
        data = pd.read_csv(data_file)
        if {"Meal", "Blood Glucose Level (mg/dL)"}.issubset(data.columns):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(data["Meal"], data["Blood Glucose Level (mg/dL)"], color="skyblue", edgecolor="black", alpha=0.8)

            ax.set_title("Blood Glucose Levels by Meal", fontsize=20)
            ax.set_xlabel("Meal", fontsize=16)
            ax.set_ylabel("Blood Glucose Level (mg/dL)", fontsize=16)
            ax.tick_params(axis="x", rotation=45, labelsize=12)
            ax.tick_params(axis="y", labelsize=12)
            ax.grid(alpha=0.7, linestyle="--")

            self.display_graph_window(fig)
        else:
            messagebox.showerror(
                "Error", "Dataset must include 'Meal' and 'Blood Glucose Level (mg/dL)' columns."
            )

    def display_graph_window(self, fig):
        """
        Creates a new window to display the graph.

        Args:
            fig (matplotlib.figure.Figure): The figure to display.
        """
        graph_window = ctk.CTkToplevel(self.app.root)
        graph_window.title("Blood Glucose Graph")
        graph_window.geometry("800x600")
        graph_window.lift()
        graph_window.config(bg=c.BG_COLOR)

        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(5, 20))
        canvas.draw()

        save_button = ctk.CTkButton(graph_window, text="Save Graph", command=lambda: self.app.save_graph(fig))
        save_button.pack(pady=10)

    def show_bmi_all_users(self, users, bmis):
        max_bmi = max(bmis)
        min_bmi = min(bmis)
        max_bmi_user = users[bmis.index(max_bmi)]
        min_bmi_user = users[bmis.index(min_bmi)]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(users, bmis, marker='o', color='#4682B4', label='BMI')
        ax.plot(max_bmi_user, max_bmi, marker='o', color='red', label='Highest BMI')
        ax.plot(min_bmi_user, min_bmi, marker='o', color='purple', label='Lowest BMI')
        ax.set_xlabel('Users')
        ax.set_ylabel('BMI')
        ax.set_title('BMI of All Users')
        ax.legend()
        fig.tight_layout()

        self.display_graph_window(fig)

    def show_avg_bmi_by_type(self, avg_bmi_per_type):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        for i, (dtype, avg_bmi) in enumerate(avg_bmi_per_type.items()):
            dtype_wrapped = dtype.replace(" ", "\n")
            ax.bar(dtype_wrapped, avg_bmi, color=colors[i % len(colors)])
        ax.set_xlabel('Diabetes Type')
        ax.set_ylabel('Average BMI')
        ax.set_title('Average BMI for Each Diabetes Type')
        fig.tight_layout()

        self.display_graph_window(fig)