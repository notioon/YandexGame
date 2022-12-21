import sys
import os
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fname = os.path.join('data', name)
    if not os.path.isfile(fname):
        print(f"Файл'{fname}' не найден")
        sys.exit()
    image = pygame.image.load(fname)
    return image


def start_screen():
    size = WIDTH, HEIGHT = 700, 350
    screen = pygame.display.set_mode(size=size)
    fon = pygame.transform.scale(load_image("start_fon.png"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()