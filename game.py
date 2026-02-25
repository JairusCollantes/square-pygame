import sys
import pygame
import random
import math

W, H = 1280, 720
white = (255, 255, 255)
red = (255, 0, 0)
green = (29, 124, 29)
black = (0, 0, 0)
yellow = (255, 255, 0)
pink = (255, 87, 183)
speed = 3

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Square")
clock = pygame.time.Clock()

# ------------------- CLASSES -------------------

class Player:
    def __init__(self):
        self.x = W // 2
        self.y = H // 2
        self.side = 15
        self.square = pygame.Rect(self.x-7, self.y-7, self.side, self.side)
        self.hp = 100

    def update(self):
        pygame.draw.rect(screen, black, self.square, 0)


class Attack:
    def __init__(self, x, y):
        self.side = 5
        self.t = 120
        self.rect = pygame.Rect(x - self.side//2, y - self.side//2, self.side, self.side)
        if enemies:
            closest_enemy = min(enemies, key=lambda e: math.hypot(e.x-x, e.y-y))
            dx = closest_enemy.x - x
            dy = closest_enemy.y - y
            dist = max(0.1, math.hypot(dx, dy))
            self.vx = (dx / dist) * 10
            self.vy = (dy / dist) * 10
        else:
            angle = random.uniform(0, 2 * math.pi)
            self.vx = math.cos(angle) * 10
            self.vy = math.sin(angle) * 10

    def update(self):
        self.t -= 1
        if self.t <= 0:
            return False
        self.rect.x += self.vx
        self.rect.y += self.vy
        if keys[pygame.K_w]:
            self.rect.y += speed
        if keys[pygame.K_s]:
            self.rect.y -= speed
        if keys[pygame.K_a]:
            self.rect.x += speed
        if keys[pygame.K_d]:
            self.rect.x -= speed
        pygame.draw.rect(screen, pink, self.rect, 0)
        return True


class MeleeAttack:
    def __init__(self, x, y, direction="right"):
        self.duration = 60             # frames the swing last
        self.angle_step = 15            # degrees per frame
        self.current_angle = -45       # start angle relative to direction
        self.width = 10                # sword thickness
        self.length = 70               # sword reach
        self.x = x
        self.y = y
        self.direction = direction    

    def update(self):
        if self.duration <= 0:
            return False

        # Draw the rectangle as a rotated surface
        surf = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        surf.fill(yellow)
        rotated_surf = pygame.transform.rotate(surf, self.current_angle)
        rect = rotated_surf.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surf, rect.topleft)

        # Move the swing angle
        self.current_angle += self.angle_step
        self.duration -= 1

        sword_rect = pygame.Rect(self.x - self.length//2, self.y - self.width//2, self.length, self.width)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(
                enemy.x - enemy.radius,
                enemy.y - enemy.radius,
                enemy.radius * 2,
                enemy.radius * 2
            )

            if rect.colliderect(enemy_rect):
                enemies.remove(enemy)

        return True


class Enemy:
    def __init__(self):
        side = random.choice(["top","bottom","left","right"])
        if side == "top":
            self.x = random.randint(0, W); self.y = -20
        elif side == "bottom":
            self.x = random.randint(0, W); self.y = H + 20
        elif side == "left":
            self.y = random.randint(0, H); self.x = -20
        elif side == "right":
            self.y = random.randint(0, H); self.x = W + 20
        self.speed = 1
        self.radius = 7
        self.damage = 1

    def move(self, x, y):
        dx = x - self.x
        dy = y - self.y
        d = math.hypot(dx, dy)
        self.x += (dx/d) * self.speed
        self.y += (dy/d) * self.speed
        if keys[pygame.K_w]: self.y += speed
        if keys[pygame.K_s]: self.y -= speed
        if keys[pygame.K_a]: self.x += speed
        if keys[pygame.K_d]: self.x -= speed
        pygame.draw.circle(screen, red, (int(self.x), int(self.y)), self.radius)

# ------------------- GAME STATE -------------------

player = Player()
enemies = []
bullets = []
time = 0
game_running = True
weapon_type = None
selecting_weapon = True

# ------------------- FUNCTIONS -------------------

def spawn_enemy():
    enemies.append(Enemy())

def spawn_attack():
    if weapon_type == "range":
        bullets.append(Attack(player.x, player.y))
    elif weapon_type == "melee":
        bullets.append(MeleeAttack(player.x, player.y))

def collision():
    global game_running
    for enemy in enemies[:]:
        # Player collision
        closest_x = max(min(enemy.x, player.square.right), player.square.left)
        closest_y = max(min(enemy.y, player.square.bottom), player.square.top)
        if math.hypot(enemy.x - closest_x, enemy.y - closest_y) < enemy.radius:
            player.hp -= enemy.damage
            enemies.remove(enemy)
            if player.hp <= 0:
                game_running = False
    # Bullet/Enemy collision for ranged attacks
    for bullet in bullets[:]:
        if isinstance(bullet, Attack):
            for enemy in enemies[:]:
                closest_x = max(bullet.rect.left, min(enemy.x, bullet.rect.right))
                closest_y = max(bullet.rect.top, min(enemy.y, bullet.rect.bottom))
                if math.hypot(enemy.x - closest_x, enemy.y - closest_y) < enemy.radius:
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)

def ui():
    font = pygame.font.SysFont(None, 48)
    screen.blit(font.render(f"Time: {(time/60):.2f}", True, black), (12,12))
    screen.blit(font.render(f"HP: {player.hp}", True, black), (12,100))

# ------------------- MAIN LOOP -------------------

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if selecting_weapon and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1: weapon_type = "range"; selecting_weapon = False
            elif e.key == pygame.K_2: weapon_type = "melee"; selecting_weapon = False
        elif not selecting_weapon and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and not game_running:
                player = Player()
                enemies.clear()
                bullets.clear()
                time = 0
                game_running = True
                selecting_weapon = True

    keys = pygame.key.get_pressed()

    if selecting_weapon:
        screen.fill(blue := (0,0,255))
        font = pygame.font.SysFont(None, 64)
        screen.blit(font.render("Choose Your Weapon", True, white), (W//2 - 200, H//3))
        screen.blit(font.render("1. Range (Ranged Attack)", True, white), (W//2 - 180, H//2))
        screen.blit(font.render("2. Melee (Close Range)", True, white), (W//2 - 150, H//2 + 60))
        pygame.display.flip()
        clock.tick(60)
        continue

    if game_running:
        screen.fill(green)
        time += 1
        if time % 1 == 0:
            spawn_enemy()
        if time % 60 == 0:
            spawn_attack()

        for enemy in enemies:
            enemy.move(player.x, player.y)

        for bullet in bullets[:]:
            if not bullet.update():
                bullets.remove(bullet)

        collision()
        ui()
        player.update()
    else:
        screen.fill(green)
        font = pygame.font.SysFont(None, 160)
        screen.blit(font.render("Game Over", True, white), (W//2-290, H//2-50))

    pygame.display.flip()
    clock.tick(60)