import pygame, random, os
from typing import List
from game import GameManager

def f_reset_game(main: object):
    """
    Auxiliar function that resets the game state by recreating
    the GameManager.

    Parameters
    ----------
    main : object
        The main game instance managing the game states.

    Returns
    -------
    None
    """
    del main.states["game"]
    main.states["game"] = GameManager(main)
    main.change_state("game", True)

class Button:
    """
    Represents an interactive button that responds to mouse events.

    Attributes
    ----------
    images_path : list[str]
        Paths to the button images (default and hover states).
    image_init : pygame.Surface
        Button image in the default state.
    image_hover : pygame.Surface
        Button image in the hover state.
    rect : pygame.Rect
        Rectangular area of the button for collision detection.

    Methods
    -------
    draw(screen):
        Draws the button on the screen, changing its appearance based 
        on mouse hover.

    change_state(event, main, state, music_bool):
        Changes the game state when the button is clicked.

    reset_game(event, main):
        Resets the game when the button is clicked.

    exit(event, main):
        Exits the game when the button is clicked.
    """
    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        images_path: List[str]
    ) -> None:
        """
        Initializes a button with its position, size, and image paths
        for its normal and hover states.

        Parameters
        ----------
        x : int
            The x-coordinate of the button on the screen.
        y : int
            The y-coordinate of the button on the screen.
        width : int
            The width of the button.
        height : int
            The height of the button.
        images_path : list of str
            A list containing the file paths for the normal and 
            hover button images.
        
        Returns
        -------
        None
        """
        self.images_path = images_path
        image_init = pygame.image.load(self.images_path[0]).convert_alpha()
        self.image_init = pygame.transform.scale(image_init, (width, height))
        image_hover = pygame.image.load(self.images_path[1]).convert_alpha()
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.rect = self.image_init.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the button on the screen, changing its appearance if the 
        mouse hovers over it.

        Parameters
        ----------
        screen : pygame.Surface
            The screen where the button will be drawn.

        Returns
        -------
        None
        """
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
            screen.blit(self.image_hover, self.rect)
        else:
            screen.blit(self.image_init, self.rect)

    def change_state(
        self, event: pygame.event.Event, 
        main: object, state: str, music_bool: bool
    ) -> None:
        """
        Changes the current game state when the button is clicked.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.
        state : str
            The new state to switch to.
        music_bool : bool
            Whether music should play in the new state.

        Returns
        -------
        None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                main.change_state(state, music_bool)

    def reset_game(self, event:pygame.event.Event, main: object) -> None:
        """
        Resets the game when the button is clicked.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                f_reset_game(main)

    def exit(self, event:pygame.event.Event, main: object) -> None:
        """
        Exits the game when the button is clicked.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_collision = self.rect.collidepoint(event.pos)
            if event.button == 1 and has_collision:
                main.is_running = False

