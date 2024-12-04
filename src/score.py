import pygame, os, sys
   
class Score:

    def __init__(self, text, Value, x, y, width, height, size_font, back_color = (0, 0, 0), transparece = 0, font_stile= None ):

        self.text = text
        self.Value = Value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size_font = size_font
        self.back_color = back_color
        self.transparece = transparece
        self.font_stile = font_stile

    def draw(self, screen: pygame.Surface):

        message = f"{self.text}: {self.Value}"
        font = self.adj_font(message, self.size_font)
        text_format = font.render(message, True, (255, 255, 255))
        rect_max = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        rect_text = text_format.get_rect(center=(rect_max.center))
        rect_surface = pygame.Surface(rect_text.size, pygame.SRCALPHA)
        rect_surface.fill(self.back_color)
        rect_surface.set_alpha(self.transparece)
        screen.blit(rect_surface, rect_text)
        screen.blit(text_format, rect_text)

    def update(self, value=None):
        
        if value is not None:
            self.Value = value  
            
    def adj_font(self, text, size_init):
        size = size_init
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))   
        interfaces_path = os.path.join(path_game, os.pardir, "assets", "Interfaces")
        if self.font_stile is not None:
            font_path = os.path.join(interfaces_path, f"{self.font_stile}.otf")
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