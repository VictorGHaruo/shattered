import pygame
import os

class Assets():
    def __init__(self) -> None:
        self.walkL_images = []
        self.walkR_images = []
        self.attackR_images = []
        self.attackL_images = []
        self.actual_Walk = 0
        self.actual_Atk = 0
        self.main_directory = os.path.dirname(os.path.dirname(__file__))


    def load_image(self, image_path, width, height, invert):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width + 300, height + 300))
        image = pygame.transform.flip(image, invert, False)
        return image

    def init_Demogorgon(self, width, height):
        for walk_left in range(10):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/walk/walk_{walk_left+1}.png", width, height, True)
            self.walkL_images.append(image)

        for walk_right in range(10):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/walk/walk_{walk_right+1}.png", width, height, False)
            self.walkR_images.append(image)

        for attack_right in range(14):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/1_atk/1_atk_{attack_right+1}.png", width, height, False)
            self.attackR_images.append(image)

        for attack_left in range(14):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/1_atk/1_atk_{attack_left+1}.png", width, height, True)
            self.attackL_images.append(image)

    def assets_Demogorgon(self, action, rect):
        if action == "WalkLeft":
            self.actual_Walk = self.actual_Walk + 0.5
            if self.actual_Walk >= len(self.walkL_images):
                self.actual_Walk = 0
            self.image = self.walkL_images[int(self.actual_Walk)]
        
        if action == "WalkRight":
            self.actual_Walk = self.actual_Walk + 0.5
            if self.actual_Walk >= len(self.walkR_images):
                self.actual_Walk = 0
            self.image = self.walkR_images[int(self.actual_Walk)]
        
        if action == "AtkLeft":
            self.actual_Atk = self.actual_Atk + 0.5
            if self.actual_Atk >= len(self.attackL_images):
                self.actual_Atk = 0
            self.image = self.attackL_images[int(self.actual_Atk)]
        
        if action == "AtkRight":
            self.actual_Atk = self.actual_Atk + 0.5
            if self.actual_Atk >= len(self.attackR_images):
                self.actual_Atk = 0
            self.image = self.attackR_images[int(self.actual_Atk)]


        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + 90 
        self.image_rect.centerx = rect.centerx
