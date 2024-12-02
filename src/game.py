import pygame
from player import Knight, Yokai, Ninja
from camera import Camera
from maker import maping
from boss import Balrog, Ganon, Demagorgon
from assets import Herolife, Bar, Bosslife
import os, sys, random
           
class GameManager:

    def __init__(self, main):
        self.heros = [
            Knight(0 , 0, 40, 70),
            Yokai(0 , 0, 40, 70),
            Ninja(0 , 0, 40, 70)
        ]
        self.atual_hero = 0
        self.hero = self.heros[self.atual_hero]
        
        self.camera = Camera(0, main.WIDTH)
    
        self.grounds = []
        self.enemies = []
        maping(self.grounds, self.enemies, self.hero)
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
        self.main = main
        

        self.bosses = [
            # Balrog(200, 100, 140, 180, self.hero),
            # Ganon(300, 0, 150, 220, self.hero),
            # Demagorgon(0, 0, 100, 300, self.hero)
        ]
        
        self.order = [
            Demagorgon(0, 0, 100, 300, self.hero),
            Balrog(200, 100, 140, 180, self.hero),
            Ganon(300, 0, 150, 220, self.hero),
        ]

        self.life_bar = Herolife(self.hero, 400, 20, 10)
        self.hero_timer = Bar(self.hero.trade_cooldown_time, 20, 30, 100, 20, (255,255,255), (0,0, 255))
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
        self.bg_boss = pygame.transform.scale(self.bg_boss, (self.WIDTH, self.HEIGHT))
        
        for i in range(1, 4):
            image_path = os.path.join(Background_path, f"background_{i}.png")
            bg_image = pygame.image.load(image_path).convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (self.WIDTH , self.HEIGHT))
            self.bg_images.append(bg_image)
        self.pos_x = -self.WIDTH
        self.pos_x_p = -self.WIDTH
            
    def music(self, main, volume):
        if main.is_changed:
            path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
            music_dir_path = os.path.join(os.path.dirname(path_game), "assets", "Music")
            
            if self.camera.boss_fase:
                music_num = random.randint(1, 2)
                music_path = os.path.join(music_dir_path, "Boss", f"B{music_num}.mp3")
                pygame.mixer.music.load(music_path)
            elif self.hero.can_push_block:
                music_num = random.randint(1, 3)
                music_path = os.path.join(music_dir_path, "Obelisk", f"O{music_num}.mp3")
                pygame.mixer.music.load(music_path)
            else:    
                music_num = random.randint(1, 3)
                music_path = os.path.join(music_dir_path, "World", f"W{music_num}.mp3")
                pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False
            
    def on_event(self, event, main):
        self.trade(event)
        self.hero.on_event(event, self.main)
        
    def on_key_pressed(self):
        key_map = pygame.key.get_pressed()
        self.hero.on_key_pressed(key_map, self.main)
        self.hero.actions(key_map)
            
    def update(self):
        self.hero.update()
        self.life_bar.update(self.hero)
        self.hero_timer.update(self.hero.trade_cooldown)
        self.camera.update_coods(self.hero, self.main)

        if len(self.bosses) == 0:
            if len(self.order) != 0:
                self.bosses.append(self.order[0])
                del self.order[0]

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
        
        if self.hero.Death:
            chage_state("over", True)
                
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