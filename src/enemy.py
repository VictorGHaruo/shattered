import pygame
import random
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(current_dir, '..')  
sys.path.append(src_path)

from src.assets import Sprites
from src.weapon import Projectile

class Monsters:
    """
    Represents a monster character in the game with attributes for 
    movement, health, and interactions with the hero.

    Attributes
    ----------
    TAG : str
        A general tag identifying the object as a "Monster".
    sub_TAG : str
        A more specific tag, also set to "Monster" by default.
    rect : pygame.Rect
        The rectangular area representing the monster's position and 
        size.
    gravity : int
        The gravity force applied to the monster's vertical movement.
    speed_y : int
        The current vertical speed of the monster.
    speed_y_max : int
        The maximum vertical speed of the monster.
    speed_x : int
        The horizontal speed of the monster.
    life : int
        The monster's health points.
    hero : object
        A reference to the hero object, used for interactions.
    immune : bool
        Indicates whether the monster is currently immune to damage.
    to_right : bool
        Indicates whether the monster is moving or facing to the right 
        (default is True).
    to_left : bool
        Indicates whether the monster is moving or facing to the left 
        (default is False).
    is_dead : bool
        Indicates whether the monster is dead.
    is_attacking : bool
        Indicates whether the monster is currently attacking.
    projectiles : list
        A list of projectiles associated with the monster.

    Methods
    -------
    update() -> None
        Update monsters attributes.
    new_hero(hero) -> None
        Update the position and the hero himself.
    draw(screen, camera) -> None
        Draws the monster and its projectiles on the screen.
    on_collision(other) -> None
        Handles collision detection and response for the monster.

    Notes
    -----
    This class manages the monster's state and interactions with the 
    game environment, including movement, health, and attacking logic.
    """

    def __init__(
        self, x : float, y : float, width : int, height : int, 
        hero : object
    ) -> None:
        """
        Initializes the class Monsters with values of atributes

        Parameters
        ----------
        x : float
            The x-coordinate of the monster's position.
        y : float
            The y-coordinate of the monster's position.
        width : int
            The width of the monster's bounding rectangle.
        height : int
            The height of the monster's bounding rectangle.
        hero : object
            The hero object for interactions and logic involving the 
            player character.
        """
        self.TAG = "Monster"
        self.sub_TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 5
        self.hero = hero
        self.immune = False
        self.to_right = True
        self.to_left =  False
        self.is_dead = False
        self.is_attacking = False
        self.projectiles = []

    def move(self) -> None:
        pass

    def update(self) -> None:
        """
        Updates the monster's vertical position by applying gravity and 
        limiting the fall speed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)
    
    def new_hero(self, hero : object) -> None:
        """
        Updates the reference to the hero object.

        Parameters
        ----------
        hero : object
            The new hero object to be associated with the monster.

        Returns
        -------
        None
        """
        self.hero = hero
        
    def draw (self, screen: pygame.Surface, camera : object) -> None:
        """
        Draws the monster and its projectiles on the screen, adjusting 
        for the camera's position.

        Parameters
        ----------
        screen : pygame.Surface
            The surface where the monster and its projectiles will be 
            drawn.
        camera : object
            The camera object, used to adjust the monster's position 
            based on its `position_x` attribute.

        Returns
        -------
        None
        """

        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile
                        
    def on_collision(self, other : object) -> None:  
        """
        Handles collision detection and response for the monster, 
        including interactions with the ground, projectiles, and the 
        player.

        Parameters
        ----------
        other : object
            The object that the monster is colliding with. This can be 
            a "Ground", "Projectile", or "Player".

        Returns
        -------
        None

        Notes
        -----
        - If the collision is with a "Ground" object and the monster is 
        falling, its vertical position (`rect.bottom`) is adjusted to 
        land on top of the ground.
        - If the collision is with a "Projectile", the monster's 
        health (`life`) is reduced by the damage of the projectile.
        - If a projectile collides with the "Ground", it is removed 
        from the monster's projectiles list.
        - If a projectile collides with the "Player", the player's 
        health (`life`) is reduced by the projectile's damage, and the 
        projectile is removed from the monster's projectiles list.
        """

        if (other.TAG == "Ground" and self.rect.colliderect(other) and 
            self.rect.bottom > other.rect.top and 
            self.rect.top < other.rect.top
        ):
                self.rect.bottom = other.rect.top
                
        if other.TAG == "Projectile":
            if self.rect.colliderect(other):       
                    self.life -= other.damage
        
        for projectile in self.projectiles:
            if other.TAG == "Ground":
                if projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
                    del projectile
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    self.projectiles.remove(projectile)
                    del projectile

class Dummy(Monsters):
    """
    Represents a dummy monster character with specific attributes for 
    movement, animation, and behavior.

    Attributes
    ----------
    speed_x : int
        The horizontal speed of the dummy.
    init_x : int
        The initial x-coordinate of the dummy's position.
    range : int
        The range within which the dummy can move horizontally.
    sprites : Sprites
        The `Sprites` object that manages the dummy's animations and 
        sprite loading.
    adjW : int
        The horizontal adjustment for the dummy's sprite positioning.
    adjH : int
        The vertical adjustment for the dummy's sprite positioning.
    adj : int
        An additional adjustment for sprite positioning (default is 0).
    images_directory : dict
        A dictionary containing the paths to the sprite sheets for 
        different actions.
    sizes_directory : dict
        A dictionary specifying the number of frames for each animation 
        type.
    images : dict
        A dictionary that stores the loaded sprite images for the 
        dummy's different actions.
    actual_dummy : dict
        A dictionary tracking the current frame of the dummy's 
        animations.
    fps : dict
        A dictionary specifying the frame rate for the dummy's 
        animations (walking and death).

    Methods
    -------
    on_collision(other) -> None
        Handles collision detection and response for the dummy monster.
    update() -> None
        Updates the dummy's state.
    move() -> None
        Handles the mechanic of movement of dummy monster.
    draw(screen, camera) -> None
        Draws the dummy and its associated sprites on the screen
    
    Notes
    -----
    - The `Dummy` class inherits from `Monsters` and specializes the 
    monster with specific animations for walking and dying.
    - The `sprites.load_spritesheets` method is used to load sprite 
    sheets for both walking and death animations, 
      adjusting for both left and right directions.
    - The dummy is designed to move horizontally within a specified 
    range (`range`), and its position is updated using the `speed_x` 
    attribute.
    """

    def __init__(
        self, x : float, y : float, width : int, height : int, 
        hero : object
    ) -> None:
        """
        Parameters
        ----------
        x : float
            The x-coordinate of the dummy's position.
        y : float
            The y-coordinate of the dummy's position.
        width : int
            The width of the dummy's bounding rectangle.
        height : int
            The height of the dummy's bounding rectangle.
        hero : object
            The hero object, used for interactions and logic involving 
            the player character.
        """
        super().__init__(x, y, width, height, hero)
        self.speed_x = 3
        self.init_x = x
        self.range = 100
        
        self.sprites = Sprites()
        self.adjW = 60
        self.adjH = 80
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Dummy_path = os.path.join(path_game, os.pardir, "assets", "Dummy")
        self.images_directory = {
            "DWalk" : os.path.join(Dummy_path),
            "DDeath" : os.path.join(Dummy_path)
        }
        self.sizes_directory = {
            "DWalk" : 7,
            "DDeath" : 15
        }
        self.images = {
            "DWalk" : [],
            "DDeath" : []
        }
        self.actual_dummy = {
            "Walk" : 0,
            "Death" : 0
        }
        self.fps = {
            "Walk" : 0.22,
            "Death" : 0.27
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "DWalk", True, self.images_directory, 
            self.images, "RUN", 80, 64, 0, width, height, self.adjW, self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "DWalk", False, self.images_directory, 
            self.images, "RUN", 80, 64, 0, width, height, self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "DDeath", True, self.images_directory, 
            self.images, "DEATH", 80, 64, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "DDeath", False, self.images_directory, 
            self.images, "DEATH", 80, 64, 0, width, height, self.adjW, 
            self.adjH
        )

    def on_collision(self, other : object) -> None:
        """
        Handles collision detection and response for the dummy monster, 
        including direction reversal when the monster reaches its 
        movement range.

        Parameters
        ----------
        other : object
            The object that the dummy is colliding with. This can be 
            any object in the game world.

        Returns
        -------
        None

        Notes
        -----
        - This method calls the `on_collision` method from the parent 
        `Monsters` class to handle basic collision logic.
        - If the dummy collides with a boundary (based on its movement 
        range, `range`), its horizontal direction is reversed:
        - If the dummy is moving right (`to_right`) and exceeds 
        its initial position (`init_x + range`), it will reverse 
        direction and start moving left (`to_left`).
        - If the dummy is moving left (`to_left`) and goes beyond its 
        initial position (`init_x - range`), it will reverse 
        direction and start moving right (`to_right`).
        - The `speed_x` is multiplied by `-1` to change the direction 
        of the dummy's movement.
        """

        super().on_collision(other)
        
        if self.rect.x > self.init_x + self.range and self.to_right:
            self.speed_x *= -1
            self.to_left = True
            self.to_right = False
        if self.rect.x < self.init_x - self.range and self.to_left:
            self.speed_x *= -1
            self.to_left = False
            self.to_right = True

    def update(self) -> None:
        """
        Updates the dummy's state, including handling death animation 
        and movement.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        
        if self.life <= 0:
            if self.to_right:
                self.sprites.assets(
                    self.rect, "Death", self.actual_dummy, "L", 
                    self.fps["Death"], self.images, self.adj, "D"
                )
                if self.actual_dummy["Death"] >= len(self.images["DDeath"])/2:
                    self.is_dead = True
            if self.to_left:     
                self.sprites.assets(
                    self.rect, "Death", self.actual_dummy, "R", 
                    self.fps["Death"], self.images, self.adj, "D"
                )
                if self.actual_dummy["Death"] >= len(self.images["DDeath"]):
                    self.is_dead = True
        else:
            self.move()
            
        return super().update()
        
    def move(self) -> None:
        """
        Moves the dummy horizontally and updates its walking animation 
        based on its current direction.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """ 

        self.rect.x = self.rect.x + self.speed_x
        if self.to_right:
            self.sprites.assets(
                self.rect, "Walk", self.actual_dummy, "L", self.fps["Walk"], 
                self.images, self.adj, "D"
            )
        else:
            self.sprites.assets(
                self.rect, "Walk", self.actual_dummy, "R", self.fps["Walk"], 
                self.images, self.adj, "D"
            )
            
    def draw(self, screen: pygame.Surface, camera : object) -> None:
        """
        Draws the dummy and its associated sprites on the screen, 
        adjusting for the camera's position.

        Parameters
        ----------
        screen : pygame.Surface
            The surface where the dummy and its sprites will be drawn.
        camera : object
            The camera object, used to adjust the dummy's position based on the camera's `position_x` and `fix_x`.

        """

        super().draw(screen, camera)
        if camera.TAG == "Camera":
            self.init_x -= camera.position_x
            if (self.rect.x < camera.fix_x - (screen.get_size()[0] // 2) and 
                self.to_left
            ):
                self.speed_x *= -1
                self.to_left = True
                self.to_right = False
        self.sprites.draw(screen)

class Mage(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.width = width
        self.speed_x = 3
        self.color = (0,0, 255)
        self.life = 60
        self.projectile_cooldown = 0
        self.cool_down = 100
        
        self.sprites = Sprites()
        self.adjW = 50
        self.adjH = 30
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Mage_path = os.path.join(path_game, os.pardir, "assets", "Mage")
        self.images_directory = {
            "MIdle" : os.path.join(Mage_path),
            "MAttack" : os.path.join(Mage_path),
            "MDeath" : os.path.join(Mage_path)
        }
        self.sizes_directory = {
            "MIdle" : 10, 
            "MAttack" : 10,
            "MDeath" : 10
        }
        self.images = {
            "MIdle" : [],
            "MAttack" : [],
            "MDeath" : []
        }
        self.actual_mage = {
            "Idle" : 0,
            "Attack" : 0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Attack" : 0.2,
            "Death" : 0.2
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "MIdle", False, self.images_directory, 
            self.images, "IDLE", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "MIdle", True, self.images_directory, 
            self.images, "IDLE", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "MAttack", False, self.images_directory, 
            self.images, "ATTACK", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "MAttack", True, self.images_directory, 
            self.images, "ATTACK", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "MDeath", False, self.images_directory, 
            self.images, "DEATH", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "MDeath", True, self.images_directory, 
            self.images, "DEATH", 80, 80, 0, width, height, self.adjW, 
            self.adjH, 3
        )
        projectile_path = os.path.join(Mage_path, "projectile.png")
        self.image_projectile_l = pygame.image.load(projectile_path)
        self.image_projectile_r = pygame.transform.flip(
            self.image_projectile_l, True, False
        )
    
    
    def update(self):
        
        if self.hero.rect.x <= self.rect.x and not self.life <= 0:
            self.to_left = True
            self.to_right = False
        elif not self.life <= 0:
            self.to_left = False
            self.to_right = True
        
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()
            
        if self.life <= 0:
            if self.to_left:
                self.sprites.assets(
                    self.rect, "Death", self.actual_mage, "L", 
                    self.fps["Death"], self.images, self.adj, "M"
                )
                if self.actual_mage["Death"] >= len(self.images["MDeath"])/2:
                    self.is_dead = True
            if self.to_right:     
                self.sprites.assets(
                    self.rect, "Death", self.actual_mage, "R", 
                    self.fps["Death"], self.images, self.adj, "M"
                )
                if self.actual_mage["Death"] >= len(self.images["MDeath"]):
                    self.is_dead = True
        else:
            self.attack()
        return super().update()
    
    def on_collision(self, other: pygame.Rect):
        return super().on_collision(other)
    
    def draw(self, screen, camera):
        super().draw(screen, camera) 
        self.sprites.draw(screen)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            if self.to_left:
                new_projectile = Projectile(
                    self.rect.left, self.rect.centery, - 20, 0, self.TAG, 20, 
                    50, 30, self.image_projectile_l
                )
                self.projectiles.append(new_projectile)
                self.sprites.assets(
                    self.rect, "Attack", self.actual_mage, "L", 
                    self.fps["Attack"], self.images, self.adj, "M"
                )
            else:
                new_projectile = Projectile(
                    self.rect.right, self.rect.centery, 20, 0, self.TAG, 20, 50,
                    30, self.image_projectile_r
                )
                self.projectiles.append(new_projectile)
                self.sprites.assets(
                    self.rect, "Attack", self.actual_mage, "R", 
                    self.fps["Attack"], self.images, self.adj, "M"
                )
            self.projectile_cooldown = self.cool_down
        else:
            if self.to_left:
                self.sprites.assets(
                    self.rect, "Idle", self.actual_mage, "L", self.fps["Idle"], 
                    self.images, self.adj, "M"
                )
            else:
                self.sprites.assets(
                    self.rect, "Idle", self.actual_mage, "R", self.fps["Idle"], 
                    self.images, self.adj, "M"
                )

class Flying(Monsters):
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height, hero)
        self.speed_x = 3
        self.gravity = 0

        self.probability = 0.5
        self.randomic = 0.5

        self.cool_down_max = 100
        self.cool_down_min = 70

        self.cool_down = 0
        self.move_cooldown = 0

        self.projectile_cooldown = 0

        self.sprites = Sprites()
        self.adjW = 30
        self.adjH = 30
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Fly_path = os.path.join(path_game, os.pardir, "assets", "Flying")
        self.images_directory = {
            "FWalk" : os.path.join(Fly_path),
            "FAttack" : os.path.join(Fly_path),
            "FDeath" : os.path.join(Fly_path)
        }
        self.sizes_directory = {
            "FWalk" : 4, 
            "FAttack" : 8,
            "FDeath" : 7
        }
        self.images = {
            "FWalk" : [],
            "FAttack" : [],
            "FDeath" : []
        }
        self.actual_flying = {
            "Walk" : 0,
            "Attack" : 0,
            "Death" : 0
        }
        self.fps = {
            "Walk" : 0.25,
            "Attack" : 0.25,
            "Death" : 0.25
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "FWalk", False, self.images_directory, 
            self.images, "FLYING", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "FWalk", True, self.images_directory, 
            self.images, "FLYING", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "FAttack", False, self.images_directory, 
            self.images, "ATTACK", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "FAttack", True, self.images_directory, 
            self.images, "ATTACK", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "FDeath", False, self.images_directory, 
            self.images, "DEATH", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "FDeath", True, self.images_directory, 
            self.images, "DEATH", 81, 71, 0, width, height, self.adjW, 
            self.adjH
        )
        projectile_path = os.path.join(Fly_path, "projectile.png")
        self.image_projectile = pygame.image.load(projectile_path)
        
    def move(self):
        if self.move_cooldown <= 0:
            
            self.randomic = random.random()
            self.cool_down = random.randint(
                self.cool_down_min, self.cool_down_max
            )       
            self.move_cooldown = self.cool_down
        
        if self.randomic >= self.probability:
            self.rect.x += self.speed_x
            self.to_right = True
            self.to_left = False
            if not self.is_attacking:
                self.sprites.assets(
                    self.rect, "Walk", self.actual_flying, "R", 
                    self.fps["Walk"], self.images, self.adj, "F"
                )
        else:
            self.rect.x -= self.speed_x
            self.to_right = False
            self.to_left = True
            if not self.is_attacking:
                self.sprites.assets(
                    self.rect, "Walk", self.actual_flying, "L", 
                    self.fps["Walk"], self.images, self.adj, "F"
                )

    def on_collision(self, other):
        super().on_collision(other)

    def update(self):
        super().update()
        
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()
            
        if self.life <= 0:
            if self.to_left:
                self.sprites.assets(
                    self.rect, "Death", self.actual_flying, "L", 
                    self.fps["Death"], self.images, self.adj, "F"
                )
                if self.actual_flying["Death"] >= len(self.images["FDeath"])/2:
                    self.is_dead = True
            if self.to_right:     
                self.sprites.assets(
                    self.rect, "Death", self.actual_flying, "R", 
                    self.fps["Death"], self.images, self.adj, "F"
                )
                if self.actual_flying["Death"] >= len(self.images["FDeath"]):
                    self.is_dead = True
        else:
            self.attack()
            self.move()
    
    def draw(self, screen, camera):
        super().draw(screen, camera)
        
        if self.to_right and not self.life <= 0:
            if self.actual_flying["Attack"] >= len(self.images["FAttack"]):
                self.actual_flying["Attack"] = 0
                self.is_attacking = False
            if self.is_attacking:
                self.sprites.assets(
                    self.rect, "Attack", self.actual_flying, "R", 
                    self.fps["Attack"], self.images, self.adj, "F"
                )
        elif not self.life <= 0:
            if self.actual_flying["Attack"] >= len(self.images["FAttack"])/2:
                self.actual_flying["Attack"] = 0
                self.is_attacking = False
            if self.is_attacking:
                self.sprites.assets(
                    self.rect, "Attack", self.actual_flying, "L", 
                    self.fps["Attack"], self.images, self.adj, "F"
                )
                
        self.sprites.draw(screen)
    
    def attack(self):
        if self.projectile_cooldown <= 0:
            new_projectile = Projectile(
                self.rect.left, self.rect.bottom, 0, 20, self.TAG, 20, 40, 60, 
                self.image_projectile
            )
            self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down
            self.is_attacking = True