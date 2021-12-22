from gameobject import GameObject


class Kule(GameObject):
    def __init__(self, bilde, posisjon_venstre, posisjon_topp):
        super().__init__(bilde, posisjon_venstre, posisjon_topp)

    def beveg(self):
        self._posisjon_topp -= 5


class Nuke(Kule):
    def __init__(self, bilde, posisjon_venstre, posisjon_topp):
        super().__init__(bilde, posisjon_venstre, posisjon_topp)
