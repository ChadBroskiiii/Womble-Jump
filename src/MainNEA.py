import pygame, math, socket
from pygame import Vector2
from Objects import Blocks  # Assuming you have the Blocks class in a separate module

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = 800
        self.screen_height = 600
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.movingl = True
        self.movingr = True
        self.radius = 10
        self.coords = Vector2(screen_width / 2, screen_height - 20)
        self.jump = False
        self.jumpCount = 0
        self.jumpMaximum = 10
        self.speed = 0
        self.doublejump = 0
        self.tempdouble = self.doublejump
        self.maxjumpscount = 2
        self.on_ground = True
        self.falling = False
        self.spacepressed = False
        self.circle_hbox = pygame.Rect(self.coords.x - self.radius, self.coords.y + self.radius, self.radius * 2 + 1,
                                       self.radius * 2 + 1)
        self.platforms = [
            Blocks(self.window, (200, 200, 200), (self.screen_width / 3, self.screen_height / 1.5), (100, 500), ()),
            Blocks(self.window, (200, 200, 0), (self.screen_width / 2, 250), (150, 50), ())
        ]            


    def update_position(self, keys, platforms):

        for platform in game.platforms:
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, self.platforms)
            
        if self.coords.x <= 0 + self.radius:
            #movingl = False
            self.speed = 0
            self.coords.x = 0 + self.radius
        elif self.coords.x >= game.screen_width - self.radius:
            #movingr = False
            self.speed = 0
            self.coords.x = game.screen_width - self.radius
        else:
            self.movingl = True
            self.movingr = True
        
            #Detects if colliding with the y value of the blocks and also 
        #allows the player to jump when on the blocks

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
        
        if collisionresult == False:

            if keys[pygame.K_LEFT]:
                #self.speed -= tempacc
                self.speed -= game.ACCELERATION
            else:
                if self.speed < 0:
                    self.speed += game.ACCELERATION

            if keys[pygame.K_RIGHT]:
                #self.speed += tempacc
                self.speed += game.ACCELERATION
            else:
                if self.speed > 0:
                    self.speed -= game.ACCELERATION
        
        else:
            
            if self.coords.x < platform.position.x + platform.size.x/2:
                print("right")
                self.coords.x += 1
            if self.coords.x > platform.position.x + platform.size.x/2:
                print("left")
                self.coords.x -= 1
            self.speed = 0
        #CHANGE IT SO THAT YOU REVERT AND CHECK FOR COLLISION IN THE MOVEMENT PART SO THAT YOU DONT HAVE TO CHECK LEFT AND RIGHT

        #Caps the speed at a certain max speed
        if self.speed <= -game.MAX_SPEED:
            self.speed = -game.MAX_SPEED
        elif self.speed >= game.MAX_SPEED:
            self.speed = game.MAX_SPEED
        self.coords.x += self.speed




            #print(collision_result)

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
        self.platforms = [
            Blocks(self.window, (200, 200, 200), (self.screen_width / 3, self.screen_height / 1.5), (100, 500), ()),
            Blocks(self.window, (200, 200, 0), (self.screen_width / 2, 250), (150, 50), ())
        ]

        self.player = Player(self.screen_width, self.screen_height)
        self.movingl = True
        self.movingr = True
        self.running = True


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.spacepressed = True
                    if self.player.doublejump < self.player.maxjumpscount:
                        self.player.jump = True
                        self.player.jumpCount = self.player.jumpMaximum
                        self.player.falling = True
                        self.player.doublejump += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.spacepressed == False
            if event.type == pygame.QUIT:
                self.running = False


    def run(self):
        while self.running:
            pygame.time.delay(0)

            keys = pygame.key.get_pressed()
            self.handle_events()
            self.player.update_position(keys, game.platforms)
            self.player.handle_jump()
            self.player.check_floor_collision(self.screen_height)

            self.window.fill(self.bg_colour)
            for platform in self.platforms:
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