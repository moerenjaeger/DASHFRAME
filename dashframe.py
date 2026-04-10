import pygame
import math
import random
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width , height = screen.get_size()
surf = pygame.Surface((width, height))


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dred = (100, 0, 0)
yellow = (255, 255, 0)
spriteSize = 20
coinSize = 60
speed = 10

title = pygame.font.SysFont("caladea" , 300 , bold=True)
undertitle = pygame.font.SysFont("caladea" , 50 , bold=True)
points = pygame.font.SysFont("caladea" , 50 , bold=True)

clock = pygame.time.Clock()

class GameState:
    def __init__(self):
        self.x = 0.5 * width - 0.5 * spriteSize
        self.y = 0.5 * height - 0.5 * spriteSize
        self.v = speed
        self.last = 0
        self.pulseGap = 0
        self.pulse = []
        self.pulseR = []
        self.dr = []
        self.warning = []
        self.coin = None
        self.coinGap = 0
        self.extraScore = 0


def movement(keys, state):

    vx = (keys[pygame.K_d] - keys[pygame.K_a]) * state.v
    vy = (keys[pygame.K_s] - keys[pygame.K_w]) * state.v

    #adjustement for diagonal

    if vx != 0 and vy != 0:
        vx = vx * (math.sqrt(2) / 2)
        vy = vy * (math.sqrt(2) / 2)

    state.x += vx
    state.y += vy

def borderCheck(state):

    if state.x >= width - spriteSize:
        state.x = width - spriteSize
    elif state.x <= 0:
        state.x = 0

    if state.y >= height - spriteSize:
        state.y = height - spriteSize
    elif state.y <= 0:
        state.y = 0

def dash(keys, now, state):

    #dash cooldown

    if keys[pygame.K_SPACE] and now - state.last >= 500:
        state.v = speed * 30
        state.last = pygame.time.get_ticks()


    #dash duration (1 frame)

    if now - state.last >= 1:
        state.v = speed

def overlay(state):

    if state.v == speed:
        surf.set_alpha(100)
    else:
        surf.set_alpha(255)

    surf.fill((0, 0, 0))
    screen.blit(surf, (0, 0))

def distance(x1, y1, x2, y2):

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


running = True

while running:

    #resetting everything for restart

    screen.fill(black)
    state = GameState()

    #wait til no keys are pressed
    
    while any(pygame.key.get_pressed()):
        pygame.event.pump()

    menu = True

    while menu:
        
        screen.fill(black)

        #menu text

        text = title.render("DASHFRAME", True, white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height * 0.4)
        screen.blit(text, textRect)

        text = undertitle.render("PRESS SPACE TO PLAY", True, white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height * 0.6)
        screen.blit(text, textRect)

        keys = pygame.key.get_pressed()


        #quit options

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()

            if keys[pygame.K_SPACE]:

                menu = False
        
        pygame.display.flip()

    start = pygame.time.get_ticks()
    alive = True
    
    while alive:

        #refreshing variables

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        score = str(math.floor((now - start) / 100) / 10 + state.extraScore)


        #quit options

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()
        

        #path behind player
        
        overlay(state)


        #wasd movement and adjustement for diagonal

        movement(keys , state)


        #dash cooldown and duration

        dash(keys, now, state)


        #screen borders

        borderCheck(state)


        #warning before pulse

        if now - state.pulseGap >= 1000 and now - start >= 1000 and len(state.warning) < 1 :

            state.warning.append((random.randint(0 , width) , random.randint(0 , height)))


        #add pulse

        if now - state.pulseGap >= 2000 and now - start >= 2000 and len(state.warning) > 0:

            state.pulse.append(state.warning[0])
            state.pulseR.append(0)
            state.dr.append(5)
            state.warning.pop(0)
            state.pulseGap = now


        #remove unnecessary pulses

        if len (state.pulse) > 0:

            if state.pulseR[0] > 5000:

                state.pulse.pop(0)
                state.pulseR.pop(0) 
                state.dr.pop(0)


        #add coin

        if (now - start) >= 10000 and state.coin == None and now - state.coinGap >= 5000:

            state.coin = (random.randint(0 , width - coinSize) , random.randint(0 , height - coinSize))


        #draw characters

        if state.coin != None:

            pygame.draw.rect(screen , yellow , [state.coin[0] , state.coin[1] , coinSize , coinSize])

        for i in range (len(state.warning)):

            if now % 400 < 200:
                pygame.draw.circle(screen, red, (state.warning[i]), 18 , 50)
            else:
                pygame.draw.circle(screen, dred, (state.warning[i]), 18 , 50)

        for i in range (len(state.pulse)):

            pygame.draw.circle(screen, white, (state.pulse[i]), state.pulseR[i], 8)
            state.pulseR[i] += state.dr[i]

        pygame.draw.rect(screen , green , [int(state.x) , int(state.y) , spriteSize , spriteSize])

        
        #print score

        text = points.render(score , True , white)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 8)
        screen.blit(text, textRect)


        #coin reg

        if state.coin != None:

            coinRect = pygame.Rect(state.coin[0], state.coin[1], coinSize, coinSize)
            playerRect = pygame.Rect(state.x, state.y, spriteSize, spriteSize)

            if playerRect.colliderect(coinRect) and state.v == speed:

                state.coin = None
                state.extraScore += 10
                state.coinGap = now
                


        #hitreg

        for i in range (len(state.pulse)):

            if -8 <= distance(state.x + spriteSize/2 , state.y + spriteSize/2 , state.pulse[i][0] , state.pulse[i][1]) - state.pulseR[i] <= 8 and state.v == speed:

                alive = False


        #updates

        pygame.display.flip()
        clock.tick(60)

pygame.quit()