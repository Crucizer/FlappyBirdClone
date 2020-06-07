# importing stuff
import pygame as pg
import random
import os
import time
# Tilt
# Intializing Pygame
pg.init()

# Loading Images
CURRENT_PATH = os.path.dirname(__file__)
BIRD_IMGS = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), pg.transform.scale2x(
    pg.image.load(os.path.join("imgs", "bird2.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pg.transform.scale2x(
    pg.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pg.transform.scale2x(
    pg.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pg.transform.scale2x(
    pg.image.load(os.path.join("imgs", "base.png")))

# Display Variables
DISPLAY_WIDTH = 390
DISPLAY_HEIGHT = 636
DISPLAY = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption('Flappy Bird')

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock Variables
CLOCK = pg.time.Clock()
FPS = 30

Action = "first"
bass_action = "move"
Score = 0


class Bird:
    # Bird Variables
    bird_x = 100
    bird_y = 300
    bird_tilt = 0
    bird_width, bird_height = BIRD_IMGS[0].get_size()
    # Bird Image Number Variable
    image_no = 0
    # Bird Rotation Variable
    ROT_VEL = 20
    MAX_ROT = 25
    birdi = BIRD_IMGS[image_no]
    frame = 0

    gravity = 0

    def main(self):
        # Displaying The Images
        # print(Bird.bird_tilt)
        self.bird = pg.transform.rotate(
            BIRD_IMGS[Bird.image_no], Bird.bird_tilt)
        DISPLAY.blit(BG_IMG, (0, 0))
        DISPLAY.blit(self.bird, (Bird.bird_x, Bird.bird_y))

        # Other Functions
        self.move_bird()
        # self.tilt_bird()
        self.wings()
        print_stuff(40, str(Score), WHITE, DISPLAY, 10, 10)

        # Gravity Thingy
        Bird.bird_y += Bird.gravity

    def move_bird(self):
        global Action
        self.bird_speed = 22
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_SPACE]:
            if Action == 'first':
                Bird.bird_y -= self.bird_speed
                Pipe.vel = 8
                Bird.gravity = 8
            else:
                Bird.bird_y -= self.bird_speed
                Action = 'Not First'

        if Bird.bird_y > DISPLAY_HEIGHT - Base.base_height - 70:
            Bird.bird_y = DISPLAY_HEIGHT - Base.base_height - 70

        if Bird.bird_y < 0:
            Bird.bird_y = 0

    def wings(self):
        if self.frame % 5 == 0:
            if Bird.image_no == 2:
                Bird.image_no = 0
            else:
                Bird.image_no += 1
        if self.frame == 30:
            self.frame = 0

        self.frame += 1


class Base:
    # Base Variables
    base_length, base_height = BASE_IMG.get_size()
    base_x = 0
    base_y = 548
    base2_x = -base_length - 10

    def main(self):

        # Displaying Base
        DISPLAY.blit(BASE_IMG, (Base.base_x, Base.base_y))
        DISPLAY.blit(BASE_IMG, (Base.base2_x, Base.base_y))

        # Other Functions
        print(bass_action)
        if bass_action == "move":
            self.move()

    def move(self):
        # Base Velocity
        self.base_v = 8
        Base.base_x -= self.base_v
        Base.base2_x -= self.base_v

        if Base.base_x < -Base.base_length:
            Base.base_x = DISPLAY_WIDTH - 10

        if Base.base2_x < -Base.base_length:
            Base.base2_x = DISPLAY_WIDTH - 10

        if Score > 10:
            if Pipe.GAP > 80:
                self.base_v += 2


class Pipe:
    pipe_width, pipe_height = PIPE_IMG.get_size()
    pipe_y = -pipe_height + 100
    pipe2_y = 300
    pipe_x = DISPLAY_WIDTH + pipe_width + 1000
    vel = 0
    GAP = 150

    def main(self):
        self.top_pipe = pg.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG
        DISPLAY.blit(self.bottom_pipe, (Pipe.pipe_x, Pipe.pipe2_y))
        DISPLAY.blit(self.top_pipe, (Pipe.pipe_x, Pipe.pipe_y))

        # Other Functions
        self.move()
        self.collide()
        self.levels()

    def move(self):
        global Score
        Pipe.pipe_x -= Pipe.vel

        if Pipe.pipe_x < -Pipe.pipe_width:
            random_no = random.randrange(50, 350)
            Pipe.pipe_x = DISPLAY_WIDTH + Pipe.pipe_width
            Pipe.pipe_y = -Pipe.pipe_height + random_no
            Pipe.pipe2_y = random_no + Pipe.GAP
            Score += 1

    def collide(self):
        bird_mask = pg.mask.from_surface(Bird.birdi)
        top_mask = pg.mask.from_surface(self.top_pipe)
        bottom_mask = pg.mask.from_surface(self.bottom_pipe)

        top_offset = (self.pipe_x - Bird.bird_x+10,
                      self.pipe_y - (Bird.bird_y+12))
        bottom_offset = (self.pipe_x - Bird.bird_x + 10,
                         self.pipe2_y - (Bird.bird_y-8))

        # If Doesn't Overlap Returns None, If Collides Returns The Point Of Collide
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            game_over = Over()
            game_over.main()

    def levels(self):
        if Score > 10:
            if Pipe.GAP > 80:
                Pipe.GAP -= 10
                Pipe.vel += 2


class Over():
    def main(self):
        global bass_action
        self.start_time = time.time()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            # DISPLAY.fill(BLACK)
            # DISPLAY.blit(BG_IMG, (0, 0))
            self.restart()
            print_stuff(68, 'Game Over!', WHITE, DISPLAY, 10, 90)
            print_stuff(25, 'Press Space To Play Again',
                        WHITE, DISPLAY, 30, 170)
            print_stuff(73, f'Score: {Score}', WHITE, DISPLAY, 30, 290)
            bass_action = "don't move"
            bass.main()
            CLOCK.tick(FPS)
            pg.display.update()

    def restart(self):
        global Score
        global bass_action
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.end_time = time.time()
            sec = self.end_time - self.start_time
            if sec >= 0.8:
                Bird.bird_y = 300
                Pipe.pipe_x = DISPLAY_WIDTH + Pipe.pipe_width + 1000
                Score = 0
                bass_action = "move"
                main()


# Making Class Instances
birdy = Bird()
bass = Base()
pipei = Pipe()


def print_stuff(Font_Size, text, color, surface, x, y):
    font = pg.font.Font('font/flappy.ttf', Font_Size)
    text = text
    text_render = font.render(text, 1, color)
    surface.blit(text_render, (x, y))


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        DISPLAY.fill(BLACK)
        birdy.main()
        pipei.main()
        bass.main()
        # Updating Everything In Time
        CLOCK.tick(FPS)
        pg.display.update()


main()
