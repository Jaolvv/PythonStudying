import pygame as pg
import pygame.freetype as freetype
import random
import os

directory = os.path.dirname(__file__)
image_evil = pg.image.load(os.path.join(directory, 'Image', 'ufo.png'))
image_player = pg.image.load(os.path.join(directory, 'Image', 'player.png'))
record_file = os.path.join(directory, 'Record', 'record.txt')
try:
    with open(record_file, 'x') as f:
        f.write(str(0))
except (BaseException, OSError):
    pass


class Menu():
    def __init__(self):

        self.font = freetype.SysFont('Consolas', 30)
        self.score, self.missed = 0, 0
        self.stop = True
        self.white = pg.Color('white')
        self.red = pg.Color('red')
        self.text1 = ''
        self.text2 = 'START'
        self.r1 = self.font.get_rect('GAME OVER', size=100)
        self.r2 = self.font.get_rect(self.text2)
        self.level_list = ['lov', 'high']

    def start(self):
        if self.stop:
            screen.blit(player.image, (
                (WIDTH - player.rect.w) // 2, HEIGHT - player.rect.h - 30))
            self.font.render_to(
                screen, (10, 10), f'score: {self.score}', fgcolor=self.white)
            self.font.render_to(
                screen, (10, 40), f'record: {rec[0]}', fgcolor=self.white)

            self.font.render_to(
                screen, ((WIDTH - self.r1.w) // 2, (HEIGHT - self.r1.h) // 2),
                self.text1, fgcolor=self.red, size=100)

            button = pg.draw.rect(
                screen, self.white, (WIDTH - 130, 10, 120, 40), border_radius=10)
            self.font.render_to(screen, (
                button.x + (button.w - self.r2.w) // 2,
                button.y + (button.h - self.r2.h) // 2),
                self.text2, fgcolor=self.red)

            button_level = pg.draw.rect(
                screen, self.red, ((WIDTH - 70) // 2, 10, 70, 30), border_radius=5)
            level = self.font.render_to(screen, (
                button_level.x + (10 if self.level_list[0] == 'lov' else 3),
                button_level.y + 3), self.level_list[0], fgcolor=self.white)

            all_sprites.empty()
            e = pg.event.get(pg.MOUSEBUTTONDOWN)
            if e and button.collidepoint(e[0].pos) and e[0].button == 1:
                self.text1 = 'GAME OVER'
                self.score, self.missed = 0, 0
                laser.position.xy = player.rect.center = WIDTH // 2, HEIGHT // 2
                laser.angle = player.angle = 0
                laser.velocity = vec(0, 0).rotate(laser.angle)
                laser.image = pg.transform.rotate(laser.orig_image, laser.angle)
                for _ in range(NUMBER_OF_STARS):
                    all_sprites.add(Stars())
                all_sprites.add(laser, player)
                for _ in range(10):
                    all_sprites.add(Evil())
                self.stop = False
            elif e and button_level.collidepoint(e[0].pos) and e[0].button == 1:
                self.level_list.reverse()
        else:
            self.font.render_to(screen, (10, 10), str(self.score), fgcolor=self.white)
            self.font.render_to(screen, (10, 40), str(self.missed), fgcolor=self.red)
            if self.score < self.missed:
                self.stop = True
                if self.score > rec[0]:
                    rec[0] = my_record()


class Stars(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.speed = random.randrange(5, 11, 5) * .1
        self.size = random.randint(1, 2)
        self.image = pg.Surface((self.size * 2, self.size * 2))
        pg.draw.circle(self.image, pg.Color(
            random.choice(COLOR)), [self.size, self.size], self.size)
        self.rect = self.image.get_rect()
        self.position = vec(random.randrange(WIDTH), random.randrange(HEIGHT))
        self.velocity = vec()
        self.angle = 0

    def update(self):
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        self.angle = (self.angle + .04) % 360
        self.velocity = vec(0, -self.speed).rotate(-self.angle)
        self.position += self.velocity
        self.rect.center = self.position


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = image_player
        self.angle = 0
        self.speed = 2
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
        elif keys[pg.K_UP]:
            self.rect.y -= self.speed
            if self.rect.top <= 0:
                self.rect.top = 0
        elif keys[pg.K_RIGHT]:
            self.angle -= 1
            if self.angle <= -30:
                self.angle = -30
            self.rect.x += self.speed
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        elif keys[pg.K_LEFT]:
            self.angle += 1
            if self.angle >= 30:
                self.angle = 30
            self.rect.x -= self.speed
            if self.rect.left <= 0:
                self.rect.left = 0

        self.image = pg.transform.rotate(image_player, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Laser(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((6, 40), pg.SRCALPHA)
        self.orig_image = self.image.copy()
        self.rect = self.image.get_rect()
        pg.draw.rect(
            self.orig_image, menu.red, self.rect,
            border_top_left_radius=10, border_top_right_radius=10,
            border_bottom_left_radius=5, border_bottom_right_radius=5)

        self.position = vec(player.rect.center)
        self.velocity = vec()
        self.speed = 10
        self.block = True
        self.collide = False
        self.angle = player.angle

    def update(self):
        if self.position.y < -self.rect.h // 2 or self.collide:
            self.position = player.rect.center
            self.angle = player.angle
            self.image = pg.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.position)
            self.collide = False

        self.velocity = vec(0, -self.speed).rotate(-self.angle)
        self.position += self.velocity
        self.rect.center = self.position


class Evil(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.transform.rotozoom(
            image_evil, random.randrange(-60, 61, 10), random.randint(4, 8) * 0.1)
        self.rect = self.image.get_rect(bottomright=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(1, 2)
        if menu.level_list[0] == 'lov':
            self.radius = self.rect.h // 2
        else:
            self.radius = self.rect.h // 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottomright = random.randint(0, WIDTH), 0
            self.speed = random.randint(1, 2)
            menu.missed += 1
        if pg.sprite.collide_circle(laser, self):
            self.rect.bottomright = random.randint(0, WIDTH), 0
            self.speed = random.randint(1, 2)
            menu.score += 1
            laser.collide = True


WIDTH, HEIGHT = 800, 600
NUMBER_OF_STARS = 100
BG_COLOR = (0, 0, 25)
COLOR = [
    'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4']
pg.init()
vec = pg.math.Vector2
screen = pg.display.set_mode((WIDTH, HEIGHT))
FPS = 120
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
menu = Menu()
player = Player()
laser = Laser()


def my_record():
    with open(record_file, 'r+') as f:
        record = f.read()
        if menu.score > int(record):
            record = str(menu.score)
            f.seek(0)
            f.truncate()
            f.write(record)
    return int(record)


rec = [my_record()]
while not pg.event.get(pg.QUIT):

    screen.fill(BG_COLOR)
    if not menu.stop:
        all_sprites.update()
        all_sprites.draw(screen)
    menu.start()

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Space   {round(clock.get_fps())}')
