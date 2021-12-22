import random

from gress import Gress
from queue import PriorityQueue


class Grid:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._game_borders = {"opp": 0, "ned": 13, "hoeyre": 17, "venstre": 0}  # sjekk
        self._naboer = []  # Liste over alle gyldige naboer
        self._hinder = False
        self._temp_blocked = False
        self._gress = None

    def sett_gress(self, gress):
        self._gress = gress

    def er_gress(self):
        return True if self._gress else None

    def sett_hinder(self):
        self._hinder = True

    def er_hinder(self):
        return self._hinder

    def temp_hinder(self):
        self._temp_blocked = True
        self._hinder = True

    def temp_hinder_open(self):
        if self._temp_blocked:
            self._hinder = False
            self.temp_blocked = False

    def hent_naboer(self):
        nabo_liste = []
        # Legger inn alle naboer som ikke er utenfor banen
        if self._x < self._game_borders["ned"]:
            nabo_liste.append([self._x + 1, self._y])
        if self._x > self._game_borders["opp"]:
            nabo_liste.append([self._x - 1, self._y])
        if self._y > self._game_borders["venstre"]:
            nabo_liste.append([self._x, self._y - 1])
        if self._y < self._game_borders["hoeyre"]:
            nabo_liste.append([self._x, self._y + 1])

        return nabo_liste

    def hent_posisjon(self):
        return self._x, self._y

    def sett_ledige_naboer(self, naboer):
        self._naboer = []
        for nabo_grid in naboer:
            if nabo_grid.er_hinder():
                continue
            else:
                self._naboer.append(nabo_grid)

    def __repr__(self) -> str:

        x, y = self.hent_posisjon()
        string = f" {x},{y}"
        if self.er_hinder():
            string += ", stein"
        if self.er_gress():
            string += ", gress"
        return string

    def naboer(self):
        return self._naboer

    def retning_mot(self, obj):
        return self._retninger(obj)

    def retning_fra(self, obj):
        return self._retninger(obj, fra=True)

    def _retninger(self, obj, fra=False):
        retninger = []
        if not self._x == obj._x:
            x = None
            if self._x < obj._x:
                x = "opp" if fra else "ned"
            else:
                x = "opp" if not fra else "ned"

            retninger.append(x)
        if not self._y == obj._y:
            y = None
            if self._y < obj._y:
                y = "venstre" if fra else "hoeyre"
            else:
                y = "venstre" if not fra else "hoeyre"
            retninger.append(y)
        return retninger

    def manhatten_distanse(self, annet):

        assert isinstance(annet, Grid), "kan kun sammenliggne 2 Grid objekter"

        x1, y1 = self._x, self._y
        x2, y2 = annet._x, annet._y
        return abs(x1 - x2) + abs(y1 - y2)


