import pygame

knight = {'stats': 'knight', 'rect_color': (255, 0, 0), 'jump_count_max': 1}
yokai = {'stats': 'yokai', 'rect_color': (255, 255, 0), 'jump_count_max': 2}
ninja = {'stats': 'ninja', 'rect_color': (255, 255, 255), 'jump_count_max': 3}

pygame.init()

projectiles = []

class Player:
    
    def __init__(self, x, y, width, height):
        self.max_life = 0
        self.life = 0 
        
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        
        self.gravity_y = 2 
        self.speed_y = 0
        self.jump_count = 0
        self.jump_count_max = 2
        
        self.speed_x = 0
        self.speed_x_max = 10
        self.speed_x_min = -10
        self.is_running = False
        self.to_left = False
        self.to_right = False
        self.on_ground = False
        
        self.rect_color = (255, 0, 0)
        self.stats = 'knight'
        
        self.projectile_cooldown = 0
        self.trade_cooldown = 0
        self.cooldown_time = 20

    def trade(self, key_map):

        if self.trade_cooldown <= 0:
            if key_map[pygame.K_z] and self.stats != knight['stats']:
                self.stats = knight['stats']
                self.rect_color = knight['rect_color']
                self.jump_count_max = knight['jump_count_max']
                self.trade_cooldown = self.cooldown_time
            if key_map[pygame.K_x] and self.stats != yokai['stats']:
                self.stats = yokai['stats']
                self.rect_color = yokai['rect_color']
                self.jump_count_max = yokai['jump_count_max']
                self.trade_cooldown = self.cooldown_time
            if key_map[pygame.K_c] and self.stats != ninja['stats']:
                self.stats = ninja['stats']
                self.rect_color = ninja['rect_color']
                self.jump_count_max = ninja['jump_count_max']
                self.trade_cooldown = self.cooldown_time

    def actions(self, key_map):
        if self.stats == 'yokai':

            if key_map[pygame.K_v] and self.projectile_cooldown <= 0:
                if key_map[pygame.K_UP]:  
                    new_projectile = Projectile(self.rect.centerx, self.rect.top, 0, -20)
                    projectiles.append(new_projectile)
                elif self.to_left: 
                    new_projectile = Projectile(self.rect.centerx, self.rect.top, -20, 0)
                    projectiles.append(new_projectile)
                else:
                    new_projectile = Projectile(self.rect.centerx, self.rect.top, 20, 0)
                    projectiles.append(new_projectile)

                self.projectile_cooldown = self.cooldown_time  
        
    def draw(self, screen, camera):
        if isinstance(camera, Camera):
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.rect_color, self.rect)
        
    def update(self):
        self.speed_y += self.gravity_y
        self.rect.y += self.speed_y
        
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

        if self.projectile_cooldown > 0 or self.trade_cooldown > 0:
            self.projectile_cooldown -= 1
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
            else:
                self.to_right = False
            if key_map[pygame.K_LEFT] or key_map[pygame.K_a]:
                self.speed_x -= 5
                self.to_left = True
            else:
                self.to_left = False
            
            if (self.to_left or self.to_right) and (not (self.to_left and self.to_right)):
                self.is_running = True
            else:
                self.is_running = False
                self.speed_x = 0
            
            
    def on_collision(self, other):
        if isinstance(other, Ground):
            delta_speeds = self.speed_y - self.speed_x
            delta_speeds *= 1 if delta_speeds > 0 else -1
            
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

class Projectile:
    def __init__(self, x, y, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, 15, 15) 
        self.color = (0, 0, 255)  
        self.speed_x = speed_x  
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
class Ground:
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) 
        self.rect.x = x
        self.rect.y = y
        
        self.speed_x = 0
        self.is_pushing_r = False
        self.is_pushing_l = False
        self.rect_color = (0,255,0)
     
    def draw(self, screen, camera):
        if isinstance(camera, Camera):
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.rect_color, self.rect)

    def update(self):
        pass
        
    def on_collision(self, other):
        pass
               
class Block(Ground):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        
    def update(self):
        if self.is_pushing_r:
            self.rect.x += 1
            self.is_pushing_r = False
        if self.is_pushing_l:
            self.rect.x -= 1
            self.is_pushing_l = False
            
    def on_collision(self, other):
        if isinstance(other, Player):
            if self.rect.left < other.rect.right and self.rect.top < other.rect.bottom:
                self.is_pushing_l = True
            if self.rect.right > other.rect.left and self.rect.top < other.rect.bottom:
                self.is_pushing_r = True
                
class Camera:
    
    def __init__(self, x_init, margin):
        self.position_x = x_init
        self.margin = margin
    
    def update_coods(self, hero, WIDGHT):
        if isinstance(hero, Player):
            if hero.rect.left < self.position_x + self.margin:
                self.position_x = hero.rect.left - self.margin
            elif hero.rect.right > self.position_x + WIDGHT - self.margin:
                self.position_x = hero.rect.right - WIDGHT + self.margin

class GameManager:

    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill([0, 0, 0])
        
        self.hero = Player(self.WIDTH // 2, self.HEIGHT // 2, 40, 50)
        self.camera = Camera(0, 50)
    
        self.grounds = [
            Ground(-20, self.HEIGHT - 30, 3*self.WIDTH, 500),
            Ground(self.WIDTH // 2, self.HEIGHT // 2 + 100, 1000, self.HEIGHT // 2 - 130),
            Ground(-10 , self.HEIGHT // 2, 100, self.HEIGHT // 2 - 130),
            Block(0, self.HEIGHT - 80, 50, 50)
        ]
        
    def run (self):
        clock = pygame.time.Clock()
        
        is_running = True
        while is_running:
        
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False
                self.hero.on_event(event)
                    
            key_map = pygame.key.get_pressed()
            self.hero.on_key_pressed(key_map)
            self.hero.trade(key_map)
            self.hero.actions(key_map)
            self.update()
            self.collision_decetion()
            self.draw()

            for projectile in projectiles[:]:
                projectile.update()
                projectile.draw(self.screen)
                if not self.screen.get_rect().colliderect(projectile.rect):
                    projectiles.remove(projectile)

            pygame.display.flip()
            clock.tick(30)
            
    def update(self):
        self.hero.update()
        self.camera.update_coods(self.hero, self.WIDTH)
        for ground in self.grounds:
            ground.update()
    
    def collision_decetion(self):
        for ground in self.grounds:
            is_collision = self.hero.rect.colliderect(ground)
            if is_collision:
                self.hero.on_collision(ground)
                ground.on_collision(self.hero) 
    
    def draw(self):
        self.screen.fill([0,0,0])
        self.hero.draw(self.screen, self.camera)
        for ground in self.grounds:
            ground.draw(self.screen, self.camera)
        pygame.display.flip()
            
if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()