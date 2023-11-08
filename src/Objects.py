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
        pygame.draw.polygon(self.surface, (125,125,125), trapezium_coords)


    def collision(self, coordsx, coordsy, radius, platforms):
        hitbox = pygame.rect.Rect(coordsx - radius, coordsy - radius, radius*2, radius*2)
        topresult = pygame.Rect.colliderect(hitbox, self.collisionrect)
        center = Vector2(coordsx + radius, coordsy + radius)

        closest_y = (self.position.y - min(center.y, self.position.y + self.size.y))
        
        #print(f"result: {result}, closest_x: {closest_x}, self.position.x: {self.position.x}, self.size.x: {self.size.x}")
        for platform in platforms:
            result = pygame.Rect.colliderect(hitbox, platform)
            return result