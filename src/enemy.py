import pygame
from weapon import Projectile

class Monsters:
    def __init__(self, x, y, width, height):
        self.TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 50

    def on_key_pressed(self, key_map):
        if key_map[pygame.K_RIGHT]:
            self.rect.x += 10
        if key_map[pygame.K_LEFT]:
            self.rect.x -= 10

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)
        
    def draw (self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.color, self.rect)

    def on_collision(self, other : pygame.Rect):  

        if other.TAG == "Ground":
            if self.rect.left < other.rect.right and self.rect.right > other.rect.right:
                self.speed_x *= -1
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                self.speed_x *= -1
            if self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                    self.rect.bottom = other.rect.top

        if other.TAG == "Player": #Mata o monstro
            if self.rect.top < other.rect.bottom and self.rect.bottom > other.rect.bottom:
                self.life = 0
        if isinstance(other, Projectile):
            if self.rect.left < other.rect.right and self.rect.right > other.rect.right: 
                if not other.who == "Monster":             
                    self.life -= 40
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                if not other.who == "Monster":   
                    self.life -= 40

class Dummy(Monsters):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed_x = 3

    def update(self):
        self.move()
        return super().update()
        
    def move(self):
        self.rect.x = self.rect.x + self.speed_x

class Flying(Monsters):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.width = width
        self.speed_x = 3
        self.color = (0,0, 255)
        self.life = 40
        self.projectile_cooldown = 0
        self.cool_down = 20      
    
    def update(self):
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1
        return super().update()
    
    def attack(self, projectiles, x_player):
        if self.projectile_cooldown <= 0:
            if x_player <= self.rect.x:
                new_projectile = Projectile(self.rect.left, self.rect.y - self.width/2, - 20, 0, self.TAG)
                projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.right, self.rect.y - self.width/2, 20, 0, self.TAG)
                projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down