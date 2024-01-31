import pygame
from pygame import Vector2

class Button:
    def __init__(self, image, pos, text, font, colour, alt_colour):
        self.image = image
        self.pos = Vector2(pos)
        self.text = text
        self.font = font
        self.colour, self.alt_colour = colour, alt_colour
        self.text_render = self.font.render(self.text, True, self.colour)
        if self.image == None:
            self.image = self.text
        self.rect = self.image.get_rect(center= self.pos)
        self.text_rect = self.text_render.get_rect(center= self.pos)

    def update(self, window):
        if self.image == None:
            window.blit(self.image, self.rect)
        window.blit(self.text_render, self.text_rect)

    def input_check(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def colour_change(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text_render = self.font.render(self.text, True, self.alt_colour)
        else:
            self.text_render = self.font.render(self.text, True, self.colour)
