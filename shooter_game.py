#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
#задай фон сцены

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_widht, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_widht, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx -5, self.rect.top, -15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y,player_speed,  win_width, win_height, is_asteroid = False):
        super().__init__(player_image, player_x, player_y, player_speed, win_width, win_height)
        self.is_asteroid = is_asteroid
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -50
            if not self.is_asteroid:
                lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 3), 80, 50)
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, randint(1, 5), 80, 50, True)
    asteroids.add(asteroid)

font.init()
font2 = font.SysFont('Arial', 30)
lost = 0
max_lost = 3
font = font.SysFont('Arial', 65)
lose = font.render( 'YOU LOSE!', True, (255, 215, 0))
score = 0
goal = 10
win = font.render( 'YOU WIN!', True, (255, 215, 0))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
FPS = 40
run = True
finish = False
life = 3
clock = time.Clock()
rocket = Player('rocket.png', 310, 400, 5, 80, 100)
num_fire = 0
rel_time =False


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key  == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire.play()
                    rocket .fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True  
    if not finish:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collide = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
            monsters.add(monster)
        for a in collide:
            asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, randint(1, 5), 80, 50, True)
            asteroids.add(asteroid)
        if sprite.spritecollide(rocket, asteroids, False) or sprite.spritecollide(rocket, monsters, False):
            sprite.spritecollide(rocket, asteroids, True)
            sprite.   spritecollide(rocket, monsters, True)
            life = life -1
        if life == 0:
            finish = True
            window.blit(lose, (200,200))
        if score >= goal:            
            finish = True
            window.blit(win, (200, 200))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,10))
        text_score = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10,40))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        lifes = font.render(str(life), 1, life_color)
        window.blit(lifes, (650,10))
    display.update()
    clock.tick(FPS)