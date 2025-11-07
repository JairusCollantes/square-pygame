import sys
import pygame
import random
import math


W, H = 1280, 720
white = (255, 255, 255)
red = (255, 0, 0)
green = (29, 124, 29)
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (255,255,0)
pink = (255,87,183)
speed = 3
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Square")
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = W//2
        self.y = H//2
        self.side = 15
        self.square = pygame.Rect(self.x-7,self.y-7,self.side,self.side)
        self.pawa = 1
        self.hp = 100
    def update(self):
        pygame.draw.rect(screen,black,self.square,0)


class Attack:
    def __init__(self,x,y):
        self.side = 5
        self.t = 90
        self.square = pygame.Rect(x,y,self.side,self.side)
        angle = random.randint(0,360)
        self.x = math.cos(angle) * 10
        self.y = math.sin(angle) * 10
    def update(self):
        self.t -= 1
        self.square.x += self.x
        self.square.y += self.y
        if keys[pygame.K_w]:
            self.square.y += speed
        if keys[pygame.K_s]:
            self.square.y -= speed
        if keys[pygame.K_a]:
            self.square.x += speed
        if keys[pygame.K_d]:
            self.square.x -= speed
        pygame.draw.rect(screen,pink,self.square,0)


class Enemy:
    def __init__(self):
        spawn = random.choice(["top","bot", "rig", "lef"])
        if spawn == "top":
            self.x = random.randint(0,W)
            self.y = -20
        elif spawn == "bot":
            self.x = random.randint(0,W)
            self.y = H + 20
        elif spawn == "lef":
            self.y = random.randint(0,H)
            self.x = -20
        elif spawn == "rig":
            self.y = random.randint(0,H)
            self.x = W + 20
        self.speed = 4
        self.radius = 7
    def move(self, x,y):
        dx = x - self.x
        dy = y - self.y
        d = math.sqrt(dx*dx + dy*dy)
        self.x += (dx/d) * self.speed
        self.y += (dy/d) * self.speed
        if keys[pygame.K_w]:
            self.y += speed
        if keys[pygame.K_s]:
            self.y -= speed
        if keys[pygame.K_a]:
            self.x += speed
        if keys[pygame.K_d]:
            self.x -= speed
        pygame.draw.circle(screen,red,(int(self.x),int(self.y)),self.radius)

p = Player()
c = []
t = 0
b = []

def spawn():
    c.append(Enemy())
    
def spawnB():
    b.append(Attack(p.x,p.y))
    
while True:
    screen.fill(green) 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    t += 1
    if t % 60==0:
        spawn()
    if t % 10==0:
        spawnB()
    for m in c:
        m.move(p.x,p.y)
    for m in b:
        m.update()
    
    # font = pygame.font.SysFont('times new roman', 12)
    # time = font.render(f"Time: {t//60}", True, black)
    # screen.blit(time,(12,12))
    p.update()
    pygame.display.flip()
    clock.tick(60)