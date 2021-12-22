import random


class Terning:
    def __init__(self):
        self.verdi = 0

    def kast(self):
        self.verdi = random.randint(1, 6)
        return self.verdi

    def hent_verdi(self):
        return self.verdi
