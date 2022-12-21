from objects import *


### Global constants ###

pygame.init()
pygame.font.init()

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 400
SPEED = 4
HIGH_SCORE = 151
K_SCORE = 1


def main():
    start_window()
    gameplay()


def gameplay():
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()
    ground_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    player = Player(player_sprite)
    ground = Ground(ground_sprites)
    ground_sprites.draw(screen)
    player_sprite.draw(screen)
    current_score = 0
    while True:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not player.isJumping and not player.isJumping is None:
                        player.isJumping = True
                if event.key == pygame.K_DOWN:
                    if not player.isDucking:
                        player.isDucking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.isDucking = False
        current_score += 10/60
        speed = current_score // 100 + SPEED
        ground.update(speed)
        player.update()
        score(screen, max(HIGH_SCORE, int(str(current_score).split('.')[0])), str(current_score).split('.')[0])
        ground_sprites.draw(screen)
        player_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


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
