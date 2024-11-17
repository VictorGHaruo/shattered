import pygame

class Projectile:
    def __init__(self, x, y, speed_x, speed_y, who, damage, width, height, image = None):
        self.TAG = "Projectile"
        self.rect = pygame.Rect(x, y, width, height) 
        self.color = (0, 0, 255)  
        self.speed_x = speed_x  
        self.speed_y = speed_y
        self.who = who
        self.damage = damage
        if image != None:
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = None

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def draw(self, screen, camera):
        self.rect.x -= camera.position_x
        pygame.draw.rect(screen, self.color, self.rect) 

class Shield:
    def __init__(self, x, y, width, height, damage):
        self.TAG = "Shield"
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height) 
        self.damage = damage
        self.test_color = (100, 100, 100)
    
    def reflect(self, user, other, list1, list2):

        if other.TAG == "Projectile" and self.rect.colliderect(other.rect):
            other.speed_x = -other.speed_x
            print(other.image)
            other.image = pygame.transform.flip(other.image, True, False)
            other.who = user
            other.damage = other.damage * self.damage
            list1.append(other)
            list2.remove(other)

    def update(self, x, y):
        self.rect  = pygame.Rect(x, y, self.width, self.height) 

    def draw(self, screen):
        pygame.draw.rect(screen, self.test_color, self.rect)


class Attack:
    def __init__(self, x, y, width, height, damage):
        self.TAG = "Attack"
        self.rect = pygame.Rect(x, y, width, height)
        self.test_color = (100, 100, 100)
        self.damage = damage

    def draw(self,screen):
        pygame.draw.rect(screen, self.test_color, self.rect)

                        