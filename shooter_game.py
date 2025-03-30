from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('стреляние по врагам')

background = transform.scale(image.load('galaxy.jpg'),(700,500))
width = 700
height = 500

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def go(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width - 60:
            self.rect.x += self.speed
    def attack(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80) 
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


hero = Player('rocket.png', 10, height - 100, 40, 80, 10)
monsters = sprite.Group()
for i in range(1, 8):
    monster =Enemy('ufo.png', randint(80, width - 80), -20, 50, 40, randint(1, 4))
    monsters.add(monster)

FPS = 60
clock = time.Clock()
game = True
finish = False

font.init()
font1 = font.SysFont('Arial', 30)

font2 = font.SysFont('Arial', 60)

win = font2.render('ты подебил!', True, (234, 141, 228))
lose = font2.render('ты проиграл, лох!', True, (142, 151, 52))
bullets = sprite.Group()

max_enemy = 50
max_collide = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                hero.attack()
    if not finish:
        window.blit(background,(0,0))
        text_score = font1.render('счёт:' + str(score), True, (123,198,255))
        window.blit(text_score, (10,20))

        text_lost = font1.render('пропущено:' + str(lost), True, (141,141,141))
        window.blit(text_lost, (10,90))

        bullets.draw(window)
        hero.reset()
        monsters.draw(window)

        hero.go()
        monsters.update()
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, width - 80), -20, 50, 40, randint(1,4))
            monsters.add(monster)
        
        if sprite.spritecollide(hero, monsters, False) or lost >= 5:
            finish = True
            window.blit(lose, (200,200))
        
        if score >= max_enemy:
            finish = True
            window.blit(win, (200,200))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, width - 80), -20, 50, 40, randint(1, 4))
            monsters.add(monster)


    clock.tick(FPS)


