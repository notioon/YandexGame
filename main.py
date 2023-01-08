import pygame.sprite
from datetime import datetime
from objects import *
from random import randrange
from sqlite.sqlite_methods import *


### Global constants ###

pygame.init()
pygame.font.init()
JUMP_SOUND = pygame.mixer.Sound('data/assets/jump.wav')
DIE_SOUND = pygame.mixer.Sound('data/assets/die.wav')
CHECKPOINT_SOUND = pygame.mixer.Sound('data/assets/checkPoint.wav')
COINS_SOUND = pygame.mixer.Sound('data/assets/coins.wav')
FONT_PATH = "data/Font.ttf"


FPS = 60
SIZE = WIDTH, HEIGHT = 800, 400
SPEED = 4
K_SCORE = 1
GRAVITY = 8
BACKGROUND_COLOR = "#100821"
CURRENT_NICKNAME = '  Nickname'
CURRENT_SKIN = "red"


def main():
    start_window()
    main_menu()


def gameplay():  # Окно игры
    ### Setting Display ###
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    screen.fill(BACKGROUND_COLOR)
    ### Setting Value ###
    high_score = high_record(CURRENT_NICKNAME)
    running = True
    k_spawn = 1
    clock = pygame.time.Clock()
    current_score = 0
    count_cloud = 0
    count_spawn = 0
    count_coins = 0
    speed = SPEED
    gravity = GRAVITY
    time_start = datetime.now()
    ### Creating Groups ###
    sprites = pygame.sprite.Group()
    ground_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    cloud_sprite = pygame.sprite.Group()
    coins_sprite = pygame.sprite.Group()
    ### Creating Objects
    player = Player(CURRENT_SKIN, player_sprite)
    Ground(ground_sprites)
    Cloud(cloud_sprite)
    Cactus(sprites)
    ground_sprites.update(speed)
    player.update(gravity)
    cloud_sprite.update(speed * 0.5)
    coins_sprite.update(speed)
    sprites.update(speed)
    ### Drawing Groups ###
    ground_sprites.draw(screen)
    player_sprite.draw(screen)
    cloud_sprite.draw(screen)
    sprites.draw(screen)
    ### Loop ###
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Проверка на прыжок
                    if not player.isJumping and not player.isJumping is None and not player.isDucking:
                        player.isJumping = True
                        if pygame.mixer.get_init() is not None:
                            JUMP_SOUND.play()

                if event.key == pygame.K_DOWN and not player.isJumping:  # Проверка на нырок
                    if not player.isDucking:
                        player.isDucking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.isDucking = False

        count_cloud += 1
        count_spawn += k_spawn * 1
        ### Spawn Clouds ###
        if randrange(0, 150) == 100 and count_cloud > 100:
            Cloud(cloud_sprite)
            count_cloud = 0
        ### Spawn Cactuses and Pteras ###
        if randrange(0, 100) == 50 and count_spawn > 50 or count_spawn == 100:
            if randrange(0, 4) == 3:
                Ptera(sprites)
                count_spawn = 0
            else:
                Cactus(sprites)
                count_spawn = 0
                k_spawn += 0.1
        ### Spawn Coins ###
        if randrange(0, 150) == 100:
            coin = Coin(coins_sprite)
            for cactus in sprites:
                if pygame.sprite.collide_mask(coin, cactus) and cactus.rect.y != 190:
                    coin.rect.y = 200


        current_score += 10/60
        ### Drawing Score
        score(screen, max(high_score, int(str(current_score).split('.')[0])), str(current_score).split('.')[0], count_coins)

        if (datetime.now() - time_start).seconds == 10:
            CHECKPOINT_SOUND.play()
            speed += 0.5
            gravity += 1
            time_start = datetime.now()
        ### Checking collision ###
        for cactus in sprites:
            if pygame.sprite.collide_mask(player, cactus):
                change_coins(CURRENT_NICKNAME, count_coins)
                record(CURRENT_NICKNAME, int(str(current_score).split('.')[0]))
                DIE_SOUND.play()
                player_sprite.update(gravity, True)
                player_sprite.draw(screen)
                pygame.display.flip()
                running = False

        for coin in coins_sprite:
            if pygame.sprite.collide_mask(player, coin):
                COINS_SOUND.play()
                count_coins += 1
                coin.isVisible = False

        ### Updating ###
        sprites.update(speed)
        ground_sprites.update(speed)
        player.update(gravity)
        cloud_sprite.update(speed * 0.5)
        coins_sprite.update(speed)
        ### Drawing ###
        ground_sprites.draw(screen)
        player_sprite.draw(screen)
        cloud_sprite.draw(screen)
        sprites.draw(screen)
        coins_sprite.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    gameover(screen)


def gameover(screen):  # Отображение окна после смерти персонажа
    buttons = pygame.sprite.Group()
    replay_button = ReplayButton(buttons)
    main_menu_button = MainMenuButton(buttons)
    GameOver(buttons)
    buttons.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.rect.collidepoint(event.pos):
                    gameplay()
                elif main_menu_button.rect.collidepoint(event.pos):
                    main_menu()


