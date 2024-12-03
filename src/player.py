import pygame
from src.weapon import Projectile, Shield, Attack
import os, sys
from src.assets import Sprites

class Player:
    
    def __init__(self, x, y, width, height):
        self.TAG = "Player"
        self.sub_TAG = "Player"
        self.teste = "teste"
        self.action = None
        self.max_life = 2000
        self.life = self.max_life
        self.Death = False
        
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        
        self.gravity_y = 2 
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_jump = -30
        self.jump_count = 0
        self.jump_count_max = 2
        
        self.speed_x = 0
        self.speed_x_max = 10
        self.speed_x_min = -10
        self.is_running = False
        self.to_left = False
        self.to_right = False
        self.on_ground = False
        self.from_the_front = True
        self.has_collision_obelisk = False
        self.touched_obelisk = False
        self.can_push_block = False
        
        
        self.trade_cooldown_time = 60
        self.trade_cooldown = self.trade_cooldown_time
        self.invincibility_time = 30
        self.collision_damage = 50
        self.damage = 0
        self.invincibility_cooldown = self.invincibility_time
        self.projectiles = []
        self.projectile_cooldown = 0
        self.cooldown_time = 20
        self.rect_color = (255, 0, 0)

        self.sprites = Sprites()
        
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            #pygame.draw.rect(screen, self.rect_color, self.rect)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile

        if self.action == "Jump":

            if self.on_ground:
                self.action = None
                
            if self.actual["Jump"] == (len(self.images[f"{self.teste}Jump"])-1)//2 or self.actual["Jump"] == len(self.images[f"{self.teste}Jump"] )-1 :
                if self.from_the_front:
                    self.sprites.assets(self.rect, "Jump", self.actual, "R", 0, self.images, self.adj, self.teste)
                else: self.sprites.assets(self.rect, "Jump", self.actual, "L", 0, self.images, self.adj, self.teste)
                return

        if self.action == "Hurt":
            if self.from_the_front:

                self.sprites.assets(self.rect, "Hurt", self.actual, "R", 0, self.images, self.adj, self.teste)
            else:
                self.sprites.assets(self.rect, "Hurt", self.actual, "L", 0, self.images, self.adj, self.teste)
            if self.on_ground:
                self.action = None
            return
        
        if self.action is not None:

            if self.from_the_front:

                self.sprites.assets(self.rect, self.action, self.actual, "R", self.fps[self.action], self.images, self.adj, self.teste)
            else:
                self.sprites.assets(self.rect, self.action, self.actual, "L", self.fps[self.action], self.images, self.adj, self.teste)

        else:
            if self.on_ground:
                if self.from_the_front:

                    self.sprites.assets(self.rect, "Idle", self.actual, "R", self.fps["Idle"], self.images, self.adj, self.teste)
                else:
                    self.sprites.assets(self.rect, "Idle", self.actual, "L", self.fps["Idle"], self.images, self.adj, self.teste)
            else:   
                if self.from_the_front:
                    self.actual["Jump"] = (len(self.images[f"{self.teste}Jump"] )-1)//2
                    self.sprites.assets(self.rect, "Jump", self.actual, "R", 0, self.images, self.adj, self.teste)
                else: 
                    self.actual["Jump"] = len(self.images[f"{self.teste}Jump"] )-1
                    self.sprites.assets(self.rect, "Jump", self.actual, "L", 0, self.images, self.adj, self.teste)
        
    def update(self):
        ##Updating Y:
        if self.life <= 0 or self.rect.y > 1000:
            self.action = "Death"
            self.speed_x = 0
            if int(self.actual["Death"]) == len(self.images[f"{self.teste}Death"] )-1 or  self.actual["Death"] == (len(self.images[f"{self.teste}Death"] )-1)//2:
                self.Death = True
        self.speed_y += self.gravity_y
        self.rect.y += min(self.speed_y, self.speed_y_max)
        
        ##Updating X:
        if self.speed_x > 0:
            # Se no pulo estivar apertando para o outro lado, ao tocar no chão zera a velocidade
            if self.to_left:
                self.speed_x = 0
            self.rect.x += min(self.speed_x, self.speed_x_max) 
        elif self.speed_x < 0:
            # Se no pulo estivar apertando para o outro lado, ao tocar no chão zera a velocidade
            if self.to_right:
                self.speed_x = 0
            self.rect.x += max(self.speed_x, self.speed_x_min)
        if self.rect.x <= 0:
            self.rect.x = 0
        
        # Se tiver no ar is_running é True, para manter constante a velocidade
        if not self.is_running:
            self.speed_x = 0
        
        ##Updating trade_cooldonw
        if self.trade_cooldown > 0 or self.invincibility_cooldown > 0 :
            self.trade_cooldown -= 1    
            self.invincibility_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1
                
                
    def on_event(self, event: pygame.event.Event, main):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.on_ground = False
            if event.key == pygame.K_f and self.has_collision_obelisk:
                if not self.can_push_block:
                    main.is_changed = True
                self.touched_obelisk = True
                self.can_push_block = True

    def jump(self):
        if self.jump_count >= self.jump_count_max or self.action == "Hurt" or self.action == "Immune" or self.action == "Death":
            return
        self.speed_y += self.speed_jump
        self.speed_y = max(self.speed_y, self.speed_jump)
        self.jump_count += 1
        #self.sprites.assets(self.rect, "Jump", self.actual, "R", self.fps["Jump"], self.images, self.adj, self.teste)
        self.action = "Jump"
        self.actual["Jump"] = 0
        
    def on_key_pressed(self, key_map, main):
        if self.on_ground and self.action != "Hurt" and self.action != "Attack" and self.action != "Immune" and self.action != "Death":
            if  key_map[pygame.K_d]:
                self.speed_x += 5
                self.to_right = True
                self.from_the_front = True
                # self.sprites.assets(self.rect, "Walk", self.actual, "Walk", self.fps["Walk"], self.images, self.adj, self.teste)
            else:
                self.to_right = False
            if  key_map[pygame.K_a]:
                self.speed_x -= 5
                self.to_left = True
                self.from_the_front = False
                #self.sprites.assets(self.rect, "Walk", self.actual, "L", self.fps["Walk"], self.images, self.adj, self.teste)
            else:
                self.to_left = False
            
            if (self.to_left or self.to_right) and (not (self.to_left and self.to_right)):
                self.is_running = True
                self.action = "Walk"
            else:
                self.is_running = False
                self.speed_x = 0
                if self.action == "Walk":
                    self.action = None
                
            # if key_map[pygame.K_f] and self.is_touching_obelisk:
            #     f_save(main)
                
            
            
    def on_collision(self, other):
        if other.TAG == "Ground" and self.rect.colliderect(other):
            if self.rect.bottom > other.rect.top and self.rect.top < other.rect.top and self.speed_y > 0:
                self.rect.bottom = other.rect.top
                self.speed_y = 0
                self.jump_count = 0
                self.on_ground = True
            elif self.rect.left < other.rect.right and self.rect.right > other.rect.right and self.speed_x < 0 :
                self.rect.left = other.rect.right
                self.speed_x = 0
            elif self.rect.right > other.rect.left and self.rect.left < other.rect.left and self.speed_x > 0 :
                self.rect.right = other.rect.left
                self.speed_x = 0
            elif self.rect.top < other.rect.bottom and self.rect.bottom > other.rect.bottom:
                self.rect.top = other.rect.bottom
                self.speed_y = 0
            
            if other.sub_TAG == "Spike":
                self.life -= 1000

        if other.TAG == "Monster":

            if self.rect.colliderect(other) and self.invincibility_cooldown <= 0:
                self.life -= self.collision_damage
                self.invincibility_cooldown = self.invincibility_time
                self.action = "Hurt"
                self.speed_x = 0
                self.speed_y = 0

            for projectile in other.projectiles:

                if self.rect.colliderect(projectile) and self.invincibility_cooldown <= 0:
                    self.life -= projectile.damage
                    self.invincibility_cooldown = self.invincibility_time
                    self.action = "Hurt"
                    self.speed_x = 0
                    self.speed_y = 0

        for projectile in self.projectiles:
                if other.TAG == "Monster" and projectile.rect.colliderect(other):
                    if not projectile.who == "Yokai" or not other.sub_TAG == "Ganon":
                            other.life -= self.damage
                    self.projectiles.remove(projectile)
                    del projectile

                    
                if other.TAG == "Ground" and projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
                    del projectile
                    
        if other.TAG == "Obelisk" and self.rect.colliderect(other.rect):
            self.has_collision_obelisk = True
            
        if other.TAG == "Obelisk" and self.touched_obelisk and self.rect.colliderect(other.rect):
            other.touched = True
            self.has_collision_obelisk = False
            self.touched_obelisk = False
            
            

            
