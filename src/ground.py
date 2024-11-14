import pygame
import os
import sys

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

         
def maping(grounds):
    
    grid = [
        "                                                                                                     I                             CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "                                                                                                     I                             CC                          CC",
        "                                                                                                   O I                             CC                          CC",
        "                                                                      TMMP         TMMMP         TMMMP                             CC                          CC",
        "                                                                                                                                   CC                          CC",
        "                                                         TMMMP                                                                     CC                          CC",
        "                                                                                                                                   CC                          CC",
        "                                                                                                                                   CC                          CC",
        "                                                                                                                                   CC                          CC",
        "                              EXXXXXXXXXXXXXXXXXD                                                                                  CC                          CC",
        "                              LGGGGGGGGGGGGGGGGGR                                                                                  CC                          CC",
        "                    TMMMMP    LGGGGGGGGGGGGGGGGGR                                                                                  CC                          CC",
        "  O   B                       LGGGGGGGGGGGGGGGGGR   TMP                                                                             B                          CC",
        "XXXXXXX XXXXXXXD              LGGGGGGGGGGGGGGGGGR        EXXXXXXXXXXXXXXXXXXD           EXXXD                       EXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGR   EXXD    LGGGR    EXXXXXXXD    EXD   LGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGRSSSLGGRSSSSLGGGRSSSSLGGGGGGGRSSSSLGRSSSLGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    ]
    
    path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
    Ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
    Ground_path = os.path.abspath(Ground_path)
    image_ground_X = os.path.join(Ground_path, "Ground_01.png")
    image_ground_E = os.path.join(Ground_path, "Ground_02.png")
    image_ground_G = os.path.join(Ground_path, "Ground_04.png")
    image_ground_D = os.path.join(Ground_path, "Ground_06.png")
    image_ground_L = os.path.join(Ground_path, "Ground_07.png")
    image_ground_T = os.path.join(Ground_path, "Ground_08.png")        
    image_ground_M = os.path.join(Ground_path, "Ground_09.png")
    image_ground_P = os.path.join(Ground_path, "Ground_10.png")
    image_ground_R = os.path.join(Ground_path, "Ground_11.png")
    image_ground_B = os.path.join(Ground_path, "Wooden_Box.png")
    image_spike_S = os.path.join(Ground_path, "Spikes.png")
    image_obelisk_O = os.path.join(Ground_path, "Obelisk.png")
    image_ground_C = os.path.join(Ground_path, "Brick_02_p.png")
    
    keys_ground = [
        ["X", image_ground_X], ["E", image_ground_E], ["G", image_ground_G], ["D", image_ground_D],
        ["L", image_ground_L], ["T", image_ground_T], ["M", image_ground_M], ["P", image_ground_P],
        ["R", image_ground_R], ["C", image_ground_C]
    ] 
    
    i_range = len(grid)
    j_range = len(grid[0])
    for i in range(i_range):
        for j in range(j_range):
            if grid[i][j] == "O":
                grounds.append(Obelisk(j*50, i*50 - 185, 150, 250, image_obelisk_O))
            if grid[i][j] == "I":
                grounds.append(Invsible(j*50, i*50, 50, 50, image_ground_X))
            if grid[i][j] == "S":
                grounds.append(Spike(j*50, i*50, 50, 50, image_spike_S))    
            if grid[i][j] == "B":
                grounds.append(Block(j*50, i*50, 40, 52, image_ground_B))                
            for key in keys_ground:
                if grid[i][j] == key[0]:
                    grounds.append(Ground(j*50, i*50, 50, 50, key[1]))