class Menu:
    """
    Represents the menu screen with buttons for starting the game, 
    viewing the tutorial, and quitting.

    Attributes
    ----------
    b_start : Button
        Button for starting the game.
    b_tutorial : Button
        Button for showing the tutorial.
    b_exit : Button
        Button for quitting the game.
    image_menu : pygame.Surface
        Background image of the menu screen.

    Methods
    -------
    music(main, volume):
        Plays a random music track when the menu is displayed.

    draw(screen):
        Draws the menu screen and the buttons.

    on_event(event, main):
        Handles user input (clicking buttons and pressing keys).
    """
    def __init__(self, main: object) -> None:
        """
        Initializes the main menu with buttons for starting
        the game, showing the tutorial, and quitting.

        Parameters
        ----------
        main : object
            The main game instance, used to access global
            settings and assets.
        """
        start_images = [
            os.path.join(main.assets_path, "Interfaces", "start0.png"), 
            os.path.join(main.assets_path, "Interfaces", "start1.png")
        ]
        tutorial_images = [
            os.path.join(main.assets_path, "Interfaces", "tutorial0.png"),
            os.path.join(main.assets_path, "Interfaces", "tutorial1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        
        self.b_start = Button(555, 300, 290, 120, start_images)
        self.b_tutorial = Button(555, 425, 290, 120, tutorial_images)
        self.b_exit = Button(555, 550, 290, 120, quit_images)
        
        # Image
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Menu.png")
        image_menu = pygame.image.load(image_path).convert_alpha()
        self.image_menu = pygame.transform.scale(image_menu, dimention_screen)

    def music(self, main: object, volume: float) -> None:
        """
        Plays a random background music track for the menu.

        Parameters
        ----------
        main : object
            The main game instance.
        volume : float
            The volume at which the music should play.

        Returns
        -------
        None
        """
        if main.is_changed:
            music_dir_path = os.path.join(main.assets_path, "Music")
            
            music_num = random.randint(1, 4)
            music_path = os.path.join(
                music_dir_path, "Menu", f"M{music_num}.mp3"
            )
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the menu screen and its interactive buttons.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the menu is drawn.

        Returns
        -------
        None
        """
        screen.blit(self.image_menu, (0, 0))
        self.b_start.draw(screen)
        self.b_tutorial.draw(screen)
        self.b_exit.draw(screen)

    def on_event(self, event:pygame.event.Event, main: object) -> None:
        """
        Handles user input for the menu, including clicking buttons 
        and pressing keys.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        self.b_start.change_state(event, main, "game", True)
        
        self.b_tutorial.change_state(event, main, "tutorial", False)
        
        self.b_exit.exit(event, main)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main.change_state("game", True)

class Pause:
    """
    Represents the pause screen where players can resume,
    restart or quit.

    Attributes
    ----------
    b_continue : Button
        Button for continuing the game.
    b_restart : Button
        Button for restarting the game.
    b_quit : Button
        Button for quitting the game.
    image_pause : pygame.Surface
        Background image of the pause screen.

    Methods
    -------
    music(main, volume):
        Placeholder method for playing music in the pause menu.

    draw(screen):
        Draws the pause screen and the buttons.

    on_event(event, main):
        Handles user input for resuming, restarting, or quitting
        the game.
    """
    def __init__(self, main: object) -> None:
        """
        Initializes the pause menu with buttons for continuing
        the game, restarting, or quitting.

        Parameters
        ----------
        main : object
            The main game instance, used to access global
            settings and assets.
        """
        continue_images = [
            os.path.join(main.assets_path, "Interfaces", "continue0.png"),
            os.path.join(main.assets_path, "Interfaces", "continue1.png")
        ]
        restart_images = [
            os.path.join(main.assets_path, "Interfaces", "restart0.png"),
            os.path.join(main.assets_path, "Interfaces", "restart1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        self.b_continue = Button(555, 300, 290, 120, continue_images)
        self.b_restart = Button(555, 425, 290, 120, restart_images)
        self.b_quit = Button(555, 550, 290, 120, quit_images)
        
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Pause.png")
        image_pause = pygame.image.load(image_path).convert_alpha()
        self.image_pause = pygame.transform.scale(image_pause, dimention_screen)

    def music(self, main: object, volume: float) -> None:
        """
        Placeholder method for playing music in the pause menu.

        Parameters
        ----------
        main : object
            The main game instance.
        volume : float
            The volume at which the music should play.

        Returns
        -------
        None
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the pause screen and its interactive buttons.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the pause screen is drawn.

        Returns
        -------
        None
        """
        screen.blit(self.image_pause, (0, 0))
        self.b_continue.draw(screen)
        self.b_restart.draw(screen)
        self.b_quit.draw(screen)

    def on_event(self, event: pygame.event.Event, main: object) -> None:
        """
        Handles user input for resuming, restarting, or quitting
        the game.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        self.b_continue.change_state(event, main, "game", False)
        
        self.b_restart.reset_game(event, main)
        
        self.b_quit.reset_game(event, main)
        self.b_quit.change_state(event, main, "menu", True)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main.change_state("game", False)
            if event.key == pygame.K_r:
                f_reset_game(main)
            if event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)

class Game_Over:
    """
    Represents the game over screen with options to restart or quit.

    Attributes
    ----------
    main : Object
        Themain game instance. 
    b_restart : Button
        Button for restarting the game.
    b_quit : Button
        Button for quitting the game.
    image_over : pygame.Surface
        Background image of the game over screen.

    Methods
    -------
    music(main, volume):
        Plays a random game over music track.

    draw(screen):
        Draws the game over screen and its buttons.

    on_event(event, main):
        Handles user input for restarting or quitting the game.
    """
    def __init__(self, main: object) -> None:
        """
        Initializes the game over screen with buttons for restarting
        or quitting the game.

        Parameters
        ----------
        main : object
            The main game instance, used to access global
            settings and assets.
        """
        self.main = main
        
        restart_images = [
            os.path.join(main.assets_path, "Interfaces", "restart0.png"),
            os.path.join(main.assets_path, "Interfaces", "restart1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        self.b_restart = Button(555, 310, 290, 120, restart_images)
        self.b_quit = Button(555, 480, 290, 120, quit_images)
        
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Over.png")
        image_over = pygame.image.load(image_path).convert_alpha()
        self.image_over = pygame.transform.scale(image_over, dimention_screen)

    def music(self, main: object, volume: float) -> None:
        """
        Plays a random game over music track.

        Parameters
        ----------
        main : object
            The main game instance.
        volume : float
            The volume at which the music should play.

        Returns
        -------
        None
        """
        if main.is_changed:
            music_dir_path = os.path.join(main.assets_path, "Music")
            music_num = random.randint(1, 4)
            music_path = os.path.join(
                music_dir_path, "Over", f"D{music_num}.mp3"
            )
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the game over screen and its buttons.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the game over screen is drawn.

        Returns
        -------
        None
        """
        screen.blit(self.image_over, (0, 0))
        
        points = self.main.states["game"].hero.points
        font = ajustar_fonte(f"Points: {points}/140", "assets/Interfaces/Lumios Typewriter New.otf", 340, 55, 50) 
        text = font.render(f"Points: {points}/140", True, (255,255,255))
        rect_max = pygame.rect.Rect(530, 30, 340, 55)
        rect_surface = pygame.Surface(rect_max.size, pygame.SRCALPHA)
        rect_surface.set_alpha(100)
        rect_surface.fill((0,0,0))
        rect_text = text.get_rect(center = (rect_max.center))
        screen.blit(rect_surface, rect_max)
        screen.blit(text, rect_text)
        
        self.b_restart.draw(screen)
        self.b_quit.draw(screen)

    def on_event(self, event: pygame.event.Event, main: object) -> None:
        """
        Handles user input for restarting or quitting the game.

        Parameters
        ----------
        event : pygame.event.Event
            The event triggered by the user.
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        self.b_restart.reset_game(event, main)
        
        self.b_quit.reset_game(event, main)
        self.b_quit.change_state(event, main, "menu", True)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                f_reset_game(main)
            elif event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)

class Tutorial:
    """
    Displays the tutorial screen with images explaining the controls and characters.

    Attributes
    ----------
    main : object
        The main game instance.
    duration: int
        Transition time.
    timer : int
        A timer used to control the image transitions during the tutorial.
    idx_image : int
        The index of the current tutorial image.
    images : list of pygame.Surface
        A list containing the images that make up the tutorial.
    
    Methods
    -------
    music(main, volume):
        Placeholder method for playing music in the tutorial.

    draw(screen):
        Draws the game over screen and its buttons.

    on_event(event, main):
        Handles user input for restarting or quitting the game.
    """
    
    def __init__(self, main: object) -> None:
        """
        Initializes the tutorial with a timer, index for image display, and loading tutorial images.
        
        Parameters
        ----------
        main : object
            The main game instance, used to access global settings and assets.
        
        Returns
        -------
        None
        """
        self.main = main
        self.duration = 100
        self.timer = self.duration
        self.idx_image = 0
        
        dimention_screen = main.screen.get_size()
        images_path = [
            os.path.join(main.assets_path, "Interfaces", "Controls.png"),
            os.path.join(main.assets_path, "Interfaces", "August.png"),
            os.path.join(main.assets_path, "Interfaces", "Stella.png"),
            os.path.join(main.assets_path, "Interfaces", "Erik.png"),
        ]
        self.images = []
        for i in range(4):
            image = pygame.image.load(images_path[i]).convert_alpha()
            self.images.append(pygame.transform.scale(image, dimention_screen))

    def music(self, main: object, volume: float) -> None:
        """
        Placeholder method for playing music in the tutorial. 
        Currently does nothing.

        Parameters
        ----------
        main : object
            The main game instance.
        volume : float
            The volume level for the music.

        Returns
        -------
        None
        """
        pass
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the current tutorial image on the screen and updates
        the image display based on the timer.

        Parameters
        ----------
        screen : pygame.Surface
            The screen surface where the tutorial images will be drawn.

        Returns
        -------
        None
        """
        self.timer += 1
        if self.timer >= self.duration and self.idx_image < 4:
            self.timer = 0
            screen.blit(self.images[self.idx_image], (0,0))
            self.idx_image += 1
        if self.timer >= self.duration and self.idx_image >= 4:
            self.main.change_state("menu", False)
            self.timer = self.duration
            self.idx_image = 0
    
    def on_event(self, event: pygame.event.Event, main: object) -> None:
        """
        Handles keyboard input events to navigate through
        the tutorial images.

        Parameters
        ----------
        event : pygame.event
            The event to process (keyboard input).
        main : object
            The main game instance.

        Returns
        -------
        None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.idx_image > 1:
                    self.timer = self.duration
                    self.idx_image -= 2
            
            if event.key == pygame.K_RIGHT:
                if self.idx_image < 5:
                    self.timer = self.duration
                
            if event.key == pygame.K_q:
                main.change_state("menu", False)
                self.timer = self.duration
                self.idx_image = 0

class Win:
    """
    Handles the win screen, where the player can either restart
    the game or quit to the main menu.

    Parameters
    ----------
    main : object
        The main game instance, used to access global settings
        and assets.

    Attributes
    ----------
    b_again : Button
        A button to restart the game.
    b_quit : Button
        A button to quit to the main menu.
    image_win : pygame.Surface
        The background image displayed on the win screen.
    """

    def __init__(self, main: object) -> None:
        """
        Initializes the win screen, loading the necessary images
        and creating buttons.

        Parameters
        ----------
        main : object
            The main game instance, used to access global settings
            and assets.

        Returns
        -------
        None
        """
        again_images = [
            os.path.join(main.assets_path, "Interfaces", "again0.png"),
            os.path.join(main.assets_path, "Interfaces", "again1.png")
        ]
        quit_images = [
            os.path.join(main.assets_path, "Interfaces", "quit0.png"),
            os.path.join(main.assets_path, "Interfaces", "quit1.png")
        ]
        
        self.b_again = Button(555, 350, 290, 120, again_images)
        self.b_quit = Button(555, 480, 290, 120, quit_images)
        
        dimention_screen = main.screen.get_size()
        image_path = os.path.join(main.assets_path, "Interfaces", "Win.png")
        image_win = pygame.image.load(image_path).convert_alpha()
        self.image_win = pygame.transform.scale(image_win, dimention_screen)
    
    def music(self, main: object, volume: float) -> None:
        """
        Plays random background music for the win screen.

        Parameters
        ----------
        main : object
            The main game instance, used to access global
            settings and assets.
        volume : float
            The volume level for the background music.

        Returns
        -------
        None
        """
        if main.is_changed:
            music_dir_path = os.path.join(main.assets_path, "Music")
            music_num = random.randint(1, 5)
            music_path = os.path.join(
                music_dir_path, "Win", f"V{music_num}.mp3"
            )
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  
        main.is_changed = False
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the win screen background and buttons on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen surface where the win screen is drawn.

        Returns
        -------
        None
        """
        screen.blit(self.image_win, (0, 0))
        self.b_again.draw(screen)
        self.b_quit.draw(screen)
    
    def on_event(self, event: pygame.event.Event, main: object) -> None:
        """
        Handles events for the win screen, including button interactions
        and keyboard input.

        Parameters
        ----------
        event : pygame.event
            The event to process (mouse click or key press).
        main : object
            The main game instance, used to access global settings.

        Returns
        -------
        None
        """
        self.b_again.reset_game(event, main)
        
        self.b_quit.reset_game(event, main)
        self.b_quit.change_state(event, main, "menu", True)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                f_reset_game(main)
            elif event.key == pygame.K_q:
                f_reset_game(main)
                main.change_state("menu", True)
    
def ajustar_fonte(texto, fonte_path, largura_max, altura_max, tamanho_inicial=50):
    tamanho = tamanho_inicial
    while True:
        fonte = pygame.font.Font(fonte_path, tamanho)
        largura, altura = fonte.size(texto)
        if largura <= largura_max and altura <= altura_max:
            return fonte
        tamanho -= 1
        if tamanho < 1:  # Impede tamanho de fonte inválido
            raise ValueError("Texto muito grande para caber no retângulo!")    