import pygame, os, sys

class Score:
    """
    Represents a score display element that shows text and a 
    numerical value on the screen.

    Attributes
    ----------
    text : str
        The label text displayed with the score.
    Value : int
        The numerical value of the score.
    x : int
        The x-coordinate for the score display.
    y : int
        The y-coordinate for the score display.
    width : int
        The max width of the score display area.
    height : int
        The max height of the score display area.
    size_font : int
        The initial font size for the score text.
    back_color : tuple
        Background color of the score display as an RGB tuple.
        Defaults to (0, 0, 0).
    transparece : int
        Transparency level of the background color (0 to 255).
        Defaults to 0.
    font_stile : str
        The style or name of the font file.
        Defaults to None.

    Methods
    -------
    draw(screen) -> None
        Renders the score display onto the given Pygame surface.
    update(value) -> None
        Updates the numerical value of the score.
    adj_font(text, size_init) -> Font
        Adjusts the font size dynamically to fit within the specified
        width and height.
    """
    
    def __init__(
        self,
        text: str, value: int,
        x: int, y: int,
        width: int, height: int,
        size_font: int, back_color: tuple = (0, 0, 0),
        transparece: int = 0, font_stile: str = None
    ) -> None:
        """
        Initializes a new Score instance.

        Parameters
        ----------
        text : str
            The label text displayed with the score.
        value : int
            The initial numerical value of the score.
        x : int
            The x-coordinate for the score display.
        y : int
            The y-coordinate for the score display.
        width : int
            The max width of the score display area.
        height : int
            The max height of the score display area.
        size_font : int
            The initial font size for the score text.
        back_color : tuple
            Background color of the score display 
            (default is (0, 0, 0)).
        transparece : int
            Transparency level of the background color (default is 0).
        font_stile : str
            The style or name of the font file (default is None).

        Returns
        -------
        None
        """
        self.text = text
        self.Value = value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size_font = size_font
        self.back_color = back_color
        self.transparece = transparece
        self.font_stile = font_stile

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the score display onto the given Pygame surface.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame surface where the score will be rendered.

        Returns
        -------
        None
        """
        message = f"{self.text}: {self.Value}"
        
        font = self.adj_font(message, self.size_font)
        text_format = font.render(message, True, (255, 255, 255))
        
        rect_max = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        rect_text = text_format.get_rect(center=rect_max.center)
        
        rect_surface = pygame.Surface(rect_text.size, pygame.SRCALPHA)
        rect_surface.fill(self.back_color)
        rect_surface.set_alpha(self.transparece)
        
        screen.blit(rect_surface, rect_text)
        screen.blit(text_format, rect_text)

    def update(self, value: int) -> None:
        """
        Updates the numerical value of the score.

        Parameters
        ----------
        value : int
            The new value for the score.

        Returns
        -------
        None
        """
        self.Value = value

    def adj_font(self, text: str, size_init: int) -> pygame.font.Font:
        """
        Adjusts the font size dynamically to ensure the text fits
        within the specified dimensions.

        Parameters
        ----------
        text : str
            The text to be displayed.
        size_init : int
            The initial font size to start the adjustment.

        Returns
        -------
        pygame.font.Font
            A Pygame font object with the adjusted size.

        Raises
        ------
        ValueError
            If the text cannot fit within the specified dimensions
            even with the smallest font size.
        """
        size = size_init
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        interfaces_path = os.path.join(
            path_game, os.pardir, "assets", "Interfaces"
        )
        if self.font_stile is not None:
            font_path = os.path.join(interfaces_path, f"{self.font_stile}")
        else:
            font_path = None

        while True:
            font = pygame.font.Font(font_path, size)
            width, height = font.size(text)
            if width <= self.width and height <= self.height:
                return font
            size -= 1
            if size < 1:
                raise ValueError("Text doesn't fit!")