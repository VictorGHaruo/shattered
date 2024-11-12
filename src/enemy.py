import pygame
from weapon import Projectile
import random

class Monsters:
    def __init__(self, x, y, width, height, hero):
        self.TAG = "Monster"
        self.sub_TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 50
        self.hero = hero
        self.immune = False
        self.projectiles = []   

    def move(self):
        pass

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)
    
    def new_hero(self, hero):
        self.hero = hero
        
    def draw (self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.color, self.rect)

    def on_collision(self, other : pygame.Rect):  

        if other.TAG == "Ground" and self.rect.colliderect(other) and self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                self.rect.bottom = other.rect.top
                
        if other.TAG == "Projectile":
            if self.rect.colliderect(other):       
                    self.life -= other.damage
        
        for projectile in self.projectiles:
            if other.TAG == "Ground":
                if projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    self.projectiles.remove(projectile)

class Dummy(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.speed_x = 3

    def on_collision(self, other):
        super().on_collision(other)
        if other.TAG == "Ground" and self.rect.colliderect(other):
            if self.rect.left < other.rect.right and self.rect.right > other.rect.right:
                self.speed_x *= -1
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                self.speed_x *= -1

    def update(self):
        self.move()
        return super().update()
        
    def move(self):
        self.rect.x = self.rect.x + self.speed_x
    

class Mage(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.width = width
        self.speed_x = 3
        self.color = (0,0, 255)
        self.life = 60
        self.projectile_cooldown = 0
        self.cool_down = 20   
    
    def update(self):
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()

        self.attack()
        return super().update()
    
    def on_collision(self, other: pygame.Rect):
        return super().on_collision(other)
    
    
    def draw(self, screen, camera):
        super().draw(screen, camera)
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            if self.hero.rect.x <= self.rect.x:
                new_projectile = Projectile(self.rect.left, self.rect.centery, - 20, 0, self.TAG, damage= 20)
                self.projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.right, self.rect.centery, 20, 0, self.TAG, damage= 20)
                self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down

class Flying(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.speed_x = 3
        self.gravity = 0

        self.probability = 0.5
        self.randomic = 0.5

        self.cool_down_max = 50
        self.cool_down_min = 20

        self.cool_down = 0
        self.move_cooldown = 0

        self.projectile_cooldown = 0

        self.color = (0, 255, 0)

    def move(self):
        if self.move_cooldown <= 0:
            
            self.randomic = random.random()
            self.cool_down = random.randint(self.cool_down_min, self.cool_down_max)       
            self.move_cooldown = self.cool_down
        
        if self.randomic >= self.probability:
            self.rect.x = self.rect.x + self.speed_x

        else:
            self.rect.x = self.rect.x - self.speed_x

    def on_collision(self, other):
        super().on_collision(other)

    def update(self):
        super().update()
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()
        self.move()
        self.attack()
    
    def draw(self, screen, camera):
        super().draw(screen, camera)
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            new_projectile = Projectile(self.rect.left, self.rect.bottom, self.speed_x, 30, self.TAG, damage= 20)
            self.projectiles.append(new_projectile)

            self.projectile_cooldown = self.cool_down
