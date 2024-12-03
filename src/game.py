import pygame
from player import Knight, Yokai, Ninja
from camera import Camera
from maker import maping
from boss import Balrog, Ganon, Demagorgon
from assets import Herolife, Bar, Bosslife
import os, sys, random

class GameManager:
    """
    Manages the core game mechanics, including hero selection, enemies, 
    bosses, and environment.

    Attributes
    ----------
    heros : list
        List of hero characters available for selection.
    actual_hero : int
        Index of the currently active hero.
    hero : object
        The currently active hero instance.
    camera : Camera
        Camera object to manage the visible game area.
    grounds : list
        List of ground objects in the game world.
    enemies : list
        List of enemies in the game world.
    bosses : list
        List of bosses currently active in the game.
    order : list
        List defining the spawn order of bosses.
    life_bar : Herolife
        Hero's health bar object.
    hero_timer : Bar
        Timer for hero switching cooldown.
    keys_trade : list
        Attributes shared among heroes when switching.
    bg_images : list
        Background images for parallax scrolling.
    bg_boss : Surface
        Background image for boss fights.
    pos_x : int
        X-coordinate for background scrolling.
    pos_x_p : int
        X-coordinate offset for parallax scrolling.

    Methods
    -------
    music(main, volume)
        Manages music playback based on game state.
    on_event(event, main)
        Handles events during gameplay.
    on_key_pressed()
        Handles continuous key presses.
    update()
        Updates all game elements, including enemies, bosses, 
        and camera.
    collision_decetion()
        Detects and handles collisions between game entities.
    elimination(change_state)
        Removes defeated enemies or bosses, and transitions state 
        if the hero dies.
    draw(screen)
        Draws all game elements to the screen.
    trade(event)
        Switches between available heroes.
    """

    def __init__(self, main: object) -> None:
        """
        Initializes the GameManager with heroes, enemies, bosses, and 
        other game elements.

        Parameters
        ----------
        main : object
            The main game instance, used to access global settings.

        Returns
        -------
        None
        """
        self.heros = [
            Knight(0, 0, 40, 70),
            Yokai(0, 0, 40, 70),
            Ninja(0, 0, 40, 70),
        ]
        self.actual_hero = 0
        self.hero = self.heros[self.actual_hero]
        self.camera = Camera(main.WIDTH)
        self.grounds = []
        self.enemies = []
        
        #Making the map with ground and enemies
        maping(self.grounds, self.enemies, self.hero)
        
        self.WIDTH = main.WIDTH
        self.HEIGHT = main.HEIGHT
        self.main = main
        self.bosses = []
        self.order = [
            Demagorgon(0, 0, 100, 300, self.hero),
            Balrog(200, 100, 140, 180, self.hero),
            Ganon(300, 0, 150, 220, self.hero),
        ]
        self.life_bar = Herolife(self.hero, 400, 20, 10)
        self.hero_timer = Bar(
            self.hero.trade_cooldown_time, 20, 30, 100, 20, 
            (255, 255, 255), (0, 0, 255)
        )
        
        self.keys_trade = [
            "rect", "life", "speed_x", "speed_y", "jump_count", "is_running",
            "on_ground", "to_left", "to_right", "from_the_front",
            "invincibility_time", "projectiles", "touched_obelisk", 
            "can_push_block",
        ]
        
        #BackGround image
        self.bg_images = []
        Background_path = os.path.join(main.assets_path, "Background")
        image_path = os.path.join(Background_path, "boss_fase.png")
        self.bg_boss = pygame.image.load(image_path).convert_alpha()
        self.bg_boss = pygame.transform.scale(
            self.bg_boss, (self.WIDTH, self.HEIGHT)
        )
        
        #Parallax
        for i in range(1, 4):
            image_path = os.path.join(Background_path, f"background_{i}.png")
            bg_image = pygame.image.load(image_path).convert_alpha()
            bg_image = pygame.transform.scale(
                bg_image, (self.WIDTH, self.HEIGHT)
            )
            self.bg_images.append(bg_image)
        self.pos_x = -self.WIDTH
        self.pos_x_p = -self.WIDTH

    def music(self, main: object, volume: float) -> None:
        """
        Manages background music based on the current game state.

        Parameters
        ----------
        main : object
            The main game instance.
        volume : float
            The volume level for music playback.

        Returns
        -------
        None
        """
        if main.is_changed:
            music_dir_path = os.path.join(main.assets_path, "Music")
            if self.camera.boss_fase:
                music_num = random.randint(1, 2)
                music_path = os.path.join(
                    music_dir_path, "Boss", f"B{music_num}.mp3"
                )
                pygame.mixer.music.load(music_path)
            elif self.hero.can_push_block:
                music_num = random.randint(1, 3)
                music_path = os.path.join(
                    music_dir_path, "Obelisk", f"O{music_num}.mp3"
                )
                pygame.mixer.music.load(music_path)
            else:
                music_num = random.randint(1, 3)
                music_path = os.path.join(
                    music_dir_path, "World", f"W{music_num}.mp3"
                )
                pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        main.is_changed = False

    def on_event(self, event: pygame.event.Event, main: object) -> None:
        """
        Handles events during gameplay, such as user inputs.

        Parameters
        ----------
        event : pygame.event.Event
            The event object captured during the game loop.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        self.trade(event)
        self.hero.on_event(event, main)

    def on_key_pressed(self) -> None:
        """
        Handles continuous key presses for hero movement and actions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        key_map = pygame.key.get_pressed()
        self.hero.on_key_pressed(key_map, self.main)
        self.hero.actions(key_map)

    def update(self) -> None:
        """
        Updates the state of all game entities, including the hero,
        enemies, bosses, camera, and associated objects.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.hero.update()
        self.life_bar.update(self.hero)
        self.hero_timer.update(self.hero.trade_cooldown)
        self.camera.update_coods(self.hero, self.main)

        if len(self.bosses) == 0 and len(self.order) != 0:
            self.bosses.append(self.order[0])
            del self.order[0]

        for ground in self.grounds:
            ground.update()

        for monster in self.enemies:
            monster.update()
            monster.new_hero(self.hero)

        for boss in self.bosses:
            boss.update()
            boss.new_hero(self.hero)

    def collision_decetion(self) -> None:
        """
        Detects and resolves collisions between all entities in the 
        game, such as the hero, enemies, bosses, and ground objects.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for ground in self.grounds:
            ground.on_collision(self.hero)
            self.hero.on_collision(ground)

            for enemie in self.enemies:
                self.hero.on_collision(enemie)
                enemie.on_collision(self.hero)
                enemie.on_collision(ground)
                ground.on_collision(enemie)

            for boss in self.bosses:
                boss.on_collision(self.hero)
                self.hero.on_collision(boss)
                ground.on_collision(boss)
                boss.on_collision(ground)

            if ground.sub_TAG == "Block":
                for gro in self.grounds:
                    ground.on_collision(gro)

    def elimination(self, change_state) -> None:
        """
        Eliminates defeated enemies or bosses, and transitions to 
        the game over state if the hero dies.

        Parameters
        ----------
        change_state : function
            Function to change the game state.

        Returns
        -------
        None
        """
        for monster in self.enemies:
            if monster.is_dead:
                self.enemies.remove(monster)
                del monster

        for boss in self.bosses:
            if boss.is_dead:
                self.bosses.remove(boss)
                del boss

        if self.hero.Death:
            change_state("over", True)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all game elements to the screen, including the hero, 
        enemies, bosses, and background.

        Parameters
        ----------
        screen : pygame.Surface
            The screen surface where elements will be drawn.

        Returns
        -------
        None
        """
        screen.fill([0, 0, 0])

        # Parallax background
        if self.hero.speed_x > 0:
            speed = min(self.hero.speed_x, self.hero.speed_x_max)
        else:
            speed = max(self.hero.speed_x, self.hero.speed_x_min)
        if self.camera.fix_x >= 690:
            speed = 0

        self.pos_x -= speed // 3
        self.pos_x_p -= speed // 5
        x = 0
        for i in self.bg_images:
            for j in range(8):
                screen.blit(
                    i, (self.pos_x + x * self.pos_x_p + j * self.WIDTH, 0)
                )
            x += 1

        # Boss fight background
        screen.blit(
            self.bg_boss, (((132 * 50) - 700) + self.camera.fix_x, 0)
        )

        for ground in self.grounds:
            ground.draw(screen, self.camera)

        for monster in self.enemies:
            monster.draw(screen, self.camera)

        for boss in self.bosses:
            boss.draw(screen, self.camera)

        self.hero.draw(screen, self.camera)
        self.life_bar.draw(screen)
        self.hero_timer.draw(screen)

    def trade(self, event: pygame.event.Event) -> None:
        """
        Switches the current hero with the chosen one, exchanging
        equivalent attributes.

        Parameters
        ----------
        event : pygame.event.Event
            The event object capturing the key press.

        Returns
        -------
        None
        """
        if event.type == pygame.KEYDOWN and self.hero.trade_cooldown <= 0:
            change = False
            if event.key == pygame.K_z:
                self.actual_hero = 0
                change = True
            if event.key == pygame.K_x:
                self.actual_hero = 1
                change = True
            if event.key == pygame.K_c:
                self.actual_hero = 2
                change = True

            if change:
                state_dict = self.hero.__dict__

                self.hero = self.heros[self.actual_hero]

                for key in self.keys_trade:
                    self.hero.__dict__[key] = state_dict[key]

                self.hero.trade_cooldown = self.hero.trade_cooldown_time