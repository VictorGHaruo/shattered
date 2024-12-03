import pygame
from weapon import Projectile, Attack
import random
import os
import math
from assets import Sprites
from typing import Union

class Bosses:

    """
    Represents a boss character in the game.

    Attributes
    ----------
    TAG : str
        General identifier of the boss.
    sub_TAG : str
        Specific identifier or subtype of the boss.
    rect : pygame.Rect
        Rectangle representing the boss.
    gravity : int
        Acceleration due to gravity affecting the boss.
    speed_y : float
        Current vertical speed of the boss.
    speed_y_max : float
        Maximum allowed vertical speed of the boss.
    speed_x : float
        Current horizontal speed of the boss.
    life : int
        Current life points of the boss.
    hero : Player
        Rectangle representing the hero, used for interactions with the 
        boss.
    projectiles : list
        List of projectiles shot by the boss.
    screen_width : int
        The width of the game screen.
    is_dead : bool
        Indicates whether the boss is dead.
    immune : bool
        Indicates whether the boss is immune to attacks.
    death_position : float or None
        Stores the last known horizontal position of the boss when it 
        dies, as x coordinates, or None if still alive.

    Methods
    -------
    new_hero(hero) -> None
        Updates the hero object reference used by the boss for various 
        interactions.

    move() -> None
        Handles the movement mechanics of the boss, including position 
        changes and animations.

    update() -> None
        Updates all aspects of the boss, including its state, 
        projectiles, and applying gravity effects.

    draw(screen, camera) -> None
        Renders the boss and its projectiles on the screen, 
        applying appropriate camera transformations.

    on_collision(other) -> None
        Handles collision detection and response between the boss and 
        other objects, triggering specific actions when a collision 
        occurs.
    """

    def __init__(
        self, x: float, y: float, width: int, height: int, hero: "Player"
    ) -> None:
        
        """
        Initializates the boss character and its attributes.

        Parameters
        ----------
        x : float
            Horizontal position where the boss spawn.
        y : float
            Vertical position where the boss spawn.
        width : int
            Character's width.
        height : int
            Character's height.
        hero : Player
            Rectangle representing the hero, used for interaction.

        Returns
        -------
        None
            The function just initializes attributes.

        """

        self.TAG = "Monster"
        self.sub_TAG = "Monster"
        self.rect = pygame.Rect(x, y, width, height)
        self.gravity = 2
        self.speed_y = 0
        self.speed_y_max = 40
        self.speed_x = 0
        self.life = 50
        self.hero = hero
        self.projectiles = []
        self.screen_width = pygame.display.Info().current_w
        self.is_dead = False
        self.immune = False
        self.death_position = None
        # self.color = (255, 0, 0)

    def new_hero(self, hero: "Player"):
        """
        Update object hero used in methods of the boss.

        Parameters
        ----------
        hero : Player
            Rectangle representing the hero, used for interaction.

        Returns
        -------
        None
            This method updates the hero attribute of the boss.
        """

        self.hero = hero

    def move(self):
        pass

    def update(self):
        """    
        This method is responsible for applying gravity to the boss, 
        updating its vertical position, and updating the movement of all
        projectiles shot by the boss.

        Parameters
        ----------
        None 

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            current attributes of the boss and its projectiles.

        """

        self.speed_y += self.gravity
        self.rect.y += min(self.speed_y, self.speed_y_max)

        for projectile in self.projectiles:
            projectile.update()
        
    def draw (self, screen: pygame.Surface, camera: "Camera"):
        """
        Draws the boss and its projectiles, adjusting their positions 
        based on the camera movement. Additionally, it draws all the 
        boss sprites.

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

        if camera.TAG == "Camera":
            self.rect.x -= camera.position_x
            # pygame.draw.rect(screen, self.color, self.rect)
        for projectile in self.projectiles:
            if not screen.get_rect().colliderect(projectile.rect):
                self.projectiles.remove(projectile)
                del projectile
        
        self.sprites.draw(screen)
        
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            self.shot.draw(screen)

    def on_collision(self, other: Union["Player", "Ground"]):
        """
        Tests the boss and boss's projectiles collision with other 
        objects. If the projectile hits a Player, it reduces their 
        life; if it hits the Ground, it gets deleted. If the boss 
        collides with Ground, it interacts with the ground and doesn't 
        pass through it.

        Parameters
        ----------
        other : Union[Player, Ground]
            The other object that the boss interacts with.

        Return
        ------
        None
            This method modifies the state of the player (reducing life 
            and updating action) and handles the attack's state, but it 
            does not return any value.

        """  

        if (other.TAG == "Ground" and self.rect.colliderect(other) and 
            self.rect.bottom > other.rect.top and 
            self.rect.top < other.rect.top
        ):
            self.rect.bottom = other.rect.top

        for projectile in self.projectiles:
            if other.TAG == "Ground":
                if projectile.rect.colliderect(other):
                    self.projectiles.remove(projectile)
                    del projectile
            if other.TAG == "Player":
                if projectile.rect.colliderect(other):
                    other.life -= projectile.damage
                    other.action = "Hurt"
                    self.projectiles.remove(projectile)
                    del projectile

class Balrog(Bosses):
    """
    Represents the Balrog boss character in the game.

    Attributes
    ----------
    sub_TAG : str
        Identifier tag for the boss.
    speed_x : int
        Horizontal movement speed of Balrog.
    gravity : int
        Gravity effect applied to Balrog.
    life : int
        Amount of life Balrog possesses.
    probability : float
        Probability of moving left or right; 0.5 means equal probability
        for either direction.
    randomic : float
        Random number used for comparison with `probability`.
    cool_down_max : int
        Maximum cooldown time for choosing a direction.
    cool_down_min : int
        Minimum cooldown time for choosing a direction.
    cool_down : int
        Random number selected between `cool_down_max` and 
        `cool_down_min` representing the time spent moving in a chosen
        direction.
    move_cooldown : int
        Cooldown time between movement actions.
    projectile_cooldown : int
        Cooldown time for lightning attacks.
    atk_cooldown : int
        Cooldown time for normal attacks.
    atk_cooldowns : int
        Variable controlling the cooldown time, the reference cooldown.
    atk_time : int
        Duration of the attack phase, used as a reference.
    damage_timer : int
        Timer for handling damage invulnerability or effects.
    atk_when : int
        Timing threshold for triggering attacks.
    probability_atk : int
        Probability threshold for triggering attacks.
    warning_sign : int
        Time for displaying a warning before an attack.
    timers : list[str]
        List of timers used for various cooldowns.
    number_bars : int
        Number of attack zones.
    weapon_damage : int
        Damage dealt by Balrog's weapon.
    attacks : list
        List of current active attacks.
    all_atks : list[Attack]
        List of all attack instances initialized.
    sprites : Sprites
        Object handling the sprite animations for Balrog.
    lightning : Sprites
        Object handling the lightning effects or animations.
    images_directory : dict[str, str]
        Directory paths for different sprite sheets.
    sizes_directory : dict[str, int]
        Number of frames for each animation type.
    images : dict[str, list]
        Loaded images for animations.
    actual_balrog : dict[str, int]
        Current frame index for each animation.
    fps : dict[str, float]
        Frame rates for animations.
    adjH, adjW, adjH_atk, adjW_atk, adj : int
        Adjustments for sprite positioning and scaling.

    Methods
    -------
    update() -> None
        Updates Balrog's attributes and animations.
    move() -> None
        Handles Balrog's movement.
    attack() -> None
        Manages Balrog's attack patterns.
    draw(screen, camera) -> None
        Draws Balrog and its attacks on the screen.
    on_collision(other) -> None
        Handles collision logic with other game objects.
    """

    def __init__(
        self, x: float, y: float, width: int, height: int, hero: "Player"
    ) -> None:
        """
        Initializes the class Balrog with values of atributes.

        Parameters
        ----------
        x : float
            Horizontal position where the boss spawn.
        y : float
            Vertical position where the boss spawn.
        width : int
            Character's width.
        height : int
            Character's height.
        hero : Player
            Rectangle representing the hero, used for interaction.
        """
        super().__init__(x, y, width, height, hero)
        self.sub_TAG = "Balrog"

        self.speed_x = 3
        self.gravity = 0
        self.life = 1

        self.probability = 0.5
        self.randomic = 0.5

        self.cool_down_max = 50
        self.cool_down_min = 20

        self.cool_down = 0
        self.move_cooldown = 0

        self.projectile_cooldown = 0

        self.atk_cooldown = 100
        self.atk_cooldowns = 100
        
        self.atk_time = 110
        self.damage_timer = 0
        self.atk_when = 30
        self.probability_atk = 0
        self.warning_sign = 50

        self.timers = [
            "damage_timer", "move_cooldown", "atk_cooldown", 
            "projectile_cooldown"
        ]

        self.number_bars = 3
        self.weapon_damage = 100

        self.attacks = []
        self.all_atks = []
        
        for atks in range(self.number_bars):
            self.all_atks.append(
                Attack(
                    self.screen_width/self.number_bars * atks, 10 + atks, 
                    self.screen_width / self.number_bars, 650, 
                    self.weapon_damage
                )
            )

        self.color = (255, 192, 203)

        self.sprites = Sprites()
        self.lightning = Sprites()
        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")
        self.adjH = 150
        self.adjW = 150
        self.adjH_atk = 300
        self.adjW_atk = 300
        self.adj = 50

        self.images_directory = {
            "BWalk" : os.path.join(assets_directory, "Balrog", "fly"),
            "BAttack" : os.path.join(assets_directory, "Balrog", "lightning"),
            "BDeath" : os.path.join(assets_directory, "Balrog", "death")
        }

        self.sizes_directory = {
            "BWalk" : 6,
            "BAttack" : 11,
            "BDeath" : 11
        }

        self.images = {
            "BWalk" : [],
            "BAttack" : [],
            "BDeath" : []
        }

        self.actual_balrog = {
            "Walk" : 0,
            "Attack" : 0,
            "Death" : 0
        }

        self.fps = {
            "Walk" : 0.3,
            "Attack" : 0.3,
            "Death" : 0.3
        }

        self.sprites.load_images(
            True, width, height, "BWalk", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "BWalk", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            True, width, height, "BAttack", self.images, self.sizes_directory, 
            self.images_directory, self.adjW_atk, self.adjH_atk
        )
        self.sprites.load_images(
            False, width, height, "BAttack", self.images, self.sizes_directory, 
            self.images_directory, self.adjW_atk, self.adjH_atk
        )
        self.sprites.load_images(
            True, width, height, "BDeath", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "BDeath", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )

    def attack(self) -> None:
        """
        Handles Balrog's attack mechanics. 

        When the `atk_cooldown` reaches the `warning_sign`, a random 
        attack zone is selected from the available attacks, and the 
        boss moves to a position where it won't take damage. After 
        executing the attack, the cooldown is reset, along with an 
        additional attack duration (`atk_long`).

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It updates the 
            `attacks` attribute with the chosen attack and resets the 
            `atk_cooldown` timer.
        """

        if self.atk_cooldown == self.warning_sign:
            self.probability_atk = random.randint(0, len(self.all_atks) - 1)
            self.rect.x = (
                self.screen_width/self.number_bars * self.probability_atk + 
                self.screen_width/(2*self.number_bars)
            )

        if self.atk_cooldown <= 0:
            for atks in range(len(self.all_atks)):
                if atks != self.probability_atk:
                    self.attacks.append(self.all_atks[atks])
                    self.atk_cooldown = self.atk_cooldowns
        if (
            self.atk_cooldown < self.atk_time - self.atk_when and 
            len(self.attacks) != 0
        ):

            self.attacks.clear()

    def move(self) -> None:
        """
        Handles the Balrog's movement. The direction of movement 
        (left or right) is randomly chosen based on `self.randomic`. 
        Afterward, a cooldown (`self.cool_down`) is randomly selected 
        to determine how long the boss will move in that direction. The 
        movement occurs only if `self.move_cooldown` is less than or 
        equal to zero. The method also updates the movement animation 
        based on the direction.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            position of the boss and updates its animation state.
        
        """
        if self.move_cooldown <= 0 :
            self.randomic = random.random()
            self.cool_down = random.randint(
                self.cool_down_min, self.cool_down_max
            )       
            self.move_cooldown = self.cool_down
        
        if self.randomic >= self.probability:
            self.rect.x = self.rect.x + self.speed_x
            self.sprites.assets(
                self.rect, "Walk", self.actual_balrog, "R", self.fps["Walk"], 
                self.images, self.adj, "B"
            )

        else:
            self.rect.x = self.rect.x - self.speed_x
            self.sprites.assets(
                self.rect, "Walk", self.actual_balrog, "L", 
                self.fps["Walk"], self.images, self.adj, "B"
            )

    def draw(self, screen: pygame.Surface, camera: "Camera") -> None:
        """
        Draws the boss lightning attacks putting its sprites.

        Parameters
        ----------
        screen : pygame.Surface
            The surface where the lightning will be drawn.
        camera : Camera
            The camera object used to adjust the boss's position.

        Returns 
        -------
        None
            This method does not return a value. It directly modifies 
            the screen by drawing the lightning attack sprites.

        """
        super().draw(screen, camera)
        if len(self.attacks) != 0:
            for atks in self.attacks:
                # atks.draw(screen)
                self.lightning.assets(
                    atks.rect, "Attack", self.actual_balrog, "L", 
                    self.fps["Attack"], self.images, 0, "B"
                )
                self.lightning.draw(screen)       

    def on_collision(self, other: "Player") -> None:
        """
        Tests for collisions between the boss's attacks and the player.
        If an attack (lightning) hits the player, the player's life is 
        reduced. If the attack collides with the ground after hitting 
        the player, it is deleted.

        This method checks all active attacks for collisions with the 
        player. If a collision is detected, the player's life is 
        decreased by the attack's damage, and the player's action is 
        set to "Hurt". After the attack, a cooldown is applied before 
        further damage can be dealt.

        Parameters
        ----------
        other : Player
            The Player that the boss interacts with.

        Return
        ------
        None
            This method modifies the state of the player (reducing life 
            and updating action) and handles the attack's state, but it 
            does not return any value.

        """ 
        for atks in self.attacks:
            if other.TAG == "Player":
                if atks.rect.colliderect(other) and self.damage_timer == 0:
                    other.life -= atks.damage
                    other.action = "Hurt"
                    self.damage_timer = self.atk_cooldowns
            del atks
        return super().on_collision(other)

    def update(self) -> None:
        """        
        Updates the attributes of the Ganon boss. This method 
        manages the timers, detects when and where the boss dies, 
        and animates the boss.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            current attributes of the boss and updates the corresponding 
            animations for death.
       
        """

        if self.life > 0:
            self.move()
            self.attack()

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        for time in self.timers:
            if getattr(self,time) > 0:
                setattr(self, time, getattr(self, time) - 1)

        if self.life <= 0:
            self.gravity = 2
            if self.rect.x - self.death_position > 0:
                self.sprites.assets(
                    self.rect, "Death", self.actual_balrog, "L", 
                    self.fps["Death"], self.images, self.adj, "B"
                )
                if self.actual_balrog["Death"] >= len(self.images["BDeath"])/2:
                    self.is_dead = True
            elif self.rect.x - self.death_position <= 0:
                self.sprites.assets(
                    self.rect, "Death", self.actual_balrog, "R", 
                    self.fps["Death"], self.images, self.adj, "B"
                )
                if self.actual_balrog["Death"] >= len(self.images["BDeath"]):
                    self.is_dead = True

        return super().update()

class Ganon(Bosses):
    """
    A class representing the boss character Ganon, inheriting from the 
    Bosses base class. This class handles Ganon's attributes, 
    animations, and attack logic within the game.

    Attributes
    ----------
    sub_TAG : str
        The sub-type identifier for the boss (set to "Ganon").
    width : int
        The width of Ganon's hitbox.
    life : int
        The current life of Ganon.
    is_dead : bool
        Flag indicating whether Ganon is dead.
    atk_timer : int
        Timer controlling Ganon's attack frequency.
    atk_cooldown : int
        The cooldown period after each attack.
    atk_long : int
        The duration of the attack's cooldown period.
    teleport : int
        The duration for which Ganon can teleport.
    teleport_cooldown : int
        Timer for teleportation cooldown.
    adjH : int
        Adjustment value for height used in sprite rendering.
    adjW : int
        Adjustment value for width used in sprite rendering.
    adj : int
        General adjustment value for Ganon's position.
    sprites : Sprites
        Instance of the Sprites class used to manage Ganon's sprite 
        sheets.
    shot : Sprites
        Instance of the Sprites class used for Ganon's projectile 
        sprites.
    images_directory : dict
        A dictionary storing the paths to Ganon's image directories.
    sizes_directory : dict
        A dictionary storing the sprite sizes for different animation 
        states.
    images : dict
        A dictionary storing the loaded images for each animation state.
    actual_ganon : dict
        A dictionary tracking the current frame of each animation state.
    fps : dict
        A dictionary specifying the frames per second for each 
        animation.

    Methods
    -------
    update() -> None
        Updates Ganon's attributes and animations.
    attack() -> None
        Executes Ganon's attack logic.
    distance(other) -> float
        Calculates the distance to another object.
    move() -> None
        Controls Ganon's movement.
    
    """

    def __init__(
        self, x: float, y: float, width: int, height: int, hero: "Player"
    ) -> None:
        """
        Inicializes the class Ganon with values of atributes

        Parameters
        ----------
        x : float
            Horizontal position where the boss spawn.
        y : float
            Vertical position where the boss spawn.
        width : int
            Character's width.
        height : int
            Character's height.
        hero : Player
            Rectangle representing the hero, used for interaction.
        
        """
        super().__init__(x, y, width, height, hero)

        self.sub_TAG = "Ganon"
        self.width = width

        self.color = (160, 32, 240)

        self.life = 1
        self.is_dead = False

        self.atk_timer = 100
        self.atk_cooldown = self.atk_timer
        self.atk_long = 30

        self.teleport = 40
        self.teleport_cooldown = self.teleport

        self.adjH = 100
        self.adjW = 120 
        self.adj = 25

        self.sprites = Sprites()
        self.shot = Sprites()

        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")

        self.images_directory = {
            "GIdle" : os.path.join(assets_directory, "Ganon"),
            "GAttack" : os.path.join(assets_directory, "Ganon"),
            "GImmune" : os.path.join(assets_directory, "Ganon"),
            "GProjectile" : os.path.join(assets_directory, "Ganon"),
            "GDeath" : os.path.join(assets_directory, "Ganon")
        }

        self.sizes_directory = {
            "GIdle" : 4,
            "GAttack" : 5,
            "GImmune" : 8,
            "GProjectile" : 1,
            "GDeath" : 14
        }

        self.images = {
            "GIdle" : [],
            "GAttack" : [],
            "GImmune" : [],
            "GProjectile" : [],
            "GDeath" : []
        }

        self.actual_ganon = {
            "Idle" : 0,
            "Attack" : 0,
            "Immune" : 0,
            "Death" : 0
        }

        self.fps = {
            "Idle" : 0.2,
            "Attack" : 0.15,
            "Immune" : 0.4,
            "Death" : 0.2
        }

        self.sprites.load_spritesheets(
            self.sizes_directory, "GIdle", True, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 0, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GIdle", False, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 0, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GAttack", True, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 100, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GAttack", False, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 100, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GImmune", True, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 300, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GImmune", False, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 300, width, height, 
            self.adjW, self.adjH
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GDeath", False, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 700, width, height, 
            self.adjW, self.adjH, 10
        )
        self.sprites.load_spritesheets(
            self.sizes_directory, "GDeath", True, self.images_directory, 
            self.images, "Character_sheet", 100, 100, 700, width, height, 
            self.adjW, self.adjH, 10
        )
        self.sprites.load_images(
            True, 70, 28, "GProjectile", self.images, self.sizes_directory, 
            self.images_directory, 0, 0
        )
        self.sprites.load_images(
            False, 70, 28, "GProjectile", self.images, self.sizes_directory, 
            self.images_directory, 0, 0
        ) 

    def update(self) -> None:
        """
        Updates the attributes of the Ganon boss. This method manages 
        the timers, detects when the boss dies, and animates the boss.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            current attributes of the boss and updates the corresponding
            animations for movement and death.
        """

        if self.atk_timer > 0:
            self.atk_timer -= 1        

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        if self.life <= 0 and self.rect.x - self.death_position <= 0:
            self.sprites.assets(
                self.rect, "Death", self.actual_ganon, "L", self.fps["Death"], 
                self.images, self.adj, "G"
            )

            if self.actual_ganon["Death"] >= len(self.images["GDeath"])/2:
                
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.death_position > 0:
            self.sprites.assets(
                self.rect, "Death", self.actual_ganon, "R", self.fps["Death"], 
                self.images, self.adj, "G"
            )

            if self.actual_ganon["Death"] >= len(self.images["GDeath"]):
                self.is_dead = True
            
        if self.life > 0:
            self.attack()
            self.move()
        return super().update()

    def attack(self) -> None:
        """
        Handles Ganon's attack mechanics. When the `atk_timer` reaches 
        zero and the distance between Ganon and the Player exceeds 200 
        units, Ganon launches multiple projectiles in the direction of 
        the Player. The attack animation and projectile creation are 
        managed within this method.

        After executing the attack, the attack timer (`atk_timer`) is 
        reset to control the cooldown.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies 
            `self.projectiles` by adding new instances of `Projectile` 
            and updates the attack timer.
        """
        if self.atk_timer <= self.atk_long and self.distance(self.hero) > 200:

            if self.hero.rect.x - self.rect.x <= 0:
                self.sprites.assets(
                    self.rect, "Attack", self.actual_ganon, "L", 
                    self.fps["Attack"], self.images, self.adj, "G"
                )
                if self.atk_timer <= 0:
                    self.actual_ganon["Attack"] = 0
                    self.new_projectiles = [
                                Projectile(
                                    self.rect.left -50, self.rect.centery + 47,
                                    -10, 0, self.TAG, 20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                                Projectile(
                                    self.rect.left -31, self.rect.centery + 8,
                                    -10, 0, self.TAG, 20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                                Projectile(
                                    self.rect.left -42, self.rect.centery - 54, 
                                    -10, 0, self.TAG, 20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                                Projectile(
                                    self.rect.left + 5, 
                                    self.rect.centery - 113, -10, 0, self.TAG, 
                                    20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                                Projectile(
                                    self.rect.left - 37, 
                                    self.rect.centery - 150, -10, 0, self.TAG, 
                                    20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                                Projectile(
                                    self.rect.left - 33, 
                                    self.rect.centery - 212, -10, 0, self.TAG, 
                                    20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),                    
                                Projectile(
                                    self.rect.left - 50, 
                                    self.rect.centery - 257, -10, 0, self.TAG, 
                                    20, 35*2, 14*2, 
                                    self.images["GProjectile"][1]
                                ),
                    ]

                    for projectile in self.new_projectiles:
                        self.projectiles.append(projectile)
                    self.atk_timer = self.atk_cooldown + self.atk_long 

            if self.hero.rect.x - self.rect.x  > 0:
                self.sprites.assets(
                    self.rect, "Attack", self.actual_ganon, "R", 
                    self.fps["Attack"], self.images, self.adj, "G"
                )

                if self.atk_timer <= 0:
                    self.actual_ganon["Attack"] = 0
                    self.new_projectiles = [
                        Projectile(
                            self.rect.right +50, self.rect.centery + 47, 10, 0, 
                            self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                        Projectile(
                            self.rect.right +31, self.rect.centery + 8, 10, 0, 
                            self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                        Projectile(
                            self.rect.right +42, self.rect.centery - 54, 10, 0, 
                            self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                        Projectile(
                            self.rect.right - 5, self.rect.centery  - 113, 10, 
                            0, self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                        Projectile(
                            self.rect.right + 37, self.rect.centery - 150, 10, 
                            0, self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                        Projectile(
                            self.rect.right + 33, self.rect.centery  - 212, 10, 
                            0, self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),                    
                        Projectile(
                            self.rect.right + 50, self.rect.centery - 257, 10, 
                            0, self.TAG, 20, 35*2, 14*2, 
                            self.images["GProjectile"][0]
                        ),
                    ]
                    for projectile in self.new_projectiles:
                        self.projectiles.append(projectile)
                    self.atk_timer = self.atk_cooldown + self.atk_long

    def distance(self, other: "Player") -> float:
        """
        Calculates the Euclidean distance between boss and another 
        object.

        Parameters
        ----------
        other : Player
            Object to be calcute the distance. Must have a `rect` 
            attribute with `centerx` and `centery` properties.

        Return
        float
            Euclidean distance between Ganon and other.

        """

        delta_x = self.rect.centerx - other.rect.centerx
        delta_y = self.rect.centery - other.rect.centery

        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
        return distance

    def move(self) -> None:
        """
        Manages Ganon's movement and teleportation mechanics based on 
        the distance from the Player. If Ganon is far from the Player 
        and not attacking, he remains idle. When the Player is close, 
        Ganon activates his "Immune" animation and teleports to the 
        opposite side of the screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It updates Ganon's 
            position, animation state, and teleport cooldown.
        """

        if self.distance(self.hero) > 200 and self.atk_timer > self.atk_long:
            self.immune = False
            self.teleport_cooldown = self.teleport
            if self.hero.rect.centerx - self.rect.centerx < 0:
                self.actual_ganon["Immune"] = 0 
                self.sprites.assets(
                    self.rect, "Idle", self.actual_ganon, "L", 
                    self.fps["Idle"], self.images, self.adj, "G"
                )

            elif self.hero.rect.centerx - self.rect.centerx > 0:
                self.actual_ganon["Immune"] = 8
                self.sprites.assets(
                    self.rect, "Idle", self.actual_ganon, "R", 
                    self.fps["Idle"], self.images, self.adj, "G"
                )

        if self.distance(self.hero) <= 200:
            self.immune = True
            if self.teleport_cooldown > 0:
                self.teleport_cooldown -= 1
                if (
                    self.hero.rect.centerx - self.rect.centerx < 0 and 
                    self.actual_ganon["Immune"] < 8
                ):
                    self.sprites.assets(
                        self.rect, "Immune", self.actual_ganon, "L", 
                        self.fps["Immune"], self.images, self.adj, "G"
                    )

                if (
                    self.hero.rect.centerx - self.rect.centerx > 0 and 
                    self.actual_ganon["Immune"] < 16 and 
                    self.actual_ganon["Immune"] >= 8
                ):
                    self.sprites.assets(
                        self.rect, "Immune", self.actual_ganon, "R", 
                        self.fps["Immune"], self.images, self.adj, "G"
                    )
                    

            if (
                self.hero.rect.centerx - self.rect.centerx < 0 and 
                self.teleport_cooldown <= 0
            ):
                self.actual_ganon["Immune"] = 0
                self.rect.x = 0.1 * self.screen_width
                self.rect.y = 0 #retirar dps
            elif (
                self.hero.rect.centerx - self.rect.centerx > 0 and 
                self.teleport_cooldown <= 0
            ):
                self.actual_ganon["Immune"] = 8
                self.rect.x = 0.9 * self.screen_width
                self.rect.y = 0 #retirar dps

class Demagorgon(Bosses):

    """
    A class representing the boss character Demagorgon, inheriting from 
    the Bosses base class. This class handles Demagorgon's attributes, 
    animations, and attack logic within the game.

    Attributes
    ----------
    sub_TAG : str
        A unique identifier for Demagorgon.
    speed_x : int
        The horizontal movement speed of Demagorgon.
    attacks : None or Attack
        The attack object associated with Demagorgon.
    atk_cooldown : int
        The cooldown time (frames) between attacks.
    atk_timer : float
        A timer tracking attack cooldown.
    atk_long : int
        The duration (frames) of Demagorgon's attack animation.
    weapon_width : int
        The width of Demagorgon's weapon.
    weapon_height : int
        The height of Demagorgon's weapon.
    weapon_damage : int
        The damage dealt by Demagorgon's weapon.
    damage_timer : float
        A timer tracking invulnerability frames after attacking.
    sprites : Sprites
        An object responsible for handling sprite animations and image 
        loading.
    main_directory : str
        The main directory path of the project.
    assets_directory : str
        The directory path containing asset files.
    adjH : int
        Height adjustment factor for sprites.
    adjW : int
        Width adjustment factor for sprites.
    adj : int
        General adjustment factor for positioning.
    images_directory : dict[str, str]
        Paths to different Demagorgon animation folders.
    sizes_directory : dict[str, int]
        Frame counts for each animation type.
    images : dict[str, list]
        Loaded image frames for each animation type.
    actual_demagorgon : dict[str, float]
        Current frame indices for each animation type.
    fps : dict[str, float]
        Frame rates for each animation type.

    Methods
    -------
    attack() -> None
        Executes Demagorgon's attack logic.
    move() -> None
        Executes Demagorgon's movement logic.
    update() -> None
        Updates Demagorgon's attributes and animations.

    """

    def __init__(
            self, x: float, y: float, width: int, height: int, hero: "Player"
    ) ->None :
        """
        Initializes the class Demagorgon with values of atributes

        Parameters
        ----------
        x : float
            Horizontal position where the boss spawn.
        y : float
            Vertical position where the boss spawn.
        width : int
            Character's width.
        height : int
            Character's height.
        hero : Player
            Rectangle representing the hero, used for interaction.
        """

        super().__init__(x, y, width, height, hero)
        self.sub_TAG = "Demagorgon"

        #hitbox
        # self.color = (255, 255, 0)

        self.speed_x = 3

        self.attacks = None
        self.atk_cooldown = 100
        self.atk_timer = self.atk_cooldown
        self.atk_long = 50

        self.weapon_width = 130
        self.weapon_height = height
        self.weapon_damage = 100
        self.damage_timer = 0

        self.sprites = Sprites()
        main_directory = os.path.dirname(os.path.dirname(__file__))
        assets_directory = os.path.join(main_directory, "assets")

        self.adjH = 200
        self.adjW = 200
        self.adj = 75

        self.images_directory = {
            "DWalk" : os.path.join(assets_directory, "Demagorgon", "walk"),
            "DIdle" : os.path.join(assets_directory, "Demagorgon", "idle"),
            "DAttack" : os.path.join(assets_directory, "Demagorgon", "1_atk"),
            "DDeath" : os.path.join(assets_directory, "Demagorgon", "death")
        }

        self.sizes_directory = {
            "DWalk" : 10,
            "DIdle" : 6,
            "DAttack" : 14,
            "DDeath" : 16
        }

        self.images = {
            "DWalk" : [],
            "DIdle" : [],
            "DAttack" : [],
            "DDeath" : []
        }

        self.actual_demagorgon = {
            "Walk" : 0,
            "Idle" : 0,
            "Attack" : 0,
            "Death" : 0
        }

        self.fps = {
            "Walk" : 0.4,
            "Idle" : 0.4,
            "Attack" : 0.3,
            "Death" : 0.25
        }

        self.sprites.load_images(
            True, width, height, "DWalk", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "DWalk", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            True, width, height, "DIdle", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "DIdle", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            True, width, height, "DAttack", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "DAttack", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            True, width, height, "DDeath", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )
        self.sprites.load_images(
            False, width, height, "DDeath", self.images, self.sizes_directory, 
            self.images_directory, self.adjW, self.adjH
        )

    def attack(self) -> None:
        """
        Handles Demagorgon's  attack mechanics. When the `atk_timer` 
        is less than or equal to zero, it creates a rectangle that 
        simulates the Demagorgon's punch, and the Demagorgon attacks 
        in the direction of the hero.

        After executing the attack, the `atk_timer` is reset with the 
        cooldown time and additional attack duration (`atk_long`).

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            `attacks` attribute and resets the `atk_timer`.
         """

        if self.atk_timer <= 0:
            if self.rect.x - self.hero.rect.x <= 0:
                self.attacks = Attack(
                    self.rect.right, self.rect.top, self.weapon_width, 
                    self.weapon_height, self.weapon_damage
                )
                self.atk_timer = self.atk_cooldown + self.atk_long

            if self.rect.x - self.hero.rect.x > 0:
                self.attacks = Attack(
                    self.rect.left - self.weapon_width, self.rect.top, 
                    self.weapon_width, self.weapon_height, self.weapon_damage
                )
                self.atk_timer = self.atk_cooldown + self.atk_long

    def move(self) -> None:
        """
        Handles the Demagorgon's movement. If Demagorgon is not 
        attacking, it follows the hero.
        If Demagorgon collides with the hero, it stops following.

        This method also handles the boss's animation: 
        - If the Demagorgon is not colliding with the hero, it walks 
        towards the hero.
        - If it collides with the hero, it becomes idle.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            position of the boss and updates its animation state.
        """
        super().move()
        if self.atk_timer < self.atk_cooldown:
            if self.rect.x - self.hero.rect.x <= 0:
                
                if self.rect.colliderect(self.hero) == False:
                    self.sprites.assets(
                        self.rect, "Walk", self.actual_demagorgon, "L", 
                        self.fps["Walk"], self.images, self.adj, "D"
                    )
                    self.rect.x = self.rect.x + self.speed_x
                else:
                    self.sprites.assets(
                        self.rect, "Idle", self.actual_demagorgon, "L", 
                        self.fps["Idle"], self.images, self.adj, "D"
                    )

            elif self.rect.x - self.hero.rect.x > 0:
                if self.rect.colliderect(self.hero) == False:
                    self.sprites.assets(
                        self.rect, "Walk", self.actual_demagorgon, "R", 
                        self.fps["Walk"], self.images, self.adj, "D"
                    )

                    self.rect.x = self.rect.x - self.speed_x
                else:
                    self.sprites.assets(
                        self.rect, "Idle", self.actual_demagorgon, "R", 
                        self.fps["Idle"], self.images, self.adj, "D"
                    )
    
    def update(self) -> None:
        """
        Updates the attributes of the Demagorgon boss. This method 
        manages the timers, detects when the boss dies, and animates 
        the boss and its attacks accordingly.

        It updates the attack timer (`atk_timer`) and damage timer 
        (`damage_timer`), checks for the boss's death and animates the 
        death sequence, as well as handling the movement and attack 
        animations when the boss is still alive.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It modifies the 
            current attributes of the boss and updates the corresponding 
            animations for movement, attack, and death.
        """
        if self.atk_timer > 0:
            self.atk_timer -= 1
        
        if self.damage_timer > 0:
            self.damage_timer -=1

        if self.life <= 0 and self.death_position == None:
            self.death_position = self.hero.rect.x

        if self.life <= 0 and self.rect.x - self.death_position <= 0:
            self.sprites.assets(
                self.rect, "Death", self.actual_demagorgon, "L", 
                self.fps["Death"], self.images, self.adj, "D"
            )

            if self.actual_demagorgon["Death"] >= len(self.images["DDeath"])/2:
                
                self.is_dead = True
        elif self.life <= 0 and self.rect.x - self.death_position > 0:
            self.sprites.assets(
                self.rect, "Death", self.actual_demagorgon, "R", 
                self.fps["Death"], self.images, self.adj, "D"
            )

            if self.actual_demagorgon["Death"] >= len(self.images["DDeath"]):
                self.is_dead = True

        if self.life > 0:
            if (
                self.atk_timer > self.atk_cooldown and 
                self.rect.x - self.hero.rect.x <= 0
            ):
                self.sprites.assets(
                    self.rect, "Attack", self.actual_demagorgon, "L", 
                    self.fps["Attack"], self.images, self.adj, "D"
                )

            if (
                self.atk_timer > self.atk_cooldown and 
                self.rect.x - self.hero.rect.x > 0
            ):
                self.sprites.assets(
                    self.rect, "Attack", self.actual_demagorgon, "R", 
                    self.fps["Attack"], self.images, self.adj, "D"
                )

            self.move()
            self.attack()
        
        return super().update()