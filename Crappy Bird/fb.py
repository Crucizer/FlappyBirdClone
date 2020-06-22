import pygame as pg
import random as rm
import time
pg.init()


class Flappy:
    # Clock Variables
    FPS = 30
    clock = pg.time.Clock()
    # Display Variables
    display_width = 350
    display_height = 350
    # Some Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    # Y-Axis Position of the Ball(Bird)
    pos_y = 50
    score = 0
    # Making The Screen
    dp = pg.display.set_mode(
        (display_width, display_height))
    pillar_width = 50
    pillar_height = rm.randint(75, 100)
    pillar2_height = rm.randint(75, 100)
    pillar_x = display_width + pillar_width

    def main(self):

        self.pillar_speed = 2  # 2
        self.pillar_min_height = 100
        self.pillar_max_height = 170

        pg.display.set_caption('Crappy Bird')
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            Flappy.dp.fill(Flappy.black)
            self.draw_ball()
            # Generating Random Pillars
            self.pillars(Flappy.pillar_x, 0,
                         Flappy.pillar_width, Flappy.pillar_height)
            self.pillars(Flappy.pillar_x, Flappy.display_height - Flappy.pillar2_height,
                         Flappy.pillar_width, Flappy.pillar2_height)
            Flappy.pillar_x -= self.pillar_speed
            if Flappy.pillar_x + Flappy.pillar_width < 0:
                Flappy.pillar_x = Flappy.display_width
                Flappy.pillar_height = rm.randint(40, 160)
                Flappy.pillar2_height = rm.randint(40, 160)
                Flappy.score += 1
                # A Function To Make Sure That The Distane Between The Pillars Is Neither Too High Nor Too Low
                while self.display_height - (Flappy.pillar2_height + Flappy.pillar_height) > 100 or self.display_height - (Flappy.pillar2_height + Flappy.pillar_height) < 60:
                    Flappy.pillar_height = rm.randint(20, 250)
                    Flappy.pillar2_height = rm.randint(20, 250)

            # Gravity
            self.gravity = 6
            Flappy.pos_y += self.gravity

            if Flappy.pos_y > Flappy.display_height - self.ball_size:
                Flappy.pos_y = Flappy.display_height - self.ball_size

            # Moving The Ball
            self.move_ball()
            self.collison()
            self.print_score()
            self.pause_thingy()

            # Updating Everything In Time
            Flappy.clock.tick(Flappy.FPS)
            pg.display.update()

    # Drawing The Ball
    def draw_ball(self):
        self.pos_x = 100
        self.ball_size = 10
        pg.draw.circle(Flappy.dp, Flappy.white, (self.pos_x,
                                                 Flappy.pos_y), self.ball_size, self.ball_size)

    # Moving The Ball
    def move_ball(self):
        self.keys = pg.key.get_pressed()
        self.ball_speed = 14
        if self.keys[pg.K_SPACE] and Flappy.pos_y > self.ball_size:
            Flappy.pos_y -= self.ball_speed
        if self.keys[pg.K_DOWN] and Flappy.pos_y < Flappy.display_height - self.ball_size:
            Flappy.pos_y += self.ball_speed - 2

    # Function To Draw The Pillar
    def pillars(self, x, y, width, height):
        pillar = pg.draw.rect(Flappy.dp, Flappy.white, (x, y, width, height))

    # Function To Check For Collison Between Pillar And Bird
    def collison(self):
        if Flappy.pos_y - self.ball_size - 2 < Flappy.pillar_height and self.pos_x + self.ball_size > Flappy.pillar_x and Flappy.pillar_x + Flappy.pillar_width > self.pos_x + self.ball_size:
            self.instance = Over()
            self.instance.main_thing(Flappy.dp)

        if self.pos_x + self.ball_size > Flappy.pillar_x and Flappy.pillar_x + Flappy.pillar_width > self.pos_x and Flappy.pos_y + self.ball_size + 2 > Flappy.display_height - Flappy.pillar2_height:
            self.instance1 = Over()
            self.instance1.main_thing(Flappy.dp)

    # Printing The Score On The Screen
    def print_score(self):
        self.font = pg.font.Font(None, 20)
        self.text = f'Score:{Flappy.score}'
        self.score_render = self.font.render(self.text, 1, Flappy.white)
        Flappy.dp.blit(self.score_render, (10, 10))

    def pause_thingy(self):
        if self.keys[pg.K_p]:
            pause_dat = Pause(self.dp)
            pause_dat()


