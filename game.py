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
pygame.init()
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
        self.t = 60
        self.square = pygame.Rect(x,y,self.side,self.side)
        angle = random.randint(0,360)
        self.x = math.cos(angle) * 10
        self.y = math.sin(angle) * 10
    def update(self):
        self.t -= 1
        if self.t > 0:
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
        self.speed = 1
        self.radius = 7
        self.damage = 1
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
game = True

def spawn():
    c.append(Enemy())
    
def spawnB():
    b.append(Attack(p.x,p.y))

def collision():
    global game
    for m in c:
        cx = max(min(m.x ,p.square.right), p.square.left)
        cy = max(min(m.y ,p.square.bottom), p.square.top)
        dx = m.x - cx
        dy = m.y - cy
        d = math.sqrt(dx*dx + dy*dy)
        if d < m.radius:
            p.hp -= m.damage
            c.remove(m)
            if p.hp <= 0:
                game = False

def ui():
    font = pygame.font.SysFont(None, 48)
    time = font.render(f"Time: {(t/60):.2f}", True, black)
    hp = font.render(f"HP: {p.hp}", True, black)
    screen.blit(time,(12,12))
    screen.blit(hp,(12,100))

while True:
    # screen.fill(green) 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and not game:
                p = Player()
                c.clear()
                t = 0
                b.clear()
                game = True
    if game:
        screen.fill(green) 
        keys = pygame.key.get_pressed()
        t += 1
        if t % 1 == 0:
            spawn()
        if t % 60==0:
            spawnB()
        for m in c:
            m.move(p.x,p.y)
        for m in b:
            m.update()
        collision()

        ui()
        
        p.update()
        if not game:
            font = pygame.font.SysFont(None, 160)
            text = font.render(f"Game Over", True, white)
            screen.blit(text,(W//2 - 290,H//2-50))
    pygame.display.flip()
    clock.tick(60)