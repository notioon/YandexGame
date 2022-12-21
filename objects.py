import os
import sys
import pygame


def load_image(name):
    fname = os.path.join('data/assets/', name)
    if not os.path.isfile(fname):
        print(f"Файл'{fname}' не найден")
        sys.exit()
    image = pygame.image.load(fname)
    return image



class Player(pygame.sprite.Sprite):
    image_usualy = load_image("player.png")
    image_ducking = load_image("player_ducking.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = self.image_usualy
        self.isJumping = False
        self.Jumping_count = 0
        self.isDucking = False
        self.gravity = 8
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 240

    def update(self):
        if self.isJumping:  # Прыжок
            if self.rect.y > 130:
                self.rect.y -= self.gravity
            elif self.Jumping_count < 7:
                self.Jumping_count += 1
            else:
                self.isJumping = None
        elif self.isJumping is None:
            if self.rect.y != 240:
                self.rect.y += self.gravity
            else:
                self.Jumping_count = 0
                self.isJumping = False
        if self.isDucking:
            self.image = self.image_ducking
        else:
            self.image = self.image_usualy


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