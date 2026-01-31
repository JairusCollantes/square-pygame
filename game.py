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
        self.power = 1
        self.hp = 100
    def update(self):
        pygame.draw.rect(screen,black,self.square,0)

class Attack:
    def __init__(self,x,y):
        self.side = 5
        self.t = 120
        self.rect = pygame.Rect(x - self.side//2, y - self.side//2, 
                               self.side, self.side)
        
        if enemies:
            closest_enemy = None
            min_dist = float('inf')
            for enemy in enemies:
                dx = enemy.x - x
                dy = enemy.y - y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < min_dist:
                    min_dist = dist
                    closest_enemy = enemy
            
            if closest_enemy:
                dx = closest_enemy.x - x
                dy = closest_enemy.y - y
                dist = max(0.1, min_dist)
                self.x = (dx / dist) * 10
                self.y = (dy / dist) * 10
        else:
            angle = random.uniform(0, 2 * math.pi)
            self.x = math.cos(angle) * 10
            self.y = math.sin(angle) * 10
    def update(self):
        self.t -= 1
        if self.t > 0:
            self.rect.x += self.x
            self.rect.y += self.y
            if keys[pygame.K_w]:
                self.rect.y += speed
            if keys[pygame.K_s]:
                self.rect.y -= speed
            if keys[pygame.K_a]:
                self.rect.x += speed
            if keys[pygame.K_d]:
                self.rect.x -= speed
            pygame.draw.rect(screen,pink,self.rect,0)

class Enemy:
    def __init__(self):
        spawn_side = random.choice(["top","bottom", "right", "left"])
        if spawn_side == "top":
            self.x = random.randint(0,W)
            self.y = -20
        elif spawn_side == "bottom":
            self.x = random.randint(0,W)
            self.y = H + 20
        elif spawn_side == "left":
            self.y = random.randint(0,H)
            self.x = -20
        elif spawn_side == "right":
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

player = Player()
enemies = []
time = 0
bullets = []
game_running = True

def spawn_enemy():
    enemies.append(Enemy())
    
def spawn_bullet():
    bullets.append(Attack(player.x, player.y))

def collision():
    global game_running
    for enemy in enemies:
        closest_x = max(min(enemy.x ,player.square.right), player.square.left)
        closest_y = max(min(enemy.y ,player.square.bottom), player.square.top)
        distance_x = enemy.x - closest_x
        distance_y = enemy.y - closest_y
        distance = math.sqrt(distance_x*distance_x + distance_y*distance_y)
        if distance < enemy.radius:
            player.hp -= enemy.damage
            enemies.remove(enemy)
            if player.hp <= 0:
                game_running = False
        enemies_hit = []
        bullets_hit = []
        
        for bullet in bullets:
            for enemy in enemies:
                closest_x = max(bullet.rect.left, min(enemy.x, bullet.rect.right))
                closest_y = max(bullet.rect.top, min(enemy.y, bullet.rect.bottom))
                
                distance_x = enemy.x - closest_x
                distance_y = enemy.y - closest_y
                distance = math.sqrt(distance_x * distance_x + distance_y * distance_y)
            
                if distance < enemy.radius:
                    if enemy not in enemies_hit:
                        enemies_hit.append(enemy)
                    if bullet not in bullets_hit:
                        bullets_hit.append(bullet)
        
        for enemy in enemies_hit:
            if enemy in enemies:
                enemies.remove(enemy)
        
        for bullet in bullets_hit:
            if bullet in bullets:
                bullets.remove(bullet)

def ui():
    font = pygame.font.SysFont(None, 48)
    time_text = font.render(f"Time: {(time/60):.2f}", True, black)
    hp_text = font.render(f"HP: {player.hp}", True, black)
    screen.blit(time_text,(12,12))
    screen.blit(hp_text,(12,100))

while True:
    # screen.fill(green) 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and not game_running:
                player = Player()
                enemies.clear()
                time = 0
                bullets.clear()
                game_running = True
    if game_running:
        screen.fill(green) 
        keys = pygame.key.get_pressed()
        time += 1
        if time % 60 == 0:
            spawn_enemy()
        if time % 60==0:
            spawn_bullet()
        for enemy in enemies:
            enemy.move(player.x, player.y)
        for bullet in bullets:
            bullet.update()
        collision()

        ui()
        
        player.update()
        if not game_running:
            font = pygame.font.SysFont(None, 160)
            text = font.render(f"Game Over", True, white)
            screen.blit(text,(W//2 - 290,H//2-50))
    pygame.display.flip()
    clock.tick(60)