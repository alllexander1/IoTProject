# Model class representing the list of temperatures
class Model:
    def __init__(self):
        self.__data = []

    @property
    def data(self):
        return self.__data

    def update_data(self, new_data):
        self.__data.extend(new_data)

    def get_data(self):
        return self.data

