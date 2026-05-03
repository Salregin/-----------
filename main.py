from pygame import *
font.init()
mixer.init()
font1 = font.Font(None, 100)

ping = mixer.Sound("ping.mp3")
win = mixer.Sound("win.mp3")

bg = transform.scale(image.load("фон.jpg"),(700,500))
ball = transform.scale(image.load("мячик.jpg"),(50,50))
player1sprite = Surface((30,150))
player2sprite = Surface((30,150))
player1sprite.fill((0,255,255))
player2sprite.fill((255,153,51))

game = True
finish = False
window = display.set_mode((700,500))
display.set_caption("пинги понги")
display.set_icon(ball)

clock = time.Clock()
FPS = 60

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
    def move(self):
        keuys = key.get_pressed()
        if keuys[K_w] and self.rect.y > 15:
            self.rect.y -= self.speed
        elif keuys[K_s] and self.rect.y < 340:
            self.rect.y += self.speed

class Player2(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
    def move(self):
        keuys = key.get_pressed()
        if keuys[K_UP] and self.rect.y > 15:
            self.rect.y -= self.speed
        elif keuys[K_DOWN] and self.rect.y < 340:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        self.Xdir = "Left"
        self.Ydir = "Down"
    def move(self):
        if self.Xdir == "Left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.Ydir == "Down":
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        if self.rect.y > 430:
            ping.play()
            self.Ydir = "Up"
        elif self.rect.y < 15:
            ping.play()
            self.Ydir = "Down"

plr1 = Player1(player1sprite,5,250,5)
plr2 = Player2(player2sprite,660,250,5)
bal = Ball(ball,350,250,7)

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    if finish == False:
        window.blit(bg,(0,0))
        bal.reset()
        plr1.reset()
        plr2.reset()
        plr1.move()
        plr2.move()
        bal.move()
        if sprite.collide_rect(plr1,bal):
            ping.play()
            bal.Xdir = "Right"
            bal.speed += 1
        elif sprite.collide_rect(plr2,bal):
            ping.play()
            bal.Xdir = "Left"
        if bal.rect.x < -15:
            text_win = font1.render("Player2 won!",1,(255,150,0))
            window.blit(text_win,(150,200))
            win.play()
            finish = True
        elif bal.rect.x > 700:
            text_win = font1.render("Player1 won!",1,(255,200,0))
            window.blit(text_win,(150,200))
            win.play()
            finish = True
        display.update()
        clock.tick(FPS)
        