import pygame
from weapon import Projectile, Attack
from assets import Assets
import random
import math

class Bosses:
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
        self.projectiles = []
        self.screen_width = pygame.display.Info().current_w
        self.is_dead = False
        self.immune = False

    def new_hero(self, hero):
        self.hero = hero

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
                    del projectile
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    self.projectiles.remove(projectile)
                    del projectile

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

        self.atk_cooldown = 100
        self.atk_cooldowns = 100
        
        self.atk_time = 110
        self.atk_counter = self.atk_time
        self.damage_timer = 0
        self.atk_when = 30
        self.probability_atk = 0
        self.warning_sign = 20


        self.number_bars = 5
        self.weapon_damage = 100

        self.attacks = []
        self.all_atks = []
        
        for atks in range(self.number_bars):
            self.all_atks.append(Attack(self.screen_width/self.number_bars * atks, 10 + atks, self.screen_width / self.number_bars, 200, self.weapon_damage))

        self.color = (255, 192, 203)

    def attack(self):
        if self.atk_cooldown == self.warning_sign:
            self.probability_atk = random.randint(0, len(self.all_atks) - 1)
            self.rect.x = self.screen_width/self.number_bars * self.probability_atk + self.screen_width/(2*self.number_bars)

        if self.atk_cooldown <= 0:
            for atks in range(len(self.all_atks)):
                if atks != self.probability_atk:
                    self.attacks.append(self.all_atks[atks])
                    self.atk_cooldown = self.atk_cooldowns
        if self.atk_cooldown < self.atk_time - self.atk_when and len(self.attacks) != 0:

            self.attacks.clear()


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
        if len(self.attacks) != 0:
            for atks in self.attacks:
                atks.draw(screen)


        return super().draw(screen, camera)

    def on_collision(self, other: pygame.Rect):
        for atks in self.attacks:
            if other.TAG == "Player":
                if atks.rect.colliderect(other) and self.damage_timer == 0:
                    other.life -= atks.damage
                    self.damage_timer = self.atk_cooldowns
        return super().on_collision(other)

    def update(self):
        self.move()
        self.attack()

        if self.damage_timer > 0:
            self.damage_timer -=1

        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        
        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        return super().update()

