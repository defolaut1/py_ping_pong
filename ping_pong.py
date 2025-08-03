from pygame import *

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))

display.set_caption('Ping pong')

back_color = (8, 222, 255)

class GameSprite(sprite.Sprite):
    def __init__(self, file_image, x, y, speed, width, height):
        super().__init__()
        
        self.image = transform.scale(
            image.load(file_image),
            (width, height)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        ny = self.rect.y
        if keys[K_w]:
            ny -= self.speed
        elif keys[K_s]:
            ny += self.speed
        
        self.cheeck_coord_y(ny)

    def update_r(self):
        keys = key.get_pressed()
        ny = self.rect.y
        if keys[K_UP]:
            ny -= self.speed
        elif keys[K_DOWN]:
            ny += self.speed
        
        self.cheeck_coord_y(ny)

    def cheeck_coord_y(self, ny):
        global win_height
        if 0 < ny < win_height - self.height:
            self.rect.y = ny

player_height = 150
player_speed = 10

player_l_x = 0
player_l = Player('line.png', player_l_x, 100, player_speed, 55, player_height)

player_r_x = win_width - 50
player_r = Player('line.png', player_r_x, 200, player_speed, 55, player_height)
ball = GameSprite('tennis.png', 200, 150, 10, 55, 55)

FPS = 60
timer = time.Clock()

game_flag = True
while game_flag:
    for e in event.get():
        if e.type == QUIT:
            game_flag = False

    player_r.update_r()
    player_l.update_l()

    window.fill(back_color)
    player_l.reset()
    player_r.reset()
    ball.reset()

    display.update()
    timer.tick(FPS)