# When You Collide This Shows Up
class Over(Flappy):
    def main_thing(self, surface):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            surface.fill(Flappy.black)
            self.print_stuff(40, 'Game Over!', Flappy.white, surface, 90, 110)
            self.print_stuff(
                40, f'Score: {Flappy.score}', Flappy.white, surface, 120, 140)
            self.click_button(surface)
            Flappy.clock.tick(Flappy.FPS)
            pg.display.update()

    # To Print Stuff On Screen

    def print_stuff(self, Font_Size, text, color, surface, x, y):
        self.font = pg.font.Font(None, Font_Size)
        self.text = text
        self.text_render = self.font.render(self.text, 1, color)
        surface.blit(self.text_render, (x, y))

    def draw_button(self, surface, x, y, color, width, height):
        button = pg.draw.rect(surface, color, (x, y, width, height))

    def click_button(self, surface):
        self.btn_x = 110
        self.btn_y = 175
        self.btn_width = 140
        self.btn_height = 40

        # Play again button
        self.click = pg.mouse.get_pressed()
        self.mouse = pg.mouse.get_pos()
        self.mouse_x = self.mouse[0]
        self.mouse_y = self.mouse[1]
        # Making The Button
        self.draw_button(surface, self.btn_x, self.btn_y, Flappy.white,
                         self.btn_width, self.btn_height)
        self.print_stuff(30, 'Play Again', Flappy.black,
                         surface, self.btn_x + 12, self.btn_y + 12)
        # Checking If The Mouse Is Hovering Over The Button And If Clicks Then Redirect it to the Game
        if self.btn_x + self.btn_width > self.mouse_x > self.btn_x:
            if self.btn_y + self.btn_width > self.mouse_y > self.btn_y:
                if self.click[0] == 1:
                    Flappy.score = 0
                    Flappy.pillar_x = Flappy.display_width + Flappy.pillar_width
                    Flappy.pos_y = 30
                    crappy = Flappy()
                    crappy.main()


# Intro Of The Game
class Intro(Over):
    def the_intro(self, surface):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            surface.fill(Flappy.black)
            Over.print_stuff(self, 40, 'Crappy Bird',
                             Flappy.white, surface, 90, 60)
            self.btns(surface)
            Flappy.clock.tick(Flappy.FPS)
            pg.display.update()

    def btns(self, surface):
        self.btn_x = 110
        self.btn2_x = 110
        self.btn_y = 125
        self.btn2_y = 215
        self.btn_width = 140
        self.btn_height = 50
        self.action = None

        # Play again button
        self.click = pg.mouse.get_pressed()
        self.mouse = pg.mouse.get_pos()
        self.mouse_x = self.mouse[0]
        self.mouse_y = self.mouse[1]
        # Making The Play Button
        self.draw_button(surface, self.btn_x, self.btn_y, Flappy.green,
                         self.btn_width, self.btn_height)
        self.draw_button(surface, self.btn2_x, self.btn2_y,
                         Flappy.red, self.btn_width, self.btn_height)
        self.print_stuff(50, 'Play', Flappy.black,
                         surface, self.btn_x + self.btn_width/2 - 37, self.btn_y + 7)
        self.print_stuff(50, 'Quit', Flappy.black, surface,
                         self.btn2_x + self.btn_width/2 - 37, self.btn2_y + 7)
        # Checking If The Mouse Is Hovering Over The Button And If Clicks Then Redirect it to the Game
        if self.btn_x + self.btn_width > self.mouse_x > self.btn_x:
            if self.btn_y + self.btn_width > self.mouse_y > self.btn_y:
                if self.click[0] == 1:
                    self.action = "play"

        if self.btn2_x + self.btn_width > self.mouse_x > self.btn2_x:
            if self.btn2_y + self.btn_width > self.mouse_y > self.btn2_y:
                if self.click[0] == 1:
                    self.action = 'quit'

        if self.action == 'play':
            Flappy.score = 0
            crappy = Flappy()
            crappy.main()
        if self.action == 'quit':
            pg.quit()
            quit()


class Pause(Intro):
    def __init__(self, surface):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            surface.fill(Flappy.black)
            self.pause_it(surface)
            Flappy.clock.tick(Flappy.FPS)
            pg.display.update()

    def pause_it(self, surface):
        surface.fill(Flappy.black)
        Over.print_stuff(self, 70, 'Paused', Flappy.white, surface, 90, 120)
        Over.print_stuff(self, 30, 'Press R To Resume',
                         Flappy.white, surface, 90, 180)
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_r]:
            crappy.main()


# Running The Intro
crappy = Flappy()
thing = Intro()
thing.the_intro(crappy.dp)
