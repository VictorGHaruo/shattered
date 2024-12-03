import pygame

class Ground:
    """
    Base class for objects representing the ground or static 
    elements in the game.

    Attributes
    ----------
    TAG : str
        General identifier of the class.
    sub_TAG : str
        Specific identifier of the class.
    image : pygame.Surface
        Image associated with the object.
    rect : pygame.Rect
        Rectangular boundary defining the object's position and size.
        
    Methods
    -------
    draw(screen, camera)
        Draws the object in the screen
    update()
        Updates posicion in the interactive type
    on_collision(other)
        Detects and handles collisions between ground and ohter objects.
    """

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        image_path: str
    ) -> None:
        """
        Initializes the ground object with position, size, and image.
        The function initializes the object's attributes.

        Parameters
        ----------
        x : int
            Horizontal position of the object.
        y : int
            Vertical position of the object.
        width : int
            Width of the object.
        height : int
            Height of the object.
        image_path : str
            File path to the image used for the object.

        Returns
        -------
        None
        """
        self.TAG = "Ground"
        self.sub_TAG = "Ground"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen: pygame.Surface, camera) -> None:
        """
        Renders the object on the screen adjusted by the camera.

        Parameters
        ----------
        screen : pygame.Surface
            The surface where the object will be drawn.
        camera : Camera
            The camera used to adjust the position of the object.

        Returns
        -------
        None
        """
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            screen.blit(self.image, self.rect)

    def update(self) -> None:
        """
        Placeholder for object updates.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass

    def on_collision(self, other) -> None:
        """
        Placeholder for handling collisions with other objects.

        Parameters
        ----------
        other : object
            The object that collided with this instance.

        Returns
        -------
        None
        """
        pass


class Block(Ground):
    """
    Represents an interactive Ground affected by gravity 
    and player actions.

    Attributes
    ----------
    TAG : str
        General identifier of the class.
    sub_TAG : str
        Specific identifier of the class.
    image : pygame.Surface
        Image associated with the object.
    rect : pygame.Rect
        Rectangular boundary defining the object's position and size.
    gravity_y : int
        The intensity of gravity applied to the block.
    speed_y : int
        The vertical speed of the block.
    speed_y_max : int
        The maximum allowable vertical speed.
    is_pushing_r : bool
        Indicates if the block is being pushed to the right.
    is_pushing_l : bool
        Indicates if the block is being pushed to the left.
    
    Methods
    -------
    draw(screen, camera)
        Draws the object in the screen
    update()
        Updates posicion in the interactive type
    on_collision(other)
        Detects and handles collisions between ground and ohter objects.
    """

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        image_path: str
    ) -> None:
        """
        Initializes the block, object that inherits from the Ground 
        class, with position, size, and image.

        Parameters
        ----------
        x : int
            Horizontal position of the block.
        y : int
            Vertical position of the block.
        width : int
            Width of the block.
        height : int
            Height of the block.
        image_path : str
            File path to the image used for the block.

        Returns
        -------
        None
        """
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Block"
        self.gravity_y = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.is_pushing_r = False
        self.is_pushing_l = False

    def update(self) -> None:
        """
        Updates the block's position based on gravity and pushes.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super().update()
        self.speed_y += self.gravity_y
        self.rect.y += min(self.speed_y, self.speed_y_max)
        if self.is_pushing_r:
            self.rect.x -= 1.5
            self.is_pushing_r = False
        if self.is_pushing_l:
            self.rect.x += 1.5
            self.is_pushing_l = False

    def on_collision(self, other) -> None:
        """
        Handles collisions with other objects.

        Parameters
        ----------
        other : object
            The object that collided with the block.

        Returns
        -------
        None
        """
        super().on_collision(other)
        if other.TAG == "Ground" and self.rect.colliderect(other.rect):
            if (
                self.rect.bottom > other.rect.top 
                and self.rect.top < other.rect.top
            ):
                self.rect.bottom = other.rect.top
                self.speed_y = 0
        if (
            other.TAG == "Player" 
            and other.rect.colliderect(self.rect) 
            and other.can_push_block
        ):
            if other.speed_x > 0 and self.rect.top < other.rect.top:
                self.is_pushing_l = True
            if other.speed_x < 0 and self.rect.top < other.rect.top:
                self.is_pushing_r = True

    def draw(self, screen: pygame.Surface, camera) -> None:
        """
        Renders the object on the screen adjusted by the camera.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to which the image will be drawn.
        camera : Camera
            The camera used to adjust the position of the object.

        Returns
        -------
        None
        """
        super().draw(screen, camera)
                
