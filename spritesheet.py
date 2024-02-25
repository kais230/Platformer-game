import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT= 1000,800
FPS = 60
PLAYER_VEL=5

pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))


def get_block(size,x,y):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(x,y, size, size)
    surface.blit(image, (0,0), rect)

    return pygame.transform.scale2x(surface)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles=[]
    # With these for loops we find out how many tiles we need for our screen and their position
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)

    return tiles, image

def get_background2():
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.fill((255, 255, 255))

    #pine1_img = pygame.image.load(join("assets","Background2","pine1.png"))
    #pine2_img = pygame.image.load(join("assets","Background2","pine2.png"))
    #mountain_img = pygame.image.load(join("assets","Background2","mountain.png"))
    #sky_img = pygame.image.load(join("assets","Background2","sky_cloud.png"))

    #background_surface.blit(sky_img, (0, 0))
    #background_surface.blit(mountain_img, (0, HEIGHT - mountain_img.get_height() - 300))
    #background_surface.blit(pine1_img, (0, HEIGHT - pine1_img.get_height() - 150))
    #background_surface.blit(pine2_img, (0, HEIGHT - pine2_img.get_height()))
    back = pygame.image.load(join("assets", "Background2", "moon.jpg")).convert_alpha()
    window.blit(back, (0, 0))


  #  return sky_img, mountain_img, pine1_img, pine2_img





def flip(sprites): #animation
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2 ,width, height ,direction=False):
    path = join ("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites ={}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() #Transparent background remover

        sprites=[]
        for i in range(sprite_sheet.get_width()//width):
            surface =pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet, (0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)

        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites
