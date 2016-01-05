"""Pong game. Made by Michael Khimich."""

import os
import pygame
import random


class Player(object):

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], pos[2], pos[3])

    def move(self, dy):
        if dy != 0:
            self.move_single_axis(dy)

    def move_single_axis(self, dy):
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Moving down; Hit the top side of the wall
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                # Moving up; Hit the bottom side of the wall
                if dy < 0:
                    self.rect.top = wall.rect.bottom


class Ball(object):

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], pos[2], pos[3])

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_to_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], pos[2], pos[3])


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 150, 150, 150
RED = 180, 0, 0

screen_size = width, height = 640, 480
screen = pygame.display.set_mode(screen_size)
screen_caption = pygame.display.set_caption('SenyaPong')

ball = Ball((height * 0.5, width * 0.5, 10, 10))
speed = [6, 6]
x_dir = speed[0]
y_dir = speed[1]
ball.move(x_dir, y_dir)

leftScore = 0
leftPlayer = Player((int(width * 0.02), int(height * 0.5), int(width * 0.02), int(height * 0.15)))

rightScore = 0
rightPlayer = Player((int(width * 0.96 - 5), int(height * 0.5), int(width * 0.02), int(height * 0.15)))

walls = []

topWall = Wall((0, 0, width, 10))
bottomWall = Wall((0, height - 10, width, 10))
leftWall = Wall((0, 10, 5, height - 20))
rightWall = Wall((width - 5, 10, 5, height - 20))

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(30)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        rightPlayer.move(-10)
    if key[pygame.K_DOWN]:
        rightPlayer.move(10)
    if key[pygame.K_w]:
        leftPlayer.move(-10)
    if key[pygame.K_s]:
        leftPlayer.move(10)

    # DRAW SCENE
    screen.fill(BLACK)
    pygame.draw.line(screen, (GREY), [width * 0.5, 0], [width * 0.5, height - 1], 5)
    pygame.draw.rect(screen, (WHITE), topWall)
    pygame.draw.rect(screen, (WHITE), bottomWall)

    r_score = pygame.font.Font(None, 48).render(str(rightScore), 1, (WHITE))
    screen.blit(r_score, (width * 0.5 + 50, 50))
    l_score = pygame.font.Font(None, 48).render(str(leftScore), 1, (WHITE))
    screen.blit(l_score, (width * 0.5 - 70, 50))

    if ball.rect.colliderect(rightWall):
        pygame.draw.rect(screen, (RED), rightWall)
        rightScore += 1
        ball.move_to_position(width * 0.5, height * random.random())
        ball.move(random.choice([-5, 5]), random.choice([-5, 5]))
    elif ball.rect.colliderect(leftWall):
        pygame.draw.rect(screen, (RED), leftWall)
        leftScore += 1
        ball.move_to_position(width * 0.5, height * random.random())
        ball.move(random.choice([-5, 5]), random.choice([-5, 5]))
    else:
        pygame.draw.rect(screen, (GREY), leftWall)
        pygame.draw.rect(screen, (GREY), rightWall)

        if ball.rect.colliderect(topWall) or ball.rect.colliderect(bottomWall):
            y_dir = - y_dir
        elif ball.rect.colliderect(leftPlayer) or ball.rect.colliderect(rightPlayer):
            x_dir = - x_dir
        ball.move(x_dir, y_dir)

    pygame.draw.rect(screen, (WHITE), ball.rect)

    pygame.draw.rect(screen, (WHITE), leftPlayer.rect)
    pygame.draw.rect(screen, (WHITE), rightPlayer.rect)

    pygame.display.flip()
