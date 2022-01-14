import pygame as p
import random
import Globals

from Globals import IMAGES


class Jojo(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jojo_skin = 0
        self.images = self.fill_images_list()
        self.fan = IMAGES['FAN']
        self.fan_index = 0
        self.image_set = 1
        self.image_index = random.randint(0, len(self.images[self.image_set]) - 1)
        self.current_image = self.images[self.image_set][self.image_index]
        self.image = None
        self.x = Globals.WIDTH // 2
        self.y = Globals.HEIGHT - Globals.HEIGHT * Globals.GROUND_RATIO - self.current_image.get_height() // 2 + 2

        self.rect = self.current_image.get_rect(center=(self.x, self.y))
        self.dir = 1
        self.mask = p.mask.from_surface(self.current_image)

    def fill_images_list(self):
        curr_jojo = IMAGES['JOJO'][self.jojo_skin]
        right = [curr_jojo[0]]
        right = right * 10
        right.append(curr_jojo[1])
        right.append(curr_jojo[2])
        right.extend(right[::-1])

        left = [p.transform.flip(i, flip_x=True, flip_y=False) for i in right]

        return [left, right]

    def move(self, offset):
        self.x += self.dir * offset

    def change_jojo_skin(self, number=-1):
        if number == -2:
            self.jojo_skin += 1
            if self.jojo_skin == len(Globals.IMAGES['JOJO']):
                self.jojo_skin = 0
        elif number == -1:
            self.jojo_skin = random.randint(0, 4)
        else:
            self.jojo_skin = number
        self.images = self.fill_images_list()


    def update(self, move=True):
        if move:
            self.move(Globals.GAME_SPEED)
            fan_index = self.fan_index
            current_image = self.current_image
        else:
            fan_index = 0
            current_image = self.images[self.image_set][0]
        rect_fan = self.fan[self.fan_index].get_rect()
        rect_jojo = self.current_image.get_rect()

        self.rect = p.Rect((0, 0),
                           (max(rect_fan.width, rect_jojo.width), rect_fan.height + rect_jojo.height + Globals.JOJO_FAN_OFFSET))

        combine_image = p.Surface((self.rect.width, self.rect.height), p.SRCALPHA, 32).convert_alpha()
        combine_image.blit(self.fan[fan_index], self.fan[fan_index].get_rect(midtop=self.rect.midtop))
        combine_image.blit(current_image, current_image.get_rect(midbottom=self.rect.midbottom))
        self.image = combine_image
        self.rect.center = (self.x, self.y)
        self.mask = p.mask.from_surface(self.image)


    def changeDir(self):
        self.dir *= -1
        self.image_set = 1 if self.dir == 1 else 0


    def blink_animation(self):
        if self.image_index >= len(self.images[self.image_set]):
            self.image_index = 0
        self.current_image = self.images[self.image_set][self.image_index]
        self.image_index += 1

    def fan_animation(self):
        if self.fan_index >= len(self.fan) - 1:
            self.fan_index = 0
        else:
            self.fan_index += 1

    def is_hit_wall(self):
        return self.rect.left <= 0 or self.rect.right >= Globals.WIDTH

    def is_hit_armature(self, armature):
        return p.sprite.spritecollide(self, armature, False, p.sprite.collide_mask)

    def is_hit_hammer(self, hammer):
        return p.sprite.spritecollide(self, hammer, False, p.sprite.collide_mask)
