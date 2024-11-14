import pygame
import os

class Assets():
    def __init__(self) -> None:
        self.main_directory = os.path.dirname(os.path.dirname(__file__))

        #Demagorgon
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
        self.Dadjust = 300

        #Ganon
        self.Ganon_spritesheet = pygame.image.load(f"{self.main_directory}/assets/Ganon/Character_sheet.png").convert_alpha()
        self.Ganon_projectile = pygame.image.load(f"{self.main_directory}/assets/Ganon/arm_projectile_glowing.png").convert_alpha()
        self.GidleL_images = []
        self.GidleR_images = []
        self.GattackL_images = []
        self.GattackR_images = []
        self.GimmuneL_images = []
        self.GimmuneR_images = []
        self.GdeathL_images = []
        self.GdeathR_images = []
        # self.GprojectileL_images = []
        self.GprojectileR_images = []

        self.Gactual_Idle = 0
        self.Gactual_Attack = 0
        self.Gactual_Immune = 0
        self.Gactual_Death = 0
        self.Gadjust = 100

        #Balrog
        self.BflyL_images = []
        self.BflyR_images = []
        self.Blightning_images = []

        self.Bactual_Fly = 0
        self.Bactual_Lightning = 0

        self.Badjust = 100

    def load_image(self, image_path, width, height, invert):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        image = pygame.transform.flip(image, invert, False)
        return image
    
    def load_spritesheet(self, size_x, size_y, line,idle_left, width, height, invert, spritesheet):
        image = spritesheet.subsurface((idle_left * size_x, line), (size_x, size_y)) #arrumar
        image = pygame.transform.scale(image, (width, height))
        image = pygame.transform.flip(image, invert, False)
        return image
    
    def init_Demogorgon(self, width, height):
        for walk_left in range(10):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/walk/walk_{walk_left+1}.png", width + self.Dadjust, height + self.Dadjust, True)
            self.walkL_images.append(image)

        for walk_right in range(10):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/walk/walk_{walk_right+1}.png", width + self.Dadjust, height + self.Dadjust, False)
            self.walkR_images.append(image)

        for attack_right in range(14):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/1_atk/1_atk_{attack_right+1}.png", width + self.Dadjust, height + self.Dadjust, False)
            self.attackR_images.append(image)

        for attack_left in range(14):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/1_atk/1_atk_{attack_left+1}.png", width + self.Dadjust, height + self.Dadjust, True)
            self.attackL_images.append(image)
        
        for death_left in range(16):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/death/death_{death_left+1}.png", width + self.Dadjust, height + self.Dadjust, True)
            self.deathL_images.append(image)

        for death_right in range(16):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/death/death_{death_right+1}.png", width + self.Dadjust, height + self.Dadjust, False)
            self.deathR_images.append(image)

        for idle_left in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/idle/idle_{idle_left+1}.png", width + self.Dadjust, height + self.Dadjust, True)
            self.idleL_images.append(image)
        
        for idle_right in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Demagorgon/idle/idle_{idle_right+1}.png", width + self.Dadjust, height + self.Dadjust, False)
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

    def init_Projectile (self,width, height):
        image = self.load_spritesheet(100, 150, 100, 0, width + 200, height + 200, False, self.Ganon_projectile)
        self.GprojectileR_images.append(image)

        image = self.load_spritesheet(100, 150, 100, 0, width + 1200, height + 1200, True, self.Ganon_projectile)
        self.GprojectileR_images.append(image)
    
    def assets_Projectile(self, action):


        if action == "ProjectileLeft":
            self.projectile = self.GprojectileR_images[0]
            return self.projectile
        elif action == "ProjectileRight":
            self.projectile = self.GprojectileR_images[1]
            return self.projectile

    def init_Ganon(self, width, height):
        for idle_left in range(4):
            image = self.load_spritesheet(100, 100, 0, idle_left, width + self.Gadjust, height + self.Gadjust, True, self.Ganon_spritesheet)
            self.GidleL_images.append(image)
        
        for idle_right in range(4):
            image = self.load_spritesheet(100, 100, 0, idle_right, width + self.Gadjust, height + self.Gadjust, False, self.Ganon_spritesheet)
            self.GidleR_images.append(image)
            
        for attack_left in range(6):
            image = self.load_spritesheet(100, 100, 100, attack_left, width + self.Gadjust, height + self.Gadjust, True, self.Ganon_spritesheet)
            self.GattackL_images.append(image)

        for attack_right in range(6):
            image = self.load_spritesheet(100, 100, 100, attack_right, width + self.Gadjust, height + self.Gadjust, False, self.Ganon_spritesheet)
            self.GattackR_images.append(image)

        for immune_left in range(8):
            image = self.load_spritesheet(100, 100, 300, immune_left, width + self.Gadjust, height + self.Gadjust, True, self.Ganon_spritesheet)
            self.GimmuneL_images.append(image)

        for immune_right in range(8):
            image = self.load_spritesheet(100, 100, 300, immune_right, width + self.Gadjust, height + self.Gadjust, False, self.Ganon_spritesheet)
            self.GimmuneR_images.append(image)
        
        for death_left in range(10):
            image = self.load_spritesheet(100, 100, 700, death_left, width + self.Gadjust, height + self.Gadjust, False, self.Ganon_spritesheet)
            self.GdeathL_images.append(image)
        
        for death_left in range(4):
            image = self.load_spritesheet(100, 100, 800, death_left, width + self.Gadjust, height + self.Gadjust, False, self.Ganon_spritesheet)
            self.GdeathL_images.append(image)

        for death_right in range(10):
            image = self.load_spritesheet(100, 100, 700, death_right, width + self.Gadjust, height + self.Gadjust, True, self.Ganon_spritesheet)
            self.GdeathR_images.append(image)
        
        for death_right in range(4):
            image = self.load_spritesheet(100, 100, 800, death_right, width + self.Gadjust, height + self.Gadjust, True, self.Ganon_spritesheet)
            self.GdeathR_images.append(image)


    def assets_Ganon(self, action, rect):
        if action == "IdleLeft" or action == "IdleRight":
            self.Gactual_Idle = self.Gactual_Idle + 0.2
            if self.Gactual_Idle >= len(self.GidleL_images):
                self.Gactual_Idle = 0
            
            if action == "IdleLeft":
                self.image = self.GidleL_images[int(self.Gactual_Idle)]

            if action == "IdleRight":
                self.image = self.GidleR_images[int(self.Gactual_Idle)]
        
        if action == "AttackLeft" or action == "AttackRight":
            self.Gactual_Attack = self.Gactual_Attack + 0.1
            if self.Gactual_Attack >= len(self.GattackL_images):
                self.Gactual_Attack = 5
            
            if action == "AttackLeft":
                self.image = self.GattackL_images[int(self.Gactual_Attack)]
            
            if action == "AttackRight":
                self.image = self.GattackR_images[int(self.Gactual_Attack)]
    
        if action == "ImmuneLeft" or action == "ImmuneRight":
            if self.Gactual_Immune >= len(self.GimmuneL_images):
                self.Gactual_Immune = 7

            if action == "ImmuneLeft":
                self.image = self.GimmuneL_images[int(self.Gactual_Immune)]
            
            if action == "ImmuneRight":
                self.image = self.GimmuneR_images[int(self.Gactual_Immune)]
            
            self.Gactual_Immune = self.Gactual_Immune + 0.3
        
        if action == "DeathLeft" or action == "DeathRight":
            if action == "DeathLeft":
                self.image = self.GdeathL_images[int(self.Gactual_Death)]
            
            if action == "DeathRight":
                self.image = self.GdeathR_images[int(self.Gactual_Death)]
            self.Gactual_Death = self.Gactual_Death + 0.2
        


        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + 30
        self.image_rect.centerx = rect.centerx 

    def init_Balrog(self, width, height):
        for fly_left in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Balrog/fly/fly_{fly_left+1}.png", width + self.Badjust, height + self.Badjust, True)
            self.BflyL_images.append(image)
        
        for fly_right in range(6):
            image = self.load_image(f"{self.main_directory}/assets/Balrog/fly/fly_{fly_right+1}.png", width + self.Badjust, height + self.Badjust, False)
            self.BflyR_images.append(image)

        for lightning in range(11):
            image = self.load_image(f"{self.main_directory}/assets/Balrog/lightning/Lightning{lightning+1}.png", width + self.Badjust + 200, height + self.Badjust + 200, False)
            self.Blightning_images.append(image)

    def assets_Balrog(self, action, rect):
        # print(len(self.BflyL_images))
        if action == "FlyLeft" or action == "FlyRight":
            self.Bactual_Fly = self.Bactual_Fly + 0.4
            if self.Bactual_Fly >= len(self.BflyL_images):
                self.Bactual_Fly = 0
            if action == "FlyLeft":
                self.image = self.BflyL_images[int(self.Bactual_Fly)]
                print(self.Bactual_Fly)
            if action == "FlyRight":
                self.image = self.BflyR_images[int(self.Bactual_Fly)]

            # if self.Bactual_Lightning >= len(self.Blightning_images):
            #     self.Bactual_Lightning = self.Bactual_Lightning + 0.4
            #     self.Bactual_Lightning = 0
            # self.image = self.Blightning_images[int(self.Bactual_Lightning)]

        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + 90 
        self.image_rect.centerx = rect.centerx
