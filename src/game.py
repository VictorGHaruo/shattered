import pygame
import sys
from player import Knight, Yokai, Ninja
from camera import Camera
from ground import Ground, Block, maping
from enemy import Dummy, Mage, Flying
from boss import Balrog, Ganon, Demagorgon
from text import Text
import os
import sys

pygame.init()
           
class GameManager:

    def __init__(self, main):
        self.heros = [
            Knight(main.WIDTH // 2, main.HEIGHT // 2, 40, 50),
            Yokai(main.WIDTH // 2, main.HEIGHT // 2, 40, 50),
            Ninja(main.WIDTH // 2, main.HEIGHT // 2, 40, 50)
        ]
        self.atual_hero = 0
        self.hero = self.heros[self.atual_hero]
        
        self.projectiles = []
        self.camera = Camera(0, main.WIDTH)
    
        self.grounds = []
        maping(self.grounds)
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
        
        self.enemies = [
            Dummy(main.WIDTH  // 2 + 200, main.HEIGHT // 2, 40, 50, self.hero),
            Mage(200,0,40,50,self.hero),
            Flying(200, 50, 40, 50,self.hero)
        ]

        self.bosses = [
            Balrog(200, 0, 80, 100, self.hero),
            Ganon(300, 0, 80, 100, self.hero),
            Demagorgon(0, 0, 100, 300, self.hero)
        ]

        self.texts = [
        Text('Hero', type(self.hero).__name__, main.screen, 0, 0, pygame.font.SysFont("Times New Roman", 22)),
        Text('Life', self.hero.life, main.screen, 0, 20, pygame.font.SysFont("Times New Roman", 22))
        ]

        self.Values = [type(self.hero).__name__, self.hero.life]

        self.bg_images = []
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Background_path = os.path.join(path_game, os.pardir, "assets", "Background")
        Background_path = os.path.abspath(Background_path)
        for i in range(1, 4):
            image_path = os.path.join(Background_path, f"background_{i}.png")
            bg_image = pygame.image.load(image_path).convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (self.WIDTH , self.HEIGHT))
            self.bg_images.append(bg_image)
        self.pos_x = -self.WIDTH
        self.pos_x_p = -self.WIDTH
            
    def on_event(self, event, main):
        self.trade(event)
        self.hero.on_event(event)
        
    def on_key_pressed(self):
        key_map = pygame.key.get_pressed()
        self.hero.on_key_pressed(key_map)
        self.hero.actions(key_map)
            
    def update(self):
        self.hero.update()
        self.camera.update_coods(self.hero)
        for ground in self.grounds:
            ground.update()

        for monster in self.enemies:
            monster.update()
            monster.new_hero(self.hero)

        for projectile in self.projectiles:
            projectile.update()

        for boss in self.bosses:
            boss.update()
            boss.new_hero(self.hero)

        self.Values[0] = type(self.hero).__name__  
        self.Values[1] = self.hero.life 

        for i, text in enumerate(self.texts):
            text.update(value=self.Values[i])
        
    def collision_decetion(self):
        for ground in self.grounds:
            is_collision_hero = self.hero.rect.colliderect(ground)
            if is_collision_hero:
                self.hero.on_collision(ground)
                ground.on_collision(self.hero) 
                
            for enemie in self.enemies:
                self.hero.on_collision(enemie)
                enemie.on_collision(self.hero)
                enemie.on_collision(ground)
                ground.on_collision(enemie)

            for boss in self.bosses:
                boss.on_collision(self.hero)
                self.hero.on_collision(boss)
                ground.on_collision(ground)
                boss.on_collision(ground)

    def elimination(self, chage_state):
        for monster in self.enemies:
            if monster.life <= 0:
                self.enemies.remove(monster)

        for boss in self.bosses:
            if boss.is_dead == True:
                self.bosses.remove(boss)

        for projectile in self.projectiles:
                if not self.screen.get_rect().colliderect(projectile.rect):
                    self.projectiles.remove(projectile) 
        
        if self.hero.life <= 0 or self.hero.rect.y > 1400:
            chage_state("over")
                
    def draw(self, screen: pygame.Surface):
        screen.fill([0,0,0])
        
        speed = min(self.hero.speed_x, self.hero.speed_x_max) if self.hero.speed_x > 0 else max(self.hero.speed_x, self.hero.speed_x_min)
        self.pos_x -= speed // 3
        self.pos_x_p -= speed // 5
        x = 0
        for i in self.bg_images:
            for j in range(7):
                screen.blit(i, (self.pos_x +  x * self.pos_x_p + j*self.WIDTH, 0))
            x+=1
        
        self.hero.draw(screen, self.camera)

        for text in self.texts:  
            text.draw()  
            
        for ground in self.grounds:
            ground.draw(screen, self.camera)
        
        for monster in self.enemies:
            monster.draw(screen, self.camera)
            
        for projectile in self.projectiles:
                projectile.draw(screen)

        for boss in self.bosses:
            boss.draw(screen, self.camera)
            
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
        hero_life = self.hero.life
        speed_y_actual = self.hero.speed_y    
        speed_x_actual = self.hero.speed_x
        jump_count_actual = self.hero.jump_count
        is_running_actual = self.hero.is_running
        on_ground_actual = self.hero.on_ground
        to_left_actual = self.hero.to_left
        to_right_actual = self.hero.to_right
        trade_cooldonw_actual  = self.hero.trade_cooldown
        from_the_front_actual = self.hero.from_the_front
            
        self.hero = self.heros[self.atual_hero]
        
        self.hero.rect.x = x_atual 
        self.hero.rect.y = y_atual
        self.hero.life = hero_life
        self.hero.speed_y = speed_y_actual 
        self.hero.speed_x = speed_x_actual
        self.hero.jump_count = jump_count_actual
        self.hero.is_running = is_running_actual
        self.hero.on_ground = on_ground_actual
        self.hero.to_left = to_left_actual
        self.hero.to_right = to_right_actual
        self.hero.trade_cooldown = trade_cooldonw_actual
        self.hero.from_the_front = from_the_front_actual

if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()