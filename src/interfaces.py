import pygame, random, os, sys
from game import GameManager
# import time

def f_reset_game(main):
    del main.states["game"]
    main.states["game"] = GameManager(main)
    main.change_state("game", True)

class Button():
    
    def __init__(self, x, y, width, height, images_path):
        self.images_path = images_path
        image_init = pygame.image.load(self.images_path[0]).convert_alpha()
        self.image_init = pygame.transform.scale(image_init, (width, height))
        image_tounching = pygame.image.load(self.images_path[1]).convert_alpha()
        self.image_tounching = pygame.transform.scale(image_tounching, (width, height))
        self.rect = self.image_init.get_rect()
        self.rect.x = x
        self.rect.y = y
                
    def draw(self, screen: pygame.Surface):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
            screen.blit(self.image_tounching, self.rect)
        else:
            screen.blit(self.image_init, self.rect)
        
    def change_state(self, event, main, state, music_bool):
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                main.change_state(state, music_bool)
                
    def reset_game(self, event, main):
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_colission = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_colission:
                f_reset_game(main)
                
    def exit(self, event, main):
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_colission = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_colission:
                main.is_running = False
                
class Menu():
    
    def __init__(self, main):
        
        start_images = [
            os.path.join(main.assets_path, "Interfaces", "start0.png"), 
            os.path.join(main.assets_path, "Interfaces", "start1.png")
        ]
        tutorial_images = [
            os.path.join(main.assets_path, "Interfaces", "tutorial0.png"),
            os.path.join(main.assets_path, "Interfaces", "tutorial1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        
        self.b_start = Button(555, 300, 290, 120, start_images)
        self.b_tutorial = Button(555, 425, 290, 120, tutorial_images)
        self.b_exit = Button(555, 550, 290, 120, quit_images)
        
        #Image
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Menu.png")
        image_menu = pygame.image.load(image_path).convert_alpha()
        self.image_menu = pygame.transform.scale(image_menu, dimention_screen)
    
    def music(self, main, volume):
        if main.is_changed:
            path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
            music_dir_path = os.path.join(os.path.dirname(path_game), "assets", "Music")
            
            music_num = random.randint(1, 2)
            music_path = os.path.join(music_dir_path, "Menu", f"M{music_num}.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_menu, (0,0))
        self.b_start.draw(screen)
        self.b_tutorial.draw(screen)
        self.b_exit.draw(screen)
        
    def on_event(self, event, main):
        self.b_start.change_state(event, main, "game", True)
        
        self.b_tutorial.change_state(event, main, "tutorial", False)
        
        self.b_exit.exit(event, main)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main.change_state("game", True)
        
class Pause():
    
    def __init__(self, main):
        continue_images = [
            os.path.join(main.assets_path, "Interfaces", "continue0.png"),
            os.path.join(main.assets_path, "Interfaces", "continue1.png")
        ]
        restart_images = [
            os.path.join(main.assets_path, "Interfaces", "restart0.png"),
            os.path.join(main.assets_path, "Interfaces", "restart1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        self.b_continue = Button(555, 300, 290, 120, continue_images)
        self.b_restart = Button(555, 425, 290, 120, restart_images)
        self.b_quit = Button(555, 550, 290, 120, quit_images)
        
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Pause.png")
        image_pause = pygame.image.load(image_path).convert_alpha()
        self.image_pause = pygame.transform.scale(image_pause, dimention_screen)
        
    def music(self, main, volume):
        pass
    
    def draw(self, screen):
        screen.blit(self.image_pause, (0,0))
        self.b_continue.draw(screen)
        self.b_restart.draw(screen)
        self.b_quit.draw(screen)
        
    def on_event(self, event, main):
        self.b_continue.change_state(event, main, "game", False)
        
        self.b_restart.reset_game(event, main)
        
        self.b_quit.reset_game(event, main)
        self.b_quit.change_state(event, main, "menu", True)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main.change_state("game", False)
            if event.key == pygame.K_r:
                f_reset_game(main)
            if event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)

class Game_Over():
    
    def __init__(self, main):
        restart_images = [
            os.path.join(main.assets_path, "Interfaces", "restart0.png"),
            os.path.join(main.assets_path, "Interfaces", "restart1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        self.b_restart = Button(555, 350, 290, 120, restart_images)
        self.b_quit = Button(555, 480, 290, 120, quit_images)
        
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Over.png")
        image_pause = pygame.image.load(image_path).convert_alpha()
        self.image_pause = pygame.transform.scale(image_pause, dimention_screen)
    
    def music(self, main, volume):
        if main.is_changed:
            path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
            music_dir_path = os.path.join(os.path.dirname(path_game), "assets", "Music")
            
            music_num = random.randint(1, 2)
            music_path = os.path.join(music_dir_path, "Over", f"D{music_num}.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False
                
    def draw(self, screen):
        screen.blit(self.image_pause, (0,0))
        self.b_restart.draw(screen)
        self.b_quit.draw(screen)

    def on_event(self, event, main):
        self.b_restart.reset_game(event, main)
        
        self.b_quit.reset_game(event, main)
        self.b_quit.change_state(event, main, "menu", True)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                f_reset_game(main)
            elif event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)
                
class Tutorial():
    
    def __init__(self, main):
        
        self.main = main
        self.timer = 100
        self.idx_image = 0
        
        dimention_screen = main.screen.get_size()
        images_path = [
        os.path.join(main.assets_path, "Interfaces", "Controls.png"),
        os.path.join(main.assets_path, "Interfaces", "August.png"),
        os.path.join(main.assets_path, "Interfaces", "Stella.png"),
        os.path.join(main.assets_path, "Interfaces", "Erik.png"),   
        ]
        self.images = []
        for i in range(4):
            image = pygame.image.load(images_path[i]).convert_alpha()
            self.images.append(pygame.transform.scale(image, dimention_screen))
            
    def music(self, main, volume):
        pass
    
    def draw(self, screen):
        self.timer += 1
        if self.timer >= 100 and self.idx_image < 4:
            self.timer = 0
            screen.blit(self.images[self.idx_image], (0,0))
            self.idx_image += 1
        if self.timer >= 100 and self.idx_image >= 4:
            self.main.change_state("menu", False)
            self.timer = 100
            self.idx_image = 0
            
    
    def on_event(self, event, main):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.idx_image > 1:
                    self.timer = 100
                    self.idx_image -= 2
            
            if event.key == pygame.K_RIGHT:
                if self.idx_image < 5:
                    self.timer = 100
                                
            if event.key == pygame.K_q:
                main.change_state("menu", False)
                self.timer = 100
                self.idx_image = 0
                
            