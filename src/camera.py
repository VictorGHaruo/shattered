import pygame 

class Camera:
    
    def __init__(self, x_init, margin):
        self.TAG = "Camera"
        self.position_x = x_init
        self.margin = margin
    
    def update_coods(self, hero, WIDGHT):
        if hero.TAG == "Player":
            if hero.rect.left < self.position_x + self.margin:
                self.position_x = hero.rect.left - self.margin
            elif hero.rect.right > self.position_x + WIDGHT - self.margin:
                self.position_x = hero.rect.right - WIDGHT + self.margin
