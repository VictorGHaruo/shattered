import pygame 

class Camera:
    """
    Class responsible for changing the visible part of the game
    
    Atributes
    ---------
    TAG : str
        General identifier of the class.
    position_x : int
        Coordinate of the top-left corner of the screen, which 
        will be updated with the hero's movement.
    WIDTH: int
        Screen width.
    fix_x : int
        Coordinates of the top-left corner, but fixed in the initial
        coordinate system.
    boss_fase : bool
        Bool of when the player is on boss fase.
        
    Methods
    -------
    update_coods(hero, main) -> None
        Updates the coordinate of the attributes.
    """
    
    
    def __init__(self, WIDTH: int, x_init: int = 0) -> None:
        """
        Initializes the camera.

        Parameters
        ----------
        WIDTH : int
            Screen width
        x_init : int
            Initial position of the camera, default is 0.
        
        Returns
        -------
        None
        """
        
        self.TAG = "Camera"
        self.position_x = x_init
        self.WIDTH = WIDTH
        self.fix_x = x_init + self.WIDTH // 2
        self.boss_fase = False
    
    def update_coods(self, hero: object, main: object):
        """
        Updates the coordinate of the attributes.

        Parameters
        ----------
            hero : object
                Player, to update the coordinates of the camera.
            main : object
                The main game instance.
        """
        
        if hero.TAG == "Player":
            if self.fix_x <= (132 * (-50)) + 700 and not self.boss_fase:
                self.boss_fase = True
                main.is_changed = True
            if hero.rect.centerx >= self.fix_x and not self.boss_fase:
                self.position_x = hero.rect.centerx - self.WIDTH // 2
                self.fix_x -= self.position_x
            else:
                self.position_x = 0
