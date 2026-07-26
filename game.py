import pygame
import os
import random
import time
pygame.font.init()

WIDTH = 600
HIGHIT = 600
WIND = pygame.display.set_mode((WIDTH,HIGHIT)) 
pygame.display.set_caption("Space Shooter Game")
main_font = pygame.font.SysFont("conicsans",35)
main_font = pygame.font.SysFont("conicsans",45)

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
    lost_lables= main_font.render("You Lost!!",1,(255,255,255))
    WIND.blit(lost_lables,(WIDTH//2 - lost_lables.get_width()//2-10,10))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png"))(WIDTH,HIGHIT))

red_enemy = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
green_enemy = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blue_enemy = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
green_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
blue_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))

player_ship = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))
player_laser = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