class Spike(Ground):
    
    """
    Represents a Ground where you take damage when touching.
    
    Attributes
    ----------
    TAG : str
        General identifier of the class.
    sub_TAG : str
        Specific identifier of the class.
    image : pygame.Surface
        Image associated with the object.
    rect : pygame.Rect
        Rectangular boundary defining the object's position and size.
    """
    
    def __init__(
        self, 
        x: int, y: int,
        width: int, height: int, 
        image_path: str
    ) -> None:
        """
        Initializes a spike, object that inherits from the Ground class.

        Parameters
        ----------
        x : int
            The horizontal position where the spike will be placed.
        y : int
            The vertical position where the spike will be placed.
        width : int
            The width of the spike.
        height : int
            The height of the spike.
        image_path : str
            The file path to the image that will represent the spike.

        Returns
        -------
        None
        """
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Spike"
    
class Invisible(Ground):
    """
    Represents an invisble Ground.

    Attributes
    ----------
    TAG : str
        General identifier of the class.
    sub_TAG : str
        Specific identifier of the class.
    image : pygame.Surface
        Image associated with the object.
    rect : pygame.Rect
        Rectangular boundary defining the object's position and size.

    Methods
    -------
    draw(screen, camera)
        Updates the coordinate of ground.
    """
    
    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int,
        image_path: str
    ) -> None:
        """
        Initializes an invisible ground object.

        Parameters
        ----------
        x : int
            The horizontal position where the invisible object will
            be placed.
        y : int
            The vertical position where the invisible object will
            be placed.
        width : int
            The width of the invisible object.
        height : int
            The height of the invisible object.
        image_path : str
            The file path to the image that will represent the 
            invisible object.

        Returns
        -------
        None
        """
        super().__init__(x, y, width, height, image_path)
        self.sub_TAG = "Invisible"
        
    def draw(self, screen: pygame.Surface, camera) -> None:
        """
        Placeholder for object draws.
        Updates the coordinate of ground.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to which the object will be drawn.
        camera : Camera
            The camera used to adjust the object's position based 
            on scrolling.

        Returns
        -------
        None
        """
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x

class Obelisk:
    
    """
    Represents the object that the player touches to be able to 
    push blocks.
    
    Attributes
    ----------
    TAG : str
        General identifier of the class.
    sub_TAG : str
        Specific identifier of the class.
    sheet_im: pygame.Surface
        Image of the sheet of sprites passed.
    images : list
        List with the imagens used to animation.
    image : pygame.Surface
        Image associated with the object.
    num_image: int
        The current image of animation.
    rect : pygame.Rect
        Rectangular boundary defining the object's position and size.
        
    Methods
    -------
    draw(screen, camera)
        Draws the object in the screen
    on_collision(other)
        Placeholder to handles collision with other objects.
    update()
        Placeholder to updates the obelisk object.
    """
    
    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        image_path: str
    ) -> None:
        """
        Initializes an obelisk object with multiple frames from 
        a sprite sheet.

        Parameters
        ----------
        x : int
            The horizontal position where the obelisk will be placed.
        y : int
            The vertical position where the obelisk will be placed.
        width : int
            The width of the obelisk.
        height : int
            The height of the obelisk.
        image_path : str
            The file path to the sprite sheet image.

        Returns
        -------
        None
        """
        self.TAG = "Obelisk"
        self.sub_TAG = "Obelisk"
        self.sheet_im = pygame.image.load(image_path).convert_alpha()
        self.images = []
        for i in range(14):
            image = self.sheet_im.subsurface((i*190, 0), (190, 380))
            image = pygame.transform.scale(image, (width, height))
            self.images.append(image)
        self.num_image = 0
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.touched = False
    
    def draw(self, screen: pygame.Surface, camera) -> None:
        """
        Draws the obelisk object on the screen, updating its sprite 
        based on the interaction.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to which the obelisk will be drawn.
        camera : Camera
            The camera used to adjust the object's position based 
            on scrolling.

        Returns
        -------
        None
        """
        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            if self.touched and self.num_image < 14:
                screen.blit(self.images[int(self.num_image)], self.rect)
                self.num_image += 0.25
            else: 
                screen.blit(self.images[0], self.rect)
                self.num_image = 0
                self.touched = False
            
    def on_collision(self, other) -> None:
        """
        Placeholder to handles collision with other objects.

        Parameters
        ----------
        other : object
            The other object that the obelisk collides as 
            Hero, Ground, etc.

        Returns
        -------
        None
        """
        pass
            
    def update(self) -> None:
        """
        Placeholder to updates the obelisk object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass
