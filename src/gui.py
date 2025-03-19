import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from chart_generator import ChartGenerator
from isochore_plotter import IsochorePlotter
from scatter_plotter import ScatterPlotter
import os


class DNAAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Segment Analyzer")
        self.root.geometry("600x400")
        self.root.configure(bg="#F0F4F8")  # Soft background color

        # ==== Load Logo ====
        self.load_logo()

        # ==== Title ====
        tk.Label(root, text="DNA Segment Analyzer", font=("Arial", 22, "bold"), bg="#F0F4F8", fg="#333333").pack(pady=5)

        # ==== Input Directory Button ====
        self.input_dir = tk.StringVar()
        self.create_button("Select Input Directory", self.select_input_dir, "icons/folder.png")
        tk.Label(root, textvariable=self.input_dir, bg="#F0F4F8", fg="#1E88E5", font=("Arial", 10)).pack(pady=2)

        # ==== Output Directory Button ====
        self.output_dir = tk.StringVar()
        self.create_button("Select Output Directory", self.select_output_dir, "icons/folder.png")
        tk.Label(root, textvariable=self.output_dir, bg="#F0F4F8", fg="#1E88E5", font=("Arial", 10)).pack(pady=2)

        # ==== Chart Type Dropdown ====
        self.mode = tk.StringVar()
        self.mode.set("Select Mode")
        self.mode_dropdown = tk.OptionMenu(root, self.mode,
                                           "Word Frequency Chart",
                                           "Isochore GC Content Chart",
                                           "Scatter Plot")
        self.mode_dropdown.config(width=30, font=("Arial", 12), bg="#FFFFFF", fg="#333333")
        self.mode_dropdown.pack(pady=10)

        # ==== Generate Button ====
        self.create_button("Generate Chart", self.generate_chart, "icons/start.png")

        # ==== Status Bar ====
        self.status_label = tk.Label(root, text="", bg="#F0F4F8", fg="#4CAF50", font=("Arial", 10))
        self.status_label.pack(pady=5)

    # ==== Load Logo ====
    def load_logo(self):
        try:
            logo = Image.open("icons/dna.png")
            logo = logo.resize((120, 120), Image.LANCZOS)
            logo = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=logo, bg="#F0F4F8").pack(pady=5)
            self.root.logo = logo  # Keep reference to avoid garbage collection
        except Exception as e:
            print(f"⚠️ Error loading logo: {e}")

    # ==== Create Button with Icon ====
    def create_button(self, text, command, icon_path):
        frame = tk.Frame(self.root, bg="#F0F4F8")
        frame.pack(pady=5)

        try:
            icon = Image.open(icon_path)
            icon = icon.resize((20, 20), Image.LANCZOS)
            icon = ImageTk.PhotoImage(icon)
        except Exception as e:
            print(f"⚠️ Error loading icon '{icon_path}': {e}")
            icon = None

        button = tk.Button(frame, text=text, command=command,
                           compound="left", padx=10, pady=5,
                           font=("Arial", 12),
                           bg="#1E88E5", fg="white", activebackground="#1976D2",
                           relief="flat", borderwidth=2)
        button.pack(side="left")

        if icon:
            button.config(image=icon)
            button.image = icon  # Keep reference to avoid garbage collection

    def select_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.set(directory)

    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def generate_chart(self):
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        mode = self.mode.get()

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories.")
            return

        if mode == "Select Mode":
            messagebox.showerror("Error", "Please select a chart mode.")
            return

        try:
            if mode == "Word Frequency Chart":
                generator = ChartGenerator(input_dir, output_dir, threshold=20)
                generator.process_files()
            elif mode == "Isochore GC Content Chart":
                plotter = IsochorePlotter(input_dir, output_dir)
                plotter.process_all()
            elif mode == "Scatter Plot":
                scatter_plotter = ScatterPlotter(input_dir, output_dir)
                scatter_plotter.process_all()
            else:
                messagebox.showerror("Error", "Invalid mode selected.")
                return

            self.status_label.config(text="✅ Chart generated successfully!", fg="#4CAF50")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text=f"❌ Error: {e}", fg="red")
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from chart_generator import ChartGenerator
from isochore_plotter import IsochorePlotter
from scatter_plotter import ScatterPlotter
import os
import subprocess

class DNAAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Segment Analyzer")
        self.root.geometry("600x400")
        self.root.configure(bg="#F0F4F8")

        # ==== Load Logo ====
        self.load_logo()

        # ==== Title ====
        tk.Label(root, text="DNA Segment Analyzer", font=("Arial", 22, "bold"), bg="#F0F4F8", fg="#333333").pack(pady=5)

        # ==== Input Directory Button ====
        self.input_dir = tk.StringVar()
        self.create_button("Select Input Directory", self.select_input_dir, "icons/folder.png")
        tk.Label(root, textvariable=self.input_dir, bg="#F0F4F8", fg="#1E88E5", font=("Arial", 10)).pack(pady=2)

        # ==== Output Directory Button ====
        self.output_dir = tk.StringVar()
        self.create_button("Select Output Directory", self.select_output_dir, "icons/folder.png")
        tk.Label(root, textvariable=self.output_dir, bg="#F0F4F8", fg="#1E88E5", font=("Arial", 10)).pack(pady=2)

        # ==== Chart Type Dropdown ====
        self.mode = tk.StringVar()
        self.mode.set("Select Mode")
        self.mode_dropdown = tk.OptionMenu(root, self.mode,
                                           "Word Frequency Chart",
                                           "Isochore GC Content Chart",
                                           "Scatter Plot")
        self.mode_dropdown.config(width=30, font=("Arial", 12), bg="#FFFFFF", fg="#333333")
        self.mode_dropdown.pack(pady=10)

        # ==== Generate Button ====
        self.create_button("Generate Chart", self.generate_chart, "icons/start.png")

        # ==== View Charts Button ====
        self.create_button("View Saved Charts", self.view_charts, "icons/view.png")

        # ==== Status Bar ====
        self.status_label = tk.Label(root, text="", bg="#F0F4F8", fg="#4CAF50", font=("Arial", 10))
        self.status_label.pack(pady=5)

    # ==== Load Logo ====
    def load_logo(self):
        try:
            logo = Image.open("icons/dna.png")
            logo = logo.resize((120, 120), Image.LANCZOS)
            logo = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=logo, bg="#F0F4F8").pack(pady=5)
            self.root.logo = logo
        except Exception as e:
            print(f"⚠️ Error loading logo: {e}")

    # ==== Create Button with Icon ====
    def create_button(self, text, command, icon_path):
        frame = tk.Frame(self.root, bg="#F0F4F8")
        frame.pack(pady=5)

        try:
            icon = Image.open(icon_path)
            icon = icon.resize((20, 20), Image.LANCZOS)
            icon = ImageTk.PhotoImage(icon)
        except Exception as e:
            print(f"⚠️ Error loading icon '{icon_path}': {e}")
            icon = None

        button = tk.Button(frame, text=text, command=command,
                           compound="left", padx=10, pady=5,
                           font=("Arial", 12),
                           bg="#1E88E5", fg="white", activebackground="#1976D2",
                           relief="flat", borderwidth=2)
        button.pack(side="left")

        if icon:
            button.config(image=icon)
            button.image = icon

    def select_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.set(directory)

    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def generate_chart(self):
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        mode = self.mode.get()

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories.")
            return

        if mode == "Select Mode":
            messagebox.showerror("Error", "Please select a chart mode.")
            return

        try:
            if mode == "Word Frequency Chart":
                generator = ChartGenerator(input_dir, output_dir, threshold=20)
                generator.process_files()
            elif mode == "Isochore GC Content Chart":
                plotter = IsochorePlotter(input_dir, output_dir)
                plotter.process_all()
            elif mode == "Scatter Plot":
                scatter_plotter = ScatterPlotter(input_dir, output_dir)
                scatter_plotter.process_all()
            else:
                messagebox.showerror("Error", "Invalid mode selected.")
                return

            self.status_label.config(text="✅ Chart generated successfully!", fg="#4CAF50")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text=f"❌ Error: {e}", fg="red")

    # ==== Open Saved Charts Folder ====
    def view_charts(self):
        output_dir = self.output_dir.get()
        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("Error", "No charts found. Please generate charts first.")
            return

        try:
            # Open folder using system's file manager
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif os.name == 'posix':  # MacOS or Linux
                subprocess.Popen(['xdg-open', output_dir])
            else:
                messagebox.showerror("Error", "Unsupported operating system.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening folder: {e}")


def main():
    root = tk.Tk()
    app = DNAAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


def main():
    root = tk.Tk()
    app = DNAAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
