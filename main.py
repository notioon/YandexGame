import pygame.sprite
from datetime import datetime
from objects import *
from random import randrange


### Global constants ###

pygame.init()
pygame.font.init()

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 400
SPEED = 4
HIGH_SCORE = 0
K_SCORE = 1
GRAVITY = 8


def main():
    start_window()
    gameplay()


def gameplay():
    ### Setting Display ###
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    screen.fill((69, 69, 69))
    ### Setting Value ###
    k_spawn = 1
    running = True
    clock = pygame.time.Clock()
    current_score = 0
    world_map = []
    count_cloud = 0
    count_cactus = 0
    speed = SPEED
    gravity = GRAVITY
    time_start = datetime.now()
    ### Creating Groups ###
    ground_sprites = pygame.sprite.Group()
    cactus_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    cloud_sprite = pygame.sprite.Group()
    ### Creating Objects
    player = Player(player_sprite)
    ground = Ground(ground_sprites)
    Cloud(cloud_sprite)
    Cactus(cactus_sprites)
    ### Drawing Groups ###
    ground_sprites.draw(screen)
    player_sprite.draw(screen)
    cloud_sprite.draw(screen)
    cactus_sprites.draw(screen)
    ### Loop ###
    while running:
        screen.fill((69, 69, 69))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not player.isJumping and not player.isJumping is None and not player.isDucking:
                        player.isJumping = True
                if event.key == pygame.K_DOWN and not player.isJumping:
                    if not player.isDucking:
                        player.isDucking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.isDucking = False

        count_cloud += 1
        count_cactus += k_spawn * 1
        ### Spawn Clouds
        if randrange(0, 150) == 100 and count_cloud > 100:
            Cloud(cloud_sprite)
            count_cloud = 0
        ### Spawn Cactuses
        if randrange(0, 100) == 50 and count_cactus > 100:
            Cactus(cactus_sprites)
            count_cactus = 0
            k_spawn += 0.1


        current_score += 10/60
        ### Drawing Score
        score(screen, max(HIGH_SCORE, int(str(current_score).split('.')[0])), str(current_score).split('.')[0])

        if (datetime.now() - time_start).seconds == 10:
            speed += 0.5
            gravity += 1
            time_start = datetime.now()
        ### Checking collision ###
        for cactus in cactus_sprites:
            if pygame.sprite.collide_mask(player, cactus):
                player.isDead = True
                running = False
        ### Updating ###
        cactus_sprites.update(speed)
        ground.update(speed)
        player.update(gravity)
        cloud_sprite.update(speed * 0.5)
        ### Drawing ###
        ground_sprites.draw(screen)
        player_sprite.draw(screen)
        cloud_sprite.draw(screen)
        cactus_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    gameover()


def gameover():
    pass


def score(screen, max, score):
    font = pygame.font.Font("Font.ttf", 13)
    text = font.render("HI:" + str(max) + " " + str(score), True, (pygame.Color("black")))
    text_print = text.get_rect()
    text_print.center = 690, 40
    screen.blit(text, text_print)


def start_window():
    pygame.display.set_caption("Dino 🦕")
    size = width, height = 700, 350
    screen = pygame.display.set_mode(size=size)
    fon = pygame.transform.scale(load_image("start_fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_image(name):
    fname = os.path.join('data', name)
    if not os.path.isfile(fname):
        print(f"Файл'{fname}' не найден")
        sys.exit()
    image = pygame.image.load(fname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
