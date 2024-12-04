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
        self.sprites.draw(screen)


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
        player. If the collision is with a "Ground" object and the 
        monster is falling, its vertical position is adjusted to land 
        on top of the ground. If the collision is with a "Projectile", 
        the monster's health is reduced by the damage of the projectile.
        If a projectile collides with the "Ground", it is removed 
        from the monster's projectiles list. If a projectile collides 
        with the "Player", the player's health is reduced by the 
        projectile's damage, and the projectile is removed from the 
        monster's projectiles list.

        Parameters
        ----------
        other : object
            The object that the monster is colliding with. This can be 
            a "Ground", "Projectile", or "Player".

        Returns
        -------
        None
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
        Draws the dummy and its associated sprites on the screen.
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
        movement range. If the dummy collides with a boundary, 
        its horizontal direction is reversed.

        Parameters
        ----------
        other : object
            The object that the dummy is colliding with. This can be 
            any object in the game world.

        Returns
        -------
        None

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
            The camera object, used to adjust the dummy's position 
            based on the camera's `position_x` and `fix_x`.

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
    """
    Represents a Mage enemy with unique animations, projectiles, and 
    movement behavior.

    Attributes
    ----------
    width : int
        Width of the mage.
    speed_x : int
        Horizontal speed of the mage.
    life : int
        Health points of the mage.
    projectile_cooldown : int
        Current cooldown state for projectile firing.
    cool_down : int
        Maximum cooldown time between projectiles.
    sprites : Sprites
        Instance of `Sprites` for handling mage animations.
    adjW : int
        Horizontal adjustment for mage sprites.
    adjH : int
        Vertical adjustment for mage sprites.
    adj : int
        General adjustment for sprite drawing.
    images_directory : dict
        Paths to sprite sheets for different animations.
    sizes_directory : dict
        Number of frames in each sprite animation set.
    images : dict
        Dictionary holding loaded sprite frames for each action.
    actual_mage : dict
        Tracks the current frame for each animation state.
    fps : dict
        Frame rate settings for each animation.
    image_projectile_l : pygame.Surface
        Image of the projectile when facing left.
    image_projectile_r : pygame.Surface
        Image of the projectile when facing right.

    Methods
    -------
    update() -> None
        Updates the Mage's states.
    attack() -> None
         Handles the Mage's attack actions.


    """

    def __init__(
        self, x : float, y : float, width : int, height : int, 
        hero : object
    ) -> None:
        """
        Initializes the class Mage with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the mage.
        y : float
            Initial y-coordinate of the mage.
        width : int
            Width of the mage's bounding box.
        height : int
            Height of the mage's bounding box.
        hero : object
            Reference to the hero object for interaction.
        """
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
    
    def update(self) -> None:
        """
        Updates the Mage's state, including movement, animations, 
        projectiles, and handling death. The Mage adjusts its facing 
        direction (`to_left` or `to_right`) based on the hero's 
        position. If the projectile cooldown is active, it decrements 
        the timer.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        
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
    
    def attack(self) -> None:
        """
        Handles the Mage's attack actions, including spawning 
        projectiles and playing animations. The Mage attacks by 
        launching projectiles in the direction it is facing. 

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

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
                    self.rect.right, self.rect.centery, 20, 0, self.TAG, 20, 
                    50, 30, self.image_projectile_r
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
    """
    Represents a flying enemy character in the game, inheriting from the 
    Monsters class.

    Attributes
    ----------
    speed_x : int
        Horizontal speed of the flying enemy.
    gravity : int
        Gravity affecting the flying enemy. Set to 0 as flying enemies 
        do not need gravity.
    probability : float
        Probability factor used for random movements or attacks.
    randomic : float
        Randomization factor influencing behavior.
    cool_down_max : int
        Maximum cooldown time for attacking.
    cool_down_min : int
        Minimum cooldown time for attacking.
    cool_down : int
        Current cooldown time for attack actions.
    move_cooldown : int
        Cooldown time for movement actions.
    projectile_cooldown : int
        Cooldown time for firing projectiles.
    sprites : Sprites
        An instance of the Sprites class for managing animations.
    adjW : int
        Width adjustment for sprite scaling.
    adjH : int
        Height adjustment for sprite scaling.
    adj : int
        General adjustment parameter for sprite alignment.
    images_directory : dict
        Dictionary mapping animation types to their file paths.
    sizes_directory : dict
        Dictionary specifying the number of frames in each animation.
    images : dict
        Dictionary holding loaded image frames for each animation.
    actual_flying : dict
        Dictionary tracking the current frame of each animation type.
    fps : dict
        Dictionary defining the frame rate for each animation type.
    image_projectile : pygame.Surface
        Image used for the flying enemy's projectile.
    
    Methods
    -------
    move() -> None
        Moves the flying enemy horizontally.
    update() -> None
        Updates the flying enemy's states.
    draw(screen, camera) -> None
        Draws the flying enemy.
    attack() -> None 
        Handles the flying enemy's attack behavior.
    
    """

    def __init__(
        self, x : float, y : float, width : int, height : int, 
        hero : object
    ) -> None:
        """
        Initializes the class Flying with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the flying.
        y : float
            Initial y-coordinate of the flying.
        width : int
            Width of the flying's bounding box.
        height : int
            Height of the flying's bounding box.
        hero : object
            Reference to the hero object for interaction.
        """
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
        
    def move(self) -> None:
        """
        Moves the flying enemy horizontally and triggers appropriate 
        animations. The direction of movement is determined by a random 
        factor, and movement alternates between left and right based on 
        a probability threshold. The function also resets the movement 
        cooldown after each decision, ensuring varied behavior over 
        time. 

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

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

    def update(self) -> None:
        """
        Updates the flying enemy's state, including movement, 
        animations, projectiles, and handling of the death state. This 
        method is called every frame to ensure continuous behavior and 
        state transitions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

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
    
    def draw(self, screen : pygame.Surface, camera: object) -> None:
        """
        Draws the flying enemy and its current animation state to the 
        screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen or surface where the enemy's sprite should be 
            drawn.
        camera : object
            The camera used for adjusting the enemy's position on the 
            screen.
        
        Returns
        -------
        None
        """

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
    
    def attack(self) -> None:
        """
        Handles the flying enemy's attack behavior, including 
        projectile creation.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.projectile_cooldown <= 0:
            new_projectile = Projectile(
                self.rect.left, self.rect.bottom, 0, 20, self.TAG, 20, 40, 60, 
                self.image_projectile
            )
            self.projectiles.append(new_projectile)
            self.projectile_cooldown = self.cool_down
            self.is_attacking = True