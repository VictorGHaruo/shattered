import pygame
from player import Knight, Yokai, Ninja
from camera import Camera
from ground import Ground, Block
from enemy import Dummy

pygame.init()
           
class GameManager:

    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill([0, 0, 0])
        
        self.heros = [
            Knight(self.WIDTH // 2, self.HEIGHT // 2, 40, 50),
            Yokai(self.WIDTH // 2, self.HEIGHT // 2, 40, 50),
            Ninja(self.WIDTH // 2, self.HEIGHT // 2, 40, 50)
        ]
        self.atual_hero = 0
        self.hero = self.heros[self.atual_hero]
        
        self.projectiles = []
        self.camera = Camera(0, 50)
    
        self.grounds = [
            Ground(-20, self.HEIGHT - 30, 3*self.WIDTH, 500),
            Ground(self.WIDTH // 2, self.HEIGHT // 2 + 100, 1000, self.HEIGHT // 2 - 130),
            Ground(-10 , self.HEIGHT // 2, 100, self.HEIGHT // 2 - 130),
            Block(0, self.HEIGHT - 80, 50, 50)
        ]
        
        self.enemies = [
            Dummy(100, 0, 40, 50),
            Dummy(self.WIDTH  // 2 + 200, self.HEIGHT // 2, 40, 50)
        ]
        
    def run (self):
        clock = pygame.time.Clock()
        
        is_running = True
        while is_running:
        
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False
                self.trade(event)
                self.hero.on_event(event)
                    
            key_map = pygame.key.get_pressed()
            self.hero.on_key_pressed(key_map)
            # for monster in self.enemies:
            #     monster.on_key_pressed(key_map)
            
            #TO CHANGE EVERY HERO DO SMT
            if type(self.hero) == Yokai:
                self.hero.actions(key_map, self.projectiles)
                
            self.update()
            self.collision_decetion()
            self.elimination()
            self.draw()

            clock.tick(30)
            
    def update(self):
        self.hero.update()
        self.camera.update_coods(self.hero, self.WIDTH)
        for ground in self.grounds:
            ground.update()
        for monster in self.enemies:
            monster.update()
        for projectile in self.projectiles:
                projectile.update()
    
    def collision_decetion(self):
        for ground in self.grounds:
            is_collision_hero = self.hero.rect.colliderect(ground)
            if is_collision_hero:
                self.hero.on_collision(ground)
                ground.on_collision(self.hero) 
                
            for enemie in self.enemies:
                is_collision_monster = enemie.rect.colliderect(ground)

                if is_collision_monster:
                    enemie.on_collision(ground)
                    ground.on_collision(enemie) 

            for projectile in self.projectiles:
                is_collision_projectile = projectile.rect.colliderect(ground)
                if is_collision_projectile:
                    self.projectiles.remove(projectile)

        for enemie in self.enemies:
            is_collision_hero = self.hero.rect.colliderect(enemie)
            if is_collision_hero:
                self.hero.on_collision(enemie)
                enemie.on_collision(self.hero)
            
            for projectile in self.projectiles:
                is_collision_p_m = projectile.rect.colliderect(enemie)
                if is_collision_p_m:
                    enemie.on_collision(projectile)
                    self.projectiles.remove(projectile)
                    
        

    def elimination(self):
        for monster in self.enemies:
            if monster.life <= 0:
                self.enemies.remove(monster)
        
        for projectile in self.projectiles:
                if not self.screen.get_rect().colliderect(projectile.rect):
                    self.projectiles.remove(projectile)
                
    def draw(self):
        self.screen.fill([0,0,0])
        self.hero.draw(self.screen, self.camera)
            
        for ground in self.grounds:
            ground.draw(self.screen, self.camera)
        
        for monster in self.enemies:
            monster.draw(self.screen, self.camera)
            
        for projectile in self.projectiles:
                projectile.draw(self.screen)
                
        pygame.display.flip()
        
    def trade(self, event):
        if event.type == pygame.KEYDOWN and self.hero.trade_cooldown <= 0:
            change = False
            if event.key == pygame.K_z:
                self.atual_hero = 0
                change = True
            if event.key == pygame.K_x:
                self.atual_hero = 1
                change = True
            if event.key == pygame.K_c:
                self.atual_hero = 2
                change = True
            
            if change:    
                self.change()
                self.hero.trade_cooldown = self.hero.trade_cooldown_time
        
    def change(self):
        x_atual = self.hero.rect.x
        y_atual = self.hero.rect.y
        speed_y_actual = self.hero.speed_y    
        speed_x_actual = self.hero.speed_x
        jump_count_actual = self.hero.jump_count
        is_running_actual = self.hero.is_running
        on_ground_actual = self.hero.on_ground
        to_left_actual = self.hero.to_left
        to_right_actual = self.hero.to_right
        trade_cooldonw_actual  = self.hero.trade_cooldown
            
        self.hero = self.heros[self.atual_hero]
        
        self.hero.rect.x = x_atual 
        self.hero.rect.y = y_atual
        self.hero.speed_y = speed_y_actual 
        self.hero.speed_x = speed_x_actual
        self.hero.jump_count = jump_count_actual
        self.hero.is_running = is_running_actual
        self.hero.on_ground = on_ground_actual
        self.hero.to_left = to_left_actual
        self.hero.to_right = to_right_actual
        self.hero.trade_cooldown = trade_cooldonw_actual

if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()