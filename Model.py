class Model:
    def __init__(self):
        self.toughness = 0
        self.save = 0
        self.health = 0

    def __init__(self, toughness: int, save: int, health: int):
        self.toughness = toughness
        self.save = save
        self.health = health