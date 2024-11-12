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
        
        self.speed_x = 0
        self.is_pushing_r = False
        self.is_pushing_l = False
        self.rect_color = (0,255,0)
     
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
        
    def update(self):
        super().update()
    
        if self.is_pushing_r:
            self.rect.x += 1
            self.is_pushing_r = False
        if self.is_pushing_l:
            self.rect.x -= 1
            self.is_pushing_l = False
            
    def on_collision(self, other):
        super().on_collision(other)
        
        if other.TAG == "Player":
            if self.rect.left < other.rect.right and self.rect.top < other.rect.bottom:
                self.is_pushing_l = True
            if self.rect.right > other.rect.left and self.rect.top < other.rect.bottom:
                self.is_pushing_r = True
        if other.TAG == "Projectile":
            other.who.projectiles.remove(other)
            del other
                
class Spike(Ground):
    
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Spike"
    
class Invsible(Ground):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        
    def draw(self, screen, camera):
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
         
def maping(grounds):
    
    grid = [
        "I                                                                                                     I                              XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "I                                                                                                     I                              XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "I                                                                                                     N                              X                          X",
        "I                                                                      TMMP         TMMMP         TMMMP                              X                          X",
        "I                                                                                                                                    X                          X",
        "I                                                         TMMMP                                                                      X                          X",
        "I                                                                                                                                    X                          X",
        "I                                                                                                                                    X                          X",
        "I                                                                                                                                    X                          X",
        "I                              EXXXXXXXXXXXXXXXXXD                                                                                   X                          X",
        "I                              LGGGGGGGGGGGGGGGGGR                                                                                   X                          X",
        "I                    TMMMMP    LGGGGGGGGGGGGGGGGGR   TP                                                                              X                          X",
        "I                              LGGGGGGGGGGGGGGGGGR                                                                                   X                          X",
        "IXXXXXXXXXXXXXXXD              LGGGGGGGGGGGGGGGGGR        EXXXXXXXXXXXXXXXXXXD           EXXXD                                                                  X",
        "IGGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGR   EXXD    LGGGR    ED  EXXXD     ED   EXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "IGGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGRSSSLGGRSSSSLGGGRSSSSLRSSLGGGRSSSSSLRSSSLGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    ]
    
    path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
    assets_path = os.path.join(path_game, os.pardir, "assets")
    assets_path = os.path.abspath(assets_path)
    image_ground_X = os.path.join(assets_path, "Ground", "Ground_01.png")
    image_ground_E = os.path.join(assets_path, "Ground", "Ground_02.png")
    image_ground_G = os.path.join(assets_path, "Ground", "Ground_04.png")
    image_ground_D = os.path.join(assets_path, "Ground", "Ground_06.png")
    image_ground_L = os.path.join(assets_path, "Ground", "Ground_07.png")
    image_ground_T = os.path.join(assets_path, "Ground", "Ground_08.png")        
    image_ground_M = os.path.join(assets_path, "Ground", "Ground_09.png")
    image_ground_P = os.path.join(assets_path, "Ground", "Ground_10.png")
    image_ground_R = os.path.join(assets_path, "Ground", "Ground_11.png")
    image_ground_S = os.path.join(assets_path, "Ground", "Spikes.png")
    image_ground_N = os.path.join(assets_path, "Ground", "Stone.png")
    
    
    i_range = len(grid)
    j_range = len(grid[0])
    for i in range(i_range):
        for j in range(j_range):
            if grid[i][j] == "X":
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_X))
            if grid[i][j] == "E":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_E))
            if grid[i][j] == "G":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_G))
            if grid[i][j] == "D":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_D))
            if grid[i][j] == "L":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_L))
            if grid[i][j] == "R":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_R))
            if grid[i][j] == "T":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_T))
            if grid[i][j] == "M":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_M))
            if grid[i][j] == "P":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_P))
            if grid[i][j] == "S":  
                grounds.append(Spike(j*50 - 50, i*50, 50, 50, image_ground_S))
            if grid[i][j] == "N":  
                grounds.append(Ground(j*50 - 50, i*50, 50, 50, image_ground_N))
            if grid[i][j] == "I":  
                grounds.append(Invsible(j*50 - 50, i*50, 50, 50, image_ground_N))
    