import pygame
import os
import random
import time
pygame.init()
pygame.font.init()


WIDTH = 600
HIGHIT = 600
WIND = pygame.display.set_mode((WIDTH,HIGHIT)) 
pygame.display.set_caption("Space Shooter Game")
main_font = pygame.font.SysFont("comicsans",35)
lost_font = pygame.font.SysFont("comicsans",45)

def collide(obj1,obj2):
    offset_x = obj1.x - obj1.x
    offset_y = obj1.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

def draw_lives(lives):
    lives_lables= main_font.render(f"Lives {lives}",1,(255,255,255))
    WIND.blit(lives_lables,(10,10))

def draw_levels(level):
    levels_lables= main_font.render(f"Lives {level}",1,(255,255,255))
    WIND.blit(levels_lables,(WIDTH - levels_lables.get_width()-10,10))

def draw_lost():
    lost_lables= lost_font.render("You Lost!!",1,(255,255,255))
    WIND.blit(lost_lables,(WIDTH//2 - lost_lables.get_width()//2-10,10))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HIGHIT))

red_enemy = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
green_enemy = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blue_enemy = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
green_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
blue_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))

player_ship = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))
player_laser = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))


def main():
    FBS = 60
    level = 0
    lives = 5 

    clock =pygame.time.Clock()

    def redraw():
        WIND.blit(bg , (0,0))
        draw_levels(level)
        draw_lives(lives) 
        pygame.display.update()

    while True:
        clock.tick(FBS)
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

def main_menu():
    while True:
        WIND.blit(bg , (0,0))
        title_lable = lost_font.render("Press the mouse to begin....",1,(255,255,255))
        WIND.blit(title_lable,(WIDTH//2-title_lable.get_width()//2 ,HIGHIT//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
        # pygame.quit()

main_menu()

