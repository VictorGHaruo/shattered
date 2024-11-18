import pygame, random
from game import GameManager

class Button():
    
    def __init__(self, x, y, width, height, text, fontsize=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, fontsize)
        
    def draw(self, screen: pygame.Surface, bool):
        if bool:
            pygame.draw.rect(screen, "grey", self.rect)
        text_box = self.font.render(self.text, True, "white")
        text_box_rect = text_box.get_rect(center = self.rect.center)
        screen.blit(text_box, text_box_rect)
        
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
        self.b_start = Button(575, 345, 250, 50, "Start")
        self.b_exit = Button(575, 405, 250, 50, "Exit game")
        self.title = pygame.font.Font(None, 74)
        self.title = self.title.render("Shattered", True, "White")
        self.text_rect = self.title.get_rect(center=(main.WIDTH // 2, 300))
    
    def music(self, main, volume):
        if main.is_changed:
            music_num = random.randint(1, 2)
            pygame.mixer.music.load(f"../assets/Music/Menu/M{music_num}.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()  
        main.is_changed = False
    
    def draw(self, screen: pygame.Surface):
        screen.fill((0,0,0))
        screen.blit(self.title, self.text_rect)
        self.b_start.draw(screen, True)
        self.b_exit.draw(screen, True)
        
    def on_event(self, event, main):
        self.b_start.change_state(event, main, "game", True)
        self.b_exit.exit(event, main)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main.change_state("game", True)
        
class Pause():
    
    def __init__(self, main):
        self.b_continue = Button(575, 320, 250, 50, "Continue")
        self.b_restart = Button(575, 375, 250, 50, "Restart")
        self.b_quit = Button(575, 430, 250, 50, "Quit")
        
    def music(self, main, volume):
        pass
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.b_continue.draw(screen, True)
        self.b_restart.draw(screen, True)
        self.b_quit.draw(screen, True)
        
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
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
    
    def music(self, main, volume):
        if main.is_changed:
            music_num = random.randint(1, 2)
            pygame.mixer.music.load(f"../assets/Music/Over/D{music_num}.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()  
        main.is_changed = False
                
    def draw(self, screen):
        screen.fill([100, 100, 100])
        font_gameover = pygame.font.Font(None, 74)
        font_control = pygame.font.Font(None, 36)
        
        text_gameover = font_gameover.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_gameover.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
        screen.blit(text_gameover, text_rect)

        text_control = font_control.render("Press 'R' to restart or 'Q' to quit.", True, (50, 50, 50))
        control_rect = text_control.get_rect(center=(self.WIDTH// 2, self.HEIGHT // 2))
        screen.blit(text_control, control_rect)

    def on_event(self, event, main):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                f_reset_game(main)
            elif event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)
                
def f_reset_game(main):
    del main.states["game"]
    main.states["game"] = GameManager(main)
    main.change_state("game", True)
    
    

    # if main.save_state != {}:
    #     main.states["game"].__dict__ = main.save_state