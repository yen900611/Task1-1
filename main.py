import pygame
from os import path

# pygame 開始
pygame.init()

# 設定長寬
WIDTH = 800
HEIGHT = 600

# 設定顏色數值
BLACK = (0,0,0)
RED = (255, 50, 0)
YELLOW = (225, 255, 0)
GREEN = (0, 255, 0)

# 設定每秒繪製幾張圖
FPS = 60


font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 28)

# 載入各種圖片
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
sling = pygame.image.load("sling.png")
red_bird = pygame.image.load("red-bird.png")
coin_img = pygame.image.load("coin.png")
meteor_img = pygame.image.load("meteor.png")

# 開啟一個視窗
score = 0
bird_limits = 3
display = pygame.display.init()
pygame.display.set_caption("Lesson1-1")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_score():
    text_surface = font.render("Score: "+str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2, 20)
    screen.blit(text_surface, text_rect)
    pass

from math import *
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(red_bird,(50,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = 180
        self.rect.centery = HEIGHT - 200
        self.isClicked = False
        self.isFlying = False
        self.origin = self.rect.center
        self.radius = 100
        self.energy = 0
        self.mass = 10
        self.vel_x = 0
        self.vel_y = 0
        self.pos = []
        self.skill = False

    def before_shot(self, mouse_pos):
        dx = mouse_pos[0] - self.origin[0]
        dy = mouse_pos[1] - self.origin[1]
        dist = hypot(dx, dy)
        if dist > self.radius:
            self.rect.centerx = self.origin[0] + self.radius * dx / dist
            self.rect.centery = self.origin[1] + self.radius * dy / dist
        else:
            self.rect.center = mouse_pos

    def update(self):
        if self.isFlying:
            self.pos.append((self.rect.centerx,self.rect.centery))
        for position in self.pos:
            pygame.draw.circle(screen,BLACK,position,1)
        global bird_limits
        if pygame.mouse.get_pressed()[0]:
            if self.isClicked:
                bird.before_shot(pygame.mouse.get_pos())
            else:
                self.isClicked = self.rect.collidepoint(pygame.mouse.get_pos())
        else:
            if self.isClicked:
                self.shot()
        if self.isFlying:
            self.flying()
        

    def flying(self):
        global bird_limits
        
        self.rect.centerx += self.vel_x
        if self.skill == False:
            self.vel_y += 0.98
        else:
            self.vel_y = 0
        self.rect.centery=self.rect.centery+self.vel_y

        if self.rect.centerx > WIDTH or self.rect.centery > HEIGHT:
            self.vel_x = 0
            self.vel_y = 0
            self.rect.center = self.origin
            bird_limits -= 1
            self.isFlying = False
            self.pos = []
            self.skill = False
        

    def shot(self):
        dx = self.origin[0] - self.rect.centerx
        dy = self.origin[1] - self.rect.centery
        self.vel_x = sqrt(pow(dx, 2) / self.mass)
        self.vel_y = sqrt(pow(dy, 2) / self.mass)
        if dx < 0:
            self.vel_x = 0 - self.vel_x
        if dy < 0:
            self.vel_y = 0 - self.vel_y
        self.isFlying = True
        self.isClicked = False
    



class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(coin_img,(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Slingshot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sling,(30,200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 180
        self.rect.bottom = HEIGHT
class Enemy():
    def showEnemy(self):
        self.image = pygame.Surface((30, 200))
        self.rect = self.image.get_rect()
        pass
    def attack():
        pass
    def update(self):
        pass

class Meteor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteor_img,(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = [0,5]
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top < 10 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]
        


# 畫出剩餘的小鳥數量
def draw_bird_limits():
    global bird_icon_rect
    bird_icon = pygame.transform.scale(red_bird,(50,50))
    bird_icon_rect = bird_icon.get_rect()
    bird_icon_rect.x = 50
    bird_icon_rect.y = 50
    for i in range(0, bird_limits+5):
        bird_icon_rect.x += 40
        screen.blit(bird_icon, bird_icon_rect)


# 初始化一些物件
bird = Bird()
slingshot = Slingshot()
coins = pygame.sprite.Group()
enemy = Enemy()
for i in range(0, 10):
    coin = Coin(WIDTH / 2 + 40 * (i % 5), HEIGHT / 2 + 40 * (i % 2))
    coins.add(coin)
meteors = pygame.sprite.Group()
meteor1=Meteor(500,200)
meteor2=Meteor(700,400)
meteor3=Meteor(300,500)
meteors.add(meteor1,meteor2,meteor3)

all_sprites = pygame.sprite.Group()
all_sprites.add(bird)
all_sprites.add(slingshot)
all_sprites.add(coins)
all_sprites.add(meteors)

clock = pygame.time.Clock()

running = True



while running:
    clock.tick(FPS)
    
    # 事件偵測
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.skill = True

    # 碰撞偵測 collision detection
    hits = pygame.sprite.spritecollide(bird, coins, False)
    for hit in hits:
        score = score + 100
        hit.kill()
    
    hit_dones = pygame.sprite.spritecollide(bird, meteors, False)
    for hit_done in hit_dones:
        score = score -50
    

    #  更新圖面
    screen.blit(background,(0,0))  # 填入到背景 #TODO
    all_sprites.draw(screen)
    draw_score()
    draw_bird_limits()


    #  更新物體數值狀態 update

    all_sprites.update()

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()