import pygame
import os

class Sprites():
    def __init__(self):
        self.image = None
        self.image_rect = None
        self.before = 0
        self.actions = ["Walk", "Idle", "Attack", "Death", "Immune", "Projectile"]

    def load_images(self, invert, width, height, action, images, sizes_directory, images_directory, adjW, adjH):
        for i in range(sizes_directory[action]):
            image = pygame.image.load(os.path.join(images_directory[action], f"{i+1}.png")).convert_alpha()
            image = pygame.transform.scale(image, (width + adjW, height + adjH))
            if invert == True:
                image = pygame.transform.flip(image, invert, False)
            images[action].append(image)


    def load_spritesheets(self, sizes_directory, action, invert, images_directory, images, file_name, size_x, size_y, line, width, height, adjW, adjH, gap=None, teste = 0):
        sheet = pygame.image.load(os.path.join(images_directory[action], f"{file_name}.png")).convert_alpha()
        
        for i in range(sizes_directory[action]):
            column = i % gap if gap else i
            row = i // gap if gap else 0
            
            image = sheet.subsurface((column * size_x, line + size_y * row), (size_x, size_y))
            image = pygame.transform.scale(image, (width + adjW, height + adjH))
            
            if invert == True:
                image = pygame.transform.flip(image, invert, False)
            
            images[action].append(image)

    def assets(self, rect, action, actual, direction, fps, images, adjust, name):

        for act in self.actions:
            if action == act:
                if direction == "L":
                    if actual[action] >= len(images[name+action])/2: #>=
                        actual[action] = 0
                    self.image = images[name+action][int(actual[action])]
                elif direction == "R":
                    if (actual[action] >= len(images[name+action]) or actual[action] < len(images[name+action])/2) :
                        actual[action] = len(images[name+action])/2
                    self.image = images[name+action][int(actual[action])]
                actual[action] = actual[action] + fps

        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + adjust
        self.image_rect.centerx = rect.centerx 
        self.before = action
    
    def draw(self, screen):
        if self.image and self.image_rect:
            screen.blit(self.image, self.image_rect)
        