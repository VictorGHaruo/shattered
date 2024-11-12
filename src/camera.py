import pygame 

class Camera:
    
    def __init__(self, x_init, WIDGHT):
        self.TAG = "Camera"
        self.position_x = x_init
        self.WIDGHT = WIDGHT
        self.fix_X = x_init + self.WIDGHT // 2
        self.boss_fase = False
    
    def update_coods(self, hero):
        if hero.TAG == "Player":
            if self.fix_X <= -5700:
                self.boss_fase = True
            if hero.rect.centerx >= self.fix_X and not self.boss_fase:
                self.position_x = hero.rect.centerx - self.WIDGHT // 2
                self.fix_X -= self.position_x
            else:
                self.position_x = 0
