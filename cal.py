import tkinter as tk
from tkinter import ttk, messagebox
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Calculator")
        self.root.geometry("520x680")
        self.root.resizable(False, False)

        self.expression = ""
        self.history = []
        self.dark_mode = False

        self.light_theme = {
            "bg": "#f3f6fb",
            "panel": "#ffffff",
            "text": "#172033",
            "button": "#e7ecf5",
            "operator": "#4f7cff",
            "operator_text": "#ffffff",
            "equals": "#19a974",
            "danger": "#e05252",
        }

        self.dark_theme = {
            "bg": "#181c24",
            "panel": "#242a36",
            "text": "#f5f7fb",
            "button": "#343c4d",
            "operator": "#6d8dff",
            "operator_text": "#ffffff",
            "equals": "#2fc483",
            "danger": "#ff6b6b",
        }

        self.theme = self.light_theme
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, padx=18, pady=18)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.main_frame,
            text="Calculator",
            font=("Segoe UI", 22, "bold")
        )
        self.title_label.pack(anchor="w")

        self.display = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 24),
            justify="right",
            bd=0,
            relief="flat"
        )
        self.display.pack(fill="x", ipady=14, pady=(16, 12))

        top_controls = tk.Frame(self.main_frame)
        top_controls.pack(fill="x", pady=(0, 12))

        self.theme_button = tk.Button(
            top_controls,
            text="Dark Theme",
            command=self.toggle_theme,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=12,
            pady=8
        )
        self.theme_button.pack(side="left")

        self.history_button = tk.Button(
            top_controls,
            text="View Last 5 Actions",
            command=self.show_history,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=12,
            pady=8
        )
        self.history_button.pack(side="right")

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill="x")

        buttons = [
            ["C", "√", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "⌫", "="],
        ]

        for row_index, row in enumerate(buttons):
            button_frame.rowconfigure(row_index, weight=1)
            for col_index, text in enumerate(row):
                button_frame.columnconfigure(col_index, weight=1)

                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 16, "bold"),
                    bd=0,
                    height=2,
                    command=lambda value=text: self.on_button_click(value)
                )
                btn.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )

        self.button_frame = button_frame

        chart_label = tk.Label(
            self.main_frame,
            text="Result Chart",
            font=("Segoe UI", 13, "bold")
        )
        chart_label.pack(anchor="w", pady=(18, 6))
        self.chart_label = chart_label

        self.figure, self.ax = plt.subplots(figsize=(5, 2.2), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill="x")

        self.update_chart()

    def on_button_click(self, value):
        if value == "C":
            self.expression = ""
        elif value == "⌫":
            self.expression = self.expression[:-1]
        elif value == "=":
            self.calculate()
            return
        elif value == "√":
            self.calculate_root()
            return
        elif value == "^":
            self.expression += "**"
        else:
            self.expression += value

        self.update_display()

    def update_display(self):
        visible_expression = self.expression.replace("**", "^")
        self.display.delete(0, tk.END)
        self.display.insert(0, visible_expression)

    def calculate(self):
        try:
            if not self.expression:
                return

            result = eval(self.expression, {"__builtins__": None}, {})
            action = f"{self.expression.replace('**', '^')} = {result}"

            self.expression = str(result)
            self.add_to_history(action, result)
            self.update_display()

        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
        except Exception:
            messagebox.showerror("Input Error", "Please enter a valid calculation.")

    def calculate_root(self):
        try:
            if not self.expression:
                return

            number = eval(self.expression, {"__builtins__": None}, {})

            if number < 0:
                messagebox.showerror("Math Error", "Cannot find square root of a negative number.")
                return

            result = sqrt(number)
            action = f"√({self.expression.replace('**', '^')}) = {result}"

            self.expression = str(result)
            self.add_to_history(action, result)
            self.update_display()

        except Exception:
            messagebox.showerror("Input Error", "Please enter a valid number before using root.")

    def add_to_history(self, action, result):
        self.history.append((action, result))
        self.history = self.history[-5:]
        self.update_chart()

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Last 5 Actions")
        history_window.geometry("420x280")
        history_window.resizable(False, False)

        bg = self.theme["bg"]
        text = self.theme["text"]
        panel = self.theme["panel"]

        history_window.configure(bg=bg)

        label = tk.Label(
            history_window,
            text="Last 5 Calculations",
            font=("Segoe UI", 16, "bold"),
            bg=bg,
            fg=text
        )
        label.pack(pady=(16, 10))

        listbox = tk.Listbox(
            history_window,
            font=("Segoe UI", 12),
            bg=panel,
            fg=text,
            bd=0,
            highlightthickness=0
        )
        listbox.pack(fill="both", expand=True, padx=18, pady=12)

        if not self.history:
            listbox.insert(tk.END, "No calculations yet.")
        else:
            for action, _ in reversed(self.history):
                listbox.insert(tk.END, action)

    def update_chart(self):
        self.ax.clear()

        self.ax.set_title("Last 5 Results")
        self.ax.set_xlabel("Action")
        self.ax.set_ylabel("Result")

        if self.history:
            labels = [str(i + 1) for i in range(len(self.history))]
            values = [item[1] for item in self.history]

            self.ax.bar(labels, values, color="#4f7cff")
        else:
            self.ax.text(
                0.5,
                0.5,
                "No data yet",
                ha="center",
                va="center",
                transform=self.ax.transAxes
            )

        self.figure.tight_layout()
        self.canvas.draw()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme = self.dark_theme if self.dark_mode else self.light_theme
        self.theme_button.config(text="Light Theme" if self.dark_mode else "Dark Theme")
        self.apply_theme()

    def apply_theme(self):
        bg = self.theme["bg"]
        panel = self.theme["panel"]
        text = self.theme["text"]
        button = self.theme["button"]

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=text)
        self.chart_label.configure(bg=bg, fg=text)
        self.display.configure(bg=panel, fg=text, insertbackground=text)

        self.theme_button.configure(
            bg=self.theme["operator"],
            fg=self.theme["operator_text"],
            activebackground=self.theme["operator"],
            activeforeground=self.theme["operator_text"]
        )

        self.history_button.configure(
            bg=button,
            fg=text,
            activebackground=button,
            activeforeground=text
        )

        for child in self.button_frame.winfo_children():
            value = child["text"]

            if value == "=":
                color = self.theme["equals"]
                fg = "#ffffff"
            elif value == "C":
                color = self.theme["danger"]
                fg = "#ffffff"
            elif value in ["+", "-", "*", "/", "^", "√"]:
                color = self.theme["operator"]
                fg = self.theme["operator_text"]
            else:
                color = button
                fg = text

            child.configure(
                bg=color,
                fg=fg,
                activebackground=color,
                activeforeground=fg
            )

        self.figure.patch.set_facecolor(panel)
        self.ax.set_facecolor(panel)
        self.ax.tick_params(colors=text)

        for spine in self.ax.spines.values():
            spine.set_color(text)

        self.ax.title.set_color(text)
        self.ax.xaxis.label.set_color(text)
        self.ax.yaxis.label.set_color(text)
        self.canvas.get_tk_widget().configure(bg=panel)
        self.update_chart()


root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()
