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
        self.life = 5
        self.hero = hero
        self.immune = False
        self.is_dead = False
        self.projectiles = []

    def move(self):
        pass

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)
    
    def new_hero(self, hero):
        self.hero = hero
        
    def draw (self, screen: pygame.Surface, camera, image_actual):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            screen.blit(image_actual, self.rect)
                        
    def on_collision(self, other):  

        if other.TAG == "Ground" and self.rect.colliderect(other) and self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                self.rect.bottom = other.rect.top
                
        if other.TAG == "Projectile":
            if self.rect.colliderect(other):       
                    self.life -= other.damage
        
        for projectile in self.projectiles:
            if other.TAG == "Ground":
                if projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
                    del projectile
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    self.projectiles.remove(projectile)
                    del projectile

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
                new_projectile = Projectile(self.rect.left, self.rect.centery, - 20, 0, self.TAG, 20, 15, 15)
                self.projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.right, self.rect.centery, 20, 0, self.TAG, 20, 15, 15)
                self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down

class Flying(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.speed_x = 3
        self.gravity = 0

        self.probability = 0.5
        self.randomic = 0.5

        self.cool_down_max = 100
        self.cool_down_min = 70

        self.cool_down = 0
        self.move_cooldown = 0

        self.projectile_cooldown = 0

        imgs_fly_r = []
        imgs_fly_l = []
        imgs_atk_r = []
        imgs_atk_l = []
        imgs_death_r = []
        imgs_death_l = []
        self.imgs_list = [imgs_fly_r, imgs_fly_l, imgs_atk_r, imgs_atk_l, imgs_death_r, imgs_death_l]
        self.projectile_image = pygame.image.load("../assets/Flying/projectile.png").convert_alpha()
        self.sheet_im_atk = pygame.image.load("../assets/Flying/ATTACK.png").convert_alpha()
        self.sheet_im_fly = pygame.image.load("../assets/Flying/FLYING.png").convert_alpha()
        self.sheet_im_death = pygame.image.load("../assets/Flying/DEATH.png").convert_alpha()
        self.action_idx = 0
        self.img_idx = 0
        self.is_atking = False
        for i in range(4):
            image = self.sheet_im_fly.subsurface((i*81, 0), (81, 71))
            image = pygame.transform.scale(image, (width, height))
            imgs_fly_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_fly_l.append(image)
        for i in range(8):
            image = self.sheet_im_atk.subsurface((i*81, 0), (81, 71))
            image = pygame.transform.scale(image, (width, height))
            imgs_atk_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_atk_l.append(image)
        for i in range(7):
            image = self.sheet_im_death.subsurface((i*81, 0), (81, 71))
            image = pygame.transform.scale(image, (width, height))
            imgs_death_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_death_l.append(image)
        self.image_actual = self.imgs_list[self.action_idx][self.img_idx]
        
    def move(self):
        if self.move_cooldown <= 0:
            
            self.randomic = random.random()
            self.cool_down = random.randint(self.cool_down_min, self.cool_down_max)       
            self.move_cooldown = self.cool_down
        
        if self.randomic >= self.probability:
            self.rect.x += self.speed_x
            self.image("fly", "l")
        else:
            self.rect.x -= self.speed_x
            self.image("fly", "r")

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
        super().draw(screen, camera, self.image_actual)
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            new_projectile = Projectile(self.rect.left, self.rect.bottom, 0, 30, self.TAG, 20, 15, 15, self.projectile_image)
            self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down
            
            if self.speed_x > 0:
                self.image("atk", "l")
            else:
                self.image("atk", "r")
            
    def image(self, action, side):
        
        self.img_idx += 0.25
        if self.action_idx in (2, 3) and self.img_idx >= 8: 
            self.is_atking = False
        if self.action_idx in (4, 5) and self.img_idx >= 7:
            self.is_dead = True
    
        if self.life <= 0:
            if side == "r":
                self.action_idx = 4
            if side == "l":
                self.action_idx = 5
        else:    
            if action == "fly" and not self.is_atking:
                if side == "r":
                    self.action_idx = 0
                if side == "l":
                    self.action_idx = 1
                    
            if action == "atk":
                self.is_atking = True
            if side == "r" and self.is_atking:
                self.action_idx = 2
            if side == "l" and self.is_atking:
                self.action_idx = 3
                
        self.img_idx %= len(self.imgs_list[self.action_idx])
        
        self.image_actual = self.imgs_list[self.action_idx][int(self.img_idx)]