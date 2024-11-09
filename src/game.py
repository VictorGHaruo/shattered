import pygame
import sys
from player import Knight, Yokai, Ninja
from camera import Camera
from ground import Ground, Block
from enemy import Dummy, Mage, Flying
from boss import Balrog, Ganon
from text import Text
import os
import sys

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
    
        self.grounds = []
        self.maping()
        
        self.enemies = [
            Dummy(self.WIDTH  // 2 + 200, self.HEIGHT // 2, 40, 50, self.hero),
            Mage(200,0,40,50,self.hero),
            Flying(200, 50, 40, 50,self.hero)
        ]

        self.bosses = [
            # Balrog(200, 0, 80, 100),
            # Ganon(300, 0, 80, 100)
        ]

        self.texts = [
        Text('Hero', type(self.hero).__name__, self.screen, 0, 0, pygame.font.SysFont("Times New Roman", 22)),
        Text('Life', self.hero.life, self.screen, 0, 20, pygame.font.SysFont("Times New Roman", 22))
        ]

        self.Values = [type(self.hero).__name__, self.hero.life]

        
    def run(self):

        clock = pygame.time.Clock()
        is_running = True
        game_over = False

        is_running = True
        while is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False
                self.trade(event)
                self.hero.on_event(event)
            
            if not game_over:
                key_map = pygame.key.get_pressed()
                self.hero.on_key_pressed(key_map)
                self.hero.actions(key_map)
                
                self.update()
                self.collision_decetion()
                self.elimination()
                self.draw()

                if self.hero.life <= 0 or self.hero.rect.y > 1400:  
                    game_over = True
                    self.gameover() 
            else:
                self.gameover()  
                
            clock.tick(30)
        
        pygame.quit()
            
    def update(self):
        self.hero.update()
        self.camera.update_coods(self.hero, self.WIDTH)
        for ground in self.grounds:
            ground.update()

        for monster in self.enemies:
            monster.update()

        for projectile in self.projectiles:
            projectile.update()

        for boss in self.bosses:
            boss.update()
            if boss.TAG =="Ganon":
                boss.move(self.hero)
                boss.attack(self.projectiles, self.hero.rect.x)

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
                is_collision_boss = boss.rect.colliderect(ground)
                if is_collision_boss:
                    ground.on_collision(ground)
                    boss.on_collision(ground)

    def maping(self):
        
        grid = [
            "                                                             XXXXXXXXX",
            "                                                             XXXXXXXXX",
            "                                                             X       X",
            "                                                             X       X",
            "                                                             X       X",
            "                                                             X       X",
            "                                                             X       X",
            "                                                             X       X",
            "                                                             X       X",
            "         XXXXXXX                                                     X",
            "         X     X                                                     X",
            "      XXX       XX                   XX                              X",
            "      X          X                   XX                              X",
            "XXXXXX            XXXXXXXXXXXXX   XXX  X   XXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "                              X   X X  X   X                          ",
            "                               XXX      XXX                           ",
        ]
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        imagem_chão = os.path.join(path_game, os.pardir, "assets", "piso_terra_crop.png")
        imagem_chão = os.path.abspath(imagem_chão)
        print(imagem_chão)
        self.grounds_apend(grid, imagem_chão)
        
    def grounds_apend(self, grid, image_path):
        
        i_range = len(grid)
        j_range = len(grid[0])
        for i in range(i_range):
            for j in range(j_range):
                if grid[i][j] == "X":
                    self.grounds.append(Ground(j*150, i*50, 150, 50, image_path))
                

    def elimination(self):
        for monster in self.enemies:
            if monster.life <= 0:
                self.enemies.remove(monster)

        for boss in self.bosses:
            if boss.life <= 0:
                self.bosses.remove(boss)
        
        for projectile in self.projectiles:
                if not self.screen.get_rect().colliderect(projectile.rect):
                    self.projectiles.remove(projectile)
                
    def draw(self):
        self.screen.fill([0,0,0])
        self.hero.draw(self.screen, self.camera)

        for text in self.texts:  
            text.draw()  

            
        for ground in self.grounds:
            ground.draw(self.screen, self.camera)
        
        for monster in self.enemies:
            monster.draw(self.screen, self.camera)
            
        for projectile in self.projectiles:
                projectile.draw(self.screen)

        for boss in self.bosses:
            boss.draw(self.screen, self.camera)

                
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
        from_the_front_actual = self.hero.from_the_front
            
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
        self.hero.from_the_front = from_the_front_actual

    
    def gameover(self):
        
        self.screen.fill([100, 100, 100])
        font_gameover = pygame.font.Font(None, 74)
        font_control = pygame.font.Font(None, 36)
        
        text_gameover = font_gameover.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_gameover.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
        self.screen.blit(text_gameover, text_rect)

        text_control = font_control.render("Press 'R' to restart or 'Q' to exit.", True, (50, 50, 50))
        control_rect = text_control.get_rect(center=(self.WIDTH// 2, self.HEIGHT // 2))
        self.screen.blit(text_control, control_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  
                        self.reset()
                        waiting = False
                        self.run()
                    elif event.key == pygame.K_q:  
                        pygame.quit()
                        sys.exit()

    def reset(self):

        self.hero = self.heros[self.atual_hero]  
        self.hero.life = 200  
        self.hero.rect.x = self.WIDTH // 2  
        self.hero.rect.y = self.HEIGHT // 2  
        self.hero.speed_x = 0  
        self.hero.speed_y = 0  
        self.hero.jump_count = 0  
        self.hero.is_running = False  
        self.hero.on_ground = True  
        
        self.projectiles = []
        self.camera = Camera(0, 50)
        
        self.enemies = [
            Dummy(self.WIDTH  // 2 + 200, self.HEIGHT // 2, 40, 50),
            Mage(200,0,40,50),
            Flying(200, 50, 40, 50)
        ]

        self.bosses = [
            Balrog(200, 0, 80, 100),
            Ganon(300, 0, 80, 100)
        ]

if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()