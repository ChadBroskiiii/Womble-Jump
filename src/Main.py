import pygame, socket, json, random, os, sys, time
from waiting import wait, TimeoutExpired
from pygame import Vector2
from Objects import Blocks
from Button import Button

class Player:
    def __init__(self, screen_width, screen_height, main_map):
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
        self.jumpMaximum = 9
        self.main_map = main_map
        self.speed = 0
        self.sprinting = False
        self.sprint_level = 50
        self.doublejump = 0
        self.tempdouble = self.doublejump
        self.maxjumpscount = 2
        self.falling = False
        self.circle_hbox = pygame.Rect(self.coords.x - self.radius, self.coords.y + self.radius, self.radius * 2 + 1,
                                       self.radius * 2 + 1)
        #self.main_map = gameinstance.main_map
        self.directory = os.getcwd()
        self.image = pygame.image.load(self.directory +"/res/avatars/Womble_Blue.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def update_position(self, keys, max_speed):
        #Iterates through each platform and checks for collisions individually
        for platform in self.main_map:
            midpoint = platform.get_position_x() + platform.get_size_x()/2
            bottom = platform.get_main_position_y() + platform.get_size_y() - 5
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, platform)
            
            #Controls the left and right movement with acceleration and deceleration
            if collisionresult == False:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.speed -= gameinstance.ACCELERATION
                else:
                    if self.speed < 0:
                        self.speed += gameinstance.ACCELERATION
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.speed += gameinstance.ACCELERATION
                else:
                    if self.speed > 0:
                        self.speed -= gameinstance.ACCELERATION
                
            #Reverts movement after a collision
            elif collisionresult == "other_coll":     
                if bottom < self.coords.y:
                    if self.jumpCount >= 0:
                        self.jumpCount = -1.5
                else:          
                    if midpoint > self.coords.x:
                        self.coords.x = platform.get_position_x() - 10
                    elif midpoint < self.coords.x:
                        self.coords.x = platform.get_position_x() + platform.get_size_x() + 10
                
                
        #Caps the speed at a certain max speed
        if self.speed <= -max_speed:
            self.speed = -max_speed
        elif self.speed >= max_speed:
            self.speed = max_speed
        self.coords.x += self.speed

        if self.coords.x <= 0 + self.radius:
            self.speed = 0
            self.coords.x = 0 + self.radius
        elif self.coords.x >= gameinstance.screen_width - self.radius:
            self.speed = 0
            self.coords.x = gameinstance.screen_width - self.radius
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
        for platform in self.main_map:
            collisionresult = platform.collision(self.coords.x, self.coords.y, self.radius, platform)

            if collisionresult == "top_coll":
                if self.jumpCount <= 0:
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
        if self.coords.y >= (gameinstance.screen_height-2*self.radius):
            self.jump = False
            self.doublejump = 0
            self.falling = False

    def check_floor_collision(self, screen_height):
        if self.coords.y >= (screen_height - 2 * self.radius):
            self.jump = False
            self.doublejump = 0
            self.falling = False

