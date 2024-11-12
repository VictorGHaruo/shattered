import pygame 

class Camera:
    
    def __init__(self, x_init, WIDGHT):
        self.TAG = "Camera"
        self.position_x = x_init
        self.WIDGHT = WIDGHT
        self.fix_X = x_init + self.WIDGHT // 2
    
    def update_coods(self, hero):
        if hero.TAG == "Player":
            if hero.rect.right >= self.fix_X:
                self.position_x = hero.rect.right - self.WIDGHT // 2
                self.fix_X -= self.position_x
            else:
                self.position_x = 0
