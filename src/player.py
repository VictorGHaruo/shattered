import pygame
from weapon import Projectile, Shield, Attack
import copy

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
        
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.rect_color, self.rect)

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
        print(self.rect.x)
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
        self.jump_count_max = 1
        self.rect_color = (255, 0, 0)
        self.shield_width = 15
        self.shield_height = 70
        self.shield_x = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 50
        self.shield_y = self.rect.y
        self.shield_damage = 0.7
        self.shield = None  

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
        super().draw(screen, camera)

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
        self.jump_count_max = 3
        self.rect_color = (255, 255, 255)
        self.range = self.rect.centerx + 35 if self.from_the_front else self.rect.centerx - 60
        self.attack_cooldown = 0
        self.cooldown_time = 20
        self.damage = 100
        self.attack = None

    def actions(self, key_map):

        if key_map[pygame.K_v] and self.attack_cooldown <= 0:

            self.attack = Attack(self.range, self.rect.y, 25, 15, self.damage)
            self.attack_cooldown = self.cooldown_time

        else:
            self.attack = None

    def on_collision(self, other):
        super().on_collision(other)

        if self.attack is not None:

            if other.TAG == "Monster" and self.attack.rect.colliderect(other) and other.immune == False:
                other.life -= self.damage


    def draw(self, screen, camera):
        super().draw(screen, camera)

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