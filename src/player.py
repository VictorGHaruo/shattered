import pygame
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(current_dir, '..')  
sys.path.append(src_path)

from src.weapon import Projectile, Shield, Attack
from src.assets import Sprites

class Player:
    """
    A class representing the player character.

    Attributes
    ----------
    TAG : str
        A tag identifying this class as the player character.
    sub_TAG : str
        A sub-tag specifying the player character.
    teste : str
        Auxiliar to draw assets.
    action : str or None
        The current action of the player.
    max_life : int
        The maximum life of the player.
    life : int
        The current life of the player.
    Death : bool
        A flag indicating if the player is dead.
    rect : pygame.Rect
        A rectangle defining the player's position and dimensions.
    gravity_y : int
        The gravity effect on the player's vertical movement.
    speed_y : int
        The vertical speed of the player.
    speed_y_max : int
        The maximum vertical speed.
    speed_jump : int
        The speed of the player's jump.
    jump_count : int
        The current count of jumps performed by the player.
    jump_count_max : int
        The maximum allowed number of jumps.
    speed_x : int
        The horizontal speed of the player.
    speed_x_max : int
        The maximum horizontal speed.
    speed_x_min : int
        The minimum horizontal speed.
    is_running : bool
        A flag indicating if the player is running.
    to_left : bool
        A flag indicating if the player is moving to the left.
    to_right : bool
        A flag indicating if the player is moving to the right.
    on_ground : bool
        A flag indicating if the player is currently on the ground.
    from_the_front : bool
        A flag indicating the player's front-facing direction.
    has_collision_obelisk : bool
        A flag indicating if the player has collided with an obelisk.
    touched_obelisk : bool
        A flag indicating if the player has touched an obelisk.
    can_push_block : bool
        A flag indicating if the player can push a block.
    trade_cooldown_time : int
        The cooldown time for the player's trade action.
    trade_cooldown : int
        The current cooldown time for the trade action.
    invincibility_time : int
        The time duration of the player's invincibility after being 
        hurt.
    collision_damage : int
        The damage taken by the player from collisions.
    damage : int
        The current damage the player is dealing.
    invincibility_cooldown : int
        The cooldown for the player's invincibility.
    hurt_time : int
        The time duration of the player's hurt state.
    hurt_cooldown : int
        The cooldown for the player's hurt state.
    projectiles : list
        A list of projectiles the player is currently firing.
    projectile_cooldown : int
        The cooldown time for firing projectiles.
    cooldown_time : int
        The cooldown time for various actions (e.g., projectile firing).
    
    Methods
    -------
    draw(screen, camera) -> None
        Draws the player and all associated projectiles onto the screen.
    update() -> None
        Updates the player's states
    on_event(event, main) -> None
        Handles user input events and updates the player's state.
    jump() -> None
        Handles the player's jump logic.
    on_key_pressed(key_map, main) -> None
        Handles player movement based on key presses.
    on_collision(other) -> None
        Handles collision detection and response for the player with 
        various game objects
    """
    
    def __init__(
            self, x : float, y : float, width : int, height : int
    ) -> None:
        """
        Initializes the class Player with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the Player.
        y : float
            Initial y-coordinate of the Player.
        width : int
            Width of the Player's bounding box.
        height : int
            Height of the Player's bounding box.

        """
        self.TAG = "Player"
        self.sub_TAG = "Player"
        self.teste = "teste"
        self.action = None
        self.max_life = 2000
        self.life = self.max_life
        self.Death = False
        self.points = 0
        
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        
        self.gravity_y = 2 
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_jump = -30
        self.jump_count = 0
        self.jump_count_max = 2
        
        self.speed_x = 0
        self.speed_x_max = 10
        self.speed_x_min = -10
        self.is_running = False
        self.to_left = False
        self.to_right = False
        self.on_ground = False
        self.from_the_front = True
        self.has_collision_obelisk = False
        self.touched_obelisk = False
        self.can_push_block = False
        
        self.trade_cooldown_time = 60
        self.trade_cooldown = self.trade_cooldown_time
        self.invincibility_time = 30
        self.collision_damage = 50
        self.damage = 0
        self.invincibility_cooldown = 0
        self.hurt_time = 5
        self.hurt_cooldown = 0
        self.projectiles = []
        self.projectile_cooldown = 0
        self.cooldown_time = 20
        self.rect_color = (255, 0, 0)

        self.sprites = Sprites()

    def draw(self, screen : pygame.Surface, camera : object) -> None:
        """
        Draws the player and all associated projectiles onto the screen, 
        considering the camera's position.

        The method handles drawing the player in different states and 
        manages the display of projectiles. The player's action 
        determines which animation frame to display.

        Parameters
        ----------
        screen : pygame.Surface
            The surface (screen) to draw the player and projectiles on.
        camera : Camera
            The camera object that determines the player's position 
            relative to the screen.

        Returns
        -------
        None


        """

        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            #pygame.draw.rect(screen, self.rect_color, self.rect)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile

        if self.action == "Jump":

            if self.on_ground:
                self.action = None
                
            if (
                int(self.actual["Jump"]) == 
                (len(self.images[f"{self.teste}Jump"])-1)//2 or 
                int(self.actual["Jump"]) == 
                len(self.images[f"{self.teste}Jump"] )-1 
            ):

                if self.from_the_front:
                    self.sprites.assets(
                        self.rect, "Jump", self.actual, "R", 0, 
                        self.images, self.adj, self.teste
                    )
                else: self.sprites.assets(
                    self.rect, "Jump", self.actual, "L", 0, 
                    self.images, self.adj, self.teste
                )
                return

        if self.action == "Hurt":
            if self.from_the_front:

                self.sprites.assets(
                    self.rect, "Hurt", self.actual, "R", 0, self.images, 
                    self.adj, self.teste
                )
            else:
                self.sprites.assets(
                    self.rect, "Hurt", self.actual, "L", 0, self.images, 
                    self.adj, self.teste
                )
            if self.on_ground and self.hurt_cooldown <= 0:
                self.action = None
            return
        
        if self.action is not None:

            if self.from_the_front:

                self.sprites.assets(
                    self.rect, self.action, self.actual, "R", 
                    self.fps[self.action], self.images, self.adj, self.teste
                )
            else:
                self.sprites.assets(
                    self.rect, self.action, self.actual, "L", 
                    self.fps[self.action], self.images, self.adj, self.teste
                )

        else:
            if self.on_ground:
                if self.from_the_front:

                    self.sprites.assets(
                        self.rect, "Idle", self.actual, "R", self.fps["Idle"], 
                        self.images, self.adj, self.teste
                    )
                else:
                    self.sprites.assets(
                        self.rect, "Idle", self.actual, "L", self.fps["Idle"], 
                        self.images, self.adj, self.teste
                    )
            else:   
                if self.from_the_front:
                    self.actual["Jump"] = ((len(
                        self.images[f"{self.teste}Jump"] )-1)//2
                    )
                    self.sprites.assets(
                        self.rect, "Jump", self.actual, "R", 0, self.images, 
                        self.adj, self.teste
                    )
                else: 
                    self.actual["Jump"] = (
                        len(self.images[f"{self.teste}Jump"] ) - 1
                    )
                    self.sprites.assets(
                        self.rect, "Jump", self.actual, "L", 0, self.images, 
                        self.adj, self.teste
                    )

    def update(self) -> None:
        """
        Updates the player's state, including movement, gravity, 
        projectiles, and cooldowns.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        ##Updating Y:

        if self.life <= 0 or self.rect.y > 1000:
            self.action = "Death"
            self.speed_x = 0
            if (
                int(self.actual["Death"]) == 
                len(self.images[f"{self.teste}Death"] )-1 or 
                int(self.actual["Death"]) == 
                (len(self.images[f"{self.teste}Death"] )-1)//2
            ):
                self.Death = True
        self.speed_y += self.gravity_y
        self.rect.y += min(self.speed_y, self.speed_y_max)
        
        ##Updating X:
        if self.speed_x > 0:
            # Se no pulo estivar apertando para o outro lado, ao tocar 
            # no chão zera a velocidade
            if self.to_left:
                self.speed_x = 0
            self.rect.x += min(self.speed_x, self.speed_x_max) 
        elif self.speed_x < 0:
            # Se no pulo estivar apertando para o outro lado, ao tocar 
            # no chão zera a velocidade
            if self.to_right:
                self.speed_x = 0
            self.rect.x += max(self.speed_x, self.speed_x_min)
        if self.rect.x <= 0:
            self.rect.x = 0
        
        # Se tiver no ar is_running é True, para manter constante 
        # a velocidade
        if not self.is_running:
            self.speed_x = 0
        
        ##Updating trade_cooldonw
        if self.trade_cooldown >= 0 or self.invincibility_cooldown >= 0:
            self.trade_cooldown -= 1    
            self.invincibility_cooldown -= 1
            self.hurt_cooldown -= 1

        for projectile in self.projectiles:
            projectile.update()

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1
                          
    def on_event(self, event: pygame.event.Event, main : object) -> None:
        """
        Handles user input events and updates the player's state accordingly.

        Parameters
        ----------
        event : pygame.event.Event
            The event that triggered the function.
        main : object
            The main game object, used to modify game state.

        Returns
        -------
        None
        """
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.on_ground = False
            if event.key == pygame.K_f and self.has_collision_obelisk:
                if not self.can_push_block:
                    main.is_changed = True
                self.touched_obelisk = True
                self.can_push_block = True

    def jump(self) -> None:
        """
        Handles the player's jump logic, updating vertical speed and 
        jump count.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if (
            self.jump_count >= self.jump_count_max or 
            self.action == "Hurt" or self.action == "Immune" or 
            self.action == "Death"
        ):
            return
        self.speed_y += self.speed_jump
        self.speed_y = max(self.speed_y, self.speed_jump)
        self.jump_count += 1
        self.action = "Jump"
        self.actual["Jump"] = 0
        
    def on_key_pressed(self, key_map : dict, main : object) -> None:
        """
        Handles player movement based on key presses, adjusting speed 
        and state accordingly.

        Parameters
        ----------
        key_map : dict
            A dictionary mapping pygame key events to their states.
        main : object
            The main game object, used for managing the game's state.

        Returns
        -------
        None
        """

        if (
            self.on_ground and self.action != "Hurt" and 
            self.action != "Attack" and self.action != "Immune" and 
            self.action != "Death"
        ):

            if  key_map[pygame.K_d]:
                self.speed_x += 5
                self.to_right = True
                self.from_the_front = True
            else:
                self.to_right = False
            if  key_map[pygame.K_a]:
                self.speed_x -= 5
                self.to_left = True
                self.from_the_front = False
            else:
                self.to_left = False
            
            if (
                (self.to_left or self.to_right) and 
                (not (self.to_left and self.to_right))
            ):
                self.is_running = True
                self.action = "Walk"
            else:
                self.is_running = False
                self.speed_x = 0
                if self.action == "Walk":
                    self.action = None
            
    def on_collision(self, other : object) -> None:
        """
        Handles collision detection and response for the player with 
        various game objects. If the player collides with an Obelisk, 
        then he can push the block. 

        Parameters
        ----------
        other : object
            The other object the player is colliding with.

        Returns
        -------
        None
        """
        if other.TAG == "Ground" and self.rect.colliderect(other):
            if (
                self.rect.bottom > other.rect.top and 
                self.rect.top < other.rect.top and self.speed_y > 0
            ):
                self.rect.bottom = other.rect.top
                self.speed_y = 0
                self.jump_count = 0
                self.on_ground = True
            elif(
                self.rect.left < other.rect.right and 
                self.rect.right > other.rect.right and self.speed_x < 0 
            ):
                self.rect.left = other.rect.right
                self.speed_x = 0
            elif (
                self.rect.right > other.rect.left and 
                self.rect.left < other.rect.left and self.speed_x > 0
            ):
                self.rect.right = other.rect.left
                self.speed_x = 0
            elif (
                self.rect.top < other.rect.bottom and 
                self.rect.bottom > other.rect.bottom
            ):
                self.rect.top = other.rect.bottom
                self.speed_y = 0
            
            if other.sub_TAG == "Spike":
                self.life -= 1000

        if other.TAG == "Monster":

            if (
                self.rect.colliderect(other) and 
                self.invincibility_cooldown <= 0
            ):
                self.life -= self.collision_damage
                self.invincibility_cooldown = self.invincibility_time
                self.action = "Hurt"
                self.hurt_cooldown = self.hurt_time
                self.speed_x = 0
                self.speed_y = 0

            for projectile in other.projectiles:

                if (
                    self.rect.colliderect(projectile) and 
                    self.invincibility_cooldown <= 0
                ):
                    self.life -= projectile.damage
                    self.invincibility_cooldown = self.invincibility_time
                    self.action = "Hurt"
                    self.hurt_cooldown = self.hurt_time
                    self.speed_x = 0
                    self.speed_y = 0

        for projectile in self.projectiles:
                if (
                    other.TAG == "Monster" and 
                    projectile.rect.colliderect(other)
                ):
                    if (
                        not projectile.who == "Yokai" or 
                        not other.sub_TAG == "Ganon"
                    ):
                            other.life -= self.damage
                    self.projectiles.remove(projectile)
                    del projectile

                    
                if (
                    other.TAG == "Ground" and 
                    projectile.rect.colliderect(other)
                ):
                    self.projectiles.remove(projectile)
                    del projectile
                    
        if other.TAG == "Obelisk" and self.rect.colliderect(other.rect):
            self.has_collision_obelisk = True
            
        if (other.TAG == "Obelisk" and self.touched_obelisk and 
            self.rect.colliderect(other.rect)
        ):
            other.touched = True
            self.has_collision_obelisk = False
            self.touched_obelisk = False
                   
