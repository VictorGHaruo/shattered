import pygame
   
class Text:

    def __init__(self , text, Value, screen,width, height ,font):

        self.text = text
        self.Value = Value
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font

    def draw(self):

        message = f"{self.text} : {self.Value}"
        text_format = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text_format, ( self.width, self.height ))
                