import pygame
from weapon import Projectile, Shield, Attack
import copy
import os, sys

def change_image(dict):
    if dict.sub_TAG == "Ninja":
        if dict.action is not None:

            if dict.action == "Jump":
                dict.img_idx += dict.fps
                dict.action_idx = 4 if dict.from_the_front else 5

                if dict.img_idx >= 7:
                    dict.img_idx = 7

                if dict.on_ground:
                    dict.action = None

            if dict.action == "Atk":
                dict.img_idx += dict.fps*2
                dict.action_idx = 8 if dict.from_the_front else 9

                if dict.img_idx >= 5:
                    dict.action = None

                dict.img_idx %= len(dict.image_list[dict.action_idx])

            if dict.action == "Hurt":
                dict.img_idx += dict.fps/5
                dict.action_idx = 6 if dict.from_the_front else 7
                if dict.img_idx >= 1:
                    dict.img_idx = 0
                    dict.action = None

        else:
                dict.img_idx += dict.fps
                if dict.to_right and dict.on_ground :
                    dict.action_idx = 2
                elif dict.to_left and dict.on_ground :
                    dict.action_idx = 3
                else: 
                    dict.action_idx = 0 if dict.from_the_front else 1

                dict.img_idx %= len(dict.image_list[dict.action_idx])
    #dict.img_idx %= len(dict.image_list[dict.action_idx])
    dict.image_actual = dict.image_list[dict.action_idx][int(dict.img_idx)]
 


