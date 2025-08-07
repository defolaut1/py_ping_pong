from pygame import *

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))

display.set_caption('Ping pong')

back_color = (8, 222, 255)

keys = {}

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
        global keys

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

class Ball(GameSprite):
    def __init__(self, file_image, x, y, speed, width, height):
        super().__init__(file_image, x, y, speed, width, height)

        self.bounce = 0
        self.speed_x = speed
        self.speed_y = speed

    def init_speed(self):
        self.bounce = 0
        self.speed_x = self.speed - 1
        self.speed_y = self.speed - 1

        global win_height, win_width
        self.rect.x = win_width // 3
        self.rect.y = win_height // 2

    def update(self):
        if self.bounce >= 2:
            self.bounce = 0
            self.speed_x += 1
            self.speed_y += 1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        global win_height
        if self.rect.y <= 0 or self.rect.y >= win_height - self.height:
            self.speed_y *= -1

player_width, player_height = 15, 130
player_speed = 10

player_l_x = 10
player_l = Player('line.png', player_l_x, 100, player_speed, player_width, player_height)

player_r_x = win_width - 20
player_r = Player('line.png', player_r_x, 200, player_speed, player_width, player_height)

ball_speed = 4
ball = Ball('tennis.png', 200, 150, ball_speed, 55, 55)

font.init()
my_font = font.SysFont("Arial", 35)
font_color = (180, 0, 0)

text_player_coord = (win_width // 3, win_height // 3)
win_l_text = my_font.render('Left player WIN!', True, font_color)
win_r_text = my_font.render('Right player WIN!', True, font_color)

text_repeat_coord = (text_player_coord[0], text_player_coord[1] + 35)
repeat_text = my_font.render('Repeat? (y/n)', True, font_color)

FPS = 60
timer = time.Clock()

game_flag = True
on_play_flag = True
left_win_flag = False
while game_flag:
    keys = key.get_pressed()

    for e in event.get():
        if e.type == QUIT:
            game_flag = False

    if on_play_flag:
        player_r.update_r()
        player_l.update_l()
        ball.update()

        if sprite.collide_rect(player_l, ball) or sprite.collide_rect(player_r, ball):
            ball.bounce += 1
            ball.speed_x *= -1
            ball.rect.x += ball.speed_x * 3

        if ball.rect.x <= 0 or ball.rect.x >= win_width - ball.width:
            on_play_flag = False

        window.fill(back_color)
        player_l.reset()
        player_r.reset()
        ball.reset()
    else:
        window.blit(win_l_text if ball.rect.x > 0 else win_r_text, text_player_coord)
        window.blit(repeat_text, text_repeat_coord)

        if keys[K_y]:
            on_play_flag = True
            ball.init_speed()
        if keys[K_n]:
            game_flag = False

    display.update()
    timer.tick(FPS)
