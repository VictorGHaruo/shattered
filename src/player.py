import pygame
from weapon import Projectile
from weapon import Shield
from weapon import Attack

class Player:
    
    def __init__(self, x, y, width, height):
        self.TAG = "Player"
        self.max_life = 0
        self.life = 0 
        
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        
        self.gravity_y = 2 
        self.speed_y = 0
        self.speed_y_max = 40
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
        
        
        self.trade_cooldown_time = 60
        self.trade_cooldown = self.trade_cooldown_time
        self.rect_color = (255, 0, 0)
        
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.rect_color, self.rect)
        
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
        
        # Se tiver no ar is_running é True, para manter constante a velocidade
        if not self.is_running:
            self.speed_x = 0
        
        ##Updating trade_cooldonw
        if self.trade_cooldown > 0:   
            self.trade_cooldown -= 1    
                
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.on_ground = False

    def jump(self):
        if self.jump_count >= self.jump_count_max:
            return
        self.speed_y -= 30
        self.jump_count += 1
        
    def on_key_pressed(self, key_map):
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
            
            
    def on_collision(self, other):
        if other.TAG == "Ground":
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
            
class Knight(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.jump_count_max = 1
        self.rect_color = (255, 0, 0)
        self.shield = None  

    def actions(self, key_map, other):

        if key_map[pygame.K_v]:
            if self.shield is None: 
                
                shield_x = self.rect.right if self.from_the_front else self.rect.x - 15  
                shield_y = self.rect.y
                self.shield = Shield(shield_x, shield_y, 15, 70)
                if self.on_ground:
                    self.speed_x_max = 0
                    self.speed_x_min = 0

        else:
            self.shield = None
            self.speed_x_max = 10
            self.speed_x_min = -10
            
        if self.shield is not None:
            for projectile in other:
                self.shield.reflect(self.TAG ,projectile)
        
class Yokai(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.jump_count_max = 2
        self.rect_color = (255, 255, 0)
        
        self.projectile_cooldown = 0
        self.cooldown_time = 20
        
    def actions(self, key_map, projectiles):

        if key_map[pygame.K_v] and self.projectile_cooldown <= 0:
            if key_map[pygame.K_UP]:  
                new_projectile = Projectile(self.rect.centerx, self.rect.top, 0, -20, self.TAG, damage= 10)
                projectiles.append(new_projectile)
            elif self.from_the_front: 
                new_projectile = Projectile(self.rect.centerx, self.rect.top, 20, 0, self.TAG, damage= 10)
                projectiles.append(new_projectile)
            else:
                new_projectile = Projectile(self.rect.centerx, self.rect.top, -20, 0, self.TAG, damage=10)
                projectiles.append(new_projectile)

            self.projectile_cooldown = self.cooldown_time
                
    def update(self):
        super().update()
        
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1       
                
class Ninja(Player):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.jump_count_max = 3
        self.rect_color = (255, 255, 255)
        self.attack_cooldown = 0
        self.cooldown_time = 20

    def actions(self, key_map, other):

        if key_map[pygame.K_v] and self.attack_cooldown <= 0:

            attack_x = self.rect.x + (50 if self.from_the_front else - 50)  
            attack = Attack(attack_x, self.rect.y, 50, 15)
            for monster in other:
                attack.strike(100, monster)  

            self.attack_cooldown = self.cooldown_time

    def update(self):
        super().update()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1    
