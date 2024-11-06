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
        self.speed_x_max = 10
        self.speed_x_min = -10
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
        if not self.is_running:
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
            if key_map[pygame.K_d]:
                self.speed_x += 5
                self.to_right = True
            else:
                self.to_right = False
            if key_map[pygame.K_a]:
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

class Monsters:
    def __init__(self, x, y, width, height):
        self.monster = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed = 0
        self.speed_x = 0
    def on_key_pressed(self, key_map):
        if key_map[pygame.K_RIGHT]:
            self.monster.x += 10
        if key_map[pygame.K_LEFT]:
            self.monster.x -= 10
    def update(self):
        self.speed = self.gravity + self.speed
        self.monster.y = self.speed + self.monster.y

        if self.monster.y > 800 - self.monster.height:
            self.monster.y = 800 - self.monster.height
            self.speed = 0
        
    
    def on_collision(self, other : pygame.Rect):

        if self.monster.colliderect(other):
            if isinstance(other, Player):
                if other.speed_x > 0 or self.speed:
                    print ("bateu pela esquerda")
                pass
            else:
                self.speed = -self.speed
                return True  
        
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.monster)
        
    def border (self):
        if self.monster.x > 1400 - self.monster.width:
            self.monster.x = 1400 - self.monster.width
        if self.monster.x < 0:
            self.monster.x = 0

class Dummy(Monsters):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed_x = 3
    def update(self):
        self.move()
        return super().update()
        
    def move(self):
        self.monster.x = self.monster.x + self.speed_x

    def on_collision(self, other : pygame.Rect):
        if not isinstance(other, Player):
            if self.monster.bottom > other.rect.top and self.monster.top < other.rect.top:
                    self.monster.bottom = other.rect.top
                    self.on_ground = True
            elif self.monster.left < other.rect.right and self.monster.right > other.rect.right:
                # self.monster.left = other.rect.right
                self.speed_x = -self.speed_x
                # self.speed_x = 0
            elif self.monster.right > other.rect.left and self.monster.left < other.rect.left:
                # self.monster.right = other.rect.left
                self.speed_x = -self.speed_x
                # self.speed_x = 0
            # elif self.monster.top < other.rect.bottom and self.monster.bottom > other.rect.bottom:
            #     self.monster.top = other.rect.bottom
            #     self.speed = 0
        if isinstance(other, Player):
            print ("oi")
            if self.monster.top < other.rect.bottom and self.monster.bottom > other.rect.bottom:
                self.monster.top = other.rect.bottom
                self.speed = 0
        # if self.monster.colliderect(other):
        #     if isinstance(other, Player):
        #         if self.monster.bottom > other.rect.top:
        #             print ("oi")

        #         if other.speed_x > 0:
        #             print ("bateu pela esquerda")
        #         pass
        #     else:
        #         self.speed_x = -self.speed_x
        #         return True           
    # def attack(self):

class GameManager:

    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill([0, 0, 0])
        
        self.hero = Player(self.WIDTH // 2, self.HEIGHT // 2, 40, 50)
        self.monster = Dummy(self.WIDTH // 2, self.HEIGHT // 2, 40, 50)
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
            self.monster.on_key_pressed(key_map)
            self.update()
            self.collision_decetion()
            self.draw()


            clock.tick(30)
            
    def update(self):
        self.hero.update()
        self.monster.update()
        self.camera.update_coods(self.hero, self.WIDTH)
        for ground in self.grounds:
            ground.update()
    
    def collision_decetion(self):
        for ground in self.grounds:
            is_collision = self.hero.rect.colliderect(ground)
            if is_collision:
                self.hero.on_collision(ground)
                ground.on_collision(self.hero) 
            m_is_collision = self.monster.monster.colliderect(ground)
            if m_is_collision:
                self.monster.on_collision(ground)
                
                self.monster.on_collision(self.hero)

                ground.on_collision(self.monster) 
    
    def draw(self):
        self.screen.fill([0,0,0])
        self.hero.draw(self.screen, self.camera)
        self.monster.draw(self.screen)
        for ground in self.grounds:
            ground.draw(self.screen, self.camera)
        pygame.display.flip()
            
        
    
if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()