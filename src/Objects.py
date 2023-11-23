import pygame
from pygame import Vector2


class Blocks:
    def __init__(self, surface, color, position, size, rect):
        self.surface = surface
        self.color = color
        self.position = Vector2(position)
        self.size = Vector2(size)
        self.rect = pygame.Rect(self.position, self.size)
        self.collisionrect = pygame.rect.Rect(self.position.x + 5, self.position.y - 17, self.size.x - 10, 26)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

        widthdiff = 10
        height = 50
        bottomleft = Vector2((self.position.x), (self.position.y))
        topleft = Vector2((self.position.x + widthdiff), (self.position.y - height))
        bottomright = Vector2((self.position.x + self.size.x), (self.position.y))
        topright = Vector2((self.position.x + self.size.x - widthdiff), (self.position.y - height))
        trapezium_coords = [topleft, bottomleft, bottomright, topright]
        pygame.draw.polygon(self.surface, (125, 125, 125), trapezium_coords)

    def collision(self, coordsx, coordsy, radius, platform):
        hitbox = pygame.rect.Rect(coordsx - radius, coordsy - radius, radius * 2, radius * 2)
        center = Vector2(coordsx + radius, coordsy + radius)
        closest_y = self.position.y - min(center.y, self.position.y + self.size.y)

        topresult = pygame.Rect.colliderect(hitbox, self.collisionrect)
        result = pygame.Rect.colliderect(hitbox, platform)

        if result == True:
            return "side_coll"

        if topresult == True:
            return "top_coll"

        return False

    def get_position_y(self):
        return self.position.y - 17
    
    def get_position_x(self):
        return self.position.x
    
    def get_size_y(self):
        return self.size.y
    
    def get_size_x(self):
        return self.size.x
