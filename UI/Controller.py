from datetime import datetime
import Model
import time
from Client import Client
import matplotlib.pyplot as plt


# Controller class to control the view
class Controller:
    def __init__(self, model, view):
        self.model: Model = model
        self.view = view
        self.client = Client()
        self.last_id = 0

    # Update the model
    def update(self):
        self.last_id, new_data = self.client.get_all(self.last_id)
        self.model.update_data(new_data)
        return new_data

    # Send request
    def request(self):
        response = self.client.request()
        return response

    def set_status(self, status):
        self.view.set_status(status)

    # Create diagram for todays temperature
    def plot_today(self):
        if len(self.model.get_data()) == 0:
            return
        today = datetime.now()
        temps = []
        for t in self.model.get_data():
            date = t[1].split(".")
            d, m, y = int(date[0]), int(date[1]), int(date[2])
            if d == today.day and m == today.month and y == today.year:
                time = t[2]
                temp = t[3] * 10 ** t[4]
                temps.append((time, temp))

        labels = [row[0] for row in temps]
        temps = [row[1] for row in temps]
        plt.plot(labels, temps)
        plt.scatter(labels, temps, color="black", marker="o")
        plt.xlabel("Time")
        plt.ylabel("Temperature")
        plt.show()

    # Plot diagram for this month temperature
    def plot_month(self):
        if len(self.model.get_data()) == 0:
            return
        today = datetime.now()
        temps = []
        for t in self.model.get_data():
            date = t[1].split(".")
            d, m, y = int(date[0]), int(date[1]), int(date[2])
            if m == today.month and y == today.year:
                date = t[1]
                temp = t[3] * 10 ** t[4]
                temps.append((date, temp))

        # Find max temps for each day
        max_temps = {}
        for t in temps:
            if t[0] not in max_temps:
                max_temps[t[0]] = t[1]
            else:
                if max_temps[t[0]] < t[1]:
                    max_temps[t[0]] = t[1]

        # Plot
        labels = list(max_temps.keys())
        temps = list(max_temps.values())
        plt.plot(labels, temps)
        plt.scatter(labels, temps, color="black", marker="o")
        plt.xlabel("Date")
        plt.ylabel("Temperature")
        plt.show()

