import pygame
from game import GameManager

class Button():
    
    def __init__(self, x, y, width, height, text, fontsize=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, fontsize)
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "grey", self.rect)
        text_box = self.font.render(self.text, True, "black")
        text_box_rect = text_box.get_rect(center = self.rect.center)
        screen.blit(text_box, text_box_rect)
        
    def on_event(self, event, change_state, state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                change_state(state)

class Menu():
    
    def __init__(self, main):
        self.button = Button(575, 350, 250, 45, "Start")
    
    def draw(self, screen: pygame.Surface):
        screen.fill((0,0,0))
        self.button.draw(screen)
        
    def on_event(self, event, main):
        self.button.on_event(event, main.change_state, "game")
        
class Pause():
    
    def __init__(self, main):
        self.button = Button(575, 350, 250, 45, "Continue")
        
    def draw(self, screen):
        screen.fill((0,0,0))
        self.button.draw(screen)
        
    def on_event(self, event, main):
        self.button.on_event(event, main.change_state, "game")

class Game_Over():
    
    def __init__(self, main):
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
        self.change_state = main.change_state
        
    def draw(self, screen):
        screen.fill([100, 100, 100])
        font_gameover = pygame.font.Font(None, 74)
        font_control = pygame.font.Font(None, 36)
        
        text_gameover = font_gameover.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_gameover.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
        screen.blit(text_gameover, text_rect)

        text_control = font_control.render("Press 'R' to restart or 'Q' to exit.", True, (50, 50, 50))
        control_rect = text_control.get_rect(center=(self.WIDTH// 2, self.HEIGHT // 2))
        screen.blit(text_control, control_rect)

    def on_event(self, event, main):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                del main.states["game"]
                main.states["game"] = GameManager(main)
                self.change_state("game")
            elif event.key == pygame.K_q:
                main.is_running = False