def main_menu():  # Отображение главного меню
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    screen.fill(BACKGROUND_COLOR)
    ground_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    Player(CURRENT_SKIN, player_sprite)
    Ground(ground_sprites)
    ground_sprites.draw(screen)
    player_sprite.draw(screen)
    skins_btn = SkinsBtn(buttons)
    leaderboards_btn = LeaderbjardsBtn(buttons)
    nickname_btn = EmptyBtn(buttons)
    Logo(buttons)
    Tip(buttons)
    buttons.draw(screen)
    pygame.display.flip()
    input_active = False
    font = pygame.font.Font(FONT_PATH, 12)
    global CURRENT_NICKNAME
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if nickname_btn.rect.collidepoint(event.pos):
                    EmptyBtn(buttons)
                    buttons.remove(nickname_btn)
                    CURRENT_NICKNAME = ''
                    input_active = True
                elif skins_btn.rect.collidepoint(event.pos):
                    skins_menu()
                elif leaderboards_btn.rect.collidepoint(event.pos):
                    leaderboard_window()
                else:
                    if check_users(CURRENT_NICKNAME) is None:
                        register_users(CURRENT_NICKNAME)
                    gameplay()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    CURRENT_NICKNAME = CURRENT_NICKNAME[:-1]
                else:
                    CURRENT_NICKNAME += event.unicode
            buttons.draw(screen)
            nick_surf = font.render(CURRENT_NICKNAME, True, (255, 255, 255))
            screen.blit(nick_surf, (330, 190))
            pygame.display.flip()


def skins_menu():  # Отображение окна "Skins"
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    font = pygame.font.Font(FONT_PATH, 14)
    global CURRENT_SKIN
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    try:
        coins, green, red, yellow, blue = get_coins(CURRENT_NICKNAME)
        coins_surf = font.render(str(coins), True, (255, 255, 255))
        screen.blit(coins_surf, (700, 30))
        screen.fill(BACKGROUND_COLOR)
        CoinsLabel(sprites)
        ShopItems(sprites)
        main_menu_button = MainMenuButton(sprites)
        if red == 0:
            a = Price(sprites)
            b_red = Locker(buttons)
            a.rect.x, a.rect.y = 285, 201
            b_red.rect.x, b_red.rect.y = 282, 74
        if yellow == 0:
            a = Price(sprites)
            b_yellow = Locker(buttons)
            a.rect.x, a.rect.y = 138, 201
            b_yellow.rect.x, b_yellow.rect.y = 134, 74
        if blue == 0:
            a = Price(sprites)
            b_blue = Locker(buttons)
            a.rect.x, a.rect.y = 438, 201
            b_blue.rect.x, b_blue.rect.y = 430, 74
        sprites.draw(screen)
        buttons.draw(screen)
        screen.blit(coins_surf, (700, 30))
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.rect.collidepoint(event.pos):
                        main_menu()
                    for button in buttons:
                        if button.rect.collidepoint(event.pos) and coins >= 100:
                            if 282 <= event.pos[0] <= 375:
                                change_coins(CURRENT_NICKNAME, -100)
                                buy_dino(CURRENT_NICKNAME, "red_skin")
                            elif 134 <= event.pos[0] <= 227:
                                change_coins(CURRENT_NICKNAME, -100)
                                buy_dino(CURRENT_NICKNAME, "yellow_skin")
                            else:
                                change_coins(CURRENT_NICKNAME, -100)
                                buy_dino(CURRENT_NICKNAME, "blue_skin")
                    for sprite in sprites:
                        if sprite.rect.collidepoint(event.pos):
                            if 116 <= event.pos[0] <= 244 and yellow == 1:
                                CURRENT_SKIN = "yellow"
                                main_menu()
                            elif 264 <= event.pos[0] <= 392 and red == 1:
                                CURRENT_SKIN = "red"
                                main_menu()
                            elif 412 <= event.pos[0] <= 540 and blue == 1:
                                CURRENT_SKIN = "blue"
                                main_menu()
                            elif 556 <= event.pos[0] <= 684 and green == 1:
                                CURRENT_SKIN = "green"
                                main_menu()
                    skins_menu()
            pygame.display.flip()
    except TypeError:
        main_menu()


def leaderboard_window():  # Отображение страницы "Список лидеров"
    pygame.display.set_caption("Dino 🦕")
    screen = pygame.display.set_mode(SIZE)
    screen.fill(BACKGROUND_COLOR)
    sprites = pygame.sprite.Group()
    main_menu_button = MainMenuButton(sprites)
    LeaderboardsLabel(sprites)
    font = pygame.font.Font(FONT_PATH, 10)
    lst = get_list_leaderboards()
    sprites.draw(screen)
    x, y = 185, 18
    for i, l in enumerate(lst):
        if i < 5:
            text = font.render(f"{i + 1}. {l[0].strip()} - {l[1]}", True, (255, 255, 255))
            screen.blit(text, (x, y))
            y += 62
        if i == 5:
            y = 18
            x += 235
            text = font.render(f"{i + 1}. {l[0].strip()} - {l[1]}", True, (255, 255, 255))
            screen.blit(text, (x, y))
        if i > 5:
            y += 62
            text = font.render(f"{i + 1}. {l[0].strip()} - {l[1]}", True, (255, 255, 255))
            screen.blit(text, (x, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.rect.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()


def score(screen, max_, score_, coins):  # Отображение счета очков и монет
    font = pygame.font.Font(FONT_PATH, 13)
    text = font.render("HI:" + str(max_) + " " + str(score_) + " M:" + str(coins), True, "#9296BE")
    text_print = text.get_rect()
    text_print.center = 680, 40
    screen.blit(text, text_print)


def start_window():  # Стартовое окно
    pygame.display.set_caption("Dino 🦕")
    size = width, height = 700, 350
    screen = pygame.display.set_mode(size=size)
    fon = pygame.transform.scale(load_image("start_fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_image(name):  # Загрузка изображений
    fname = os.path.join('data', name)
    if not os.path.isfile(fname):
        print(f"Файл'{fname}' не найден")
        sys.exit()
    image = pygame.image.load(fname)
    return image


def terminate():  # "Мягкое уничтожение окна"
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
