import os
import pathlib
from gameobject import GameObject

base_path = str(pathlib.Path(__file__).parent)


class Romskip(GameObject):
    def __init__(self):
        bilde = os.path.join(base_path, "images", "romskip1.png")
        posisjon_venstre = 300
        posisjon_topp = 620
        self.TEST_MODE = False
        super().__init__(bilde, posisjon_venstre, posisjon_topp)

    def sjekk_score(self, score):
        if self.TEST_MODE:
            LEVEL_2 = 1
            LEVEL_3 = 2
        else:
            LEVEL_2 = 30
            LEVEL_3 = 80
        if (score > LEVEL_2 and self.hent_level() == 1) or (
            score > LEVEL_3 and self.hent_level() == 2
        ):
            self.level_up()

    def level_up(self):
        self._level += 1
        self.level_up_bytt_bilde()

    def _valid_position_venstre(self):
        return self._posisjon_venstre in range(0, 850)

    def level_up_bytt_bilde(self):
        self._bilde = os.path.join(base_path, "images", f"romskip{self._level}.png")

    def beveg_hoyre(self):
        assert self._valid_position_venstre(), "Posisjon" + str(self._posisjon_venstre)
        if not self._posisjon_venstre == 840:
            self._posisjon_venstre += 5

    def beveg_venstre(self):
        assert self._valid_position_venstre(), "Posisjon" + str(self._posisjon_venstre)
        if not self._posisjon_venstre == 0:
            self._posisjon_venstre -= 5
