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


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    return [sheet.subsurface(pygame.Rect((rect.w * i, rect.h * j), rect.size)) for j in range(rows) for i in
            range(columns)]


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = cut_sheet(load_image("player_sprite.png"), 3, 1)
        self.frames_ducking = cut_sheet(load_image("player_ducking_sprite.png"), 2, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.isJumping = False
        self.gravity = 0
        self.Jumping_count = 0
        self.isDucking = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, 240
        self.count_frame = 0

    def update(self, gravity, isDead=None):
        self.count_frame += 1
        ### Animation ###
        if self.count_frame % 7 == 0:
            if self.cur_frame + 1 == 2:
                self.cur_frame = 0
            else:
                self.cur_frame += 1
        if isDead:
            self.cur_frame = -1
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
        if self.rect.x < -50:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        rnd = choice([0, 1, 2, 3, 4])
        if rnd == 0:
            self.image = cut_sheet(load_image("cactus_big.png"), 6, 1)[0]
        elif rnd == 1:
            self.image = cut_sheet(load_image("cactus_big.png"), 6, 1)[0]
        elif rnd == 2:
            self.image = cut_sheet(load_image("cactus_big.png"), 3, 1)[0]
        elif rnd == 3:
            self.image = cut_sheet(load_image("cactus_big.png"), 2, 1)[0]
        elif rnd == 4:
            self.image = load_image("cactus_3.png")

        self.rect = self.image.get_rect()
        self.rect.y = 260
        self.rect.x = 800

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x < -50:
            self.kill()


class ReplayButton(pygame.sprite.Sprite):
    image = load_image("replay_button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 381, 250


class GameOver(pygame.sprite.Sprite):
    image = load_image("game_over.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 260, 130


class MainMenuButton(pygame.sprite.Sprite):
    image = load_image("main_menu.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 380, 300


class Coin(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.isVisible = True
        self.frames = cut_sheet(load_image("coins.png"), 9, 1)
        self.image = self.frames[0]
        self.count = 0
        self.frame_count = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 253

    def update(self, speed):
        if not self.isVisible:
            self.kill()
        else:
            self.count += 1
            if self.count % 7 == 0:
                if self.frame_count + 1 == 6:
                    self.frame_count = 0
                else:
                    self.frame_count += 1
            self.image = self.frames[self.frame_count]
            self.rect.x -= speed
        if self.rect.x < -50:
            self.kill()