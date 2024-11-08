import pygame

class Projectile:
    def __init__(self, x, y, speed_x, speed_y, who, damage):
        self.TAG = "Projectile"
        self.rect = pygame.Rect(x, y, 15, 15) 
        self.color = (0, 0, 255)  
        self.speed_x = speed_x  
        self.speed_y = speed_y
        self.who = who
        self.damage = damage

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Shield:
    def __init__(self, x, y, width, height):
        self.TAG = "Shield"
        self.rect = pygame.Rect(x, y, width, height) 
    
    def reflect(self, user,other):

        if other.TAG == "Projectile" and self.rect.colliderect(other.rect):
            other.speed_x = -other.speed_x
            other.TAG = user

class Attack:
    def __init__(self, x, y, width, height):
        self.TAG = "Attack"
        self.rect = pygame.Rect(x, y, width, height)

    def strike(self, damage, other):
        if other.TAG == "Monster" and self.rect.colliderect(other.rect):
            other.life =  other.life - damage
                        