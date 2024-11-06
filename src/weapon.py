import pygame

class Projectile:
    def __init__(self, x, y, speed_x, speed_y, who):
        self.TAG = "Projectile"
        self.rect = pygame.Rect(x, y, 15, 15) 
        self.color = (0, 0, 255)  
        self.speed_x = speed_x  
        self.speed_y = speed_y
        self.who = who

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)