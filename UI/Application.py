import tkinter
from Model import Model
from Controller import Controller
from View import View


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("Temperature Viewer")

        # Create a model
        model = Model()

        # Create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # Create a controller
        controller = Controller(model, view)

        # Set the controller for the view
        view.set_controller(controller)
        view.read()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