class Knight(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.teste = "K"
        self.jump_count_max = 1
        self.rect_color = (255, 0, 0)
        self.shield_width = 5
        self.shield_height = 70
        self.shield_x = self.rect.centerx if self.from_the_front else self.rect.centerx - 15
        self.shield_y = self.rect.y
        self.shield_damage = 0.7
        self.shield = None  

        self.sprites = Sprites()
        self.adjW = 80
        self.adjH = 80
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Knight_path = os.path.join(path_game, os.pardir, "assets", "Knight")
        self.images_directory = {
            "KIdle" : os.path.join(Knight_path),
            "KWalk" : os.path.join(Knight_path),
            "KHurt" : os.path.join(Knight_path),
            "KJump" : os.path.join(Knight_path),
            "KImmune" : os.path.join(Knight_path),
            "KDeath" : os.path.join(Knight_path)
        }
        self.sizes_directory = {
            "KIdle" : 4,
            "KWalk" : 8,
            "KHurt" : 2,
            "KJump" : 6,
            "KImmune" : 1,
            "KDeath" : 6
        }
        self.images = {
            "KIdle" : [],
            "KWalk" : [],
            "KHurt" : [],
            "KJump" : [],
            "KImmune" : [],
            "KDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Immune" : 0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.5,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Immune" : 0,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(self.sizes_directory, "KIdle", True, self.images_directory, self.images, "Idle1", 128, 128, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "KIdle", False, self.images_directory, self.images, "Idle1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KWalk", True, self.images_directory, self.images, "Walk1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KWalk", False, self.images_directory, self.images, "Walk1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KHurt", True, self.images_directory, self.images, "Hurt1", 128, 128, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "KHurt", False, self.images_directory, self.images, "Hurt1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KJump", True, self.images_directory, self.images, "Jump1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KJump", False, self.images_directory, self.images, "Jump1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KImmune", True, self.images_directory, self.images, "Protect1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KImmune", False, self.images_directory, self.images, "Protect1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KDeath", True, self.images_directory, self.images, "Dead1", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "KDeath", False, self.images_directory, self.images, "Dead1", 128, 128, 0, width, height, self.adjW, self.adjH)
    def actions(self, key_map):

        if key_map[pygame.K_v] and self.action != "Hurt" and self.action != "Death":

            self.action = "Immune"

            if self.action == "Immune":
                if self.shield is None: 
                    self.shield = Shield(self.shield_x, self.shield_y, self.shield_width, self.shield_height, self.shield_damage)
                    self.action = "Immune"

                if self.on_ground:
                    self.speed_x_max = 0
                    self.speed_x_min = 0
                    self.speed_jump = 0
                    
        else:
            self.shield = None
            if self.action == "Immune":
                self.action = None
            self.speed_x_max = 10
            self.speed_x_min = -10
            self.speed_jump = -30
            

    def on_collision(self, other):

        super().on_collision(other)

        if self.shield is not None:
            if other.TAG == "Monster":
                for projectile in other.projectiles:
                    self.damage = self.shield.damage * projectile.damage
                    self.shield.reflect(self.TAG, projectile, self.projectiles, other.projectiles)

    def draw(self, screen, camera):
        super().draw(screen, camera)

        #if self.shield is not None:
            #self.shield.draw(screen)

        self.sprites.draw(screen)

        
    def update(self):

        super().update()

        self.shield_x = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 50

        self.shield_y = self.rect.y

        if self.shield is not None:
            self.shield.update(self.shield_x, self.shield_y)

class Yokai(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.sub_TAG = "Yokai"
        self.teste = "Y"
        self.jump_count_max = 2
        self.rect_color = (255, 255, 0)
        self.damage = 20
        self.attack_animation = 5
        self.attack_time = 0
        
        self.sprites = Sprites()
        self.adjW = 60
        self.adjH = 60
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Yokai_path = os.path.join(path_game, os.pardir, "assets", "Yokai")
        self.images_directory = {
            "YIdle" : os.path.join(Yokai_path),
            "YWalk" : os.path.join(Yokai_path),
            "YHurt" : os.path.join(Yokai_path),
            "YJump" : os.path.join(Yokai_path),
            "YAttack" : os.path.join(Yokai_path),
            "YAttack_2": os.path.join(Yokai_path),
            "YDeath" : os.path.join(Yokai_path)
        }
        self.sizes_directory = {
            "YIdle" : 8,
            "YWalk" : 8,
            "YHurt" : 2,
            "YJump" : 10,
            "YAttack" : 7,
            "YAttack_2" : 10,
            "YDeath" : 10
        }
        self.images = {
            "YIdle" : [],
            "YWalk" : [],
            "YHurt" : [],
            "YJump" : [],
            "YAttack" : [],
            "YAttack_2": [],
            "YDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Attack" : 0,
            "Attack_2":0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.5,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Attack" : 1.5,
            "Attack_2": 1.5,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(self.sizes_directory, "YIdle", True, self.images_directory, self.images, "Idle", 128, 128, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "YIdle", False, self.images_directory, self.images, "Idle", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YWalk", True, self.images_directory, self.images, "Walk", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YWalk", False, self.images_directory, self.images, "Walk", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YHurt", True, self.images_directory, self.images, "Hurt", 128, 128, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "YHurt", False, self.images_directory, self.images, "Hurt", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YJump", True, self.images_directory, self.images, "Jump", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YJump", False, self.images_directory, self.images, "Jump", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YAttack", True, self.images_directory, self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YAttack", False, self.images_directory, self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YAttack_2", True, self.images_directory, self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YAttack_2", False, self.images_directory, self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YDeath", True, self.images_directory, self.images, "Dead", 128, 128, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "YDeath", False, self.images_directory, self.images, "Dead", 128, 128, 0, width, height, self.adjW, self.adjH)
        projectile_path = os.path.join(Yokai_path, "Fire.png")
        self.image_projectile_r = pygame.image.load(projectile_path)
        self.image_projectile_l = pygame.transform.flip(self.image_projectile_r, True, False)
        self.image_projectile_u = pygame.transform.rotate(self.image_projectile_l, 270)

        
    def actions(self, key_map):

        if key_map[pygame.K_v] and self.projectile_cooldown <= 0 and self.action != "Hurt" and self.action != "Death":
            self.attack_time = 0
            if key_map[pygame.K_w]:  
                new_projectile = Projectile(self.rect.centerx, self.rect.centery, 0, -20, self.sub_TAG, self.damage, 30, 30, self.image_projectile_u)
                self.projectiles.append(new_projectile)
                self.action = "Attack_2"
                self.actual["Attack_2"] = 0
            elif self.from_the_front: 
                new_projectile = Projectile(self.rect.centerx, self.rect.top, 20, 0, self.sub_TAG, self.damage, 30, 30, self.image_projectile_r)
                self.projectiles.append(new_projectile)
                self.action = "Attack"
                self.actual["Attack"] = 0
            else:
                new_projectile = Projectile(self.rect.centerx, self.rect.top, -20, 0, self.sub_TAG, self.damage, 30, 30, self.image_projectile_l)
                self.projectiles.append(new_projectile)
                self.action = "Attack"
                self.actual["Attack"] = 0

            self.projectile_cooldown = self.cooldown_time

    def update(self):
        super().update()
        self.attack_time += 1
        if self.attack_time >= self.attack_animation and (self.action == "Attack" or self.action == "Attack_2"):
            self.action = None

    def draw(self, screen, camera):
        super().draw(screen, camera)

        self.sprites.draw(screen)
                
                
class Ninja(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.teste = "N"
        self.jump_count_max = 3
        self.rect_color = (255, 255, 255)
        self.range = self.rect.centerx + 30 if self.from_the_front else self.rect.centerx - 40
        self.attack_cooldown = 0
        self.attack_time = 0
        self.attack_animation = 5
        self.cooldown_time = 20
        self.damage = 100
        self.attack = None

        self.sprites = Sprites()
        self.adjW = 50
        self.adjH = 35
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Ninja_path = os.path.join(path_game, os.pardir, "assets", "Ninja")
        self.images_directory = {
            "NIdle" : os.path.join(Ninja_path),
            "NWalk" : os.path.join(Ninja_path),
            "NHurt" : os.path.join(Ninja_path),
            "NJump" : os.path.join(Ninja_path),
            "NAttack" : os.path.join(Ninja_path),
            "NDeath" : os.path.join(Ninja_path)
        }
        self.sizes_directory = {
            "NIdle" : 6,
            "NWalk" : 8,
            "NHurt" : 2,
            "NJump" : 8,
            "NAttack" : 6,
            "NDeath" : 4
        }
        self.images = {
            "NIdle" : [],
            "NWalk" : [],
            "NHurt" : [],
            "NJump" : [],
            "NAttack" : [],
            "NDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Attack" : 0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.5,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Attack" : 1.5,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(self.sizes_directory, "NIdle", True, self.images_directory, self.images, "Idle", 96, 96, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "NIdle", False, self.images_directory, self.images, "Idle", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NWalk", True, self.images_directory, self.images, "Walk", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NWalk", False, self.images_directory, self.images, "Walk", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NHurt", True, self.images_directory, self.images, "Hurt", 96, 96, 0, width, height, self.adjW, self.adjH)        
        self.sprites.load_spritesheets(self.sizes_directory, "NHurt", False, self.images_directory, self.images, "Hurt", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NJump", True, self.images_directory, self.images, "Jump", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NJump", False, self.images_directory, self.images, "Jump", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NAttack", True, self.images_directory, self.images, "Attack_1", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NAttack", False, self.images_directory, self.images, "Attack_1", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NDeath", True, self.images_directory, self.images, "Dead", 96, 96, 0, width, height, self.adjW, self.adjH)
        self.sprites.load_spritesheets(self.sizes_directory, "NDeath", False, self.images_directory, self.images, "Dead", 96, 96, 0, width, height, self.adjW, self.adjH)
    def actions(self, key_map):

        if key_map[pygame.K_v] and self.attack_cooldown <= 0 and not self.action == "Hurt" and self.action != "Death":

            self.attack = Attack(self.range, self.rect.y, 20, 60, self.damage)
            self.attack_cooldown = self.cooldown_time
            self.action = "Attack"
            self.actual["Attack"] = 0
            self.attack_time = 0
        else:
            self.attack = None

    def on_collision(self, other):
        super().on_collision(other)

        if self.attack is not None:

            if other.TAG == "Monster" and self.attack.rect.colliderect(other) and other.immune == False:
                other.life -= self.damage
                self.attack = None


    def draw(self, screen, camera):
        super().draw(screen, camera)

        #if self.attack is not None:
            #self.attack.draw(screen)

        self.sprites.draw(screen)

    def on_key_pressed(self, key_map, main):
        return super().on_key_pressed(key_map, main)



    def update(self):
        super().update()

        self.range = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 60

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1   

        self.attack_time += 1
        if self.attack_time >= self.attack_animation and self.action == "Attack":
            self.action = None