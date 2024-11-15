import pygame

class Ground:
    
    def __init__(self, x, y, width, height, image_path):
        self.TAG = "Ground"
        self.sub_TAG = "Ground"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
     
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            screen.blit(self.image, self.rect)

    def update(self):
        pass
        
    def on_collision(self, other):
        pass
               
class Block(Ground):
    
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Block"
        self.gravity_y = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.is_pushing_r = False
        self.is_pushing_l = False
        
    def update(self):
        super().update()
        
        self.speed_y += self.gravity_y
        self.rect.y += min(self.speed_y, self.speed_y_max)
        
        if self.is_pushing_r:
            self.rect.x -= 1.5
            self.is_pushing_r = False
        if self.is_pushing_l:
            self.rect.x += 1.5
            self.is_pushing_l = False
            
    def on_collision(self, other):
        super().on_collision(other)
        
        if other.TAG == "Ground" and self.rect.colliderect(other.rect):
            if self.rect.bottom > other.rect.top and self.rect.top < other.rect.top:
                self.rect.bottom = other.rect.top
                self.speed_y = 0
        
        if other.TAG == "Player" and other.rect.colliderect(self.rect) and other.can_push_block:
            if other.speed_x > 0 and self.rect.top < other.rect.top:
                self.is_pushing_l = True
            if other.speed_x < 0 and self.rect.top < other.rect.top:
                self.is_pushing_r = True
        
    def draw(self, screen, camera):
        super().draw(screen, camera)
                
class Spike(Ground):
    
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Spike"
    
class Invsible(Ground):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Invisible"
        
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x

class Obelisk():
    
    def __init__(self, x, y, width, height, image_path):
        self.TAG = "Obelisk"
        self.sub_TAG = "Obelisk"
        self.sheet_im = pygame.image.load(image_path).convert_alpha()
        self.images = []
        for i in range(14):
            image = self.sheet_im.subsurface((i*190, 0), (190, 380))
            image = pygame.transform.scale(image, (width, height))
            self.images.append(image)
        self.num_image = 0
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.touched = False
    
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            if self.touched and self.num_image < 14:
                screen.blit(self.images[int(self.num_image)], self.rect)
                self.num_image += 0.25
            else: 
                screen.blit(self.images[0], self.rect)
                self.num_image = 0
                self.touched = False
            
    def on_collision(self, other):
        pass
            
    def update(self):
        pass
