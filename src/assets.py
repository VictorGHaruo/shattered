import pygame
import os
import sys
from typing import Optional

class Sprites():

    """
    Loads and applies sprites to characters.

    Notes
    -----
    It is important to use the correct variable names in this class. 
    If there is any typo, some methods may raise an error. For example, 
    "Attack" is valid, but "attack" is not. The `self.action` variable 
    must always hold a valid string representing an action.
    """

    def __init__(self) -> None:

        """
        Initializes important attributes used in other methods.
        """

        self.image = None
        self.image_rect = None
        self.before = 0
        self.actions = [
            "Walk", "Run", "Idle", "Attack","Attack_2", "Death", "Immune", 
            "Jump", "Hurt", "Projectile"
        ]

    def load_images(
        self, invert: bool, width: int, height: int, action: str, 
        images: dict[str, list], sizes_directory: dict[str, str],
        images_directory: dict[str, str], adjW: int, adjH: int
    ) -> None:
        
        """
        Loads sprites from separate image files and stores them in a 
        list.

        Parameters
        ----------
        invert : bool
            Whether to flip the image horizontally.
        width : int
            The character's width, used to adjust sprites to the hitbox.
        height : int
            The character's height, used to adjust sprites to the 
            hitbox.
        action : str
            The action being performed (e.g., "Walk", "Idle") to store 
            images in the correct list, it must present in self.action 
            list.
        images : dict[str, list]
            A dictionary where keys are action names and values are 
            lists of images for each action.
        sizes_directory : dict[str, int]
            A dictionary mapping each action to the number of images 
            available for that action.
        images_directory : dict[str, str]
            A dictionary mapping each action to the directory path 
            where the sprite images are stored.
        adjW : int
            Adjustment to apply to the sprite's width.
        adjH : int
            Adjustment to apply to the sprite's height.
            
        Returns
        -------
        None
            The function does not return any value. It modifies the 
            `images` dictionary in-place.

        """

        for i in range(sizes_directory[action]):
            image = pygame.image.load(
                os.path.join(images_directory[action], f"{i+1}.png")
            ).convert_alpha()
            image = pygame.transform.scale(
                image, (width + adjW, height + adjH)
            )
            if invert:
                image = pygame.transform.flip(image, invert, False)
            images[action].append(image)


    def load_spritesheets(
        self, sizes_directory: dict[str, int], action: str, invert: bool, 
        images_directory: dict[str, str], images: dict[str, list], 
        file_name: str, size_x: int, size_y: int, line: int, width: int, 
        height: int, adjW: int, adjH: int, gap: Optional[int] = None
    ) -> None:
        
        """
        Loads a spritesheet and stores individual images in a list.

        Parameters
        ----------
        sizes_directory : dict[str, int]
            A dictionary mapping each action to the number of images 
            available for that action.
        action : str
            The action being performed (e.g., "Walk", "Idle") to store 
            images in the correct list. It must be present in the 
            `self.actions` list.
        invert : bool
            Whether to flip the image horizontally.
        images_directory : dict[str, str]
            A dictionary mapping each action to the directory path where 
            the sprite images are stored.
        images : dict[str, list]
            A dictionary where keys are action names and values are 
            lists of images for each action.
        file_name : str
            The name of the file containing the spritesheet 
            (without extension).
        size_x : int
            The width of each individual image in the spritesheet.
        size_y : int
            The height of each individual image in the spritesheet.
        line : int
            The vertical offset (in pixels) where the action starts in 
            the spritesheet.
        width : int
            The character's width, used to adjust sprites to the hitbox.
        height : int
            The character's height, used to adjust sprites to the 
            hitbox.
        adjW : int
            Adjustment to apply to the sprite's width.
        adjH : int
            Adjustment to apply to the sprite's height.
        gap : int, optional
            If the action occupies more than one line in the 
            spritesheet, `gap` defines how many images are in each line.
            If `gap` is not provided, the function assumes that all 
            images are in a single line.

        Returns
        -------
        None
            The function does not return any value. It modifies the 
            `images` dictionary in-place.
        
        Notes
        -----
        If the action utilizes more than one line in the spritesheet, 
        the `gap` parameter is used to define how many images are in 
        each line. The function will correctly read and extract images 
        from different lines based on this value.
        """
        
        sheet = pygame.image.load(
            os.path.join(images_directory[action], f"{file_name}.png")
        ).convert_alpha()
        
        for i in range(sizes_directory[action]):
            column = i % gap if gap else i
            row = i // gap if gap else 0
            
            image = sheet.subsurface((column * size_x, line + size_y * row), 
                                     (size_x, size_y))
            image = pygame.transform.scale(
                image, (width + adjW, height + adjH)
            )
            
            if invert:
                image = pygame.transform.flip(image, invert, False)
            
            images[action].append(image)

    def assets(
        self, rect: pygame.Rect, action: str, actual: dict[str, float], 
        direction: str, fps: dict[str, float], 
        images: dict[str, list[pygame.Surface]], adjust: int, name: str
    ) -> None:
        
        """
        Puts and animates assets on the character.

        Parameters
        ----------
        rect : Player
            The character's rectangle, used to position and align the 
            sprite.
        action : str
            The action being performed (e.g., "Walk", "Idle") to animate
            the character. It must be present in the `self.actions` 
            list.
        actual : dict[str, float]
            A counter that determines which image frame to display for 
            the current action.
        direction : str
            The direction the character is facing. Use "L" for left 
            (inverted sprite) and "R" for right (normal sprite).
        fps : dict[str, float]
            Speed at which the frames change. Higher values result in 
            faster animation.
        images : dict[str, list[pygame.Surface]]
            A dictionary where keys are action names and values are 
            lists of sprites used to animate the character.
        adjust : int
            A vertical adjustment value to align the sprite with the 
            hitbox rectangle.
        name : str
            A unique identifier for the character, used as a prefix in 
            the image keys.

        Returns
        -------
        None
            This method updates the `self.image` and `self.image_rect` 
            attributes.
        
        Notes
        -----
        The sprites are organized in the dictionary so that each 
        action's list contains frames for both directions: the first 
        half for the left ("L") direction and the second half for the 
        right ("R") direction. The function checks the character's 
        direction and selects the appropriate frames accordingly. In the 
        final steps, the method aligns the sprite with the center and 
        bottom of the given rectangle.
        """

        for act in self.actions:
            if action == act:
                if direction == "L":
                    if actual[action] >= len(images[name+action])/2:
                        actual[action] = 0
                    self.image = images[name+action][int(actual[action])]
                elif direction == "R":
                    if (actual[action] >= len(images[name+action]) or 
                        actual[action] < len(images[name+action])/2) :
                        actual[action] = len(images[name+action])/2
                    self.image = images[name+action][int(actual[action])]
                actual[action] += fps

        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = rect.bottom + adjust
        self.image_rect.centerx = rect.centerx
        self.before = action

    def draw(self, screen: pygame.Surface, alpha: int = 255) -> None:

        """
        Draw the assets on the screen.

        Parameters
        ----------
        screen: pygame.Surface
            Surface where sprites will be drawn.

        Returns
        -------
        None
            This method doesn't return anything. It only modifies the 
            display.

        """
        
        if self.image and self.image_rect:
            self.image.set_alpha(alpha)
            screen.blit(self.image, self.image_rect)