class Knight(Player):
    """
    A subclass of the `Player` class representing a Knight character 
    in the game.
    
    Attributes
    ----------
    teste : str
        A string identifier for the Knight ("K").
    jump_count_max : int
        The maximum number of jumps the Knight can perform.

    shield_width : int
        The width of the Knight's shield.
    shield_height : int
        The height of the Knight's shield.
    shield_x : int
        The x-position of the Knight's shield, based on facing direction.
    shield_y : int
        The y-position of the Knight's shield.
    shield_damage : float
        The damage dealt by the Knight's shield when used.
    shield : object or None
        Placeholder for the shield object.
    sprites : Sprites
        The `Sprites` object used to load and manage the Knight's 
        animations.
    adjW : int
        Width adjustment for the sprite images.
    adjH : int
        Height adjustment for the sprite images.
    adj : int
        Additional adjustment for sprite positioning.
    images_directory : dict
        A dictionary holding paths to the Knight's sprite image 
        directories.
    sizes_directory : dict
        A dictionary containing the number of frames for each animation.
    images : dict
        A dictionary for storing the loaded images for different 
        actions.
    actual : dict
        A dictionary holding the current frame index for each animation.
    fps : dict
        A dictionary defining the frame rate for each animation action.

    Methods
    -------

    """
    
    def __init__(
        self, x : float, y : float, width : int, height : int
    ) -> None:
        """
        Initializes the class Flying with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the Knight.
        y : float
            Initial y-coordinate of the Knight.
        width : int
            Width of the Knight's bounding box.
        height : int
            Height of the Knight's bounding box.
        """
        super().__init__(x, y, width, height)
        self.teste = "K"
        self.jump_count_max = 1
        self.rect_color = (255, 0, 0)
        self.shield_width = 5
        self.shield_height = 70
        self.shield_x = (
            self.rect.centerx if self.from_the_front else 
            self.rect.centerx - 15
        )
        self.shield_y = self.rect.y
        self.shield_damage = 0.7
        self.shield = None  

        self.sprites = Sprites()
        self.adjW = 80
        self.adjH = 80
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Knight_path = os.path.join(path_game, os.pardir, "assets", "Knight")
        self.images_directory = {
            "KIdle" : os.path.join(Knight_path),
            "KWalk" : os.path.join(Knight_path),
            "KHurt" : os.path.join(Knight_path),
            "KJump" : os.path.join(Knight_path),
            "KImmune" : os.path.join(Knight_path),
            "KDeath" : os.path.join(Knight_path)
        }
        self.sizes_directory = {
            "KIdle" : 4,
            "KWalk" : 8,
            "KHurt" : 2,
            "KJump" : 6,
            "KImmune" : 1,
            "KDeath" : 6
        }
        self.images = {
            "KIdle" : [],
            "KWalk" : [],
            "KHurt" : [],
            "KJump" : [],
            "KImmune" : [],
            "KDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Immune" : 0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.5,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Immune" : 0,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "KIdle", True, self.images_directory, 
            self.images, "Idle1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "KIdle", False, self.images_directory, 
            self.images, "Idle1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KWalk", True, self.images_directory, 
            self.images, "Walk1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KWalk", False, self.images_directory, 
            self.images, "Walk1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KHurt", True, self.images_directory, 
            self.images, "Hurt1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "KHurt", False, self.images_directory, 
            self.images, "Hurt1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KJump", True, self.images_directory, 
            self.images, "Jump1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KJump", False, self.images_directory, 
            self.images, "Jump1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KImmune", True, self.images_directory, 
            self.images, "Protect1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KImmune", False, self.images_directory, 
            self.images, "Protect1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KDeath", True, self.images_directory, 
            self.images, "Dead1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "KDeath", False, self.images_directory, 
            self.images, "Dead1", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )

    def actions(self, key_map : dict) -> None:
        """
        Handles the player's actions based on key inputs and updates 
        the player's state accordingly, including activating the shield 
        and changing movement properties when the "Immune" action is 
        triggered.

        Parameters
        ----------
        key_map : dict
            A dictionary mapping keys to their pressed states. It is 
            used to check if specific keys are pressed.

        Returns
        -------
        None
        """

        if (
            key_map[pygame.K_v] and self.action != "Hurt" and 
            self.action != "Death"
        ):

            self.action = "Immune"

            if self.action == "Immune":
                if self.shield is None: 
                    self.shield = Shield(
                        self.shield_x, self.shield_y, self.shield_width, 
                        self.shield_height, self.shield_damage
                    )
                    self.action = "Immune"

                if self.on_ground:
                    self.speed_x_max = 0
                    self.speed_x_min = 0
                    self.speed_jump = 0
                    
        else:
            self.shield = None
            if self.action == "Immune":
                self.action = None
            self.speed_x_max = 10
            self.speed_x_min = -10
            self.speed_jump = -30
            
    def on_collision(self, other : object) -> None:
        """
        Handles the collision behavior between the player and other 
        game entities. If the player has an active shield, it reflects 
        damage from monster projectiles.

        Parameters
        ----------
        other : GameObject
            The other object that the player collides with, typically a monster or projectile.

        Returns
        -------
        None
        """

        super().on_collision(other)

        if self.shield is not None:
            if other.TAG == "Monster":
                for projectile in other.projectiles:
                    self.damage = self.shield.damage * projectile.damage
                    self.shield.reflect(
                        self.TAG, projectile, self.projectiles, 
                        other.projectiles
                    )

    def update(self) -> None:
        """
        Updates the Knight character's state, including the shield 
        position and any other character-related updates. This method 
        calls the parent class' `update` method to handle the base 
        functionality and then updates specific attributes related to 
        the shield.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        super().update()

        self.shield_x = (
            self.rect.centerx + 35 if self.from_the_front 
            else self.rect.centerx - 50
        )

        self.shield_y = self.rect.y

        if self.shield is not None:
            self.shield.update(self.shield_x, self.shield_y)

    def draw(self, screen, camera):

        super().draw(screen, camera)

        if self.invincibility_cooldown >= 0 :
            self.sprites.draw(screen,128)
        else:
            self.sprites.draw(screen)
        

class Yokai(Player):
    """
    Initializes a Yokai character with specific attributes such as
    sprite animations, damage values, and attack parameters. This 
    character has two jump counts, specific movement, and combat 
    features.
    
    Attributes:
    -----------
    sub_TAG : str
        Specifies the type of entity as "Yokai".
    damage : int
        The damage dealt by the Yokai's attacks.
    jump_count_max : int
        The maximum number of jumps allowed.
    attack_time : int
        Time in frames during which the attack is active.
    sprites : Sprites
        An instance of the Sprites class to load and manage sprite 
        sheets.
    attack_animation : int
        Specifies the frame count for the Yokai's attack animation.
    images_directory : dict
        A dictionary containing paths to the sprite directories for 
        various actions.
    sizes_directory : dict
        A dictionary specifying the number of frames for each animation 
        action.
    images : dict
        A dictionary to store loaded images for each animation.
    actual : dict
        Stores the current frame for each animation action.
    fps : dict
        The frame rate for each animation action.
    image_projectile_r : pygame.Surface
        The image for the projectile facing right.
    image_projectile_l : pygame.Surface
        The image for the projectile facing left.
    image_projectile_u : pygame.Surface
        The image for the projectile facing upwards.
    
    Methods
    -------
    actions(key_map) -> None
        Handles the actions of the Yokai character based on the input 
        keys.
    update() -> None
        Updates the state of the Yokai character.

    """
    
    def __init__(
        self, x : float, y : float, width : int, height : int
    ) -> None:
        """
        Initializes the class Yokai with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the Yokai.
        y : float
            Initial y-coordinate of the Yokai.
        width : int
            Width of the Yokai's bounding box.
        height : int
            Height of the Yokai's bounding box.
        """
        super().__init__(x, y, width, height)
        self.sub_TAG = "Yokai"
        self.teste = "Y"
        self.jump_count_max = 2
        self.rect_color = (255, 255, 0)
        self.damage = 20
        self.attack_animation = 5
        self.attack_time = 0
        
        self.sprites = Sprites()
        self.adjW = 60
        self.adjH = 60
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Yokai_path = os.path.join(path_game, os.pardir, "assets", "Yokai")
        self.images_directory = {
            "YIdle" : os.path.join(Yokai_path),
            "YWalk" : os.path.join(Yokai_path),
            "YHurt" : os.path.join(Yokai_path),
            "YJump" : os.path.join(Yokai_path),
            "YAttack" : os.path.join(Yokai_path),
            "YAttack_2": os.path.join(Yokai_path),
            "YDeath" : os.path.join(Yokai_path)
        }
        self.sizes_directory = {
            "YIdle" : 8,
            "YWalk" : 8,
            "YHurt" : 2,
            "YJump" : 9,
            "YAttack" : 7,
            "YAttack_2" : 10,
            "YDeath" : 10
        }
        self.images = {
            "YIdle" : [],
            "YWalk" : [],
            "YHurt" : [],
            "YJump" : [],
            "YAttack" : [],
            "YAttack_2": [],
            "YDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Attack" : 0,
            "Attack_2":0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.2,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Attack" : 1.5,
            "Attack_2": 1.5,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "YIdle", True, self.images_directory, 
            self.images, "Idle", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "YIdle", False, self.images_directory, 
            self.images, "Idle", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YWalk", True, self.images_directory, 
            self.images, "Run", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YWalk", False, self.images_directory, 
            self.images, "Run", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YHurt", True, self.images_directory, 
            self.images, "Hurt", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "YHurt", False, self.images_directory, 
            self.images, "Hurt", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YJump", True, self.images_directory,
            self.images, "Jump", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YJump", False, self.images_directory, 
            self.images, "Jump", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YAttack", True, self.images_directory, 
            self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YAttack", False, self.images_directory, 
            self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YAttack_2", True, self.images_directory, 
            self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YAttack_2", False, self.images_directory, 
            self.images, "Attack_2", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YDeath", True, self.images_directory, 
            self.images, "Dead", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "YDeath", False, self.images_directory, 
            self.images, "Dead", 128, 128, 0, width, height, self.adjW, 
            self.adjH
        )
        projectile_path = os.path.join(Yokai_path, "Fire.png")
        self.image_projectile_r = pygame.image.load(projectile_path)
        self.image_projectile_l = pygame.transform.flip(
            self.image_projectile_r, True, False
        )
        self.image_projectile_u = pygame.transform.rotate(
            self.image_projectile_l, 270
        )
        
    def actions(self, key_map : dict) -> None:
        """
        Handles the actions of the Yokai character based on the input 
        keys. This includes firing projectiles depending on the current 
        action and state of the character.

        Parameters
        ----------
        key_map : dict
            A dictionary that maps each key (as pygame constants) to a boolean indicating whether
            the key is pressed or not.
        
        Returns
        -------
        None

        """
        if (
            key_map[pygame.K_v] and self.projectile_cooldown <= 0 and 
            self.action != "Hurt" and self.action != "Death"
        ):
            self.attack_time = 0
            if key_map[pygame.K_w]:  
                new_projectile = Projectile(
                    self.rect.centerx, self.rect.centery, 0, -20, 
                    self.sub_TAG, self.damage, 30, 30, self.image_projectile_u
                )
                self.projectiles.append(new_projectile)
                self.action = "Attack_2"
                self.actual["Attack_2"] = 0
            elif self.from_the_front: 
                new_projectile = Projectile(
                    self.rect.centerx, self.rect.top, 20, 0, self.sub_TAG, 
                    self.damage, 30, 30, self.image_projectile_r
                )
                self.projectiles.append(new_projectile)
                self.action = "Attack"
                self.actual["Attack"] = 0
            else:
                new_projectile = Projectile(
                    self.rect.centerx, self.rect.top, -20, 0, self.sub_TAG, 
                    self.damage, 30, 30, self.image_projectile_l
                )
                self.projectiles.append(new_projectile)
                self.action = "Attack"
                self.actual["Attack"] = 0

            self.projectile_cooldown = self.cooldown_time

    def update(self) -> None:
        """
        Updates the state of the Yokai character, including tracking 
        attack time and resetting the action after a certain duration.
        This method is called every frame to keep the character's state 
        updated.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        super().update()
        self.attack_time += 1
        if (
            self.attack_time >= self.attack_animation and 
            (self.action == "Attack" or self.action == "Attack_2")
        ):
            self.action = None

    def draw(self, screen, camera):

        super().draw(screen, camera)

        if self.invincibility_cooldown >= 0 :
            self.sprites.draw(screen,128)
        else:
            self.sprites.draw(screen)

