import pygame
import os
import random
import sys

pygame.init()
pygame.font.init()

def pathing(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)



WIDTH = 600
HIGHIT = 600
WIND = pygame.display.set_mode((WIDTH,HIGHIT)) 
pygame.display.set_caption("Space Shooter Game")
main_font = pygame.font.SysFont("comicsans",35)
lost_font = pygame.font.SysFont("comicsans",45)
soundlaser = pygame.mixer.Sound(pathing("sounds/bullet.wav"))
soundlaser.set_volume(0.2)
bomsound = pygame.mixer.Sound(pathing("sounds/bom.mp3"))
bomsound.set_volume(0.2)
tryagainsound = pygame.mixer.Sound(pathing("sounds/tryagain.mp3"))
pygame.mixer.music.load(pathing("sounds/space.mp3"))
pygame.mixer.music.set_volume(0.2)


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


red_enemy_imgs = [pygame.image.load(pathing("assets/redship1.png")),pygame.image.load(pathing("assets/redship2.png")),pygame.image.load(pathing("assets/redship3.png"))]
purple_enemy_imgs = [pygame.image.load(pathing("assets/purpleship1.png")),pygame.image.load(pathing("assets/purpleship2.png")),pygame.image.load(pathing("assets/purpleship3.png")),pygame.image.load(pathing("assets/purpleship4.png"))]
green_enemy_imgs = [pygame.image.load(pathing("assets/greenship1.png")),pygame.image.load(pathing("assets/greenship2.png"))]
yellow_enemy_imgs = [pygame.image.load(pathing("assets/yellowship1.png")),pygame.image.load(pathing("assets/yellowship2.png")),pygame.image.load(pathing("assets/yellowship3.png"))]
red_enemy_laser_imgs = [pygame.image.load(pathing("assets/redshoot1.png")),pygame.image.load(pathing("assets/redshoot2.png")),pygame.image.load(pathing("assets/redshoot3.png"))]
purple_enemy_laser_imgs = [pygame.image.load(pathing("assets/purpleshoot1.png")),pygame.image.load(pathing("assets/purpleshoot2.png")),pygame.image.load(pathing("assets/purpleshoot3.png"))]
green_enemy_laser_imgs = [pygame.image.load(pathing("assets/greenshoot1.png")),pygame.image.load(pathing("assets/greenshoot2.png")),pygame.image.load(pathing("assets/greenshoot3.png"))]
yellow_enemy_laser_imgs = [pygame.image.load(pathing("assets/yellowshoot1.png")),pygame.image.load(pathing("assets/yellowshoot2.png")),pygame.image.load(pathing("assets/yellowshoot3.png"))]

player_ship_imgs = [pygame.image.load(pathing("assets/PlayerShipBlue2.png")),pygame.image.load(pathing("assets/PlayerShipBlue2.png")),pygame.image.load(pathing("assets/PlayerShipBlue3.png"))]
player_laser_imgs = [pygame.image.load(pathing("assets/playershoot1.png")),pygame.image.load(pathing("assets/playershoot2.png")),pygame.image.load(pathing("assets/playershoot3.png")),pygame.image.load(pathing("assets/playershoot4.png")),pygame.image.load(pathing("assets/playershoot5.png"))]


class Ship:
    fbs_shots = 30 
    def __init__(self,x,y,health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_imgs = None
        self.laser_img = None
        self.lasers = []
        self.fbs_counter = 0
        self.index = 0
        self.moves = 0

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
            laser = Laser(self.x + (self.get_width()//2) - self.laser_img[0].get_width()//2 , self.y , self.laser_img)
            self.lasers.append(laser)
            self.fbs_counter = self.fbs_shots
            soundlaser.play()
        else:
            self.fbs_counter -= 1

    def get_width(self):
        return self.ship_imgs[0].get_width()

    def get_height(self):
        return self.ship_imgs[0].get_height()

    # draw +=> ship
    def draw(self, screen):
        screen.blit(self.ship_imgs[int(self.index) % len(self.ship_imgs)] , (self.x, self.y))
        self.index += 0.03
        for laser in self.lasers:
            laser.draw(screen)

class Laser:
    def __init__(self,x,y,anim_imgs):
        self.x = x
        self.y = y
        self.img = anim_imgs[0]
        self.mask = pygame.mask.from_surface(self.img)
        self.anim_index = 0 
        self.anim_imgs = anim_imgs

    def move(self,vel):
        self.y += vel
    def off_screen(self,height):
        return self.y > height or self.y < 0
    def collision(self,obj):
        return collide(self,obj)


    def draw(self,screen):
        screen.blit(self.anim_imgs[int(self.anim_index) % len(self.anim_imgs)],(self.x,self.y))
        self.anim_index += 0.02
        if self.anim_index == len (self.anim_imgs):
                    self.anim_index = 0

    
class Player(Ship):
    def __init__(self,x,y,health = 100):
        super().__init__(x ,y ,health)
        self.ship_img = player_ship_imgs
        self.laser_img = player_laser_imgs
        self.moves = 0
        self.mask =pygame.mask.from_surface(self.ship_img[0])
        self.max_health = health
        self.index = 0 
        self.laserImgs = player_laser_imgs
        self.ship_imgs = player_ship_imgs

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
                        bomsound.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, screen):
            screen.blit(self.ship_imgs[int(self.index) % len(self.ship_imgs)],(self.x,self.y))
            self.index += 0.03
            if self.moves == len (self.ship_imgs):
                        self.moves = 0
            for laser in self.lasers:
                laser.draw(screen)

            self.draw_healthbar(screen)

    def draw_healthbar(self,screen):
        pygame.draw.rect(screen ,(225,0,0) ,(0 , HIGHIT -10,WIDTH,HIGHIT-10))
        pygame.draw.rect(screen ,(0,225,0) ,(0 , HIGHIT -10,WIDTH*(self.health/self.max_health),10))
        


class Enemy(Ship):
    color_ships= {
        "red":(red_enemy_imgs,red_enemy_laser_imgs),
        "green":(green_enemy_imgs,green_enemy_laser_imgs),
        "purple":(purple_enemy_imgs,purple_enemy_laser_imgs),
        "yellow":(yellow_enemy_imgs,yellow_enemy_laser_imgs)
    }

    def __init__(self,x,y,color,health = 100):
        super().__init__(x,y,health)
        self.ship_imgs,self.laser_img = self.color_ships[color]
        self.mask = pygame.mask.from_surface(self.ship_imgs[0])

    def move(self, vel):
        self.y += vel

    def shoot(self): 
        if self.fbs_counter <= 0 :
            laser = Laser((self.x + self.get_width()//2)-20  , self.y , self.laser_img )
            self.lasers.append(laser)
            self.fbs_counter = self.fbs_shots
        else:
            self.fbs_counter -= 1


def main():
    pygame.mixer.music.play()

    FBS = 60
    level = 0
    lives = 5 

    enemies = []
    wave_lenght = 7
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
                tryagainsound.play()
            else:
                continue

        if len(enemies) == 0 :
            level += 1 
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50 , WIDTH - 50), random.randrange(-1300 ,-100),random.choice(["red","purple","green","yellow"]))
                enemies.append(enemy)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0 :
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player_ship_imgs[0].get_width()< WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0 :
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel+ player_ship_imgs[0].get_height() + 20  < HIGHIT:
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
                bomsound.play()

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

