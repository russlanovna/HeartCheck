from pygame import *
font.init()
window = display.set_mode((1100, 1100))
display.set_caption('Лабиринт')
picture = transform.scale(image.load('galaxy_2.jpg'), (1100, 1100))
win = font.SysFont('Arial', 60).render('You Win!!!', True, (100, 80, 250))
lose = font.SysFont('Arial', 60).render('You Lose!!!', True, (100, 80, 250))
surf = Surface((1100, 1100))

class GameSprite(sprite.Sprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.clamp_ip(surf.get_rect())
class Player(GameSprite):
    def __init__(self, pic, x, y, w, h, speed = 0):
      super().__init__(pic, x, y, w, h)
      self.speed_x = speed
      self.speed_y = speed
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        walls_touch = sprite.spritecollide(self, walls, False)
        for w in walls_touch:
            if self.speed_x > 0:
                self.rect.right = min(self.rect.right, w.rect.left)
            elif self.speed_x < 0:
                self.rect.right = max(self.rect.left, w.rect.right)
            elif self.speed_y > 0:
                self.rect.bottom = min(self.rect.bottom, w.rect.top)
            elif self.speed_y < 0:
                self.rect.top = max(self.rect.top, w.rect.bottom)
    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.right,self.rect.centery, 25, 17))
class Enemy(GameSprite):
    def __init__(self, pic, x, y, w, h, x1, x2, speed=10):
        super(). __init__(pic, x, y, w, h)
        self.direction = 'left'
        self.speed = speed
        self.x1 = x1
        self.x2 = x2
    def update(self):
        if self.rect.x >= self.x1:
            self.direction = 'left'
        elif self.rect.x <= self.x2:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, pic, x, y, w, h, speed=20):
        super().__init__(pic, x, y, w, h)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 1100:
            self.kill()
character = Player('1-2.png', 50, 380, 60, 70)
enemies = sprite.Group()
enemies.add(Enemy('pac-6.png', 700, 150, 60, 70, 700, 500))
final = GameSprite('pac-1.png', 620, 350, 50, 60)
walls = sprite.Group()
bullets = sprite.Group()
walls.add(GameSprite('wall1.jpg', 50, 450, 150, 50))
walls.add(GameSprite('wall2.jpg', 200, 350, 50, 150))
walls.add(GameSprite('wall2.jpg', 200, 350, 130, 50))
walls.add(GameSprite('wall1.jpg', 330, 250, 50, 150))
walls.add(GameSprite('wall2.jpg', 330, 200, 150, 50))
walls.add(GameSprite('wall2.jpg', 430, 250, 50, 200))
walls.add(GameSprite('wall2.jpg', 430, 400, 160, 50))
run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                character.speed_y = -10
            elif e.key == K_s:
                character.speed_y = 10
            elif e.key == K_a:
                character.speed_x = -10
            elif e.key == K_d:
                character.speed_x = 10
            elif e.key == K_SPACE:
                character.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                character.speed_y = 0
            elif e.key == K_s:
                character.speed_y = 0
            elif e.key == K_a:
                character.speed_x = -0
            elif e.key == K_d:
                character.speed_x = 0
    if not finish:
        window.blit(picture, (0, 0))
        character.reset()
        character.update()
        enemies.draw(window)
        enemies.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        walls.draw(window)
        
    if sprite.collide_rect(character, final):
        finish = True
        window.blit(win, (450,300))
    elif sprite.spritecollide(character, enemies, False):
        finish = True
        window.blit(lose, (450, 300))
    
    sprite.groupcollide(bullets, walls, True, False)
    sprite.groupcollide(bullets, enemies, True, True)
    display.update()


