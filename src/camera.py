import pygame 

class Camera:
    
    def __init__(self, x_init, WIDGHT):
        self.TAG = "Camera"
        self.position_x = x_init
        self.WIDGHT = WIDGHT
        self.fix_x = x_init + self.WIDGHT // 2
        self.boss_fase = False
    
    def update_coods(self, hero, main):
        if hero.TAG == "Player":
            if self.fix_x <= (132 * (-50)) + 700 and not self.boss_fase:
                self.boss_fase = True
                main.is_changed = True
            if hero.rect.centerx >= self.fix_x and not self.boss_fase:
                self.position_x = hero.rect.centerx - self.WIDGHT // 2
                self.fix_x -= self.position_x
            else:
                self.position_x = 0
