import pygame
from weapon import Projectile, Attack
import random
import os
import math
from assets2 import Sprites

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
        self.death_position = None

    def new_hero(self, hero):
        """
        Update object hero.

        Parameters
        ----------
        hero : int
            O primeiro número.
       

        Returns
        -------
        None: This function doesn't return
            

        Examples
        --------
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
        """
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
            # pygame.draw.rect(screen, self.color, self.rect)
        for projectile in self.projectiles:
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile

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

class Balrog(Bosses, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.sub_TAG = "Balrog"

        self.speed_x = 3
        self.gravity = 0
        self.life = 1

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
        self.warning_sign = 50

        self.timers = ["damage_timer", "move_cooldown", "atk_cooldown", "projectile_cooldown"]

        self.number_bars = 3
        self.weapon_damage = 100

        self.attacks = []
        self.all_atks = []
        
        for atks in range(self.number_bars):
            self.all_atks.append(Attack(self.screen_width/self.number_bars * atks, 10 + atks, self.screen_width / self.number_bars, 650, self.weapon_damage))

        self.color = (255, 192, 203)

        self.sprites = Sprites()
        self.lightning = Sprites()
        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")
        self.adjH = 150
        self.adjW = 150
        self.adjH_atk = 300
        self.adjW_atk = 300
        self.adj = 50

        self.images_directory = {
            "BWalk" : os.path.join(assets_directory, "Balrog", "fly"),
            "BAttack" : os.path.join(assets_directory, "Balrog", "lightning"),
            "BDeath" : os.path.join(assets_directory, "Balrog", "death")
        }

        self.sizes_directory = {
            "BWalk" : 6,
            "BAttack" : 11,
            "BDeath" : 11
        }

        self.images = {
            "BWalk" : [],
            "BAttack" : [],
            "BDeath" : []
        }

        self.actual_balrog = {
            "Walk" : 0,
            "Attack" : 0,
            "Death" : 0
        }

        self.fps = {
            "Walk" : 0.3,
            "Attack" : 0.3,
            "Death" : 0.3
        }

        self.sprites.load_images(True, width, height, "BWalk", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "BWalk", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(True, width, height, "BAttack", self.images, self.sizes_directory, self.images_directory, self.adjW_atk, self.adjH_atk)
        self.sprites.load_images(False, width, height, "BAttack", self.images, self.sizes_directory, self.images_directory, self.adjW_atk, self.adjH_atk)
        self.sprites.load_images(True, width, height, "BDeath", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "BDeath", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)

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
            self.sprites.assets(self.rect, "Walk", self.actual_balrog, "R", self.fps["Walk"], self.images, self.adj, "B")

        else:
            self.rect.x = self.rect.x - self.speed_x
            self.sprites.assets(self.rect, "Walk", self.actual_balrog, "L", self.fps["Walk"], self.images, self.adj, "B")

    def draw(self, screen, camera):
        super().draw(screen, camera)
        if len(self.attacks) != 0:
            for atks in self.attacks:
                # atks.draw(screen)
                self.lightning.assets(atks.rect, "Attack", self.actual_balrog, "L", self.fps["Attack"], self.images, 0, "B")
                self.lightning.draw(screen)       
        self.sprites.draw(screen)


    def on_collision(self, other: pygame.Rect):
        for atks in self.attacks:
            if other.TAG == "Player":
                if atks.rect.colliderect(other) and self.damage_timer == 0:
                    other.life -= atks.damage
                    self.damage_timer = self.atk_cooldowns
        return super().on_collision(other)

    def update(self):

        if self.life > 0:
            self.move()
            self.attack()

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        for time in self.timers:
            if getattr(self,time) > 0:
                setattr(self, time, getattr(self, time) - 1)

        if self.life <= 0:
            self.gravity = 2
            if self.rect.x - self.death_position > 0:
                self.sprites.assets(self.rect, "Death", self.actual_balrog, "L", self.fps["Death"], self.images, self.adj, "B")
                if self.actual_balrog["Death"] >= len(self.images["BDeath"])/2:
                    self.is_dead = True
            elif self.rect.x - self.death_position <= 0:
                self.sprites.assets(self.rect, "Death", self.actual_balrog, "R", self.fps["Death"], self.images, self.adj, "B")
                if self.actual_balrog["Death"] >= len(self.images["BDeath"]):
                    self.is_dead = True

        return super().update()

class Ganon(Bosses):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)

        self.sub_TAG = "Ganon"
        self.width = width

        self.color = (160, 32, 240)

        self.life = 50
        self.is_dead = False

        self.atk_timer = 100
        self.atk_cooldown = self.atk_timer
        self.atk_long = 30

        self.teleport = 40
        self.teleport_cooldown = self.teleport


        self.adjH = 100
        self.adjW = 120 
        self.adj = 25

        #SPRITES V2
        self.sprites = Sprites()
        self.shot = Sprites()

        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")

        self.images_directory = {
            "GIdle" : os.path.join(assets_directory, "Ganon"),
            "GAttack" : os.path.join(assets_directory, "Ganon"),
            "GImmune" : os.path.join(assets_directory, "Ganon"),
            "GProjectile" : os.path.join(assets_directory, "Ganon"),
            "GDeath" : os.path.join(assets_directory, "Ganon")
        }

        self.sizes_directory = {
            "GIdle" : 4,
            "GAttack" : 5,
            "GImmune" : 8,
            "GProjectile" : 1,
            "GDeath" : 14
        }

        self.images = {
            "GIdle" : [],
            "GAttack" : [],
            "GImmune" : [],
            "GProjectile" : [],
            "GDeath" : []
        }

        self.actual_ganon = {
            "Idle" : 0,
            "Attack" : 0,
            "Immune" : 0,
            "Death" : 0

        }

        self.fps = {
            "Idle" : 0.2,
            "Attack" : 0.15,
            "Immune" : 0.4,
            "Death" : 0.2
        }



        self.sprites.load_spritesheets(self.sizes_directory, "GIdle", True, self.images_directory, self.images, "Character_sheet", 100, 100, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GIdle", False, self.images_directory, self.images, "Character_sheet", 100, 100, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GAttack", True, self.images_directory, self.images, "Character_sheet", 100, 100, 100, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GAttack", False, self.images_directory, self.images, "Character_sheet", 100, 100, 100, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GImmune", True, self.images_directory, self.images, "Character_sheet", 100, 100, 300, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GImmune", False, self.images_directory, self.images, "Character_sheet", 100, 100, 300, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "GDeath", False, self.images_directory, self.images, "Character_sheet", 100, 100, 700, width, height, self.adjW, self.adjH, 10)
        self.sprites.load_spritesheets(self.sizes_directory, "GDeath", True, self.images_directory, self.images, "Character_sheet", 100, 100, 700, width, height, self.adjW, self.adjH, 10)
        self.sprites.load_images(True, 70, 28, "GProjectile", self.images, self.sizes_directory, self.images_directory, 0, 0)
        self.sprites.load_images(False, 70, 28, "GProjectile", self.images, self.sizes_directory, self.images_directory, 0, 0) 


    def update(self):

        if self.atk_timer > 0:
            self.atk_timer -= 1        

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        if self.life <= 0 and self.rect.x - self.death_position <= 0:

            self.sprites.assets(self.rect, "Death", self.actual_ganon, "L", self.fps["Death"], self.images, self.adj, "G")

            if self.actual_ganon["Death"] >= len(self.images["GDeath"])/2:
                
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.death_position > 0:
            self.sprites.assets(self.rect, "Death", self.actual_ganon, "R", self.fps["Death"], self.images, self.adj, "G")

            if self.actual_ganon["Death"] >= len(self.images["GDeath"]):
                self.is_dead = True
            
        if self.life > 0:
            self.attack()
            self.move()
        return super().update()
    
    def draw(self, screen, camera):
        super().draw(screen, camera)

        self.sprites.draw(screen)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)

            self.shot.draw(screen)


    def attack(self):
        if self.atk_timer <= self.atk_long and self.distance(self.hero) > 200:

            if self.hero.rect.x - self.rect.x <= 0:
                self.sprites.assets(self.rect, "Attack", self.actual_ganon, "L", self.fps["Attack"], self.images, self.adj, "G")
                if self.atk_timer <= 0:
                    self.actual_ganon["Attack"] = 0
                    self.new_projectiles = [
                                Projectile(self.rect.left -50, self.rect.centery + 47, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                                Projectile(self.rect.left -31, self.rect.centery + 8, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                                Projectile(self.rect.left -42, self.rect.centery - 54, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                                Projectile(self.rect.left + 5, self.rect.centery  - 113, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                                Projectile(self.rect.left - 37, self.rect.centery - 150, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                                Projectile(self.rect.left - 33, self.rect.centery  - 212, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),                    
                                Projectile(self.rect.left - 50, self.rect.centery - 257, -10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][1]),
                    ]

                    for projectile in self.new_projectiles:
                        self.projectiles.append(projectile)
                    self.atk_timer = self.atk_cooldown + self.atk_long 

            if self.hero.rect.x - self.rect.x  > 0:
                self.sprites.assets(self.rect, "Attack", self.actual_ganon, "R", self.fps["Attack"], self.images, self.adj, "G")

                if self.atk_timer <= 0:
                    self.actual_ganon["Attack"] = 0
                    self.new_projectiles = [
                        Projectile(self.rect.right +50, self.rect.centery + 47, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                        Projectile(self.rect.right +31, self.rect.centery + 8, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                        Projectile(self.rect.right +42, self.rect.centery - 54, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                        Projectile(self.rect.right - 5, self.rect.centery  - 113, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                        Projectile(self.rect.right + 37, self.rect.centery - 150, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                        Projectile(self.rect.right + 33, self.rect.centery  - 212, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),                    
                        Projectile(self.rect.right + 50, self.rect.centery - 257, 10, 0, self.TAG, 20, 35*2, 14*2, self.images["GProjectile"][0]),
                    ]
                    for projectile in self.new_projectiles:
                        self.projectiles.append(projectile)
                    self.atk_timer = self.atk_cooldown + self.atk_long

    def distance(self, other):
        delta_x = self.rect.centerx - other.rect.centerx
        delta_y = self.rect.centery - other.rect.centery

        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
        return distance

    def move(self):

        if self.distance(self.hero) > 200 and self.atk_timer > self.atk_long:
            self.immune = False
            self.teleport_cooldown = self.teleport
            if self.hero.rect.centerx - self.rect.centerx < 0:
                self.actual_ganon["Immune"] = 0 
                self.sprites.assets(self.rect, "Idle", self.actual_ganon, "L", self.fps["Idle"], self.images, self.adj, "G")

            elif self.hero.rect.centerx - self.rect.centerx > 0:
                self.actual_ganon["Immune"] = 8
                self.sprites.assets(self.rect, "Idle", self.actual_ganon, "R", self.fps["Idle"], self.images, self.adj, "G")

        if self.distance(self.hero) <= 200:
            self.immune = True
            if self.teleport_cooldown > 0:
                self.teleport_cooldown -= 1
                if self.hero.rect.centerx - self.rect.centerx < 0 and self.actual_ganon["Immune"] < 8:
                    self.sprites.assets(self.rect, "Immune", self.actual_ganon, "L", self.fps["Immune"], self.images, self.adj, "G")

                if self.hero.rect.centerx - self.rect.centerx > 0 and self.actual_ganon["Immune"] < 16 and self.actual_ganon["Immune"] >= 8:

                    self.sprites.assets(self.rect, "Immune", self.actual_ganon, "R", self.fps["Immune"], self.images, self.adj, "G")
                    


            if self.hero.rect.centerx - self.rect.centerx < 0 and self.teleport_cooldown <= 0:
                self.actual_ganon["Immune"] = 0
                self.rect.x = 0.1 * self.screen_width
                self.rect.y = 0 #retirar dps
            elif self.hero.rect.centerx - self.rect.centerx > 0 and self.teleport_cooldown <= 0:
                self.actual_ganon["Immune"] = 8
                self.rect.x = 0.9 * self.screen_width
                self.rect.y = 0 #retirar dps

class Demagorgon(Bosses):
    """
    A class used to represent the boss named Demagorgon

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------

    says(sound=None)
        Prints the animals name and what sound it makes
    """
    def __init__(self, x, y, width, height, hero):
        """
        Inicializes the class Demagorgon with values of atributes
        """


        super().__init__(x, y, width, height, hero)
        self.sub_TAG = "Demagorgon"

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

        #SPRITESV2
        self.sprites = Sprites()
        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")

        self.adjH = 200
        self.adjW = 200
        self.adj = 75

        self.images_directory = {"DWalk" : os.path.join(assets_directory, "Demagorgon", "walk"),
                                "DIdle" : os.path.join(assets_directory, "Demagorgon", "idle"),
                                "DAttack" : os.path.join(assets_directory, "Demagorgon", "1_atk"),
                                "DDeath" : os.path.join(assets_directory, "Demagorgon", "death")
                                }

        self.sizes_directory = {"DWalk" : 10,
                                "DIdle" : 6,
                                "DAttack" : 14,
                                "DDeath" : 16}

        self.images = {
                        "DWalk" : [],
                        "DIdle" : [],
                        "DAttack" : [],
                        "DDeath" : []
        }

        self.actual_demagorgon = {"Walk" : 0,
                                  "Idle" : 0,
                                  "Attack" : 0,
                                  "Death" : 0
        }

        self.fps = {"Walk" : 0.4,
                    "Idle" : 0.4,
                    "Attack" : 0.3,
                    "Death" : 0.25

        }

        self.sprites.load_images(True, width, height, "DWalk", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "DWalk", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(True, width, height, "DIdle", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "DIdle", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(True, width, height, "DAttack", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "DAttack", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(True, width, height, "DDeath", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)
        self.sprites.load_images(False, width, height, "DDeath", self.images, self.sizes_directory, self.images_directory, self.adjW, self.adjH)

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
                    self.sprites.assets(self.rect, "Walk", self.actual_demagorgon, "L", self.fps["Walk"], self.images, self.adj, "D")
                    self.rect.x = self.rect.x + self.speed_x
                else:
                    self.sprites.assets(self.rect, "Idle", self.actual_demagorgon, "L", self.fps["Idle"], self.images, self.adj, "D")

            elif self.rect.x - self.hero.rect.x > 0:
                if self.rect.colliderect(self.hero) == False:
                    self.sprites.assets(self.rect, "Walk", self.actual_demagorgon, "R", self.fps["Walk"], self.images, self.adj, "D")

                    self.rect.x = self.rect.x - self.speed_x
                else:
                    self.sprites.assets(self.rect, "Idle", self.actual_demagorgon, "R", self.fps["Idle"], self.images, self.adj, "D")


    def on_collision(self, other: pygame.Rect):
        super().on_collision(other)

        if other.TAG == "Player":
            if self.attacks != None:
                if self.attacks.rect.colliderect(other) and self.damage_timer == 0:
                        other.life -= self.attacks.damage
                        self.damage_timer = self.atk_timer

    def draw(self, screen, camera):
        super().draw(screen, camera)
        self.sprites.draw(screen)

        # if self.attacks != None:
        #     self.attacks.draw(screen)
    
    def update(self):
        if self.atk_timer > 0:
            self.atk_timer -= 1
        
        if self.damage_timer > 0:
            self.damage_timer -=1

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        if self.life <= 0 and self.rect.x - self.death_position <= 0:
            self.sprites.assets(self.rect, "Death", self.actual_demagorgon, "L", self.fps["Death"], self.images, self.adj, "D")

            if self.actual_demagorgon["Death"] >= len(self.images["DDeath"])/2:
                
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.death_position > 0:
            self.sprites.assets(self.rect, "Death", self.actual_demagorgon, "R", self.fps["Death"], self.images, self.adj, "D")

            if self.actual_demagorgon["Death"] >= len(self.images["DDeath"]):
                self.is_dead = True

        if self.life > 0:
            if self.atk_timer > self.atk_cooldown and self.rect.x - self.hero.rect.x <= 0:
                self.sprites.assets(self.rect, "Attack", self.actual_demagorgon, "L", self.fps["Attack"], self.images, self.adj, "D")

            if self.atk_timer > self.atk_cooldown and self.rect.x - self.hero.rect.x > 0:
                self.sprites.assets(self.rect, "Attack", self.actual_demagorgon, "R", self.fps["Attack"], self.images, self.adj, "D")

            self.move()
            self.attack()
        
        return super().update()