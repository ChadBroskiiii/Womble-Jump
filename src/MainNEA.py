import pygame, math, socket
from pygame import Vector2
from Objects import Blocks  # Assuming you have the Blocks class in a separate module

class Player:
    def __init__(self, screen_width, screen_height):
        self.radius = 10
        self.coords = Vector2(screen_width / 2, screen_height - 20)
        self.jump = False
        self.jumpCount = 0
        self.jumpMaximum = 10
        self.speed = 0
        self.doublejump = 0
        self.maxjumpscount = 2
        self.on_ground = True
        self.falling = False
        self.circle_hbox = pygame.Rect(self.coords.x - self.radius, self.coords.y + self.radius, self.radius * 2 + 1,
                                       self.radius * 2 + 1)

    def handle_input(self, keys):
        if keys[pygame.K_SPACE]:
            if self.doublejump < self.maxjumpscount:
                self.jump = True
                self.jumpCount = self.jumpMaximum
                self.doublejump += 1
                self.falling = True

    def update_position(self, movingl, movingr, keys, platforms):
        if self.coords.x <= 0 + self.radius:
            #movingl = False
            self.speed = 0
            self.coords.x = 0 + self.radius
        elif self.coords.x >= game.screen_width - self.radius:
            #movingr = False
            self.speed = 0
            self.coords.x = game.screen_width - self.radius
        else:
            movingl = True
            movingr = True
        
            #Detects if colliding with the y value of the blocks and also 
        #allows the player to jump when on the blocks

        for platform in platforms:

            collision_result = platform.collision(Vector2(self.coords.x, self.coords.y), self.radius)

            if collision_result == "Bongo_y":
                if self.jumpCount >= -6:
                    self.jumpCount = -2
                else:
                    self.jumpCount = self.jumpCount

            elif collision_result == "Bango_y" and self.jumpCount < 0:
                self.jumpCount = 0
                self.doublejump = 0
                if keys[pygame.K_SPACE]:
                    self.jump = True
                    self.jumpCount = self.jumpMaximum
                    self.doublejump += 1
                

            #Handles the x axis collisions and stopping movement in that direction
            if collision_result == "Bango_x":
                self.coords.x = platform.position.x + platform.size.x + self.radius
                if self.coords.x == platform.position.x + platform.size.x + self.radius:
                    self.coords.x += 5
                    collision_result == False
                    movingl = False
            if collision_result == "Bongo_x":
                self.coords.x = platform.position.x - self.radius
                if self.coords.x == platform.position.x - self.radius:
                    self.coords.x -= 5
                    collision_result == False
                    movingr = False

            if collision_result == "Blango_x":
                self.coords.x = platform.position.x + platform.size.x + self.radius - 10
                if self.coords.x == platform.position.x + platform.size.x + self.radius -10:
                    self.coords.x += 5
                    collision_result == False
                    movingl = False
            if collision_result == "Blongo_x":
                self.coords.x = platform.position.x - self.radius +10
                if self.coords.x == platform.position.x - self.radius +10:
                    self.coords.x -= 5
                    collision_result == False
                    movingr = False


        #The jump calculation for the acceleration and other stuff
        if self.jump:
            self.on_ground = False
            self.coords.y -= 0.4*self.jumpCount
            if self.jumpCount == -6:
                self.falling = True
            if self.falling:
                if self.jumpCount > -self.jumpMaximum:
                    self.jumpCount -= 0.2
                else:
                    self.jump = True
        
        #Makes sure the player doesn't fall through the bottom of the window
        #And resets the double jump count when the player touches the floor
        if self.coords.y >= (game.screen_height-2*self.radius):
            self.jump = False
            self.doublejump = 0
            self.on_ground = True
            self.falling = False
            
        #Controls the left and right movement with acceleration and deceleration
        if movingl == True:
            if keys[pygame.K_LEFT]:
                self.speed -= game.ACCELERATION
            else:
                if self.speed < 0:
                    self.speed += game.ACCELERATION
        else:
            self.speed = 0

        if movingr == True:
            if keys[pygame.K_RIGHT]:
                self.speed += game.ACCELERATION
            else:
                if self.speed > 0:
                    self.speed -= game.ACCELERATION
        else:
            self.speed = 0

        #Caps the speed at a certain max speed
        if self.speed <= -game.MAX_SPEED:
            self.speed = -game.MAX_SPEED
        elif self.speed >= game.MAX_SPEED:
            self.speed = game.MAX_SPEED
        self.coords.x += self.speed

    def handle_jump(self):
        if self.jump:
            self.on_ground = False
            self.coords.y -= 0.4 * self.jumpCount
            if self.jumpCount == -6:
                self.falling = True
            if self.falling and self.jumpCount > -self.jumpMaximum:
                self.jumpCount -= 0.1
            else:
                self.jump = True

    def check_floor_collision(self, screen_height):
        if self.coords.y >= (screen_height - 2 * self.radius):
            self.jump = False
            self.doublejump = 0
            self.on_ground = True
            self.falling = False

class Game:
    def __init__(self):
        pygame.init()
        self.FPS = 120
        self.screen_width = 800
        self.screen_height = 600
        self.ACCELERATION = 0.25
        self.MAX_SPEED = 5
        self.speed = 0
        self.bg_colour = (0, 0, 0)
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Him")
        self.clock = pygame.time.Clock()
        self.platform = [
            Blocks(self.window, (200, 200, 200), (self.screen_width / 3, self.screen_height / 1.5), (100, 100), ()),
            Blocks(self.window, (200, 200, 0), (self.screen_width / 2, 250), (150, 50), ())
        ]

        self.player = Player(self.screen_width, self.screen_height)
        self.movingl = True
        self.movingr = True
        self.running = True

    def run(self):
        while self.running:
            pygame.time.delay(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update_position(self.movingl, self.movingr, keys, game.platform)
            self.player.handle_jump()
            self.player.check_floor_collision(self.screen_height)

            self.window.fill(self.bg_colour)
            for platform in game.platform:
                platform.draw()

            circle = pygame.draw.circle(self.window, (255, 0, 0), (int(self.player.coords.x), int(self.player.coords.y)),
                                        self.player.radius)
            pygame.Rect.clamp(circle, self.player.circle_hbox)

            self.clock.tick(self.FPS)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
