import pygame, math, socket, json, random, os
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
        self.maxjumpscount = 30000
        self.falling = False
        self.circle_hbox = pygame.Rect(self.coords.x - self.radius, self.coords.y + self.radius, self.radius * 2 + 1,
                                       self.radius * 2 + 1)
        self.platforms = platforms
        self.directory = os.getcwd()
        self.image = pygame.image.load(self.directory +"/res/avatars/Womble_Blue.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def update_position(self, keys, platforms):
        #Iterates through each platform and checks for collisions individually
        for platform in platforms:
            midpoint = platform.get_position_x() + platform.get_size_x()/2
            bottom = platform.get_main_position_y() + platform.get_size_y() - 5
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, platform)
            
            #Controls the left and right movement with acceleration and deceleration
            if collisionresult == False:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.speed -= game.ACCELERATION
                else:
                    if self.speed < 0:
                        self.speed += game.ACCELERATION

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
            self.falling = False

    def check_floor_collision(self, screen_height):
        if self.coords.y >= (screen_height - 2 * self.radius):
            self.jump = False
            self.doublejump = 0
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
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Womble jump")
        self.clock = pygame.time.Clock()
        self.colour_list = []
        self.directory = os.getcwd()
        self.bg = pygame.image.load(self.directory +"/res/backgrounds/blue_sky_pixel_art.jpg")
        self.finish = pygame.image.load(self.directory + "/res/assets/checkered_line.jpg")
        self.finish = pygame.transform.scale(self.finish, (self.screen_width, 250))
        for i in range(16):
            self.rand_color = random.choices(range(256), k=3)
            self.colour_list.append(self.rand_color)
        
        #List with all the playforms in the game at that moment
        self.platforms = [
            Blocks(self.window, random.choice(self.colour_list), (self.screen_width / 3, self.screen_height / 1.5), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (self.screen_width / 2, 250), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (self.screen_width / 2.5, 100), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (self.screen_width / 1.5, 50), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (self.screen_width / 5, 600), (150, 50), ())
        ]

        self.player = Player(self.screen_width, self.screen_height, self.platforms)
        self.movingl = True
        self.movingr = True
        self.running = True


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.spacepressed = True
                    if self.player.doublejump < self.player.maxjumpscount:
                        self.player.jump = True
                        self.player.jumpCount = self.player.jumpMaximum
                        self.player.falling = True
                        self.player.doublejump += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.spacepressed == False
            if event.type == pygame.QUIT:
                self.running = False


    def text(self, text, x, y, size):
        colour = (0,200,0)
        font_type = self.directory + '/res/fonts/PublicPixel.ttf'

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, colour)
        self.window.blit(text, (x,y))


    def run(self):
        while self.running:
            win_height = -800
            pygame.time.delay(0)

            keys = pygame.key.get_pressed()
            self.handle_events()
            self.player.update_position(keys, self.platforms)
            self.player.check_floor_collision(self.screen_height)
            # Calculate camera offset based on player positions
            camera_offset = Vector2(0, self.screen_height / 2 - self.player.coords.y)
            self.window.blit(self.bg, (0,-1200 - 0.2*self.player.coords.y))
            self.window.blit(self.finish, (0, win_height + camera_offset.y - 250))
            
            for platform in self.platforms:
                # if platform.position.y + camera_offset.y > self.screen_height:
                #     self.platforms.remove(platform)
                platform.draw(offset=camera_offset, coords=playerinstance.coords)
                
            window = playerinstance.window
            window.blit(playerinstance.image, (self.player.coords.x - 25, self.player.coords.y + camera_offset.y - 35))
            ip_list = []

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
            ip = other_player_positions.keys()
            ip_list = list(ip)
            if len(ip_list) != 0:
                for i in range(len(ip_list)):
                    ip_list_val = ip_list[i]
                    coordinates_dict = other_player_positions.get(ip_list_val)
                    x = coordinates_dict.get("x")
                    y = coordinates_dict.get("y") + camera_offset.y
                    pygame.draw.circle(self.window, (100,100,100), (x,y), 10)
            
            if len(ip_list) > 0:
                ip_list_val_1 = ip_list[0]
                player_2_coords = other_player_positions.get(ip_list_val_1)
                player_2_y = player_2_coords.get("y") + camera_offset.y

                if player_2_y <= win_height:
                    self.text("PLAYER 2 WINS", 78.5, self.screen_height/3, 50)
                elif self.player.coords.y <= win_height:
                    self.text("PLAYER 1 WINS", 78.5, self.screen_height/3, 50)
            else:
                if self.player.coords.y <= win_height:
                    self.text("PLAYER 1 WINS", 78.5, self.screen_height/3, 50)
            

            self.clock.tick(self.FPS)
            pygame.display.flip()

gameinstance = Game()
playerinstance = Player(800, 600, gameinstance.platforms)
playerinstance.platforms = gameinstance.platforms

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()