from gameobject import GameObject
import os
import pathlib


class Eksplosjon(GameObject):
    def _finn_bilde(self, num):
        image_folder = "/images/smokeparticleassets/png/explosion"
        base_path = str(pathlib.Path(__file__).parent)
        if num < 10:
            num = "0" + str(num)
        else:
            num = str(num)
        kule_bilde = os.path.join(
            base_path + image_folder + "/explosion" + num + ".png"
        )
        return kule_bilde

    def __init__(self, kule):
        posisjon_venstre = kule.hent_posisjon_venstre() - 250
        posisjon_topp = kule.hent_posisjon_topp() - 250
        bilde = self._finn_bilde(00)
        super().__init__(bilde, posisjon_venstre, posisjon_topp)
        self._explode = 0
        self._END_FRAME = 8
        self._parent_kule = kule

    def fjern_object_out_of_bounds(self):
        if not self._lever:
            self.forsvinner()

    def beveg(self):
        self.explode()

    def explode(self):
        if self._explode == self._END_FRAME:
            self._lever = False
        self._explode += 1
        self._endre_bilde()

    def _endre_bilde(self):
        self._bilde = self._finn_bilde(self._explode)
