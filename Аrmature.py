import pygame as p
import Globals
from Globals import IMAGES


class Armature(p.sprite.Sprite):
    def __init__(self, x, dir):
        super().__init__()
        self.image = IMAGES['ARMATURE']
        self.x = x
        self.y = -(self.image.get_height() + IMAGES['HAMMER'].get_height() - Globals.HAMMER_Y_OFFSET)
        self.dir = dir
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.y += Globals.GAME_SPEED
        if self.dir == -1:
            self.rect = self.image.get_rect(bottomright=(self.x, self.y))
        if self.dir == 1:
            self.rect = self.image.get_rect(bottomleft=(self.x + Globals.ARMATURE_SPACE, self.y))
        self.mask = p.mask.from_surface(self.image)