class Herolife:
        
    def __init__(self, hero, heart, x, y, width, height, adj = 0):
        self.max_life = hero.max_life
        self.actual_life = 0
        self.images = []
        self.heart = heart
        self.hearts = self.max_life//self.heart
        self.x = x
        self.y = y
        self.adj = adj
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        Heart_path = os.path.join(path_game, os.pardir, "assets", "Heart")
        Heart_path = os.path.abspath(Heart_path)
        for i in range(1, 6):
            image_path = os.path.join(Heart_path, f"heart_{i}.png")
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.images.append(self.image)
    def update(self, hero):
        self.actual_life = hero.life
    def draw(self,screen):
        actual_life = self.actual_life
        for i in range(self.hearts):
            if actual_life <= 0:
                screen.blit(self.images[4], (i*self.x + self.adj , self.y))
            elif actual_life >= self.heart:
                screen.blit(self.images[0], (i*self.x + self.adj , self.y))
                
            elif actual_life >= self.heart*(3/4):
                
                screen.blit(self.images[1], (i*self.x + self.adj , self.y))
            elif actual_life >= self.heart*(1/2):
                
                screen.blit(self.images[2], (i*self.x + self.adj , self.y))
            else:
                screen.blit(self.images[3], (i*self.x + self.adj , self.y))
            actual_life -= self.heart
class Bar:
    def __init__(self, Value, x, y, width, height, color1, color2):
        self.max = Value  
        self.actual = 0     
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        self.images = []
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.rect_2 = pygame.Rect(self.x, self.y, width, height)
        # path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Bars_path = os.path.join(path_game, os.pardir, "assets", "Bars")
        # Bars_path = os.path.abspath(Bars_path)
        # for i in range(1, 3):
        #     image_path = os.path.join(Bars_path, f"Bar{i}.png")
        #     bar_image = pygame.image.load(image_path).convert_alpha()
        #     bar_image = pygame.transform.scale(bar_image, (self.width, self.height))
        #     self.images.append(bar_image)
    def update(self, Value):
        self.actual = Value
        if self.actual > 0 :
            self.actual = self.max - self.actual
            self.rect.width = self.width * (self.actual/self.max)
    def draw(self, screen):
        #screen.blit(self.images[1], (self.x, self.y), self.rect)
        pygame.draw.rect(screen, self.color1, self.rect_2)
        pygame.draw.rect(screen, self.color2, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect_2, 4)
        #screen.blit(self.images[0], (self.x, self.y))
class Bosslife(Bar):
    def __init__(self, Value, x, y, width, height, color1, color2):
        super().__init__(Value, x, y, width, height, color1, color2)
        self.health_ratio = self.max / self.width
        self.health_change_speed = 3
        self.transition = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self, Value):
        self.rect.width = self.width * (Value / self.max)
        if self.transition.width > self.rect.width:
            self.transition.width -= self.health_change_speed 
    def draw(self, screen):
        
        pygame.draw.rect(screen, self.color2, self.transition)
        pygame.draw.rect(screen, self.color1, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height), 4)