class Main_Menu:
    def __init__(self):
        pygame.init()
        self.FPS = 120
        self.screen_width = 800
        self.screen_height = 600
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Womble jump")
        self.clock = pygame.time.Clock()
        self.directory = os.getcwd()
        self.bg = pygame.image.load(self.directory +"/res/backgrounds/the_wombles.png")
        self.bg = pygame.transform.scale_by(self.bg, 1.3)
        self.main_map = 0

    def get_font(self, size): 
        return pygame.font.Font(self.directory +"/res/fonts/PublicPixel.ttf", size)

    def level_select(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.window.blit(self.bg, (-4, -50))
            map_selection = self.get_font(45).render("Map Selection", True, "Red")
            map_rect = map_selection.get_rect(center=(400,50))
            map1_image = pygame.image.load(self.directory+"/res/assets/1.png")
            map1_image = pygame.transform.scale_by(map1_image, 0.5)
            map2_image = pygame.image.load(self.directory+"/res/assets/2.jpg")
            map2_image = pygame.transform.scale_by(map2_image, 0.46)
            map1_button = Button(image=map1_image, 
                                 pos=(200,400),
                                 text="MAP 1",
                                 font=pygame.font.Font(self.directory+"/res/fonts/PublicPixel.ttf"),
                                 colour="Red",
                                 alt_colour="Grey")
            map2_button = Button(image=map2_image, 
                                 pos=(600,400),
                                 text="MAP 2",
                                 font=pygame.font.Font(self.directory+"/res/fonts/PublicPixel.ttf"),
                                 colour="Red",
                                 alt_colour="Grey")
            
            for button in [map1_button]:
                button.colour_change(mouse_pos)
                button.update(self.window)

            for button in [map2_button]:
                button.colour_change(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if map1_button.input_check(mouse_pos):
                        self.main_map = 1
                        game = Game(self.main_map)
                        game.run()
                    if map2_button.input_check(mouse_pos):
                        self.main_map = 2
                        game = Game(self.main_map)
                        game.run()


            self.window.blit(map_selection, map_rect)
            pygame.display.flip()
waiter = 0
def waitinger(waiter):
    if waiter == 1:
        return True
    return False


class Game(Blocks):
    def __init__(self, main_map):
        #Pygame and variable initialisation
        pygame.init()
        self.FPS = 120
        self.screen_width = 800
        self.screen_height = 600
        self.ACCELERATION = 0.25
        self.MAX_SPEED = 3
        self.speed = 0
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Womble jump")
        self.clock = pygame.time.Clock()
        self.main_map = main_map
        self.colour_list = []
        self.directory = os.getcwd()
        self.waiter = 0
        self.bg1 = pygame.image.load(self.directory +"/res/backgrounds/blue_sky_pixel_art.jpg")
        self.bg2 = pygame.image.load(self.directory +"/res/backgrounds/desert.png")
        self.bg2 = pygame.transform.scale_by(self.bg2, 1.5)
        self.finish = pygame.image.load(self.directory + "/res/assets/checkered_line.jpg")
        self.finish = pygame.transform.scale(self.finish, (self.screen_width, 250))
        for i in range(16):
            self.rand_color = random.choices(range(256), k=3)
            self.colour_list.append(self.rand_color)
        #List with all the playforms in the game at that moment
        self.map_1_platforms = [
            Blocks(self.window, (86, 125, 70), (-20, self.screen_height + 32), (900, 500), ()),
            Blocks(self.window, random.choice(self.colour_list), (250, 500), (150, 50), ()), 
            Blocks(self.window, random.choice(self.colour_list), (100, 350), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (600, 200), (150, 50), ()), 
            Blocks(self.window, random.choice(self.colour_list), (400, 50), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (600, -100), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (450, -250), (150, 50), ()),  
            Blocks(self.window, random.choice(self.colour_list), (200, -450), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (500, -450), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (300, -650), (150, 50), ())     
        ]

        self.map_2_platforms = [
            Blocks(self.window, (200, 173, 127), (-20, self.screen_height + 32), (900, 500), ()),
            Blocks(self.window, random.choice(self.colour_list), (250, 400), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (100, 200), (150, 50), ()), 
            Blocks(self.window, random.choice(self.colour_list), (300, 50), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (100, -100), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (650, -250), (150, 50), ()),  
            Blocks(self.window, random.choice(self.colour_list), (600, -450), (150, 50), ()),
            Blocks(self.window, random.choice(self.colour_list), (100, -650), (150, 50), ()) 
        ]

        if self.main_map == 1:
            self.main_map = self.map_1_platforms
        elif self.main_map == 2:
            self.main_map = self.map_2_platforms
        self.player = Player(self.screen_width, self.screen_height, self.main_map)
        self.movingl = True
        self.movingr = True
        self.running = True


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.player.sprinting = True
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
                if event.key == pygame.K_LSHIFT:
                    self.player.sprinting = False
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()


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
            
            
            self.player.check_floor_collision(self.screen_height)
            # Calculate camera offset based on player positions
            camera_offset = Vector2(0, self.screen_height / 2 - self.player.coords.y)

            if self.main_map == self.map_1_platforms:
                self.window.blit(self.bg1, (0,-1300 - 0.2*self.player.coords.y))
            elif self.main_map == self.map_2_platforms:
                self.window.blit(self.bg2, (0,-500 - 0.2*self.player.coords.y))

            self.window.blit(self.finish, (0, win_height + camera_offset.y - 250))
            
            if self.player.sprinting:
                if self.player.sprint_level > 0:
                    self.player.sprint_level -= 0.5
                else:
                    self.player.sprinting = False
            elif self.player.sprint_level < 50:
                self.player.sprint_level += 0.25

            if self.player.sprinting:
                self.MAX_SPEED = 5
            else:
                self.MAX_SPEED = 3

            self.player.update_position(keys, self.MAX_SPEED)



            for platform in self.main_map:
                platform.draw(offset=camera_offset, coords=playerinstance.coords)
                
            sprint_rect_topleft = (50, self.screen_height -50)
            sprint_rect_topright = (50 + self.player.sprint_level, self.screen_height -50)
            sprint_rect_bottomleft = (50, self.screen_height -40)
            sprint_rect_bottomright = (50 + self.player.sprint_level, self.screen_height -40)
            sprint_coords = [sprint_rect_topleft, sprint_rect_bottomleft, sprint_rect_bottomright, sprint_rect_topright]
            pygame.draw.rect(self.window, "Black", (45, self.screen_height -55, 61, 21))
            pygame.draw.polygon(self.window, "Green", sprint_coords)

            window = playerinstance.window
            window.blit(playerinstance.image, (self.player.coords.x - 25, self.player.coords.y + camera_offset.y - 5))
            ip_list = []
            other_player_positions = 0
            other_player_1 = pygame.image.load(self.directory + "/res/avatars/Womble_Red.png")
            other_player_1 = pygame.transform.scale(other_player_1, (50, 50))

            # hostname = socket.gethostname()
            # ip_address = socket.gethostbyname(hostname)
            # coordinates_ip = {"x": self.player.coords.x, "y": self.player.coords.y, "ip": ip_address}
            # serverAddressPort = ("192.168.4.23", 7680)
            # buffersize = 2048
            # packetsToSend = str.encode(json.dumps(coordinates_ip))
            # UDPclientsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            # UDPclientsocket.sendto(packetsToSend, serverAddressPort)
            # message, _ = UDPclientsocket.recvfrom(buffersize)
            # message = message.decode()
            # other_player_positions = json.loads(message)
            # ip = other_player_positions.keys()
            # ip_list = list(ip)
            # if len(ip_list) != 0:
            #     for i in range(len(ip_list)):
            #         ip_list_val = ip_list[i]
            #         coordinates_dict = other_player_positions.get(ip_list_val)
            #         x = coordinates_dict.get("x")
            #         y = coordinates_dict.get("y") + camera_offset.y
            #         self.window.blit(other_player_1, (x - 25, y - 5))
            self.waiter = 1
            if len(ip_list) > 0:
                ip_list_val_1 = ip_list[0]
                player_2_coords = other_player_positions.get(ip_list_val_1)
                player_2_y = player_2_coords.get("y") + camera_offset.y
                if player_2_y <= win_height:
                    try:
                        self.text("PLAYER 2 WINS", 78.5, self.screen_height/3, 50)
                        self.text("RELOADING MAP", 78.5, self.screen_height/4, 50)
                        pygame.display.update()
                        wait(lambda : waitinger(waiter), timeout_seconds = 3)
                        
                    except TimeoutExpired:
                        Main_Menu()
                        break

                elif self.player.coords.y <= win_height:
                    try:
                        self.text("YOU WIN", 78.5, self.screen_height/3, 91)
                        self.text("RELOADING MAP", 78.5, self.screen_height/4, 50)
                        pygame.display.update()
                        wait(lambda : waitinger(waiter), timeout_seconds = 3)
                        
                    except TimeoutExpired:
                        Main_Menu()
                        break

            else:
                if self.player.coords.y <= win_height:
                    try:
                        self.text("YOU WIN", 78.5, self.screen_height/3, 91)
                        self.text("RELOADING MAP", 78.5, self.screen_height/4, 50)
                        pygame.display.update()
                        wait(lambda : waitinger(waiter), timeout_seconds = 3)
                        
                    except TimeoutExpired:
                        Main_Menu()
                        break

            

            self.clock.tick(self.FPS)
            pygame.display.flip()

main_menu = Main_Menu()
main_map = main_menu.main_map
gameinstance = Game(main_map)
playerinstance = Player(800, 600, gameinstance.main_map)
playerinstance.main_map = gameinstance.main_map

gaming = True

if gaming:
    menu = Main_Menu()
    menu.level_select()
    pygame.quit()
else:
    if __name__ == "__main__":
        gameinstance.run()
        pygame.quit()