class Player:
    
    def __init__(self, x, y, width, height):
        self.TAG = "Player"
        self.sub_TAG = "Player"
        self.max_life = 2000
        self.life = self.max_life
        
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
        self.action = None
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
        
    def draw(self, screen, camera, image_actual):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            #pygame.draw.rect(screen, self.rect_color, self.rect)
            screen.blit(image_actual, self.rect)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile
        
    def update(self):
        ##Updating Y:
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

        change_image(self)

                
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.on_ground = False
            if event.key == pygame.K_f and self.has_collision_obelisk:
                self.touched_obelisk = True
                self.can_push_block = True

    def jump(self):
        if self.jump_count >= self.jump_count_max:
            return
        self.speed_y += self.speed_jump
        self.speed_y = max(self.speed_y, self.speed_jump)
        self.jump_count += 1
        self.action = "Jump"
        self.img_idx = 0
        
    def on_key_pressed(self, key_map, main):
        if self.on_ground:
            if key_map[pygame.K_RIGHT] or key_map[pygame.K_d]:
                self.speed_x += 5
                self.to_right = True
                self.from_the_front = True
            else:
                self.to_right = False
            if key_map[pygame.K_LEFT] or key_map[pygame.K_a]:
                self.speed_x -= 5
                self.to_left = True
                self.from_the_front = False
            else:
                self.to_left = False
            
            if (self.to_left or self.to_right) and (not (self.to_left and self.to_right)):
                self.is_running = True
            else:
                self.is_running = False
                self.speed_x = 0
                
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
                self.speed_x = -20 if self.from_the_front else 20
                self.action = "Hurt"

            for projectile in other.projectiles:

                if self.rect.colliderect(projectile) and self.invincibility_cooldown <= 0:
                    self.life -= projectile.damage
                    self.invincibility_cooldown = self.invincibility_time

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
        self.sub_TAG = "Knight"
        self.jump_count_max = 1
        self.rect_color = (255, 0, 0)
        self.shield_width = 15
        self.shield_height = 70
        self.shield_x = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 50
        self.shield_y = self.rect.y
        self.shield_damage = 0.7
        self.shield = None 

        # imgs_idle_r = []
        # imgs_idle_l = []
        # imgs_walk_r = []
        # imgs_walk_l = []
        # imgs_jump_r = []
        # imgs_jump_l = []
        # imgs_hurt_r = []
        # imgs_hurt_l = []
        # imgs_def_r = []
        # imgs_def_l = []

        # self.image_list = [imgs_idle_r, imgs_idle_l,imgs_walk_r, imgs_walk_l, imgs_jump_r, imgs_jump_l, imgs_hurt_r, imgs_hurt_l, imgs_def_r, imgs_def_l]
        # path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Knight_path = os.path.join(path_game, os.pardir, "assets", "Knight")
        # Knight_path = os.path.abspath(Knight_path)
        # Idle_path = os.path.join(Knight_path, "Idle.png")
        # Walk_path = os.path.join(Knight_path, "Walk.png")
        # Jump_path = os.path.join(Knight_path, "Jump.png")
        # Hurt_path = os.path.join(Knight_path, "Hurt.png")
        # Defend_path = os.path.join(Knight_path, "Defend.png")

        # self.sheet_im_idle = pygame.image.load(Idle_path).convert_alpha()
        # self.sheet_im_walk = pygame.image.load(Walk_path).convert_alpha()
        # self.sheet_im_jump = pygame.image.load(Jump_path).convert_alpha()
        # self.sheet_im_hurt = pygame.image.load(Hurt_path).convert_alpha()
        # self.sheet_im_defend = pygame.image.load(Defend_path).convert_alpha()

        # for i in range(4):
        #     image = self.sheet_im_idle.subsurface((i*72.5, 0), (72.5, 86))
        #     image = pygame.transform.scale(image, (width, height))
        #     imgs_idle_r.append(image)
        #     image = pygame.transform.flip(image, True, False)
        #     imgs_idle_l.append(image)
        # for i in range(8):
        #     image = self.sheet_im_walk.subsurface((i*72.5, 0), (72.5, 86))
        #     image = pygame.transform.scale(image, (width, height))
        #     imgs_walk_r.append(image)
        #     image = pygame.transform.flip(image, True, False)
        #     imgs_walk_l.append(image)
        # for i in range(6):
        #     image = self.sheet_im_jump.subsurface((i*80, 0), (80, 86))
        #     image = pygame.transform.scale(image, (width, height))
        #     imgs_jump_r.append(image)
        #     image = pygame.transform.flip(image, True, False)
        #     imgs_jump_l.append(image)
        # for i in range(2):
        #     image = self.sheet_im_hurt.subsurface((i*70, 0), (70, 86))
        #     image = pygame.transform.scale(image, (width, height))
        #     imgs_hurt_r.append(image)
        #     image = pygame.transform.flip(image, True, False)
        #     imgs_hurt_l.append(image)
        # for i in range(5):
        #     image = self.sheet_im_defend.subsurface((i*72.5, 0), (80, 86))
        #     image = pygame.transform.scale(image, (width, height))
        #     imgs_def_r.append(image)
        #     image = pygame.transform.flip(image, True, False)
        #     imgs_def_l.append(image)
        # self.action_idx = 6
        # self.img_idx = 0
        # self.fps = 0.2
        # self.image_actual = self.image_list[self.action_idx][self.img_idx]
        

    def actions(self, key_map):

        if key_map[pygame.K_v]:
            if self.shield is None: 
                self.shield = Shield(self.shield_x, self.shield_y, self.shield_width, self.shield_height, self.shield_damage)

            if self.on_ground:
                self.speed_x_max = 0
                self.speed_x_min = 0
                self.speed_jump = 0
                    
        else:
            self.shield = None
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
        super().draw(screen, camera, self.image_actual)

        if self.shield is not None:
            self.shield.draw(screen)

        
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
        self.jump_count_max = 2
        self.rect_color = (255, 255, 0)
        self.damage = 20
        
    def actions(self, key_map):

        if key_map[pygame.K_v] and self.projectile_cooldown <= 0:
            if key_map[pygame.K_UP]:  
                new_projectile = Projectile(self.rect.centerx, self.rect.top, 0, -20, self.sub_TAG, self.damage, 15, 15)
                self.projectiles.append(new_projectile)
            elif self.from_the_front: 
                new_projectile = Projectile(self.rect.centerx, self.rect.top, 20, 0, self.sub_TAG, self.damage, 15, 15)
                self.projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.centerx, self.rect.top, -20, 0, self.sub_TAG, self.damage, 15, 15)
                self.projectiles.append(new_projectile)

            self.projectile_cooldown = self.cooldown_time
                
                
