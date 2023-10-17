import pygame, math, socket
from pygame import Vector2
from Objects import Blocks
pygame.init()

FPS = 120
WIDTH = 800
HEIGHT = 600
ACCELERATION = 0.25
speed = 0
max_speed = 6
bg_colour = (0, 0, 0)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Him")
clock = pygame.time.Clock()
clientnumber = 000

radius = 10
coords = Vector2(WIDTH/2, HEIGHT - 20)
jump = False
jumpCount = 0
jumpMaximum = 10
doublejump = 0
maxjumpscount = 2
on_ground = True
falling = False

circle_hbox = pygame.rect.Rect((coords.x - radius), (coords.y + radius), radius*2 + 1, radius*2 + 1)

blocks = [
    Blocks(window, (200,200,200), (WIDTH/3, HEIGHT/1.5), (100, 100), ()),
    Blocks(window, (200,200,0), (WIDTH/2, 250), (150, 50), ())
]


movingl = True
movingr = True
running = True
while running:
    pygame.time.delay(0)
    shadow_oval = pygame.Rect(coords.x - radius + 2, coords.y - radius, radius*2 - 2, radius*2 + 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #Allows the window to close when pressing the red X
        if event.type == pygame.KEYDOWN: 

            #Jumps when the space key is pressed
            #And can only jump once in the air
            if event.key == pygame.K_SPACE:
                spacecount = True
                if doublejump < maxjumpscount:
                    jump = True
                    jumpCount = jumpMaximum
                    doublejump += 1
                    falling = True
    keys = pygame.key.get_pressed()    


    #Stops the player from leaving the screen in the x axis
    if coords.x <= 0 + radius:
        #movingl = False
        speed = 0
        coords.x = 0 + radius
    elif coords.x >= WIDTH - radius:
        #movingr = False
        speed = 0
        coords.x = WIDTH - radius
    else:
        movingl = True
        movingr = True
    
        #Detects if colliding with the y value of the blocks and also 
    #allows the player to jump when on the blocks

    for platform in blocks:

        collision_result = platform.collision(Vector2(coords.x, coords.y), radius)

        if collision_result == "Bongo_y":
            if jumpCount >= -6:
                jumpCount = -2
            else:
                jumpCount = jumpCount

        elif collision_result == "Bango_y":
            jumpCount = 0
            doublejump = 0
            if keys[pygame.K_SPACE]:
                jump = True
                jumpCount = jumpMaximum
                doublejump += 1

        elif collision_result == "Blangus":
            jump = False
            coords.y += 0.5*jumpCount
            doublejump = 0
            coords.y -= 1

        elif collision_result == False and on_ground == False:
            jump = True
            falling = True
            

        #Handles the x axis collisions and stopping movement in that direction
        if collision_result == "Bango_x":
            coords.x = platform.position.x + platform.size.x + radius
            if coords.x == platform.position.x + platform.size.x + radius:
                coords.x += 5
                collision_result == False
                movingl = False
        if collision_result == "Bongo_x":
            coords.x = platform.position.x - radius
            if coords.x == platform.position.x - radius:
                coords.x -= 5
                collision_result == False
                movingr = False

        if collision_result == "Spaghetti_right":
            coords.x = platform.collisionrect.left - radius
            if coords.x == platform.collisionrect.left - radius:
                coords.x -= 3
                collision_result = False
                movingr = False
        if collision_result == "Spaghetti_left":
            coords.x = platform.collisionrect.right + platform.collisionrect.width + radius
            if coords.x == platform.collisionrect.right + platform.collisionrect.width + radius:
                coords.x += 3
                collision_result = False
                movingl = False

    #The jump calculation for the acceleration and other stuff
    if jump:
        on_ground = False
        coords.y -= 0.5*jumpCount
        if jumpCount == -6:
            falling = True
        if falling:
            if jumpCount > -jumpMaximum:
                jumpCount -= 0.2
            else:
                jump = True
    
    #Makes sure the player doesn't fall through the bottom of the window
    #And resets the double jump count when the player touches the floor
    if coords.y >= (HEIGHT-2*radius):
        jump = False
        doublejump = 0
        on_ground = True
        falling = False
        
    #Controls the left and right movement with acceleration and deceleration
    if movingl == True:
        if keys[pygame.K_LEFT]:
            speed -= ACCELERATION
        else:
            if speed < 0:
                speed += ACCELERATION
    else:
        speed = 0

    if movingr == True:
        if keys[pygame.K_RIGHT]:
            speed += ACCELERATION
        else:
            if speed > 0:
                speed -= ACCELERATION
    else:
        speed = 0

    #Caps the speed at a certain max speed
    if speed <= -max_speed:
        speed = -max_speed
    elif speed >= max_speed:
        speed = max_speed
    coords.x += speed


    window.fill(bg_colour)
    for platform in blocks:
        platform.draw()
    #shadow = pygame.draw.ellipse(window, (0, 0, 0), shadow_oval)
    circle = pygame.draw.circle(window, (255, 0, 0), (coords.x, coords.y), radius)
    #pygame.Rect.clamp(circle, shadow)
    pygame.Rect.clamp(circle, circle_hbox)
    clock.tick(FPS)
    pygame.display.flip()
