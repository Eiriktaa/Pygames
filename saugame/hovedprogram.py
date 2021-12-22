from spillbrett import Spillbrett
import pgzrun


TEST_MODE = False
# Dette er prekode som gjoer at pygame-zero fungerer. Ikke endre dette:
WIDTH = 900
HEIGHT = 700

## Change testcourse here!
bane = "baner/bane7.txt"

spillbrett = Spillbrett(3000)
spillbrett.legg_til_objekter_fra_fil(bane)


def run_game(bane_int):
    bane = "testbane" + str(bane_int) + ".txt"
    spillbrett = Spillbrett(3000)
    spillbrett.legg_til_objekter_fra_fil(bane)

    for x in range(0, 3000):
        update()


def draw():
    screen.fill((128, 81, 9))
    spillbrett.tegn(screen)


def run_all():
    for run in range(1, 7):
        print(run)
        run_game(run)


def update():
    spillbrett.oppdater()


if not TEST_MODE:
    pgzrun.go()
else:
    run_all()
