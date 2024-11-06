import pygame

class Monsters:
    def __init__(self, x, y, width, height):
        self.TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 50

    def on_key_pressed(self, key_map):
        if key_map[pygame.K_RIGHT]:
            self.rect.x += 10
        if key_map[pygame.K_LEFT]:
            self.rect.x -= 10

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)
        
    def draw (self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            pygame.draw.rect(screen, self.color, self.rect)

    def on_collision(self, other : pygame.Rect):  

        if other.TAG == "Ground":
            if self.rect.left < other.rect.right and self.rect.right > other.rect.right:
                self.speed_x *= -1
            if self.rect.right > other.rect.left and self.rect.left < other.rect.left:
                self.speed_x *= -1
            if self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                    self.rect.bottom = other.rect.top

        if other.TAG == "Player": #Mata o monstro
            if self.rect.top < other.rect.bottom and self.rect.bottom > other.rect.bottom:
                self.life = 0

class Dummy(Monsters):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed_x = 3

    def update(self):
        self.move()
        return super().update()
        
    def move(self):
        self.rect.x = self.rect.x + self.speed_x
