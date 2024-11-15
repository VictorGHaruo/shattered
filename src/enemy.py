import pygame
from weapon import Projectile
import random
import os, sys

def change_image(dict, action, side):
    
    if dict.sub_TAG == "Dummy" and dict.action_idx in (4, 5):
        dict.fps /= 4
    if dict.sub_TAG == "Mage" and dict.action_idx in (0,1):
        dict.fps /= 3
        
    dict.img_idx += dict.fps
    if dict.action_idx in (2, 3) and dict.img_idx >= 8: 
        dict.is_atking = False
        dict.img_idx = 0
    if dict.action_idx in (4, 5) and dict.img_idx >= 7:
        dict.is_dead = True

    if dict.life <= 0:
        if dict.action_idx in (0, 1, 2, 3):
            dict.img_idx = 0
        if side == "r":
            dict.action_idx = 4
        if side == "l":
            dict.action_idx = 5
    else:    
        if action in  ("fly", "idle", "run") and not dict.is_atking:
            if dict.action_idx in (2, 3):
                dict.img_idx = 0
            if side == "r":
                dict.action_idx = 0
            if side == "l":
                dict.action_idx = 1
                
        if action == "atk":
            dict.is_atking = True
        if side == "r" and dict.is_atking:
            dict.action_idx = 2
        if side == "l" and dict.is_atking:
            dict.action_idx = 3
            
    dict.img_idx %= len(dict.imgs_list[dict.action_idx])
    
    dict.image_actual = dict.imgs_list[dict.action_idx][int(dict.img_idx)]

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
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile
                        
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
        self.init_x = x
        self.to_left = True
        self.to_right = False
        self.range = 100
        
        imgs_run_r = []
        imgs_run_l = []
        imgs_atk_r = []
        imgs_atk_l = []
        imgs_death_r = []
        imgs_death_l = []
        self.imgs_list = [imgs_run_r, imgs_run_l, imgs_atk_r, imgs_atk_l, imgs_death_r, imgs_death_l]
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Dummy_path = os.path.join(path_game, os.pardir, "assets", "Dummy")
        Dummy_path = os.path.abspath(Dummy_path)
        ATTACK_path = os.path.join(Dummy_path, "ATTACK.png")
        RUN_path = os.path.join(Dummy_path, "RUN.png")
        DEATH_path = os.path.join(Dummy_path, "DEATH.png")
        self.sheet_im_atk = pygame.image.load(ATTACK_path).convert_alpha()
        self.sheet_im_run = pygame.image.load(RUN_path).convert_alpha()
        self.sheet_im_death = pygame.image.load(DEATH_path).convert_alpha()
        self.action_idx = 0
        self.img_idx = 0
        self.is_atking = False
        self.fps = 0.2
        for i in range(7):
            image = self.sheet_im_run.subsurface((i*80, 0), (80, 64))
            image = pygame.transform.scale(image, (width, height))
            imgs_run_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_run_l.append(image)
        for i in range(10):
            image = self.sheet_im_atk.subsurface((i*80, 0), (80, 64))
            image = pygame.transform.scale(image, (width, height))
            imgs_atk_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_atk_l.append(image)
        for i in range(15):
            image = self.sheet_im_death.subsurface((i*80, 0), (80, 64))
            image = pygame.transform.scale(image, (width, height))
            imgs_death_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_death_l.append(image)
        self.image_actual = self.imgs_list[self.action_idx][self.img_idx]

    def on_collision(self, other):
        super().on_collision(other)
        
        if self.rect.x > self.init_x + self.range and self.to_left:
            self.speed_x *= -1
            self.to_left = False
            self.to_right = True
        if self.rect.x < self.init_x - self.range and self.to_right:
            self.speed_x *= -1
            self.to_left = True
            self.to_right = False

    def update(self):
        self.move()
        return super().update()
        
    def move(self):
        self.rect.x = self.rect.x + self.speed_x
        if self.speed_x > 0:
            change_image(self, "run", "l")
        else:
            change_image(self, "run", "r")
        
    def draw(self, screen: pygame.Surface, camera):
        if camera.TAG == "Camera":
            self.init_x -= camera.position_x
            if self.rect.x < camera.fix_x - (screen.get_size()[0] // 2) and self.to_right:
                self.speed_x *= -1
                self.to_left = True
                self.to_right = False
        return super().draw(screen, camera, self.image_actual)

class Mage(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.width = width
        self.speed_x = 3
        self.color = (0,0, 255)
        self.life = 60
        self.projectile_cooldown = 0
        self.cool_down = 100
        
        imgs_idle_r = []
        imgs_idle_l = []
        imgs_atk_r = []
        imgs_atk_l = []
        imgs_death_r = []
        imgs_death_l = []
        self.imgs_list = [imgs_idle_r, imgs_idle_l, imgs_atk_r, imgs_atk_l, imgs_death_r, imgs_death_l]
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Mage_path = os.path.join(path_game, os.pardir, "assets", "Mage")
        Mage_path = os.path.abspath(Mage_path)
        ATTACK_path = os.path.join(Mage_path, "ATTACK.png")
        IDLE_path = os.path.join(Mage_path, "IDLE.png")
        DEATH_path = os.path.join(Mage_path, "DEATH.png")
        projectile_path = os.path.join(Mage_path, "projectile.png")
        self.sheet_im_atk = pygame.image.load(ATTACK_path).convert_alpha()
        self.sheet_im_idle = pygame.image.load(IDLE_path).convert_alpha()
        self.sheet_im_death = pygame.image.load(DEATH_path).convert_alpha()
        self.image_projectile_r = pygame.image.load(projectile_path).convert_alpha()
        self.image_projectile_l = pygame.transform.flip(self.image_projectile_r, True, False)
        self.action_idx = 0
        self.img_idx = 0
        self.is_atking = False
        self.fps = 0.20
        for i in range(4):
            for j in range(3):
                if i == 3 and j != 0:
                    break
                image = self.sheet_im_idle.subsurface((j*80, i*80), (80, 80))
                image = pygame.transform.scale(image, (width, height))
                imgs_idle_l.append(image)
                image = pygame.transform.flip(image, True, False)
                imgs_idle_r.append(image)

                image = self.sheet_im_atk.subsurface((j*80, i*80), (80, 80))
                image = pygame.transform.scale(image, (width, height))
                imgs_atk_l.append(image)
                image = pygame.transform.flip(image, True, False)
                imgs_atk_r.append(image)

                image = self.sheet_im_death.subsurface((j*80, i*80), (80, 80))
                image = pygame.transform.scale(image, (width, height))
                imgs_death_l.append(image)
                image = pygame.transform.flip(image, True, False)
                imgs_death_r.append(image)
        self.image_actual = self.imgs_list[self.action_idx][self.img_idx]
    
    def update(self):
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()

        if self.hero.rect.x < self.rect.x:
            change_image(self, "idle", "l")
        else:
            change_image(self, "idle", "r")
            
        self.attack()
        return super().update()
    
    def on_collision(self, other: pygame.Rect):
        return super().on_collision(other)
    
    
    def draw(self, screen, camera):
        super().draw(screen, camera, self.image_actual)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            if self.hero.rect.x <= self.rect.x:
                new_projectile = Projectile(self.rect.left, self.rect.centery, - 20, 0, self.TAG, 20, 50, 30, self.image_projectile_r)
                self.projectiles.append(new_projectile)
                change_image(self, "atk", "l")
            else:
                new_projectile = Projectile(self.rect.right, self.rect.centery, 20, 0, self.TAG, 20, 50, 30, self.image_projectile_l)
                self.projectiles.append(new_projectile)
                change_image(self, "atk", "r")
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
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Flying_path = os.path.join(path_game, os.pardir, "assets", "Flying")
        Flying_path = os.path.abspath(Flying_path)
        projectile_path = os.path.join(Flying_path, "projectile.png")
        ATTACK_path = os.path.join(Flying_path, "ATTACK.png")
        FLYING_path = os.path.join(Flying_path, "FLYING.png")
        DEATH_path = os.path.join(Flying_path, "DEATH.png")
        self.projectile_image = pygame.image.load(projectile_path).convert_alpha()
        self.sheet_im_atk = pygame.image.load(ATTACK_path).convert_alpha()
        self.sheet_im_fly = pygame.image.load(FLYING_path).convert_alpha()
        self.sheet_im_death = pygame.image.load(DEATH_path).convert_alpha()
        self.action_idx = 0
        self.img_idx = 0
        self.is_atking = False
        self.fps = 0.25
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
            change_image(self, "fly", "l")
        else:
            self.rect.x -= self.speed_x
            change_image(self, "fly", "r")

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
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            new_projectile = Projectile(self.rect.left, self.rect.bottom, 0, 30, self.TAG, 20, 30, 40, self.projectile_image)
            self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down
            
            if self.speed_x > 0:
                change_image(self, "atk", "l")
            else:
                change_image(self, "atk", "r")