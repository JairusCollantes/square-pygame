import sys
import pygame
import random


W, H = 1280, 720

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("One square")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = W//2
        self.y = H//2
        self.side = 10
        self.speed = 3
        self.pawa = 1
        self.hp = 100
    def update(self):
        if keys[pygame.K_w] and self.y > 0:
            p.y -= p.speed
        if keys[pygame.K_s] and self.y < H - self.side:
            p.y += p.speed
        if keys[pygame.K_a] and self.x > 0:
            p.x -= p.speed
        if keys[pygame.K_d] and self.x < W - self.side:
            p.x += p.speed
        pygame.draw.rect(screen,(0,0,0),(int(self.x),int(self.y),self.side,self.side),0)

p = Player()

while True:
    screen.fill((29, 124, 29)) 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    p.update()
    pygame.display.flip()
    clock.tick(60)