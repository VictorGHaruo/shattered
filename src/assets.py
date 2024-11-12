import pygame
import os

class Assets():
    def __init__(self) -> None:
        self.walkL_images = []
        self.walkR_images = []
        self.attackR_images = []
        self.attackL_images = []
        self.deathL_images = []
        self.deathR_images = []
        self.idleL_images = []
        self.idleR_images = []

        self.actual_Walk = 0
        self.actual_Atk = 0
        self.actual_Death = 0
        self.actual_Idle = 0

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
        
        for death_left in range(16):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/death/death_{death_left+1}.png", width, height, True)
            self.deathL_images.append(image)

        for death_right in range(16):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/death/death_{death_right+1}.png", width, height, False)
            self.deathR_images.append(image)

        for idle_left in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/idle/idle_{idle_left+1}.png", width, height, True)
            self.idleL_images.append(image)
        
        for idle_right in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/idle/idle_{idle_right+1}.png", width, height, False)
            self.idleR_images.append(image)

    def assets_Demogorgon(self, action, rect):
        if action == "WalkLeft" or action == "WalkRight":
            self.actual_Walk = self.actual_Walk + 0.5
            if self.actual_Walk >= len(self.walkL_images):
                self.actual_Walk = 0
            if action == "WalkLeft":
                self.image = self.walkL_images[int(self.actual_Walk)]
            if action == "WalkRight":
                self.image = self.walkR_images[int(self.actual_Walk)]
        
        if action == "AtkLeft" or action == "AtkRight":
            self.actual_Atk = self.actual_Atk + 0.5
            if self.actual_Atk >= len(self.attackL_images):
                self.actual_Atk = 0
            
            if action == "AtkLeft":
                self.image = self.attackL_images[int(self.actual_Atk)]
            
            if action == "AtkRight":
                self.image = self.attackR_images[int(self.actual_Atk)]
        
        if action == "DeathLeft" or action == "DeathRight":
            
            if action == "DeathRight" and self.actual_Death < len(self.deathL_images):
                self.image = self.deathR_images[int(self.actual_Death)]
            
            if action == "DeathLeft":
                self.image = self.deathL_images[int(self.actual_Death)]    

            self.actual_Death = self.actual_Death + 0.25

        if action == "IdleLeft" or action == "IdleRight":
            self.actual_Idle = self.actual_Idle + 0.4
            if self.actual_Idle >= len(self.idleL_images):
                self.actual_Idle = 0
            
            if action == "IdleLeft":
                self.image = self.idleL_images[int(self.actual_Idle)]
            
            if action == "IdleRight":
                self.image = self.idleR_images[int(self.actual_Idle)]         



        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + 90 
        self.image_rect.centerx = rect.centerx
