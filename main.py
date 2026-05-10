from pygame import *
from time import time as timer
from random import randint
font.init()
mixer.init()
font1 = font.Font(None, 40)

ping = mixer.Sound("ping.mp3")
win = mixer.Sound("win.mp3")
boost = mixer.Sound("Boost.mp3")
BP = mixer.Sound("BoostPickup.mp3")
pong = mixer.Sound("pong.mp3")

bg = transform.scale(image.load("фон.jpg"),(700,500))
ball = transform.scale(image.load("мячик.jpg"),(50,50))
boostBalling = transform.scale(image.load("ищщые.jpg"),(50,50))
player1sprite = Surface((30,150))
player2sprite = Surface((30,150))
player1sprite.fill((0,255,255))
player2sprite.fill((255,153,51))

player1spritebonus = Surface((30,250))
player1spritebonus.fill((0,255,255))
player2spritebonus = Surface((30,250))
player2spritebonus.fill((255,153,51))

game = True
finish = False
window = display.set_mode((700,500))
display.set_caption("пинги понги")
display.set_icon(ball)

clock = time.Clock()
FPS = 60

score1 = 0
score2 = 0

ST = timer()

"""НАСТРОЙКИ"""

win_requirement = 3
ball_cooldown = 1
bonus_ball_cooldown = 5
players_speed = 5
ball_speed = 7

"""--------""" 

class GameSprite(sprite.Sprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__()
        self.img = sprite
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.img,(self.rect.x,self.rect.y))

class Player1(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        self.bonus = False
        self.bonustimer = 0
    def move(self):
        keuys = key.get_pressed()
        if keuys[K_w] and self.rect.y > 15:
            self.rect.y -= self.speed
        elif keuys[K_s] and self.rect.y < 340:
            self.rect.y += self.speed
        elif keuys[K_a] and self.bonus == True:
            boost.play()
            self.img = player1spritebonus
            self.img.fill((0,255,255))
            bb = self.rect.x
            bby = self.rect.y
            self.rect = self.img.get_rect()
            self.rect.x = bb
            self.rect.y = bby
            self.bonustimer = timer()
            self.bonus = False
        if timer() - self.bonustimer >= 3 and self.bonustimer != 0:
            self.img = player1sprite
            bb = self.rect.x
            bby = self.rect.y
            self.rect = self.img.get_rect()
            self.rect.x = bb
            self.rect.y = bby
            self.bonustimer = 0
        elif timer() - self.bonustimer >= 2 and self.bonustimer != 0:
            self.img.fill((0,155,155))

class Player2(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        self.bonus = False
        self.bonustimer = 0
    def move(self):
        keuys = key.get_pressed()
        if keuys[K_UP] and self.rect.y > 15:
            self.rect.y -= self.speed
        elif keuys[K_DOWN] and self.rect.y < 340:
            self.rect.y += self.speed
        elif keuys[K_LEFT] and self.bonus == True:
            self.img = player2spritebonus
            boost.play()
            self.img.fill((255,153,51))
            bb = self.rect.x
            bby = self.rect.y
            self.rect = self.img.get_rect()
            self.rect.x = bb
            self.rect.y = bby
            self.bonustimer = timer()
            self.bonus = False
        if timer() - self.bonustimer >= 3 and self.bonustimer != 0:
            self.img = player2sprite
            bb = self.rect.x
            bby = self.rect.y
            self.rect = self.img.get_rect()
            self.rect.x = bb
            self.rect.y = bby
            self.bonustimer = 0
        elif timer() - self.bonustimer >= 2 and self.bonustimer != 0:
            self.img.fill((155,53,51))

class Ball(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        global score1
        global score2
        if score1 > score2:
            self.Xdir = "Left"
        else:
            self.Xdir = "Right"
        if randint(1,2) == 1:
            self.Ydir = "Down"
        else:
            self.Ydir = "Up"
    def move(self):
        if self.Xdir == "Left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.Ydir == "Down":
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        if self.rect.y > 450:
            ping.play()
            self.Ydir = "Up"
        elif self.rect.y < 0:
            ping.play()
            self.Ydir = "Down"
class BoostBall(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        global score1
        global score2
        if score1 < score2:
            self.Xdir = "Left"
        else:
            self.Xdir = "Right"
        if randint(1,2) == 1:
            self.Ydir = "Down"
        else:
            self.Ydir = "Up"
    def move(self):
        if self.Xdir == "Left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.Ydir == "Down":
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        if self.rect.y > 450:
            pong.play()
            self.Ydir = "Up"
        elif self.rect.y < 0:
            pong.play()
            self.Ydir = "Down"
        if self.rect.x < 0:
            pong.play()
            self.Xdir = "Right"
        elif self.rect.x > 650:
            pong.play()
            self.Xdir = "Left"

plr1 = Player1(player1sprite,5,250,players_speed)
plr2 = Player2(player2sprite,660,250,players_speed)
bal = None
bonusbal = None

bonusballTime = timer()

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    if finish == False:
        window.blit(bg,(0,0))
        plr1.reset()
        plr2.reset()
        plr1.move()
        plr2.move()
        if bonusbal != None:
            bonusbal.reset()
            bonusbal.move()
            if sprite.collide_rect(plr1,bonusbal):
                bonusballTime = timer()
                plr1.bonus = True
                bonusbal = None
                BP.play()
            elif sprite.collide_rect(plr2,bonusbal):
                bonusballTime = timer()
                plr2.bonus = True
                bonusbal = None
                BP.play()
        else:
            if timer()-bonusballTime >= bonus_ball_cooldown:
                bonusbal = BoostBall(boostBalling,350,250,ball_speed)
        if bal != None:
            bal.reset()
            bal.move()
            if sprite.collide_rect(plr1,bal):
                ping.play()
                bal.Xdir = "Right"
            elif sprite.collide_rect(plr2,bal):
                ping.play()
                bal.Xdir = "Left"
            if bal.rect.x < -15:
                win.play()
                bal = None
                ST =timer()
                score2 += 1
            elif bal.rect.x > 700:
                win.play()
                bal = None
                ST = timer()
                score1 += 1
        else:
            if timer()-ST >= ball_cooldown:
                bal = Ball(ball,350,250,ball_speed)
        if score1 >= win_requirement:
            finish = True
            text_win = font1.render("Player1 has won!",1,(255,255,0))
            window.blit(text_win,(200,155))
        elif score2 >= win_requirement:
            finish = True
            text_win = font1.render("Player2 has won!",1,(255,155,0))
            window.blit(text_win,(200,155))
        text_info = font1.render(str(score1)+" : "+str(score2),1,(0,0,0))
        window.blit(text_info,(320,0))
        display.update()
        clock.tick(FPS)