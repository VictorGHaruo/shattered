import pygame
from menu import Menu
from game import GameManager

class Main():
    
    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.states = {
            "menu": Menu(self),
            "game": GameManager(self)
        }
        self.current_state = self.states["menu"]
        
    def run(self):
        clock = pygame.time.Clock()
        
        is_running = True
        while is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False
                self.current_state.on_event(event)
                
            if self.current_state == self.states["game"]:
                self.current_state.on_key_pressed()
                self.current_state.update(self.WIDTH)
                self.current_state.collision_decetion()
                self.current_state.elimination()
            self.current_state.draw(self.screen)
            pygame.display.flip()
            
            clock.tick(30)
    
    def change_state(self, state):
        self.current_state = self.states[state]
            
if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()