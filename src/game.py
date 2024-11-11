import pygame
import sys
from player import Knight, Yokai, Ninja
from camera import Camera
from ground import Ground, Block
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
        self.camera = Camera(0, 50)
    
        self.grounds = []
        self.maping()
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
        for i in range(1, 3):
            bg_image = pygame.image.load(f"../assets/Background/background_layer_{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (self.WIDTH , self.HEIGHT))
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()
            
    def on_event(self, event, main):
        self.trade(event)
        self.hero.on_event(event)
        
    def on_key_pressed(self):
        key_map = pygame.key.get_pressed()
        self.hero.on_key_pressed(key_map)
        self.hero.actions(key_map)
            
    def update(self, WIDTH):
        self.hero.update()
        self.camera.update_coods(self.hero, WIDTH)
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

    def maping(self):
        
        grid = [
            "                                                                                                     XXXXXXXXXXXXXXXXXXXXXXXX",
            "                                                                                                     XXXXXXXXXXXXXXXXXXXXXXXX",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                                                                                                     X                      X",
            "                    EXXXXXXXXD                                                                                              X",
            "                    LGGGGGGGGR                                                                                              X",
            "             TMP    LGGGGGGGGR   TP                                   TP                                                    X",
            "                    LGGGGGGGGR                                                                                              X",
            "XXXXXXXXD           LGGGGGGGGR        EXXXXXXXXXXXXXD         EXXXD              EXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "GGGGGGGGR           LGGGGGGGGR        LGGGGGGGGGGGGGR         LGGGR              LGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
            "GGGGGGGGR           LGGGGGGGGR        LGGGGGGGGGGGGGR   TMP   LGGGR        TMP   LGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        ]
        
        self.grounds_apend(grid)
        
    def grounds_apend(self, grid):
        
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        assets_path = os.path.join(path_game, os.pardir, "assets")
        assets_path = os.path.abspath(assets_path)
        image_ground_X = os.path.join(assets_path, "Ground", "Ground_01.png")
        image_ground_E = os.path.join(assets_path, "Ground", "Ground_02.png")
        image_ground_G = os.path.join(assets_path, "Ground", "Ground_04.png")
        image_ground_D = os.path.join(assets_path, "Ground", "Ground_06.png")
        image_ground_L = os.path.join(assets_path, "Ground", "Ground_07.png")
        image_ground_T = os.path.join(assets_path, "Ground", "Ground_08.png")        
        image_ground_M = os.path.join(assets_path, "Ground", "Ground_09.png")
        image_ground_P = os.path.join(assets_path, "Ground", "Ground_10.png")
        image_ground_R = os.path.join(assets_path, "Ground", "Ground_11.png")
        
        
        i_range = len(grid)
        j_range = len(grid[0])
        for i in range(i_range):
            for j in range(j_range):
                if grid[i][j] == "X":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_X))
                if grid[i][j] == "E":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_E))
                if grid[i][j] == "G":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_G))
                if grid[i][j] == "D":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_D))
                if grid[i][j] == "L":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_L))
                if grid[i][j] == "R":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_R))
                if grid[i][j] == "T":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_T))
                if grid[i][j] == "M":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_M))
                if grid[i][j] == "P":
                    self.grounds.append(Ground(j*50, i*50, 50, 50, image_ground_P))
                

    def elimination(self, chage_state):
        for monster in self.enemies:
            if monster.life <= 0:
                self.enemies.remove(monster)

        for boss in self.bosses:
            if boss.life <= 0:
                self.bosses.remove(boss)

        for projectile in self.projectiles:
                if not self.screen.get_rect().colliderect(projectile.rect):
                    self.projectiles.remove(projectile) 
        
        if self.hero.life <= 0 or self.hero.rect.y > 1400:
            chage_state("over")
                
    def draw(self, screen: pygame.Surface):
        screen.fill([0,0,0])
        scroll = self.camera.position_x
        
        # path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        # assets_path = os.path.join(path_game, os.pardir, "assets")
        # assets_path = os.path.abspath(assets_path)
        
        # background_path = os.path.join(assets_path, "Background", "Background_01.png")
        # background = pygame.image.load(background_path).convert_alpha()
        # background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        for x in range(2):
            speed = 1
            for i in self.bg_images:
                screen.blit(i, ((x * self.bg_width) - scroll * speed, 0))
                speed += 0.6
        
        # background_2_path = os.path.join(assets_path, "Background", "Background_02.png")
        # background_2 = pygame.image.load(background_2_path).convert_alpha()
        # background_2 = pygame.transform.scale(background_2, (self.WIDTH, self.HEIGHT))
        # screen.blit(background_2, (0,0))
        
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