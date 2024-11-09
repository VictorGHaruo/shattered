import pygame

class Button():
    
    def __init__(self, x, y, width, height, text, callback, fontsize=36):
        self.callback = callback
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, fontsize)
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "grey", self.rect)
        text_box = self.font.render(self.text, True, "black")
        text_box_rect = text_box.get_rect(center = self.rect.center)
        screen.blit(text_box, text_box_rect)
        
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                self.callback("game")

class Menu():
    
    def __init__(self, main):
        self.button = Button(650, 380, 100, 20, "Start", main.change_state)
    
    def draw(self, screen: pygame.Surface):
        screen.fill((0,0,0))
        self.button.draw(screen)
        
    def on_event(self, event):
        self.button.on_event(event)
