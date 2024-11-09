import pygame
from weapon import Projectile
import random
import math

class Bosses:
    def __init__(self, x, y, width, height, hero):
        self.TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 50
        self.hero = hero
        self.projectiles = []

    def move(self):
        pass

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)

        for projectile in self.projectiles:
            projectile.update()
        
    def draw (self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.color, self.rect)

    def on_collision(self, other : pygame.Rect):  

        if other.TAG == "Ground" and self.rect.colliderect(other) and self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                self.rect.bottom = other.rect.top

        if other.TAG == "Monster" :
            if self.rect.left < other.rect.right and self.rect.right > other.rect.right: 
                if not other.who == "Monster":             
                    self.life -= other.damage
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                if not other.who == "Monster":   
                    self.life -= other.damage
        for projectile in self.projectiles:
            if other.TAG == "Ground":
                if projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    self.projectiles.remove(projectile)

class Balrog(Bosses):
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

        self.cooldown_atk = 40


        self.color = (255, 192, 203)

    def move(self):
        
        if self.move_cooldown <= 0 :
            
            self.randomic = random.random()
            self.cool_down = random.randint(self.cool_down_min, self.cool_down_max)       
            self.move_cooldown = self.cool_down
        
        if self.randomic >= self.probability:
            self.rect.x = self.rect.x + self.speed_x

        else:
            self.rect.x = self.rect.x - self.speed_x

    def draw(self, screen, camera):
        return super().draw(screen, camera)

    def update(self):
        self.move()
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        return super().update()
    
    def attack(self, x, y, width, height, screen):
        self.atk = pygame.Rect(x, y, width, height)
        self.color_atk = (0, 0, 255)  
        pygame.draw.rect(screen, self.color, self.rect) 


class Ganon(Bosses):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.sub_TAG = "Ganon"
        self.width = width
        self.speed_x = 3

        self.color = (160, 32, 240)
        self.color_secundary = (255, 68, 51)
        self.color_aux = ()
        self.color_change = False

        self.life = 60
        self.projectile_cooldown = 0
        self.cool_down = 20

    def update(self):

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()
        
        self.attack()
        self.move()
        return super().update()
    
    def draw(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen)

        return super().draw(screen, camera)

    def on_collision(self, other: pygame.Rect):

        return super().on_collision(other)

    def attack(self):
        if self.projectile_cooldown <= 0:
            if self.hero.rect.x <= self.rect.x:
                new_projectile = Projectile(self.rect.left, self.rect.y - self.width/2, - 20, 0, self.TAG, damage= 20)
                self.projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.right, self.rect.y - self.width/2, 20, 0, self.TAG, damage= 20)
                self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down

    def distance(self, other):
        delta_x = self.rect.centerx - other.rect.centerx
        delta_y = self.rect.centery - other.rect.centery

        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
        return distance

    def move(self):

        if self.distance(self.hero) <= 110:
            if self.hero.rect.centerx - self.rect.centerx < 0:
                print (self.hero.rect.centerx - self.rect.centerx)
                self.rect.x = 0.9 * self.width
                self.rect.y = 0
            elif self.hero.rect.centerx - self.rect.centerx > 0:
                self.rect.x = 0.1 * self.width
                self.rect.y = 0
        