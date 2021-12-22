from romskip import Romskip
from monster import Monster
from kule import Kule
from eksplosjon import Eksplosjon
import random
import os
import pathlib

base_path = str(pathlib.Path(__file__).parent)


TEST_MODE = False


class Spill:
    def __init__(self):
        self._monstre = []
        self._oppdatering = 0
        self._kuler = []
        self._eksplosjoner = []
        self._romskip = Romskip()
        self._monster_tetthet = 5
        self._forrige_skudd = 0
        self._score = 0

        if TEST_MODE:
            self._TEST_VERDIER()

    def _TEST_VERDIER(self):
        self._romskip.TEST_MODE = True

    def oppdater(self, keyboard):
        # Sjekk for trykk på keyboard
        if keyboard.left or keyboard.d:
            self._romskip.beveg_venstre()
        elif keyboard.right or keyboard.a:
            self._romskip.beveg_hoyre()
        if keyboard.space and self._oppdatering - self._forrige_skudd > 5:
            self.skyt()
            self._forrige_skudd = self._oppdatering

        ##Game events
        self._sjekk_kollisjoner()
        self._sjanse_for_a_legge_til_monster()
        self._oppdatering += 1
        self._level_up()

        ##Bevegelse
        self._beveg_object(self._kuler)
        self._beveg_object(self._monstre)
        self._beveg_object(self._eksplosjoner)

    def _sjanse_for_a_legge_til_monster(self):
        if TEST_MODE:
            self._lag_monster()

        ##Øker vansklighetsgraden når man har høyere score
        if self._score >= 40:
            self._monster_tetthet = 40
        elif self._score > 5:
            self._monster_tetthet = self._score
        sjanse = range(self._monster_tetthet)

        nr = random.choice(sjanse)
        if random.choice(range(0, 1000)) in sjanse:
            self._lag_monster()

    def _hent_bilde(self, folder_lokasjon, bilde_navn):
        funnet_bilde_path = os.path.join(base_path + folder_lokasjon)
        return os.path.join(funnet_bilde_path + str(bilde_navn))

    def _lag_monster(self):

        posisjon_topp = 0
        posisjon_venstre = random.choice(range(0, 845))
        antall_liv = 2
        monster = Monster(posisjon_venstre, posisjon_topp, antall_liv)
        self._monstre.append(monster)

    def _tegn_object(self, skjerm, object_liste):
        for object in object_liste:
            if object.lever():
                object.tegn(skjerm)

    def _beveg_object(self, game_object_list):
        for object in game_object_list:
            object.beveg()
            # Fjerner kuler utenfor mappet
            object.fjern_object_out_of_bounds()

    def _level_up(self):
        self._romskip.sjekk_score(self._score)

    def skyt(self):
        kule_bilder = "/images/kuler/"
        romskip = self._romskip
        kule = Kule(
            self._hent_bilde(kule_bilder, "kule" + str(romskip.hent_level()) + ".png"),
            romskip.hent_posisjon_venstre() + 20,
            romskip.hent_posisjon_topp(),
        )
        self._kuler.append(kule)

    def _sjekk_kollisjoner(self):
        nuke = None
        for monster in self._monstre:
            if not monster.lever():
                continue

            sjekk_kollisjon, kule = self._sjekk_kolisjon(monster)
            if sjekk_kollisjon and self._romskip.hent_level() < 3:
                monster.blir_truffet_av_kule(kule)
                self._score += 1
            elif sjekk_kollisjon and self._romskip.hent_level() <= 3:
                nuke = kule

        if nuke:
            self._splash_damage(nuke)

    def _splash_damage(self, nuke):
        ##Level 3 gir eksplosiv ammunisjon som treffer flere monstre

        for monster in self._monstre:
            if self._sjekk_kollisjon_med_storrelse(nuke, monster, 250):
                kill = Kule(
                    nuke._bilde,
                    nuke.hent_posisjon_venstre() + 20,
                    nuke.hent_posisjon_topp(),
                )
                monster.blir_truffet_av_kule(kill)

        self._eksplosjoner.append(Eksplosjon(nuke))
        nuke._lever = False

    def _sjekk_kollisjon_med_storrelse(
        self, bevegende_objekt, kollisjons_objekt, storrelse_venstre, storrelse_topp=0
    ):
        # Sjekker for kollisjon mellom 2 objekter på x og y aksen og tar høyde for at noen objekter er større
        if (
            bevegende_objekt.hent_posisjon_venstre()
            >= kollisjons_objekt.hent_posisjon_venstre() - storrelse_venstre
            and bevegende_objekt.hent_posisjon_venstre()
            < kollisjons_objekt.hent_posisjon_venstre() + 64 - 24 + storrelse_venstre
        ):
            if (
                bevegende_objekt.hent_posisjon_topp()
                > kollisjons_objekt.hent_posisjon_topp() - storrelse_topp
                and bevegende_objekt.hent_posisjon_topp()
                < kollisjons_objekt.hent_posisjon_topp() + 64 + storrelse_topp
            ):

                return True
        return False

    def _sjekk_kolisjon(self, monster):
        for kule in self._kuler:
            if not kule.lever():
                continue
            if self._sjekk_kollisjon_med_storrelse(kule, monster, 50):
                return True, kule
        return False, None

    def tegn(self, skjerm):
        self._romskip.tegn(skjerm)
        self._tegn_object(skjerm, self._monstre)
        self._tegn_object(skjerm, self._kuler)
        self._tegn_object(skjerm, self._eksplosjoner)
