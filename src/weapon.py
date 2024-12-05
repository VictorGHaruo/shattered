import pygame
from typing import Union

class Projectile:
    """
    Represents a projectile in the game, which can be used by the 
    Player, Bosses, or Enemies. A projectile is a moving object with 
    specific attributes like speed, damage, and direction.

    Attributes
    ----------
    TAG : str
        Identifier tag for the projectile.
    rect : pygame.Rect
        The rectangular area that defines the position and size of the 
        projectile.
    speed_x : int
        The horizontal speed of the projectile.
    speed_y : int
        The vertical speed of the projectile.
    who : str
        Indicates who fired the projectile (e.g., "Player", "Enemy", 
        "Boss").
    damage : int
        The damage dealt by the projectile upon collision.
    image : pygame.Surface or None
        The image representing the projectile. If no image is provided, 
        defaults to None.

    Methods
    -------
    update() -> None
        Updates projectiles' attributes of speed.
    draw(screen, camera) -> None
        Draws projectiles.
    """

    def __init__(
        self, x: float, y: float, speed_x: int, speed_y: int, who: str, 
        damage: int, width: int, height: int, image:pygame.Surface = None, 
        adj: float = 0
    ) -> None:
        """
        Initializes a new projectile instance with the given attributes.

        Parameters
        ----------
        x : float
            The initial x position of the projectile.
        y : float
            The initial y position of the projectile.
        speed_x : int
            The horizontal speed of the projectile.
        speed_y : int
            The vertical speed of the projectile.
        who : str
            The entity that fired the projectile (e.g., "Player", 
            "Enemy", "Boss").
        damage : int
            The amount of damage the projectile deals when it collides 
            with an object.
        width : int
            The width of the projectile.
        height : int
            The height of the projectile.
        image : pygame.Surface, optional
            The image to represent the projectile. If not provided, no 
            image is assigned.
        adj : int, optional
            An adjustment value for the width and height of the image. 
            Defaults to 0.

        Returns
        -------
        None
            This method initializes the attributes of the projectile 
            instance.
        """
        self.TAG = "Projectile"
        self.rect = pygame.Rect(x, y, width, height) 
        self.speed_x = speed_x  
        self.speed_y = speed_y
        self.who = who
        self.damage = damage

        if image != None:
            self.image = pygame.transform.scale(
                image, (width + adj, height + adj)
            )
        else:
            self.image = None

    def update(self) -> None:
        """    
        This method is responsible for updating the movement of all
        projectiles shot.

        Parameters
        ----------
        None 

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            current attributes of projectiles.

        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen: pygame.Surface, camera: "Camera") -> None:
        """
        Draws the projectiles, adjusting their positions 
        based on the camera movement. 

        Parameters
        ----------
        screen : pygame.Surface
            The surface where the boss and projectiles will be drawn.
        camera : Camera
            The camera object used to adjust the boss's position.

        Returns
        -------
        None
            This method does not return a value. It directly modifies 
            the screen by drawing sprites.
        """

        self.rect.x -= camera.position_x
        if self.image != None:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect) 

class Shield:
    """
    Represents a shield in the game, used by the Player to reflect 
    projectiles. When a projectile hits the shield, its velocity is 
    inverted, causing the shield to reflect all incoming projectiles.

    Attributes
    ----------
    TAG : str
        Identifier tag for the shield.
    width : int
        The width of the shield.
    height : int
        The height of the shield.
    rect : pygame.Rect
        The rectangular area that defines the position and size of the 
        shield.
    damage : float
        The percentage of damage the shield reflects upon collision.

    Methods
    -------
    reflect
    update
    draw(screen) -> None
    """

    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        """
        Initializes the shield instance with the given attributes.

        Parameters
        ----------
        x : float
            The initial x position of the shield.
        y : float
            The initial y position of the shield.
        width : int
            The width of the shield.
        height : int
            The height of the shield.

        Returns
        -------
        None
            This method initializes the attributes of the shield 
            instance.
        """
        self.TAG = "Shield"
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height) 
    
    def reflect(
        self, user: "Player", other: "Monster", list1: list, list2: list
    ) -> None:
        """
        Reflects a projectile upon collision with the shield by 
        reversing its horizontal speed and flipping its sprite. The 
        projectile is then added to the Player's projectile list and 
        removed from the original owner's list.

        Parameters
        ----------
        user : Player
            The Player using the shield.
        projectile : Projectile
            The projectile that collides with the shield.
        player_projectiles : list
            The list of the Player's projectiles.
        enemy_projectiles : list
            The list of the enemy's projectiles.

        Returns
        -------
        None
            This method modifies the projectile's attributes and updates 
            the projectile lists.
   
        """
        if other.TAG == "Projectile" and self.rect.colliderect(other.rect):
            other.speed_x = -other.speed_x
            other.image = pygame.transform.flip(other.image, True, False)
            other.who = user
            list1.append(other)
            list2.remove(other)

    def update(self, x: float, y: float) -> None:
        """
        Updates the shield's position by creating a new rectangle at the 
        specified coordinates.

        Parameters
        ----------
        x : float
            The new x-coordinate for the shield's position.
        y : float
            The new y-coordinate for the shield's position.

        Returns
        -------
        None
            This method modifies the shield's rectangle to update its 
            position.
        """
        self.rect  = pygame.Rect(x, y, self.width, self.height) 



class Attack:
    """
    Represents an attack in the game, it could be a sword for Player
    or even a punch for Demagorgon.

    Attributes
    ----------
    TAG: str
        Identifier tag for the shield.
    rect: pygame.Rect
        The rectangular area that defines the position and size of the 
        attack.
    damage: int
        The damage dealt by the attack upon collision.
    
    Methods
    -------
    None

    """
    def __init__(
        self, x: float, y: float, width: int, height: int, damage: int
    ) -> None:
        """
        Initializes a attack instance with the given attributes.

        Parameters
        ----------
        x : float
            The initial x position of the attack.
        y : float
            The initial y position of the attack.
        width : int
            The width of the attack.
        height : int
            The height of the attack.
        damage : int
            The amount of damage the attack deals when it collides 
            with an object.

        Returns
        -------
        None
            This method initializes the attributes of the attack 
            instance.
        """
        self.TAG = "Attack"
        self.rect = pygame.Rect(x, y, width, height)
        self.damage = damage    