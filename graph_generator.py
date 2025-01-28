import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import messagebox, filedialog
import colors as c
import matplotlib.colors as mcolors

class GraphGenerator:
    """
    A class used to generate various graphs for the application.

    Attributes:
        app: The main application instance.

    Args:
        app: The main application instance
    """

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
            data_file (str): The path to the CSV file containing the data.
        """
        data = pd.read_csv(data_file)
        if {"Date", "Time", "Blood Glucose Level (mg/dL)"}.issubset(data.columns):
            data["Datetime"] = pd.to_datetime(data["Date"] + " " + data["Time"])

            fig, ax = plt.subplots(figsize=(12, 6))

            ax.plot(data["Datetime"], data["Blood Glucose Level (mg/dL)"], label="Glucose Levels", marker="o",
                    color="skyblue", linewidth=2)

            hypo_data = data[data["Blood Glucose Level (mg/dL)"] < 70]
            hyper_data = data[data["Blood Glucose Level (mg/dL)"] > 180]

            ax.scatter(hypo_data["Datetime"], hypo_data["Blood Glucose Level (mg/dL)"], color="red", label="Hypoglycemia", zorder=5)
            ax.scatter(hyper_data["Datetime"], hyper_data["Blood Glucose Level (mg/dL)"], color="darkred", label="Hyperglycemia", zorder=5)

            ax.set_title("Blood Glucose Monitoring", fontsize=24, fontweight='bold')
            ax.set_xlabel("Datetime", fontsize=20, fontweight='bold')
            ax.set_ylabel("Blood Glucose Level (mg/dL)", fontsize=20, fontweight='bold')
            ax.tick_params(axis="x", rotation=45, labelsize=16)
            ax.tick_params(axis="y", labelsize=16)
            ax.legend(fontsize=18, loc='upper right', frameon=True, shadow=True, borderpad=1)
            ax.grid(alpha=0.7, linestyle="--", linewidth=0.5)

            self.display_graph_window(fig)
        else:
            messagebox.showerror(
                "Error", "Dataset must include 'Date', 'Time', and 'Blood Glucose Level (mg/dL)' columns."
            )

    def make_graph_levels_meal(self, data_file):
        """
        Creates a bar chart of blood glucose levels by meal.

        Args:
            data_file (str): The path to the CSV file containing the data.
        """
        data = pd.read_csv(data_file)
        if {"Meal", "Blood Glucose Level (mg/dL)"}.issubset(data.columns):
            unique_meals = data["Meal"].unique()
            colors = list(mcolors.TABLEAU_COLORS.values())[:len(unique_meals)]
            meal_colors = {meal: colors[i % len(colors)] for i, meal in enumerate(unique_meals)}

            fig, ax = plt.subplots(figsize=(10, 5))
            for meal in unique_meals:
                meal_data = data[data["Meal"] == meal]
                ax.bar(meal_data["Meal"], meal_data["Blood Glucose Level (mg/dL)"],
                       color=meal_colors[meal], edgecolor="black", alpha=0.8, label=meal)

            ax.set_title("Blood Glucose Levels by Meal", fontsize=20)
            ax.set_xlabel("Meal", fontsize=16)
            ax.set_ylabel("Blood Glucose Level (mg/dL)", fontsize=16)
            ax.tick_params(axis="x", rotation=45, labelsize=12)
            ax.tick_params(axis="y", labelsize=12)
            ax.grid(alpha=0.7, linestyle="--")
            ax.legend(title="Meals", fontsize=14, title_fontsize=14, loc='upper right', frameon=True, shadow=True, borderpad=1)

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
        """
        Displays the BMI of all users.

        Args:
            users (list): List of user identifiers.
            bmis (list): List of BMI values for users.
        """
        max_bmi = max(bmis)
        min_bmi = min(bmis)
        max_bmi_user = users[bmis.index(max_bmi)]
        min_bmi_user = users[bmis.index(min_bmi)]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(users, bmis, marker='o', color='#4682B4', label='BMI')
        ax.plot(max_bmi_user, max_bmi, marker='o', color='red', label='Highest BMI')
        ax.plot(min_bmi_user, min_bmi, marker='o', color='purple', label='Lowest BMI')
        ax.set_xlabel('Users', fontsize=16)
        ax.set_ylabel('BMI', fontsize=16)
        ax.set_title('BMI of All Users', fontsize=20)
        ax.legend()
        fig.tight_layout()

        self.display_graph_window(fig)

    def show_avg_bmi_by_type(self, avg_bmi_per_type):
        """
        Displays the average BMI by diabetes type.

        Args:
            avg_bmi_per_type (dict): A dictionary where keys are diabetes types and values are average BMI values.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        for i, (dtype, avg_bmi) in enumerate(avg_bmi_per_type.items()):
            dtype_wrapped = dtype.replace(" ", "\n")
            ax.bar(dtype_wrapped, avg_bmi, color=colors[i % len(colors)])
        ax.set_xlabel('Diabetes Type', fontsize=16)
        ax.set_ylabel('Average BMI', fontsize=16)
        ax.set_title('Average BMI for Each Diabetes Type', fontsize=20)
        fig.tight_layout()

        self.display_graph_window(fig)

    def show_age_distribution_by_type(self, age_data):
        """
        Displays the age distribution by diabetes type.

        Args:
            age_data (dict): A dictionary where keys are diabetes types and values are lists of ages.
        """
        diabetes_types = list(age_data.keys())
        age_values = [age_data[dtype] for dtype in diabetes_types]

        fig, ax = plt.subplots(figsize=(10, 6))
        box = ax.boxplot(age_values, labels=diabetes_types, patch_artist=True)

        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink', 'lightyellow', 'lightgray',
                  'lightcyan', 'lightgoldenrodyellow', 'lightseagreen']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_title('Age Distribution by Diabetes Type', fontsize=20)
        ax.set_xticklabels([dtype.replace(" ", "\n") for dtype in diabetes_types], fontsize=17)
        ax.set_xlabel('Diabetes Type', fontsize=18)
        ax.set_ylabel('Age', fontsize=18)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        fig.tight_layout()
        self.display_graph_window(fig)

    def show_gender_distribution_by_type(self, gender_data):
        """
        Displays the gender distribution by diabetes type.

        Args:
            gender_data (dict): A dictionary where keys are diabetes types and values are lists of genders.
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        diabetes_types = list(gender_data.keys())
        gender_categories = sorted(set(gender for genders in gender_data.values() for gender in genders))
        gender_counts = {dtype: pd.Series(genders).value_counts() for dtype, genders in gender_data.items()}

        colors = ['lightpink', 'lightblue', 'mediumpurple']
        gender_colors = {gender: colors[i % len(colors)] for i, gender in enumerate(gender_categories)}

        for i, gender in enumerate(gender_categories):
            counts = [gender_counts[dtype].get(gender, 0) for dtype in diabetes_types]
            ax.bar(np.arange(len(diabetes_types)) + i * 0.2, counts, width=0.2, label=gender,
                   color=gender_colors[gender])

        ax.set_xticks(np.arange(len(diabetes_types)) + 0.2 * (len(gender_categories) - 1) / 2)
        ax.set_xticklabels([dtype.replace(" ", "\n") for dtype in diabetes_types], fontsize=17)
        ax.set_title('Gender Distribution by Diabetes Type', fontsize=20)
        ax.set_xlabel('Diabetes Type', fontsize=18)
        ax.set_ylabel('Count', fontsize=18)
        ax.legend(title='Gender', fontsize=16, title_fontsize=16)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        fig.tight_layout()
        self.display_graph_window(fig)