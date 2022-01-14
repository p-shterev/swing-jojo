import pygame as p
import math
from Globals import IMAGES
import Globals


class Hammer(p.sprite.Sprite):
    def __init__(self, x, swing_iter, dir):
        super().__init__()
        self.dir = dir
        self.hammer = IMAGES['HAMMER']
        self.x = x - Globals.HAMMER_X_OFFSET if self.dir == -1 else x + Globals.ARMATURE_SPACE - 5
        self.y = -self.hammer.get_height()
        self.image = self.hammer.copy()
        self.swing_iter = swing_iter
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.y += Globals.GAME_SPEED
        self.swing_iter = (self.swing_iter + Globals.HAMMER_SPEED) % 60
        rot_image, rot_x, rot_y = self.rotate(self.hammer, self.theta(self.swing_iter, 100), self.x, self.y)
        self.image = rot_image
        self.rect = rot_image.get_rect()
        self.rect.x = rot_x
        self.rect.y = rot_y
        self.mask = p.mask.from_surface(self.image)

    def theta(self, t, offset):
        return 60 * math.sin(math.pi * (t - 30) / 30 + offset * math.pi / 180)

    def rotate(self, image, angle, x, y):
        """rotate an image while keeping its center"""
        rot_image = p.transform.rotate(image, angle)
        h = image.get_height() * math.sin(angle * math.pi / 180)
        w = image.get_width() * math.sin(angle * math.pi / 180) / 4
        if angle < 0:
            return rot_image, x + h - w, y + w * 2
        else:
            return rot_image, x + w, y - w * 2