class SauehjerneEiriktaa(object):
    def __init__(self, sau, spillbrett):
        self._hule = None

        self._ulve_naboer = []
        self._sau = sau
        self._spillbrett = spillbrett
        self._klar = False
        self._target = None
        self._path = []
        self._paths = []
        self._grid = []
        self._gress = []

    def klargjor(self):
        self._grid = self.sett_grid()

        self.populer_grid()
        self.hent_naboer()
        self._finn_alle_paths()
        self.finn_hulrom()
        self._klar = True

    def _hent_grid(self, obj):
        # Sjekk at objekt er av typen gameobjekt med følgdende metoder
        assert getattr(obj, "rute_topp") != None
        assert getattr(obj, "rute_venstre") != None

        # Henter ruten objektet er i basert pa koordinatene
        return self._grid[int(obj.rute_topp())][int(obj.rute_venstre())]

    def hent_sau_grid(self):
        return self._hent_grid(self._sau)

    def hent_ulv_grid(self):
        return self._hent_grid(self._spillbrett.ulv())

    def populer_grid(self):
        # Prekoden har ikke metoder til å hente variabler
        steiner = self._spillbrett._steiner  ## HENTER PRIVATE VARIABLER
        gress = self._spillbrett._gress  ## HENTER PRIVATE VARIABLER

        for stein in steiner:
            rute_topp = stein.rute_topp()
            rute_venstre = stein.rute_venstre()
            self._grid[rute_topp][rute_venstre].sett_hinder()

        for gress in gress:
            rute_topp = gress.rute_topp()
            rute_venstre = gress.rute_venstre()

            self._grid[rute_topp][rute_venstre].sett_gress(gress)
            self._gress.append(self._grid[rute_topp][rute_venstre])

    def hent_naboer(self):
        for row in self._grid:
            for rute in row:
                ## Henter en liste med kordinater til naboen og finner disse i list og sender referansen tilbake

                naboer = rute.hent_naboer()
                nabo_referanser = []
                for verdier in naboer:
                    x, y = verdier[0], verdier[1]
                    nabo_referanser.append(self._grid[x][y])

                rute.sett_ledige_naboer(nabo_referanser)

    def sett_grid(self):
        grid = []
        RUTE_LENGDE = 50

        # Statiske størrelse på skjerm
        rader = 700 // RUTE_LENGDE
        kolonner = 900 // RUTE_LENGDE

        ##Legger alle rutene inn i en nøsted liste, med 1 liste pr rad
        rad_counter = 0
        for rad in range(rader):
            rad = []
            kollonne_counter = 0
            for kollonne in range(kolonner):
                rad.append(Grid(rad_counter, kollonne_counter))
                kollonne_counter += 1
            grid.append(rad)
            rad_counter += 1
        return grid

    def pathfinding_algorithm(self, grid, start, end):
        count = 0
        # Bruker en queue som henter ut de noden med lavest score først
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        kommer_fra = {}

        g_score = {rute: 1000 for row in grid for rute in row}
        # Start noden er null distanse til seg selv
        g_score[start] = 0
        # float("inf")
        f_score = {rute: 1000 for row in grid for rute in row}
        # h bruker manhatten distance
        f_score[start] = start.manhatten_distanse(end)

        open_set_hash = {start}

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            # Legger til avstanden til ulven i vurderingen
            f_score[current] = f_score[current] + self.danger_zone(
                current._x, current._y
            )

            if current == end:
                return kommer_fra, current, g_score[current]
            for nabo in current.naboer():

                temp_g_score = (
                    g_score[current] + 1 + self.danger_zone(current._x, current._y)
                )
                if temp_g_score < g_score[nabo]:
                    kommer_fra[nabo] = current
                    g_score[nabo] = temp_g_score
                    f_score[nabo] = temp_g_score + nabo.manhatten_distanse(end)

                    if nabo not in open_set_hash:
                        count += 1
                        open_set.put((f_score[nabo], count, nabo))
                        open_set_hash.add(nabo)
        return False, False, False

    def finn_hulrom(self):
        for row in self._grid:
            for col in row:
                naboer = col.naboer()
                if len(naboer) == 1:
                    self._finn_hule(col)

    def _finn_hule(self, hule_start):
        # Fra en grid som har 1 naboe, følger den tilbake til den finner en med flere enn 2 naboer
        if not self._hule:
            self._hule = [hule_start]
        neste_hule = hule_start.naboer()[0]
        self._hule.append(neste_hule.naboer())
        while len(neste_hule.naboer()) == 2:
            if neste_hule.naboer()[0].er_hinder():
                neste_hule = neste_hule.naboer()[1]
            else:
                neste_hule = neste_hule.naboer()[0]
            self._hule.append(neste_hule)
            #:TODO sjekk blocked
            neste_hule.temp_hinder()

    def find_path(
        self,
        path_liste,
        current,
    ):
        path_til_maal = []
        # Henter den korteste pathen ifra target og følger den tilbake til måley
        path_til_maal.append(current)
        while current in path_liste:
            current = path_liste[current]
            path_til_maal.append(current)
        return path_til_maal

    def _finn_alle_paths(self):
        self._paths = []
        # Endre til å ta inn gress
        ##Optimalisering,
        sortert = sorted(
            self._gress, key=lambda x: x.manhatten_distanse(self.hent_sau_grid())
        )

        antall_gress = 0
        for gress in sortert:
            target = gress
            gress = gress._gress
            # Lager kun path til de 5 nærmeste, ikke til alle langt unna
            if antall_gress >= 7:
                return
            if gress.er_spist():
                continue
            # Sauens lokasjon er utgangspunktet
            start_sau = self.hent_sau_grid()
            # Hente  den korteste pathen til målet om den eksisterer
            path, end, value = self.pathfinding_algorithm(self._grid, start_sau, target)

            p = None
            if path:
                # Pathen er gyldig
                p = self.find_path(path, end)
                antall_gress += 1
            else:
                # Pathen er ikke gyldig
                continue
            # Fjerner det første elementet som er ruten man er i nå
            p.pop()
            self._paths.append((p, value))

    def _finn_korteste_path(self):
        self._path = []
        laveste_verdi = 9999999
        for path in self._paths:
            # Sjekker første hvor stor fscoren til pathen blir
            # ( de som går nærmer ulven er mindre attraktive selv om de er kortere)
            if path[1] < laveste_verdi and len(path[0]) != 0:
                laveste_verdi = path[1]
                self._path = path[0]

    def _finn_grid_avstander(
        self,
    ):
        laveste = {}
        for row in self._grid:
            for col in row:
                if not col.er_hinder():
                    manhatten_score = col.manhatten_distanse(self.hent_ulv_grid())
                    laveste[col] = manhatten_score

        # Sorteterer basert på hvor langt unna tilen er ulven
        sortert = sorted(laveste.items(), key=lambda x: x[1], reverse=True)
        return sortert

    def unnga_ulv(self):
        lengst_unna = self._finn_grid_avstander()

        # Leter etter en sti til en grid som er langt unna og finenr den første gyldige og returenerer den
        stier = 0
        self._paths = []
        laveste_score = 99999
        for grid in lengst_unna:
            if stier > 6:
                break
            unvikende_sti, end, score = self.pathfinding_algorithm(
                self._grid, self.hent_sau_grid(), grid[0]
            )
            # print(score)
            if score and score < laveste_score:
                laveste_score = score
            sti = None
            if unvikende_sti:
                sti = self.find_path(unvikende_sti, end)
                sti.pop()
                self._paths.append((sti, score))

                stier += 1

        if laveste_score > 999:
            self._paths = []
            stier = 0

            while True:
                random_stier = random.choice(lengst_unna)
                unvikende_sti, end, score = self.pathfinding_algorithm(
                    self._grid, self.hent_sau_grid(), random_stier[0]
                )
                print(random_stier[0], unvikende_sti)
                if self._sau.er_spist() or self._spillbrett.runde() >= 3000:
                    break
                if not score:
                    continue
                sti = None
                if unvikende_sti:
                    sti = self.find_path(unvikende_sti, end)
                    sti.pop()
                    self._paths.append((sti, score))
                if score <= 999:
                    break

    def danger_zone(self, x, y):
        # Gir en omvendt verdi som skal gjøre at det er mindre atrakttivt å dra nærme ulv
        avstand = self.hent_ulv_grid().manhatten_distanse(self._grid[x][y])

        if avstand > 8:
            return 0
        # Switcher avstand
        return {
            0: 999999,
            1: 99999,
            2: 75,
            3: 5,
            4: 3,
            5: 2,
            6: 1,
            7: 0,
            8: 0,
            "lang": 0,
        }[avstand]

    def neste_retning(self):
        if len(self._path) > 0:

            grid = self._path[len(self._path) - 1]
            self._path.pop()
            if len(self._path) == 1:
                self._path.pop()
            retninger = self.hent_sau_grid().retning_mot(grid)
            if retninger:
                return random.choice(retninger)
            else:
                return False
        else:

            return False

    def velg_retning(self):

        if self._hule:
            # Åpner huler helt på slutten så sauen får spist alt gresset
            if (self._spillbrett.runde() + len(self._hule) * 10) > 2850:
                for liste in self._hule:
                    if type(liste) == list:
                        for grid in liste:
                            grid.temp_hinder_open()
                    else:
                        liste.temp_hinder_open()
                self._hule = None
        if not self._klar:
            # Klargjor brettet slik at sauen kan lese in steiner og gress
            self.klargjor()

        # Ser hvor ulven er i gridden og finner alle mulige veier fra det
        self.sjekk_ulv()
        self._finn_alle_paths()
        # Om sauen er nærme ulven vil den forsøke å komem seg unna
        if self.hent_sau_grid().manhatten_distanse(self.hent_ulv_grid()) <= 3:
            self.unnga_ulv()

        # Finner den beste veien gitt en mengde med veir til gress og unna ulven og velger den med lavest score.
        self._finn_korteste_path()
        ret = self.neste_retning()

        if ret:
            return ret
        else:
            # Finner en path som unngår ulven dersom det ikke finnes gyldige veier til gress
            self.unnga_ulv()
            self._finn_korteste_path()
            ret = self.neste_retning()
            return ret

    def sjekk_ulv(self):

        # Finner ulvens posisjon og blokkerer alle disse så sauen tar omveier.
        gamle_naboer = self._ulve_naboer
        self._ulve_naboer = []
        # Åpner de som tidligere var stengt
        for naboer in gamle_naboer:
            naboer.temp_hinder_open()

        ulve_grid = self.hent_ulv_grid()
        # Henter alle noden som er i næreheten av ulven og setter de til hindere slik at sauen ikke går der
        ulve_grid.temp_hinder()
        self._ulve_naboer.append(ulve_grid)

        for nabo in ulve_grid.naboer():
            nabo.temp_hinder()
            self._ulve_naboer.append(nabo)
        self.hent_naboer()
