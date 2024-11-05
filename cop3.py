import pygame

pygame.init()

class Player:
    
    def __init__(self, x, y, width, height):
        self.max_life = 0
        self.life = 0 
        
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        
        self.gravity_y = 2 # pixels^2 / 
        self.speed_y = 0
        self.jump_count = 0
        self.jump_count_max = 2
        
        self.speed_x = 0
        self.speed_x_max = 15
        self.speed_x_min = -15
        self.is_running = False
        self.to_left = False
        self.to_right = False
        self.on_ground = False
        
        self.rect_color = (255, 0, 0)
        
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
        if self.is_running == False:
            self.speed_x = 0
        
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
                ground_y = other.rect.top
                self.rect.bottom = ground_y
                self.speed_y = 0
                self.jump_count = 0
                self.on_ground = True
            elif self.rect.left < other.rect.right and self.speed_x < 0 :
                self.rect.left = other.rect.right
            elif self.rect.right > other.rect.left and self.speed_x > 0 :
                self.rect.right = other.rect.left
    
class Ground:
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) 
        self.rect.x = x
        self.rect.y = y
        self.rect_color = (0,255,0)
     
    def draw(self, screen, camera):
        if isinstance(camera, Camera):
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.rect_color, self.rect)

    def update(self):
        pass

    def on_collision(self, other):
        pass

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
        self.WIDTH = 800
        self.HEIGHT = 600
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill([0, 0, 0])
        
        self.hero = Player(self.WIDTH // 2, self.HEIGHT // 2, 40, 50)
        self.camera = Camera(0, 200)
    
        self.grounds = [
            Ground(-self.WIDTH, self.HEIGHT - 30, 3*self.WIDTH, 30), 
            Ground(self.WIDTH // 2, self.HEIGHT // 2 + 100, 100, self.HEIGHT // 2 - 130)
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
            self.update()
            self.collision_decetion()
            self.draw()


            clock.tick(30)
            
    def update(self):
        self.hero.update()
        self.camera.update_coods(self.hero, self.WIDTH)
    
    def collision_decetion(self):
        for ground in self.grounds:
            collining_ground = self.hero.rect.colliderect(ground)
            if collining_ground:
                self.hero.on_collision(ground)
    
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