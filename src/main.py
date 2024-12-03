import pygame
import os
import sys
from interfaces import Menu, Game_Over, Pause
from game import GameManager
import random

pygame.init()

class Main:
    """
    Main class for managing the game's primary loop and state transitions.

    Attributes
    ----------
    WIDTH : int
        The width of the game window.
    HEIGHT : int
        The height of the game window.
    screen : Surface
        The Pygame surface representing the game screen.
    is_running : bool
        Indicates whether the game is running.
    states : dict
        A dictionary holding all game states (menu, game, pause, game over).
    current_state : object
        The current active state of the game.
    is_changed : bool
        Indicates if the game state has changed.
    volume : float
        The volume level of background music.

    Methods
    -------
    run()
        Executes the main game loop.
    change_state(state, music_bool)
        Changes the current game state.
    """

    def __init__(self):
        """
        Initializes the main game setup, including screen dimensions, states, and music.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.WIDTH = 1400
        self.HEIGHT = 800
        screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.is_running = True
        self.states = {
            "menu": Menu(self),
            "game": GameManager(self),
            "pause": Pause(self),
            "over": Game_Over(self),
        }
        self.current_state = self.states["menu"]
        self.is_changed = False
        self.volume = 0.15
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        music_dir_path = os.path.join(os.path.dirname(path_game), "assets", "Music")
        music_num = random.randint(1, 2)
        music_path = os.path.join(music_dir_path, "Menu", f"M{music_num}.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    def run(self):
        """
        Executes the main game loop, handling events, updates, and rendering.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        clock = pygame.time.Clock()

        while self.is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.current_state == self.states["game"]:
                        self.change_state("pause", False)
                        break
                self.current_state.on_event(event, self)

            if self.current_state == self.states["game"]:
                self.current_state.on_key_pressed()
                self.current_state.update()
                self.current_state.collision_decetion()
                self.current_state.elimination(self.change_state)
            self.current_state.music(self, self.volume)
            self.current_state.draw(self.screen)
            pygame.display.flip()
            clock.tick(30)

    def change_state(self, state, music_bool: bool):
        """
        Changes the current game state.

        Parameters
        ----------
        state : str
            The new state to switch to ("menu", "game", "pause", or "over").
        music_bool : bool
            Indicates whether the music should change with the state.

        Returns
        -------
        None
        """
        self.current_state = self.states[state]
        self.is_changed = music_bool


if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()
