import os
import pathlib

base_path = str(pathlib.Path(__file__).parent)


class GameObject:
    def __init__(self, bilde_relative_path, posisjon_venstre, posisjon_topp):
        self._posisjon_venstre = posisjon_venstre
        self._posisjon_topp = posisjon_topp
        self._level = 1
        self._base_path = base_path
        self._bilde = os.path.join(base_path, bilde_relative_path)
        self._lever = True

    def lever(self):
        return self._lever

    def level_up(self):
        self._level += 1

    def fjern_object_out_of_bounds(self):
        if self._posisjon_topp < 0 or self._posisjon_topp >= 900:
            self.forsvinner()

    def forsvinner(self):
        self._lever = False

    def _valid_position_venstre(self):
        return self._posisjon_venstre in range(0, 850)

    def beveg_hoyre(self):
        assert self._valid_position_venstre(), "Posisjon" + self._posisjon_venstre
        if not self._posisjon_venstre == 0:
            self._posisjon_venstre -= 5

    def beveg_venstre(self):
        assert self._valid_position_venstre(), "Posisjon" + str(self._posisjon_venstre)
        if not self._posisjon_venstre == 840:
            self._posisjon_venstre += 5

    def hent_posisjon_venstre(self):
        return self._posisjon_venstre

    def hent_posisjon_topp(self):
        return self._posisjon_topp

    def hent_level(self):
        return self._level

    def tegn(self, skjerm):
        skjerm.blit(self._bilde, (self._posisjon_venstre, self._posisjon_topp))
