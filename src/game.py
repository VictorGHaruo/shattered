import pygame
import sys
from player import Knight, Yokai, Ninja
from camera import Camera
from ground import Ground, Block
from maker import maping
from enemy import Dummy, Mage, Flying
from boss import Balrog, Ganon, Demagorgon
from assets import Herolife
from assets import Bar
from assets import Bosslife
import os
import sys


pygame.init()
           
class GameManager:

    def __init__(self, main):
        self.heros = [
            Knight(0 , 0, 40, 50),
            Yokai(0 , 0, 40, 50),
            Ninja(0 , 0, 40, 50)
        ]
        self.atual_hero = 2
        self.hero = self.heros[self.atual_hero]
        
        self.camera = Camera(0, main.WIDTH)
    
        self.grounds = []
        self.enemies = []
        maping(self.grounds, self.enemies, self.hero)
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
        

        self.bosses = [
            # Balrog(200, 0, 80, 100, self.hero),
            Ganon(300, 0, 150, 220, self.hero),
            # Demagorgon(0, 0, 100, 300, self.hero)
        ]

        self.life_bar = Herolife(self.hero, 400, 20, 5)
        self.hero_timer = Bar(self.hero.trade_cooldown_time, 20, 20, 100, 20, (255,255,255), (0,0,0))
        # Trade keys
        self.keys_trade = [
                    "rect", "life", "speed_x", "speed_y", "jump_count", "is_running",
                    "on_ground", "to_left", "to_right", "from_the_front",
                    "invincibility_time", "projectiles", "touched_obelisk", "can_push_block"
                ]

        ##BackGround
        self.bg_images = []
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Background_path = os.path.join(path_game, os.pardir, "assets", "Background")
        Background_path = os.path.abspath(Background_path)
        
        image_path = os.path.join(Background_path, "boss_fase.png")
        self.bg_boss = pygame.image.load(image_path).convert_alpha()
        self.bg_boss = pygame.transform.scale(self.bg_boss, (self.WIDTH , self.HEIGHT))
        
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
        
    def on_key_pressed(self, main):
        key_map = pygame.key.get_pressed()
        self.hero.on_key_pressed(key_map, main)
        self.hero.actions(key_map)
            
    def update(self):
        self.hero.update()
        self.life_bar.update(self.hero)
        self.hero_timer.update(self.hero.trade_cooldown)
        self.camera.update_coods(self.hero)
        for ground in self.grounds:
            ground.update()

        for monster in self.enemies:
            monster.update()
            monster.new_hero(self.hero)

        # for projectile in self.projectiles:
        #     projectile.update()

        for boss in self.bosses:
            boss.update()
            boss.new_hero(self.hero)

    def collision_decetion(self):
        for ground in self.grounds:
            
            ground.on_collision(self.hero)
            self.hero.on_collision(ground)
                
            for enemie in self.enemies:
                self.hero.on_collision(enemie)
                enemie.on_collision(self.hero)
                enemie.on_collision(ground)
                ground.on_collision(enemie)

            for boss in self.bosses:
                boss.on_collision(self.hero)
                self.hero.on_collision(boss)
                ground.on_collision(boss)
                boss.on_collision(ground)
                
            if ground.sub_TAG == "Block":
                for gro in self.grounds:
                    ground.on_collision(gro)

    def elimination(self, chage_state):
        for monster in self.enemies:
            if monster.is_dead:
                self.enemies.remove(monster)
                del monster

        for boss in self.bosses:
            if boss.is_dead == True:
                self.bosses.remove(boss)
                del boss
        
        if self.hero.life <= 0 or self.hero.rect.y > 1000:
            chage_state("over")
                
    def draw(self, screen: pygame.Surface):
        screen.fill([0,0,0])

        ## Paralax
        if self.hero.speed_x > 0: 
            speed = min(self.hero.speed_x, self.hero.speed_x_max) 
        else :
            speed = max(self.hero.speed_x, self.hero.speed_x_min)
        if self.camera.fix_x >= 690:
            speed = 0
        
        self.pos_x -= speed // 3
        self.pos_x_p -= speed // 5
        x = 0
        for i in self.bg_images:
            for j in range(8):
                screen.blit(i, (self.pos_x +  x * self.pos_x_p + j*self.WIDTH, 0))
            x += 1
        ## Boss fase (132 * 50) + self.camera.position_x
        screen.blit(self.bg_boss, ( ((132 * 50) - 700) + self.camera.fix_x, 0))        
            
        for ground in self.grounds:
            ground.draw(screen, self.camera)
        
        for monster in self.enemies:
            monster.draw(screen, self.camera)

        for boss in self.bosses:
            boss.draw(screen, self.camera)
            
        self.hero.draw(screen, self.camera)
        self.life_bar.draw(screen)
        self.hero_timer.draw(screen)  
            
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
                state_dict = self.hero.__dict__
                
                self.hero = self.heros[self.atual_hero]
                
                for key in self.keys_trade:     
                    self.hero.__dict__[key] = state_dict[key]
                    
                self.hero.trade_cooldown = self.hero.trade_cooldown_time

if __name__ == "__main__":
    Game = GameManager()
    Game.run()
    pygame.quit()