import sys
import pygame
import random


W, H = 1280, 720

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("dino with patterns")
clock = pygame.time.Clock()

x = 200
y = 200
g = 10
ax = 400
ay = 400

width = 20
height = 20
j = True
aj = True
vel = 10
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if y < H-20:
        y += g
        j = False
    if ay < H-20:
        ay += g
        aj = False
    if y == H-20:
        j = True
    if ay == H-20:
        aj = True

    if keys[pygame.K_a] and x > 0:
        x -= vel
    if keys[pygame.K_d] and x < W - width:
        x += vel
    if keys[pygame.K_w] and y > 0 and j:
        y -= 100
        j = False
    
    if keys[pygame.K_LEFT] and ax > 0:
        ax -= vel
    if keys[pygame.K_RIGHT] and ax < W - width:
        ax += vel
    
    if keys[pygame.K_UP] and ay > 0 and aj:
        ay -= 100
        aj = False


    screen.fill((0, 0, 0)) 
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(screen, (255, 0, 0), (ax, ay, width, height))
    pygame.display.update()
    clock.tick(60)