class Ninja(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.sub_TAG = "Ninja"
        self.jump_count_max = 3
        self.rect_color = (255, 255, 255)
        self.range = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 60
        self.attack_cooldown = 0
        self.cooldown_time = 20
        self.damage = 100
        self.attack = None

        imgs_idle_r = []
        imgs_idle_l = []
        imgs_walk_r = []
        imgs_walk_l = []
        imgs_jump_r = []
        imgs_jump_l = []
        imgs_hurt_r = []
        imgs_hurt_l = []
        imgs_atk_r = []
        imgs_atk_l = []

        self.image_list = [imgs_idle_r, imgs_idle_l,imgs_walk_r, imgs_walk_l, imgs_jump_r, imgs_jump_l, imgs_hurt_r, imgs_hurt_l, imgs_atk_r, imgs_atk_l]
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Knight_path = os.path.join(path_game, os.pardir, "assets", "Ninja")
        Knight_path = os.path.abspath(Knight_path)
        Idle_path = os.path.join(Knight_path, "Idle.png")
        Walk_path = os.path.join(Knight_path, "Walk.png")
        Jump_path = os.path.join(Knight_path, "Jump.png")
        Hurt_path = os.path.join(Knight_path, "Hurt.png")
        Atk_path = os.path.join(Knight_path, "Attack_1.png")

        self.sheet_im_idle = pygame.image.load(Idle_path).convert_alpha()
        self.sheet_im_walk = pygame.image.load(Walk_path).convert_alpha()
        self.sheet_im_jump = pygame.image.load(Jump_path).convert_alpha()
        self.sheet_im_hurt = pygame.image.load(Hurt_path).convert_alpha()
        self.sheet_im_atk = pygame.image.load(Atk_path).convert_alpha()

        for i in range(6):
            image = self.sheet_im_idle.subsurface((i*96, 0), (96, 96))
            image = pygame.transform.scale(image, (width, height))
            imgs_idle_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_idle_l.append(image)
        for i in range(8):
            image = self.sheet_im_walk.subsurface((i*96, 0), (96, 96))
            image = pygame.transform.scale(image, (width, height))
            imgs_walk_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_walk_l.append(image)
        for i in range(8):
            image = self.sheet_im_jump.subsurface((i*96, 0), (96, 96))
            image = pygame.transform.scale(image, (width, height))
            imgs_jump_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_jump_l.append(image)
        for i in range(2):
            image = self.sheet_im_hurt.subsurface((i*96, 0), (96, 96))
            image = pygame.transform.scale(image, (width, height))
            imgs_hurt_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_hurt_l.append(image)
        for i in range(6):
            image = self.sheet_im_atk.subsurface((i*96, 0), (96, 96))
            image = pygame.transform.scale(image, (width, height))
            imgs_atk_r.append(image)
            image = pygame.transform.flip(image, True, False)
            imgs_atk_l.append(image)
        self.action_idx = 0
        self.img_idx = 0
        self.fps = 0.5
        self.image_actual = self.image_list[self.action_idx][self.img_idx]

    def actions(self, key_map):

        if key_map[pygame.K_v] and self.attack_cooldown <= 0:

            self.attack = Attack(self.range, self.rect.y, 25, 100, self.damage)
            self.attack_cooldown = self.cooldown_time 
            self.action = "Atk"

        else:
            self.attack = None

    def on_collision(self, other):
        super().on_collision(other)

        if self.attack is not None:

            if other.TAG == "Monster" and self.attack.rect.colliderect(other) and other.immune == False:
                other.life -= self.damage


    def draw(self, screen, camera):
        super().draw(screen, camera,self.image_actual)

        if self.attack is not None:
            self.attack.draw(screen)


    def update(self):
        super().update()

        self.range = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 60

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1 

# def f_save(main):
#     keys_save = ["heros"]
#     main.save_state_game = main.current_state.__getstate__()
#     for key in keys_save:
#         print(main.save_state_game[key])
#         main.save_state_game = copy.deepcopy(main.save_state_game[key])
#         print(main.save_state_game)
#     print("Saved")