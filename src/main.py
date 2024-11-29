import pygame, os, sys
from interfaces import Menu, Game_Over, Pause
from game import GameManager
import random

pygame.init()

class Main():
    
    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.is_running = True
        self.states = {
            "menu": Menu(self),
            "game": GameManager(self),
            "pause": Pause(self),
            "over": Game_Over(self)
        }
        self.current_state = self.states["menu"]
        self.is_changed = False
        self.volume = 0.15
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        music_dir_path = os.path.join(os.path.dirname(path_game), "assets", "Music")
        music_num = random.randint(1, 2)
        music_path = os.path.join(music_dir_path, "Menu", f"M{music_num}.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)  
        
    def run(self):
        clock = pygame.time.Clock()
        
        while self.is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.current_state == self.states["game"]:
                        self.change_state("pause", False)
                        break
                self.current_state.on_event(event, self)
                
            if self.current_state == self.states["game"]:
                self.current_state.on_key_pressed()
                self.current_state.update()
                self.current_state.collision_decetion()
                self.current_state.elimination(self.change_state)
            self.current_state.music(self, self.volume)
            self.current_state.draw(self.screen)
            pygame.display.flip()
            clock.tick(30)
    
    def change_state(self, state, music_bool):
        self.current_state = self.states[state]
        self.is_changed = music_bool
            
if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()