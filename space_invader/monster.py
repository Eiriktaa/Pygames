from kule import Kule
from gameobject import GameObject
import random
import os


class Monster(GameObject):
    def __init__(self, posisjon_venstre, posisjon_topp, antall_liv):

        super().__init__("", posisjon_venstre, posisjon_topp)
        self._bilde = self._bilde = os.path.join(
            self._base_path + "/images/monster", self._hent_tilfeldig_bilde()
        )
        self._antall_liv = antall_liv
        self._retning = 1

    def beveg(self):
        if self._retning == 1:
            self._posisjon_venstre += 4
            if self._posisjon_venstre >= 900 - 64:
                self._posisjon_topp += 64
                self._retning = -1
        else:
            self._posisjon_venstre -= 4
            if self._posisjon_venstre <= 0:
                self._retning = 1
                self._posisjon_topp += 64

    def blir_truffet_av_kule(self, kule):
        assert type(kule) == Kule
        damage_taken = kule.hent_level()
        if damage_taken > self._antall_liv:
            self.forsvinner()
        else:
            self._antall_liv -= kule.hent_level()
        kule.forsvinner()

    def _hent_tilfeldig_bilde(self):
        monster_image_folder = "/images/monster/"
        monster_bilder = os.listdir(
            os.path.join(self._base_path + monster_image_folder)
        )
        return str(random.choice(monster_bilder))
