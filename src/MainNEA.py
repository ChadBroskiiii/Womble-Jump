import pygame, math, socket, json, random
from pygame import Vector2
from Objects import Blocks  # Assuming you have the Blocks class in a separate module

class Player:
    def __init__(self, screen_width, screen_height, platforms):
        #Initialisation variables
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
        self.maxjumpscount = 100000
        self.on_ground = True
        self.falling = False
        self.circle_hbox = pygame.Rect(self.coords.x - self.radius, self.coords.y + self.radius, self.radius * 2 + 1,
                                       self.radius * 2 + 1)
        self.platforms = platforms

    def update_position(self, keys, platforms):
        #Iterates through each platform and checks for collisions individually
        for platform in platforms:
            midpoint = platform.get_position_x() + platform.get_size_x()/2
            bottom = platform.get_main_position_y() + platform.get_size_y() - 5
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, platform)
            
            #Controls the left and right movement with acceleration and deceleration
            if collisionresult == False:
                if keys[pygame.K_LEFT]:
                    self.speed -= game.ACCELERATION
                else:
                    if self.speed < 0:
                        self.speed += game.ACCELERATION

                if keys[pygame.K_RIGHT]:
                    self.speed += game.ACCELERATION
                else:
                    if self.speed > 0:
                        self.speed -= game.ACCELERATION
                
            #Reverts movement after a collision
            elif collisionresult == "other_coll":               
                if midpoint > self.coords.x:
                    self.speed = 0
                    self.coords.x -= 0.75
                elif midpoint < self.coords.x:
                    self.speed = 0
                    self.coords.x += 0.75
                if self.jumpCount > 0:
                    if bottom < self.coords.y:
                        self.jumpCount = -1.5
                
        #Caps the speed at a certain max speed
        if self.speed <= -game.MAX_SPEED:
            self.speed = -game.MAX_SPEED
        elif self.speed >= game.MAX_SPEED:
            self.speed = game.MAX_SPEED
        self.coords.x += self.speed

        if self.coords.x <= 0 + self.radius:
            self.speed = 0
            self.coords.x = 0 + self.radius
        elif self.coords.x >= game.screen_width - self.radius:
            self.speed = 0
            self.coords.x = game.screen_width - self.radius
        else:
            self.movingl = True
            self.movingr = True
        
        #Jump calculations with acceleration
        if self.jump:
            self.on_ground = False
            self.coords.y -= 0.8*self.jumpCount
            if self.jumpCount == -6:
                self.falling = True
            if self.falling:
                if self.jumpCount > -self.jumpMaximum:
                    self.jumpCount -= 0.3
                else:
                    self.jump = True

        #Checks for top collisions and stops the player
        for platform in platforms:
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, platform)

            if collisionresult == "top_coll":
                if self.jumpCount < 0:
                    self.doublejump = 0
                    self.jump = False
                    self.coords.y = platform.get_position_y()# - self.radius
                    self.jumpCount = 0
                else:
                    self.jump = True
            else:
                self.jump = True

        #Makes sure the player doesn't fall through the bottom of the window
        #And resets the double jump count when the player touches the floor
        if self.coords.y >= (game.screen_height-2*self.radius):
            self.jump = False
            self.doublejump = 0
            self.on_ground = True
            self.falling = False

    def check_floor_collision(self, screen_height):
        if self.coords.y >= (screen_height - 2 * self.radius):
            self.jump = False
            self.doublejump = 0
            self.on_ground = True
            self.falling = False

class Game:
    def __init__(self):
        #Pygame and variable initialisation
        pygame.init()
        self.FPS = 120
        self.screen_width = 800
        self.screen_height = 600
        self.ACCELERATION = 0.25
        self.MAX_SPEED = 5
        self.speed = 0
        self.bg_colour = (0, 0, 0)
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Womble jump")
        self.clock = pygame.time.Clock()
        #List with all the playforms in the game at that moment
        self.platforms = [
            Blocks(self.window, (255, 209, 220), (self.screen_width / 3, self.screen_height / 1.5), (100, 100), ()),
            Blocks(self.window, (174, 198, 207), (self.screen_width / 2, 250), (150, 50), ()),
            Blocks(self.window, (207, 198, 100), (self.screen_width / 2.5, 100), (150, 50), ())
        ]

        self.player = Player(self.screen_width, self.screen_height, self.platforms)
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
            self.player.update_position(keys, self.platforms)
            self.player.check_floor_collision(self.screen_height)
            # Calculate camera offset based on player position
            camera_offset = Vector2(0, self.screen_height / 2 - self.player.coords.y)
            self.window.fill(self.bg_colour)
            # for platform in self.platforms:
            #     if platform.position.y + camera_offset.y > self.screen_height:
            #         platform.position.y += (camera_offset.y - self.screen_height)
            #     platform.draw(offset=camera_offset)
            
            for platform in self.platforms:
                platform.draw(offset=camera_offset)

            # for platform in self.platforms:
            #     if lowestplat == platform.position.y:
            #         ydistance = self.player.coords.y - camera_offset.y - lowestplat
            #         print(ydistance)
            #         if ydistance <= (self.screen_height/2):
            #             platform.position.y -= self.screen_height
            #             platform.draw(offset=camera_offset)
            #         else:
            #             platform.draw(offset=camera_offset)
            #     else:
            #         platform.draw(offset=camera_offset)
            circle = pygame.draw.circle(self.window,
                (255, 0, 0),
                (int(self.player.coords.x + camera_offset.x), int(self.player.coords.y + camera_offset.y)),
                self.player.radius
            )

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            coordinates_ip = {"x": self.player.coords.x, "y": self.player.coords.y, "ip": ip_address}
            serverAddressPort = ("192.168.4.23", 7680)
            buffersize = 2048
            packetsToSend = str.encode(json.dumps(coordinates_ip))
            UDPclientsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            UDPclientsocket.sendto(packetsToSend, serverAddressPort)
            message, _ = UDPclientsocket.recvfrom(buffersize)
            message = message.decode()
            other_player_positions = json.loads(message)
            if len(other_player_positions) != 0:
                for i in other_player_positions.items():
                    x = int(other_player_positions.get("x"))
                    y = int(other_player_positions.get("y"))
                    pygame.draw.circle(self.window, (100,100,100), (x,y), 10)

            pygame.Rect.clamp(circle, self.player.circle_hbox)

            self.clock.tick(self.FPS)
            pygame.display.flip()

gameinstance = Game()
playerinstance = Player(800, 600, gameinstance.platforms)
playerinstance.platforms = gameinstance.platforms

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()