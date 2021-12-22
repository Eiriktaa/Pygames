import pgzrun

# import pygame
from spill import Spill

WIDTH = 900
HEIGHT = 700

spill = Spill()


def draw():
    screen.fill((0, 0, 0))
    spill.tegn(screen)


def update():
    spill.oppdater(keyboard)


pgzrun.go()
