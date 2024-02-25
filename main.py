
import pygame

from player import Player
from object import Object, Block, Trap
from spritesheet import  get_block, load_sprite_sheets, flip, get_background, get_background2
from health_bar import HealthBar
from enemy import Enemy
from map_objects import initialize_objects

pygame.init()

pygame.display.set_caption("Platformer")


WIDTH, HEIGHT= 1000,800
FPS = 60
PLAYER_VEL=5
GAME_STATE_PLAYING = 0
GAME_STATE_LOSE = 1
GAME_STATE_WIN = 2

window = pygame.display.set_mode((WIDTH,HEIGHT))
wintime = 0


def draw(window, background, bg_image, player, objects, offset_x, offset_y, healthbar, game_state, enemies, font, restart_button_rect, current_time):

    #for tile in background:
    #   window.blit(bg_image, tuple(tile))  #This is where the back ground drawing occurs

    get_background2()

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

    for enemy in enemies:
        enemy.draw(window, offset_x, offset_y)

    if game_state == GAME_STATE_LOSE:
        # Display "You Lose!" message
        font_large = pygame.font.Font(None, 74)
        text_large = font_large.render("YOU LOST!", True, (255, 0, 0))
        text_large_rect = text_large.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(text_large, text_large_rect)

        # Display "Restart" button
        #restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
        pygame.draw.rect(window, (0, 255, 0), restart_button_rect)
        font_small = pygame.font.Font(None, 36)
        text_restart = font_small.render("Restart", True, (0, 0, 0))
        text_restart_rect = text_restart.get_rect(center=restart_button_rect.center)
        window.blit(text_restart, text_restart_rect)

    elif game_state == GAME_STATE_WIN:
        font_large = pygame.font.Font(None, 74)
        text_large = font_large.render("YOU WIN!", True, (0, 255, 0))
        text_large_rect = text_large.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(text_large, text_large_rect)

        #elapsed_time = pygame.time.get_ticks()
        minutes, seconds = divmod(current_time // 1000, 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"

        font_timer = pygame.font.Font(None, 24)
        text_timer = font_timer.render(timer_text, True, (0, 255, 0))
        window.blit(text_timer, (WIDTH // 2 - 45, HEIGHT // 2 - 20))

        pygame.draw.rect(window, (0, 255, 0), restart_button_rect)
        font_small = pygame.font.Font(None, 36)
        text_restart = font_small.render("Restart", True, (0, 0, 0))
        text_restart_rect = text_restart.get_rect(center=restart_button_rect.center)
        window.blit(text_restart, text_restart_rect)

    healthbar.draw(window)

    if game_state != GAME_STATE_WIN:
        minutes, seconds = divmod(current_time // 1000, 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"

        font_timer = pygame.font.Font(None, 24)
        text_timer = font_timer.render(timer_text, True, (255, 255, 255))
        window.blit(text_timer, (WIDTH - 120, 10))

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx,0)
    player.update()
    collided_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            collided_objects = obj
            break

    player.move(-dx,0)
    player.update()
    return collided_objects


def handle_move(player, objects, enemies, healthbar):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not collide_left:
        player.move_left(PLAYER_VEL)

    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not collide_right:
        player.move_right(PLAYER_VEL)

    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            player.make_hit()
            healthbar.hp = player.hp

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and (obj.name == "Fire" or obj.name == "Saw"):
            player.make_hit()
            healthbar.hp = player.hp


def main(window, time):
    clock = pygame.time.Clock()
    background, bg_image=get_background("Blue.png")

    block_size = 96

    player = Player(450, 2300, 50, 50)
    enemy1 = Enemy(1200, 27*block_size + 65, 50, 50, 950, 1800)
    enemy2 = Enemy(63 *block_size, 20 * block_size + 65, 50, 50, 59 * block_size, 66 * block_size)
    enemy3 = Enemy(54 *block_size, 20 * block_size + 65, 50, 50, 50 * block_size, 57 * block_size)
    enemy4 = Enemy(68 * block_size, 14 * block_size + 65, 50, 50, 67 * block_size, 71 * block_size)
    enemy5 = Enemy(84 * block_size, 24 * block_size + 65, 50, 50, 80 * block_size, 86 * block_size)
    enemies = [enemy1, enemy2, enemy3,enemy4, enemy5]


    healthbar= HealthBar(30,30,300,40,100)
    offset_x = 0
    offset_y = 2300
    scroll_area_width = 300
    scroll_area_height = 200

    objects = initialize_objects(block_size)
    fire_list =[]
    for obj in objects:
        if obj.name == "Fire" or obj.name == "Saw":
            fire_list.append(obj)
            obj.on()

    Portal_list = []
    for obj in objects:
        if obj.name == "Portal":
            Portal_list.append(obj)




    run = True
    game_state = GAME_STATE_PLAYING

    font = pygame.font.Font(None, 36)
    restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    current_time=pygame.time.get_ticks()
    while run:

        clock.tick(FPS)
        dt = clock.get_time() / 1000.0

        for enemy in enemies:
            enemy.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                collide_left = collide(player, objects, -PLAYER_VEL * 2)
                collide_right = collide(player, objects, PLAYER_VEL * 2)
                if collide_left or collide_right:
                    player.jump_count = 0
                if event.key == pygame.K_w and player.jump_count < 2:
                    player.jump()



        player.loop(FPS, dt)

        collide_left = collide(player, Portal_list, -PLAYER_VEL * 2)
        collide_right = collide(player, Portal_list, PLAYER_VEL * 2)
        if collide_left or collide_right:
            game_state = GAME_STATE_WIN
        for enemy in enemies:
            enemy.update_sprite()
        for fire in fire_list:
            fire.loop()

        if healthbar.hp <= 0:
            game_state = GAME_STATE_LOSE
            wintime = pygame.time.get_ticks()

        if game_state != GAME_STATE_WIN:
            current_time = pygame.time.get_ticks() - time
        else:
            wintime = pygame.time.get_ticks()


        if event.type == pygame.MOUSEBUTTONDOWN and (game_state == GAME_STATE_LOSE or game_state == GAME_STATE_WIN):
            if restart_button_rect.collidepoint(event.pos):
                restart_game(window,wintime)

        handle_move(player, objects, enemies, healthbar)

        draw(window, background, bg_image, player, objects, offset_x, offset_y, healthbar, game_state, enemies, font, restart_button_rect, current_time)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
                (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

    pygame.quit()
    quit()


def restart_game(window,wintime):
    main(window,wintime)


if __name__ == "__main__":
    main(window,0)