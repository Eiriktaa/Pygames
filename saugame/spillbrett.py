from sau import Sau
from stein import Stein
from gress import Gress
from ulv import Ulv
from random import random, randint
import pickle
import math
import sys
import timeit


def har_kollidert(objekt1, objekt2):
    if (
        objekt1.hent_posisjon_venstre() > objekt2.hent_posisjon_venstre() - 50
        and objekt1.hent_posisjon_venstre() < objekt2.hent_posisjon_venstre() + 50
        and objekt1.hent_posisjon_topp() > objekt2.hent_posisjon_topp() - 50
        and objekt1.hent_posisjon_topp() < objekt2.hent_posisjon_topp() + 50
    ):
        return True
    return False


class Spillbrett:
    TEST_MODE = True
    BEVEG_ULV = True

    def __init__(self, antall_runder):
        self._antall_runder = antall_runder
        self._sauer = []
        self._ulv = None
        self._gress = []
        self._steiner = []
        self._oppdatering = 0

    def legg_til_objekter_fra_fil(self, filnavn):
        with open(filnavn) as file:
            for linje in file:
                dyr, x_cords, y_cords = linje.split()
                opprett_dyr = getattr(self, "opprett_" + dyr)
                opprett_dyr(dyr, int(x_cords), int(y_cords))

    def tegn(self, skjerm):
        pass
        for sau in self._sauer:
            if not sau.er_spist():
                sau.tegn(skjerm)

        for stein in self._steiner:
            stein.tegn(skjerm)

        for g in self._gress:
            if not g.er_spist():
                g.tegn(skjerm)

        self._ulv.tegn(skjerm)

    def opprett_sau(self, bilde, x, y):
        self._sauer.append(Sau(bilde, x, y, self))

    def opprett_gress(self, bilde, x, y):
        self._gress.append(Gress(bilde, x, y))

    def opprett_ulv(self, bilde, x, y):
        self._ulv = Ulv(bilde, x, y, self)

    def opprett_stein(self, bilde, x, y):
        self._steiner.append(Stein(bilde, x, y))

    def skaler_fart(self, objekt, maksfart):
        fart = math.sqrt(objekt._fart_fra_topp ** 2 + objekt._fart_fra_venstre ** 2)
        if fart == 0:
            return

        faktor = maksfart / fart
        objekt._fart_fra_topp = objekt._fart_fra_topp * faktor
        objekt._fart_fra_venstre = objekt._fart_fra_venstre * faktor

    def rute_tilgjengelig(self, x, y):
        if x * 50 > 900 - 50 or x < 0 or y * 50 > 700 - 50 or y < 0:
            return False

        for stein in self._steiner:
            if (
                stein.hent_posisjon_venstre() // 50 == x
                and stein.hent_posisjon_topp() // 50 == y
            ):
                # print("Krasjer med stein på posisjon %d,%d" % (stein.hent_posisjon_venstre(), stein.hent_posisjon_topp()))
                return False

        return True

    def start_bevegelse(self, objekt):
        objekt.sett_rute_venstre(objekt.hent_posisjon_venstre() // 50)
        objekt.sett_rute_topp(objekt.hent_posisjon_topp() // 50)

        tid = timeit.default_timer()
        # code you want to evaluate
        objekt.tenk()
        tid_brukt = timeit.default_timer() - tid
        if tid_brukt > 0.2:
            print(
                "ADVARSEL! Et objekt har brukt lang tid (%.4f sek) på å tenke"
                % tid_brukt
            )

        beveg_y = 0
        beveg_x = 0
        if objekt.retning() == "ned":
            beveg_y = 1
        elif objekt.retning() == "hoeyre":
            beveg_x = 1
        elif objekt.retning() == "venstre":
            beveg_x = -1
        elif objekt.retning() == "opp":
            beveg_y = -1
        else:
            return

        ny_x = objekt.rute_venstre() + beveg_x
        ny_y = objekt.rute_topp() + beveg_y
        if not self.rute_tilgjengelig(ny_x, ny_y):
            # print("Rute %d/%d ikke tilgjengelig for %s. Retning er %s" % (ny_x, ny_y, objekt, objekt.retning()))
            objekt._retning = ""
            return
        else:
            objekt.skal_til_rute_x = ny_x
            objekt.skal_til_rute_y = ny_y

        # print(objekt, "er på %d,%d og skal til %d,%d" % (objekt.rute_venstre(), objekt.rute_topp(), objekt.skal_til_rute_x, objekt.skal_til_rute_y))

    def beveg_objekt(self, objekt):

        if objekt.retning() == "":
            self.start_bevegelse(objekt)

        posisjon_venstre = objekt.hent_posisjon_venstre()
        posisjon_topp = objekt.hent_posisjon_topp()

        beveg_y = 0
        beveg_x = 0
        if objekt.retning() == "ned":
            beveg_y = 1
        elif objekt.retning() == "hoeyre":
            beveg_x = 1
        elif objekt.retning() == "venstre":
            beveg_x = -1
        elif objekt.retning() == "opp":
            beveg_y = -1

        objekt.sett_fart(beveg_x, beveg_y)
        maksfart = 5
        if isinstance(objekt, Ulv):
            maksfart = 2.5

        self.skaler_fart(objekt, maksfart)

        ny_posisjon_venstre = objekt.hent_posisjon_venstre() + objekt._fart_fra_venstre
        ny_posisjon_topp = objekt.hent_posisjon_topp() + objekt._fart_fra_topp

        # Sjekk om vi har kommet frem til en ny rute (man kan ha passert akkurat pixelen der ruten starter)
        har_kommet_frem = False
        if objekt.retning() == "ned":
            if posisjon_topp // 50 != ny_posisjon_topp // 50:
                ny_posisjon_topp = 50 * (ny_posisjon_topp // 50)
                har_kommet_frem = True
        elif objekt.retning() == "hoeyre":
            if posisjon_venstre // 50 != ny_posisjon_venstre // 50:
                ny_posisjon_venstre = 50 * (ny_posisjon_venstre // 50)
                har_kommet_frem = True
        elif objekt.retning() == "opp":
            if ny_posisjon_topp // 50 < objekt.skal_til_rute_y:
                ny_posisjon_topp = objekt.skal_til_rute_y * 50
                har_kommet_frem = True
        elif objekt.retning() == "venstre":
            if ny_posisjon_venstre // 50 < objekt.skal_til_rute_x:
                ny_posisjon_venstre = objekt.skal_til_rute_x * 50
                har_kommet_frem = True

        objekt.sett_posisjon(ny_posisjon_venstre, ny_posisjon_topp)
        if har_kommet_frem:
            objekt._retning = ""

    def oppdater(self):
        self._oppdatering += 1
        if self._oppdatering == self._antall_runder:
            print(
                " ========= Spillet er over, %d runder er utført =========="
                % self._antall_runder
            )
            print("Sauer:")
            for sau in self._sauer:
                if not sau.er_spist():
                    sau.legg_til_score(10)
                print(sau, "har scoren:", sau.score())
            if not Spillbrett.TEST_MODE:
                sys.exit()
            return False

        for sau in self._sauer:
            self.beveg_objekt(sau)
        self.beveg_objekt(self._ulv)

        for sau in self._sauer:
            if sau.er_spist():
                continue

            for g in self._gress:
                if g.er_spist():
                    continue
                if har_kollidert(sau, g):
                    g.blir_spist()
                    sau.legg_til_score(1)

            if har_kollidert(sau, self._ulv):
                sau.blir_spist()
                print(" ========== Spillet er over, sauen har blitt spist =====")
                print("Score til slutt: %d" % self._sauer[0].score())
                if not Spillbrett.TEST_MODE:
                    sys.exit()
                else:
                    return False

    def runde(self):
        return self._oppdatering

    def ulv(self):
        return self._ulv
