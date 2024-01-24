
class Player:
    def __init__(self, board, name, value):
        self._name = name
        self._value = value

    def move(self, *args):
        pass

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value




