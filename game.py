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
soundlaser = pygame.mixer.Sound("sounds/bullet.wav")
soundlaser.set_volume(0.2)

def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

def draw_lives(lives):
    lives_lables= main_font.render(f"Lives {lives}",1,(255,255,255))
    WIND.blit(lives_lables,(10,10))

def draw_levels(level):
    levels_lables= main_font.render(f"Level {level}",1,(255,255,255))
    WIND.blit(levels_lables,(WIDTH - levels_lables.get_width()-10,10))

def draw_lost():
    lost_lables= lost_font.render("You Lost!!",1,(255,255,255))
    WIND.blit(lost_lables,(WIDTH//2 - lost_lables.get_width()//2-10,HIGHIT//2))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HIGHIT))

red_enemy = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
green_enemy = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blue_enemy = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
green_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
blue_enemy_laser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))


player_ship = [pygame.image.load("assets/PlayerShipBlue2.png"),pygame.image.load("assets/PlayerShipBlue2.png"),pygame.image.load("assets/PlayerShipBlue3.png")]
player_laser = [pygame.image.load("assets/blueshoot.png"),pygame.image.load("assets/blueshoot2.png"),pygame.image.load("assets/blueshoot3.png")]


class Ship:
    fbs_shots = 30 
    def __init__(self,x,y,health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.fbs_counter = 0

    def move_laser(self,vel,obj):
        self.fbs_counter -= 1
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HIGHIT):
                self.lasers.remove(laser)
            if laser.collision (obj):
                obj.health -= 10 
                self.lasers.remove(laser)

    def shoot(self):
        if self.fbs_counter <= 0 :
            laser = Laser(self.x , self.y , self.laser_img)
            self.lasers.append(laser)
            self.fbs_counter = self.fbs_shots
            soundlaser.play()
        else:
            self.fbs_counter -= 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    # draw +=> ship
    def draw(self, screen):
        screen.blit(self.ship_img , (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.move =0

    def move(self,vel):
        self.y += vel
    def off_screen(self,height):
        return self.y > height or self.y < 0
    def collision(self,obj):
        return collide(self,obj)


    def draw(self,screen):
        screen.blit(player_ship[self.move],(self.x,self.y))
        self.move += 1
        if self.move == len (player_ship):
                    self.move = 0

    
class Player(Ship):
    def __init__(self,x,y,health = 100):
        super().__init__(x ,y ,health)
        self.ship_img = player_ship[0]
        self.laser_img = player_laser
        self.move = 0
        self.mask =pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self, vel, objs):
        self.fbs_counter -=1
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HIGHIT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, screen):
            screen.blit(player_laser[self.move],(self.x,self.y))
            self.move += 1
            if self.move == len (player_laser):
                        self.move = 0

            self.draw_healthbar(screen)

    def draw_healthbar(self,screen):
        pygame.draw.rect(screen ,(225,0,0) ,(0 , HIGHIT -10,WIDTH,HIGHIT-10))
        pygame.draw.rect(screen ,(0,225,0) ,(0 , HIGHIT -10,WIDTH*(self.health/self.max_health),10))
        


class Enemy(Ship):
    color_ships= {
        "red":(red_enemy,red_enemy_laser),
        "green":(green_enemy,green_enemy_laser),
        "blue":(blue_enemy,blue_enemy_laser)
    }

    def __init__(self,x,y,color,health = 100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img = self.color_ships[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self): 
        if self.fbs_counter <= 0 :
            laser = Laser(self.x -20 , self.y , self.laser_img)
            self.lasers.append(laser)
            self.fbs_counter = self.fbs_shots
        else:
            self.fbs_counter -= 1


def main():
    FBS = 60
    level = 0
    lives = 5 

    enemies = []
    wave_lenght = 5
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5 
    player = Player(250,450)
    lost = False
    lost_counter = 0 



    clock =pygame.time.Clock()

    def redraw():
        WIND.blit(bg , (0,0))
        draw_levels(level)
        draw_lives(lives) 
        for enemy in enemies :
            enemy.draw(WIND)

        player.draw(WIND)

        if lost:
            draw_lost()
        
        pygame.display.update()

    run = True

    while run:
        clock.tick(FBS)
        redraw()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_counter += 1

        if lost :
            if lost_counter > FBS*3:
                run = False
            else:
                continue

        if len(enemies) == 0 :
            level += 1 
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50 , WIDTH - 50), random.randrange(-1300 ,-100),random.choice(["red","blue","green"]))
                enemies.append(enemy)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0 :
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player_ship[0].get_width()< WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0 :
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel+ player_ship[0].get_height() + 20  < HIGHIT:
            player.y += player_vel
        if keys[pygame.K_SPACE] :
            player.shoot()


        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel ,player)

            if random.randrange(0,2*60) == 1 :
                enemy.shoot()

            if collide(enemy,player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HIGHIT:
                lives -= 1 
                enemies.remove(enemy)
        player.move_laser(-laser_vel , enemies)
        
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

