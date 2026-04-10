import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width , height = screen.get_size()

black = (0 , 0 , 0)
white = (255 , 255 , 255)
green = (0 , 255 , 0)
red = (255 , 0 , 0)
dred = (100 , 0 , 0)
yellow = (255 , 255 , 0)
spriteSize = 20
coinSize = 60
vx = 0
vy = 0
speed = 10
v = 0
x = 0.5 * width - 0.5 * spriteSize
y = 0.5 * height - 0.5 * spriteSize
last = 0
pulseGap = 0
pulse= []
pulseR = []
dr = []
warning = []
coins = (0 , 0)
extraScore = 0
coinGap = 0




title = pygame.font.SysFont("caladea" , 300 , bold=True)
undertitle = pygame.font.SysFont("caladea" , 50 , bold=True)
points = pygame.font.SysFont("caladea" , 50 , bold=True)

clock = pygame.time.Clock()

def movement(keys , v , x , y):

    vx = (keys[pygame.K_d] - keys[pygame.K_a]) * v
    vy = (keys[pygame.K_s] - keys[pygame.K_w]) * v

    if vx != 0 and vy != 0:
        vx = vx*(math.sqrt(2)/2)
        vy = vy*(math.sqrt(2)/2)
    
    x += vx
    y += vy
    
    return x , y

def borderCheck(x , y):

    if x >= width - spriteSize:
        x = width - spriteSize
    elif x <= 0:
        x = 0
    
    if y >= height - spriteSize:
        y = height - spriteSize       
    elif y <= 0:
        y = 0
    
    return x , y

def dash(keys , now , last , speed , v):

    if keys[pygame.K_SPACE] and now - last >= 8.3 * 60:
        v = speed * 30
        last = pygame.time.get_ticks()

    if now - last >= 10:
        v = speed

    return v , last

def overlay(v , speed):

    overlay = pygame.Surface((width, height))

    if v == speed:
        overlay.set_alpha(100)
    else:
        overlay.set_alpha(255)

    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

def distance(x1 , y1 , x2 , y2):

    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)   

    return dist

running = True

while running:

    #resetting everything for restart

    screen.fill(black)
    x = 0.5 * width - 0.5 * spriteSize
    y = 0.5 * height - 0.5 * spriteSize
    v = speed
    last = 0
    pulseGap = 0
    pulse= []
    pulseR = []
    dr = []
    warning = []
    coins = (0 , 0)
    coinGap = 0
    extraScore = 0

    #wait til no keys are pressed
    
    while any(pygame.key.get_pressed()):
        pygame.event.pump()

    menu = True

    while menu:
        
        #menu text

        text = title.render("DASHFRAME", True, white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height * 0.4)
        screen.blit(text, textRect)

        text = undertitle.render("PRESS SPACE TO PLAY", True, white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height * 0.6)
        screen.blit(text, textRect)


        #quit options

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()

            if keys[pygame.K_SPACE]:

                menu = False
        
        pygame.display.flip()


    start = pygame.time.get_ticks()

    alive = True
    
    while alive:

        #refreshing variables

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        score = str(math.floor((now - start) / 60) / 10 + extraScore)


        #quit options

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()
        

        #path behind player
        
        overlay(v , speed)


        #wasd movement and adjustement for diagonal

        x , y = movement(keys , v , x , y)


        #dash cooldown and duration

        v , last = dash(keys , now , last , speed , v)


        #screen borders

        x , y = borderCheck(x , y)


        #warning before pulse

        if now - pulseGap >= 16.6 * 60 and now - start >= 16.6 * 60 and len(warning) < 1 :

            warning.append((random.randint(0 , width) , random.randint(0 , height)))


        #add pulse

        if now - pulseGap >= 33.3 * 60 and now - start >= 33.3 * 60:

            pulse.append(warning[0])
            pulseR.append(0)
            dr.append(5)
            warning.pop()
            pulseGap = now


        #remove unnecessary pulses

        if len (pulse) > 0:

            if pulseR[0] > 5000:

                pulse.pop(0)
                pulseR.pop(0) 
                dr.pop(0)


        #add coins

        if (now - start) >= 100 * 60 and coins == (0 , 0) and now - coinGap >= 50 * 60:

            coins = (random.randint(1 , width - coinSize) , random.randint(1 , height - coinSize))


        #draw characters

        if coins != (0 , 0):

            pygame.draw.rect(screen , yellow , [coins[0] , coins[1] , coinSize , coinSize])

        for i in range (0 , len(warning)):

            if now % 400 < 200:
                pygame.draw.circle(screen, red, (warning[i]), 18 , 50)
            else:
                pygame.draw.circle(screen, dred, (warning[i]), 18 , 50)

        for i in range (0 , len(pulse)):

            pygame.draw.circle(screen, white, (pulse[i]), pulseR[i], 8)
            pulseR[i] += dr[i]

        pygame.draw.rect(screen , green , [x , y , spriteSize , spriteSize])

        
        #print score

        text = points.render(score , True , white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 8)
        screen.blit(text, textRect)


        #coin reg


        if -40 <= distance(x + spriteSize/2 , y + spriteSize/2 , coins[0] + coinSize / 2 , coins[1] + coinSize / 2) <= 40 and v == speed:

            coins = (0 , 0)
            extraScore += 10
            coinGap = now
                


        #hitreg

        for i in range (0 , len(pulse)):

            if -8 <= distance(x + spriteSize/2 , y + spriteSize/2 , pulse[i][0] , pulse[i][1]) - pulseR[i] <= 8 and v == speed:

                alive = False


        #updates

        pygame.display.flip()
        clock.tick(60)

pygame.quit()