class Ganon(Bosses, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        pygame.sprite.Sprite.__init__(self)

        self.sub_TAG = "Ganon"
        self.width = width
        self.speed_x = 3

        self.color = (160, 32, 240)
        self.color_secundary = (255, 68, 51)
        self.color_aux = ()
        self.color_change = False

        self.life = 60

        self.atk_timer = 200
        self.atk_cooldown = self.atk_timer
        self.atk_long = 100

        self.teleport = 60
        self.teleport_cooldown = self.teleport



        #sprites
        self.assets = Assets()
        self.assets.init_Ganon(width, height)

    def update(self):

        if self.atk_timer > 0:
            self.atk_timer -= 1

        for projectile in self.projectiles:
            self.assets.assets_Ganon("ProjectileRight", projectile.rect)
            projectile.update()
        

        #ARRUMAR
        # if self.life > 0:
        #     if self.atk_cooldown > self.atk_timer and self.rect.x - self.hero.rect.x <= 0:
        #         self.assets.assets_Ganon("AttackRight", self.rect)

        #     if self.atk_cooldown > self.atk_timer and self.rect.x - self.hero.rect.x > 0:
        #         self.assets.assets_Ganon("AttackLeft", self.rect)


        print(self.life)

        if self.life <= 0 and self.rect.x - self.hero.rect.x <= 0 and self.assets.Gactual_Death <=14:
            self.assets.assets_Ganon("DeathLeft", self.rect)
            if self.assets.Gactual_Death >= 13.5:
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.hero.rect.x > 0 and self.assets.Gactual_Death <=14:
            if self.assets.Gactual_Death >= 13.5:
                self.is_dead = True
            self.assets.assets_Ganon("DeathRight", self.rect)

        self.attack()
        self.move()
        return super().update()
    
    def draw(self, screen, camera):
        super().draw(screen, camera)

        for projectile in self.projectiles: 
            projectile.draw(screen)
        
        self.image = self.assets.image
        screen.blit(self.image, self.assets.image_rect)

    def on_collision(self, other: pygame.Rect):
        return super().on_collision(other)

    def attack(self):
        if self.atk_timer <= self.atk_long:
            if self.hero.rect.x - self.rect.x <= 0:
                self.assets.assets_Ganon("AttackLeft", self.rect)
                if self.atk_timer <= 0:
                    if self.assets.Gactual_Attack >= 5:
                        self.assets.Gactual_Attack = 0
                    new_projectile_1 = Projectile(self.rect.left, self.rect.centery + 40, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_2 = Projectile(self.rect.left, self.rect.centery + 80, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_3 = Projectile(self.rect.left, self.rect.centery + 120, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_4 = Projectile(self.rect.left, self.rect.centery - 40, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_5 = Projectile(self.rect.left, self.rect.centery - 80, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_6 = Projectile(self.rect.left, self.rect.centery - 120, - 20, 0, self.TAG, 20, 40, 40)
                    new_projectile_7 = Projectile(self.rect.left, self.rect.centery, - 20, 0, self.TAG, 20, 40, 40)


                    self.projectiles.append(new_projectile_1)
                    self.projectiles.append(new_projectile_2)
                    self.projectiles.append(new_projectile_3)
                    self.projectiles.append(new_projectile_4)
                    self.projectiles.append(new_projectile_5)
                    self.projectiles.append(new_projectile_6)
                    self.projectiles.append(new_projectile_7)
                    self.atk_timer = self.atk_cooldown + self.atk_long 

            if self.hero.rect.x - self.rect.x  > 0:
                self.assets.assets_Ganon("AttackRight", self.rect)
                if self.atk_timer <= 0:
                    if self.assets.Gactual_Attack >= 6:
                        self.assets.Gactual_Attack = 0
                    new_projectile = Projectile(self.rect.right, self.rect.centery, 20, 0, self.TAG, 20, 40, 40)
                    self.projectiles.append(new_projectile)
                    self.atk_timer = self.atk_cooldown+ self.atk_long

    def distance(self, other):
        delta_x = self.rect.centerx - other.rect.centerx
        delta_y = self.rect.centery - other.rect.centery

        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
        return distance

    def move(self):
        if self.life > 0 and self.atk_timer > self.atk_long:

            if self.distance(self.hero) > 200:
                self.immune = False
                self.teleport_cooldown = self.teleport
                self.assets.Gactual_Immune = 0
                if self.hero.rect.centerx - self.rect.centerx < 0:
                    self.assets.assets_Ganon("IdleLeft", self.rect)   
                elif self.hero.rect.centerx - self.rect.centerx > 0:
                    self.assets.assets_Ganon("IdleRight", self.rect)

            if self.distance(self.hero) <= 200:
                self.immune = True
                if self.teleport_cooldown > 0:
                    self.teleport_cooldown -= 1
                    if self.hero.rect.centerx - self.rect.centerx < 0:

                        self.assets.assets_Ganon("ImmuneLeft", self.rect)
                    elif self.hero.rect.centerx - self.rect.centerx > 0:

                        self.assets.assets_Ganon("ImmuneRight", self.rect)
                        

                if self.hero.rect.centerx - self.rect.centerx < 0 and self.teleport_cooldown <= 0:
                    self.rect.x = 0.1 * self.screen_width
                    self.rect.y = 0 #retirar dps
                elif self.hero.rect.centerx - self.rect.centerx > 0 and self.teleport_cooldown <= 0:
                    self.rect.x = 0.9 * self.screen_width
                    self.rect.y = 0 #retirar dps

class Demagorgon(Bosses, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        pygame.sprite.Sprite.__init__(self)

        #hitbox
        self.color = (255, 255, 0)

        #movement speed
        self.speed_x = 3

        #attack
        self.attacks = None
        self.atk_cooldown = 100
        self.atk_timer = self.atk_cooldown
        self.atk_long = 50

        #weapon
        self.weapon_width = 130
        self.weapon_height = height
        self.weapon_damage = 100
        self.damage_timer = 0

        #sprites
        self.assets = Assets()
        self.assets.init_Demogorgon(width, height)

    def attack(self):
        if self.atk_timer <= 0:
            if self.rect.x - self.hero.rect.x <= 0:
                self.attacks = Attack(self.rect.right, self.rect.top, self.weapon_width, self.weapon_height, self.weapon_damage)
                self.atk_timer = self.atk_cooldown + self.atk_long

            if self.rect.x - self.hero.rect.x > 0:
                self.attacks = Attack(self.rect.left - self.weapon_width, self.rect.top, self.weapon_width, self.weapon_height, self.weapon_damage)
                self.atk_timer = self.atk_cooldown + self.atk_long

        if self.atk_timer < self.atk_cooldown and self.attacks != None:
            self.attacks = None

    def move(self):
        super().move()
        if self.atk_timer < self.atk_cooldown:
            if self.rect.x - self.hero.rect.x <= 0:
                
                if self.rect.colliderect(self.hero) == False:
                    self.assets.assets_Demogorgon("WalkLeft", self.rect)
                    self.rect.x = self.rect.x + self.speed_x
                else:
                    self.assets.assets_Demogorgon("IdleLeft", self.rect)
            elif self.rect.x - self.hero.rect.x > 0:
                if self.rect.colliderect(self.hero) == False:
                    self.assets.assets_Demogorgon("WalkRight", self.rect)
                    self.rect.x = self.rect.x - self.speed_x
                else:
                    self.assets.assets_Demogorgon("IdleRight", self.rect)

    def on_collision(self, other: pygame.Rect):
        super().on_collision(other)

        if other.TAG == "Player":
            if self.attacks != None:
                if self.attacks.rect.colliderect(other) and self.damage_timer == 0:
                        other.life -= self.attacks.damage
                        self.damage_timer = self.atk_timer

    def draw(self, screen, camera):
        super().draw(screen, camera)

        self.image = self.assets.image
        screen.blit(self.image, self.assets.image_rect)

        # if self.attacks != None:
        #     self.attacks.draw(screen)
    
    def update(self):
        if self.atk_timer > 0:
            self.atk_timer -= 1
        
        if self.damage_timer > 0:
            self.damage_timer -=1

        if self.life <= 0 and self.rect.x - self.hero.rect.x <= 0 and self.assets.actual_Death <=16:
            self.assets.assets_Demogorgon("DeathLeft", self.rect)
            if self.assets.actual_Death >= len(self.assets.deathL_images):
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.hero.rect.x > 0 and self.assets.actual_Death <=16:
            self.assets.assets_Demogorgon("DeathRight", self.rect)
            if self.assets.actual_Death >= len(self.assets.deathR_images):
                self.is_dead = True

        if self.life > 0:
            if self.atk_timer > self.atk_cooldown and self.rect.x - self.hero.rect.x <= 0:
                self.assets.assets_Demogorgon("AtkLeft", self.rect)

            if self.atk_timer > self.atk_cooldown and self.rect.x - self.hero.rect.x > 0:
                self.assets.assets_Demogorgon("AtkRight", self.rect)

            self.move()
            self.attack()
        
        return super().update()