class Ninja(Player):
    """
    A class representing the Ninja character in the game. Inherits from 
    the `Player` class and adds specific behavior, animations, and 
    attributes for the Ninja.

    Attributes
    ----------
    jump_count_max : int
        Maximum number of jumps allowed for the Ninja.
    range : int
        The effective range of the Ninja's attack, calculated based on 
        the facing direction.
    attack_cooldown : int
        Tracks the cooldown time between attacks.
    attack_time : int
        Tracks the time spent in the attack animation.
    attack_animation : int
        Duration of the attack animation (in frames).
    cooldown_time : int
        Time interval between attacks.
    damage : int
        The amount of damage dealt by the Ninja in an attack.
    attack : str or None
        Holds the current attack state (could be None or a specific 
        attack type).
    sprites : Sprites
        An instance of `Sprites` to handle the Ninja's animations.
    adjW : int
        Width adjustment for sprite size.
    adjH : int
        Height adjustment for sprite size.
    adj : int
        General adjustment for the sprite's positioning.
    images_directory : dict
        Directory paths for each animation type.
    sizes_directory : dict
        Dictionary mapping each animation type to the number of frames.
    images : dict
        A dictionary holding the loaded images for each animation type.
    actual : dict
        Tracks the current frame of each animation.
    fps : dict
        Frames per second for each animation state, controlling 
        animation speed.

    Methods
    -------
    actions(key_map) -> None
        Handles the actions triggered by key presses.
    on_collision(other) -> None
        Handles the collision logic between the player and another 
        object.
    update() -> None
        Updates the state of the player.

    """
    def __init__(
        self, x : float, y : float, width : int, height : int
    ) -> None:
        """
        Initializes the class Ninja with values of atributes

        Parameters
        ----------
        x : float
            Initial x-coordinate of the Ninja.
        y : float
            Initial y-coordinate of the Ninja.
        width : int
            Width of the Ninja's bounding box.
        height : int
            Height of the Ninja's bounding box.
        """
        super().__init__(x, y, width, height)
        self.teste = "N"
        self.jump_count_max = 3
        self.rect_color = (255, 255, 255)
        self.range = (
            self.rect.centerx + 30 if self.from_the_front else 
            self.rect.centerx - 40
        )
        self.attack_cooldown = 0
        self.attack_time = 0
        self.attack_animation = 5
        self.cooldown_time = 20
        self.damage = 100
        self.attack = None

        self.sprites = Sprites()
        self.adjW = 50
        self.adjH = 35
        self.adj = 0
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        Ninja_path = os.path.join(path_game, os.pardir, "assets", "Ninja")
        self.images_directory = {
            "NIdle" : os.path.join(Ninja_path),
            "NWalk" : os.path.join(Ninja_path),
            "NRun" : os.path.join(Ninja_path),
            "NHurt" : os.path.join(Ninja_path),
            "NJump" : os.path.join(Ninja_path),
            "NAttack" : os.path.join(Ninja_path),
            "NDeath" : os.path.join(Ninja_path)
        }
        self.sizes_directory = {
            "NIdle" : 6,
            "NWalk" : 6,
            "NHurt" : 2,
            "NJump" : 7,
            "NAttack" : 6,
            "NDeath" : 4
        }
        self.images = {
            "NIdle" : [],
            "NWalk" : [],
            "NHurt" : [],
            "NJump" : [],
            "NAttack" : [],
            "NDeath" : []
        }
        self.actual = {
            "Idle" : 0,
            "Walk" : 0,
            "Hurt" : 0,
            "Jump" : 0,
            "Attack" : 0,
            "Death" : 0
        }
        self.fps = {
            "Idle" : 0.2,
            "Walk" : 0.5,
            "Hurt" : 0.1,
            "Jump" : 0.5,
            "Attack" : 1.5,
            "Death" : 0.3
        }
        self.sprites.load_spritesheets(
            self.sizes_directory, "NIdle", True, self.images_directory, 
            self.images, "Idle", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "NIdle", False, self.images_directory, 
            self.images, "Idle", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NWalk", True, self.images_directory, 
            self.images, "Run", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NWalk", False, self.images_directory, 
            self.images, "Run", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NHurt", True, self.images_directory, 
            self.images, "Hurt", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )        
        self.sprites.load_spritesheets(
            self.sizes_directory, "NHurt", False, self.images_directory, 
            self.images, "Hurt", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NJump", True, self.images_directory, 
            self.images, "Jump", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NJump", False, self.images_directory, 
            self.images, "Jump", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NAttack", True, self.images_directory, 
            self.images, "Attack_1", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NAttack", False, self.images_directory, 
            self.images, "Attack_1", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NDeath", True, self.images_directory, 
            self.images, "Dead", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "NDeath", False, self.images_directory, 
            self.images, "Dead", 96, 96, 0, width, height, self.adjW, 
            self.adjH
        )

    def actions(self, key_map : dict) -> None:
        """
        Handles the actions triggered by key presses, specifically 
        managing the attack action based on the provided key map and 
        cooldown conditions.

        Parameters
        ----------
        key_map : dict
            A dictionary mapping pygame key constants to boolean values 
            indicating whether the corresponding key is pressed.

        Returns
        -------
        None
        """ 

        if (
            key_map[pygame.K_v] and self.attack_cooldown <= 0 and 
            not self.action == "Hurt" and self.action != "Death"
        ):
            self.attack = Attack(self.range, self.rect.y, 20, 60, self.damage)
            self.attack_cooldown = self.cooldown_time
            self.action = "Attack"
            self.actual["Attack"] = 0
            self.attack_time = 0
        else:
            self.attack = None

    def on_collision(self, other : object) -> None:
        """
        Handles the collision logic between the player and another 
        object, specifically checking for interactions when the player 
        has an active attack.

        Parameters
        ----------
        other : GameObject
            The other object that the player collides with.

        Returns
        -------
        None
        """
        super().on_collision(other)

        if self.attack is not None:
            if (
                other.TAG == "Monster" and self.attack.rect.colliderect(other) 
                and other.immune == False
            ):
                other.life -= self.damage
                self.attack = None

    def update(self) -> None:
        """
        Updates the state of the player, including the attack cooldown, 
        attack time, and attack range based on the player's facing 
        direction.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super().update()

        self.range = (
            self.rect.centerx + 35 
            if self.from_the_front else self.rect.centerx - 60
        )

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1   

        self.attack_time += 1
        if (
            self.attack_time >= self.attack_animation and 
            self.action == "Attack"
        ):
            self.action = None

    def draw(self, screen, camera):

        super().draw(screen, camera)

        if self.invincibility_cooldown >= 0 :
            self.sprites.draw(screen,128)
        else:
            self.sprites.draw(screen)