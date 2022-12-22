import os
import sys
import pygame
from random import randrange, choice


def load_image(name):
    fname = os.path.join('data/assets/', name)
    if not os.path.isfile(fname):
        print(f"Файл'{fname}' не найден")
        sys.exit()
    image = pygame.image.load(fname)
    return image



class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = []
        self.frames_ducking = []
        self.cut_sheet(load_image("player_sprite.png"), 5, 1, self.frames)
        self.cut_sheet(load_image("player_ducking_sprite.png"), 2, 1, self.frames_ducking)
        del self.frames[1], self.frames[0]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.isJumping = False
        self.gravity = 0
        self.Jumping_count = 0
        self.isDucking = False
        self.isDead = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, 240
        self.count_frame = 0

    def cut_sheet(self, sheet, columns, rows, lst):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                lst.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, gravity):
        self.count_frame += 1
        ### Animation ###
        if self.isDead:
            self.image = self.frames[-1]
        if self.count_frame % 7 == 0:
            if self.cur_frame + 1 == 2:
                self.cur_frame = 0
            else:
                self.cur_frame += 1
        self.image = self.frames[self.cur_frame]

        ### Jumping ###
        if self.isJumping:
            if self.rect.y > 140:
                self.rect.y -= self.gravity
            elif self.Jumping_count < 15:
                self.Jumping_count += 1
            else:
                self.isJumping = None
        elif self.isJumping is None:
            if self.rect.y != 240:
                self.rect.y += self.gravity
            else:
                self.Jumping_count = 0
                self.isJumping = False
        else:
            self.gravity = gravity

        ### Ducking ###
        if self.isDucking:
            self.image = self.frames_ducking[self.cur_frame]
        else:
            self.image = self.frames[self.cur_frame]


class Ground(pygame.sprite.Sprite):
    image = load_image("ground.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.y = 300

    def update(self, speed):
        if self.rect.x < -2598:
            self.rect.x = 0
        self.rect.x -= speed


class Scoreboard(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)


class Cloud(pygame.sprite.Sprite):
    image = load_image("cloud.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = randrange(20, 100)
        self.speed = 2

    def update(self, speed):
        self.rect.x -= speed


class Cactus(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        rnd = choice([0, 1, 2, 3, 4])
        if rnd == 0:
            self.image = self.cut_sheet(load_image("cactus_big.png"), 6, 1)[0]
        elif rnd == 1:
            self.image = self.cut_sheet(load_image("cactus_big.png"), 6, 1)[0]
        elif rnd == 2:
            self.image = self.cut_sheet(load_image("cactus_big.png"), 3, 1)[0]
        elif rnd == 3:
            self.image = self.cut_sheet(load_image("cactus_big.png"), 2, 1)[0]
        elif rnd == 4:
            self.image = load_image("cactus_3.png")

        self.rect = self.image.get_rect()
        self.rect.y = 260
        self.rect.x = 800

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                return [sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))]

    def update(self, speed):
        self.rect.x -= speed