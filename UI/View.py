import datetime
import tkinter as tk
from tkinter import ttk
from Controller import Controller


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add buttons and select box
        self.status_l = tk.Label(self, width=50)
        self.status_l.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

        self.read_btn = ttk.Button(buttons_frame, text="Update", command=self.read)
        self.read_btn.pack(side=tk.LEFT, padx=5)
        self.request_btn = ttk.Button(
            buttons_frame, text="Request", command=self.request
        )
        self.request_btn.pack(side=tk.LEFT, padx=5)

        plot_frame = tk.Frame(self)
        plot_frame.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

        self.combo = ttk.Combobox(
            plot_frame, state="readonly", values=["Today", "This month"]
        )
        self.combo.current(1)
        self.combo.pack(side=tk.LEFT, padx=5)

        self.plot_btn = ttk.Button(plot_frame, text="Plot", command=self.plot)
        self.plot_btn.pack(side=tk.LEFT, padx=5)

        # Add table
        self.table = ttk.Treeview(self, columns=("ID", "Date", "Time", "Temperature"))
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Date", text="Date", anchor=tk.CENTER)
        self.table.heading("Time", text="Time", anchor=tk.CENTER)
        self.table.heading("Temperature", text="Temperature", anchor=tk.CENTER)
        self.table.column("ID", anchor=tk.CENTER)
        self.table.column("Date", anchor=tk.CENTER)
        self.table.column("Time", anchor=tk.CENTER)
        self.table.column("Temperature", anchor=tk.CENTER)
        self.table.grid(row=3, column=1, columnspan=3, padx=10, pady=5)

        self.controller: Controller = None

    def set_controller(self, controller):
        self.controller = controller

    # Read button clicked
    def read(self):
        if self.controller:
            try:
                data = self.controller.update()
                if not (data == []):
                    self.__add(data)
                    self.status_l.config(text="Data updated.", fg="green")
            except:
                self.status_l.config(text="Error: Could not update data.", fg="red")

    def __add(self, data):
        for row in data:
            temp = row[3] * (10 ** row[4])
            temp_str = f"{temp}\u00b0"
            self.table.insert("", "end", values=(row[0], row[1], row[2], temp_str))

    # Request button clicked
    def request(self):
        if self.controller:
            try:
                response = self.controller.request()
                color = "green" if response == "Data requested" else "red"
                self.status_l.config(text="Request sent.", fg=color)
            except:
                self.status_l.config(text="Error: Could not send request.", fg="red")

    # Plot button clicked
    def plot(self):
        if self.controller:
            if self.combo.get() == "Today":
                self.controller.plot_today()
            if self.combo.get() == "This month":
                self.controller.plot_month()

