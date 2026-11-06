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
coinSize = 50
speed = 10 
scoreGap = 6

logo = pygame.image.load("logo.png")
spacetoplay = pygame.image.load("spacetoplay.png")
digitImages = {}
for d in "0123456789":
    img = pygame.image.load(f"{d}.png").convert_alpha()
    digitImages[d] = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
img = pygame.image.load("dot.png").convert_alpha()
digitImages["."] = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))

# title = pygame.font.SysFont("caladea" , 300 , bold=True)
# undertitle = pygame.font.SysFont("caladea" , 50 , bold=True)
# points = pygame.font.SysFont("caladea" , 70 , bold=True)

clock = pygame.time.Clock()


class GameState:
    def __init__(self):
  
        self.pulse = []
        self.line = []

        self.pulseSpawnInterval = 0
        self.lineSpawnInterval = 0
        self.lastLine = 0
        self.lastPulse = 0


        self.coin = None
        self.coinGap = 0

        self.extraScore = 0


class Player:
    def __init__(self):
        self.x = 0.5 * width - 0.5 * spriteSize
        self.y = 0.5 * height - 0.5 * spriteSize
        self.v = speed
        self.lastDash = 0
        
        
class Pulse:
    def __init__(self):
        self.pos = (0 , 0)
        self.radius = 0
        self.deltaRadius = 0
        self.real = False
        self.spawntime = 0
        self.warningLength = 0

# class Line:
#     def __init__(self):
#         self.lineStart = ""
#         self.lineWarning = []
#         self.line = []
#         self.lineWarningStart = 0
#         self.linePos = []
#         self.linePosD = []
#         self.lineSide = []


def movement(keys, player):

    vx = (keys[pygame.K_d] - keys[pygame.K_a]) * player.v
    vy = (keys[pygame.K_s] - keys[pygame.K_w]) * player.v

    #adjustement for diagonal

    if vx != 0 and vy != 0:
        vx = vx * (math.sqrt(2) / 2)
        vy = vy * (math.sqrt(2) / 2)

    player.x += vx
    player.y += vy


def borderCheck(player):

    if player.x >= width - spriteSize:
        player.x = width - spriteSize
    elif player.x <= 0:
        player.x = 0

    if player.y >= height - spriteSize:
        player.y = height - spriteSize
    elif player.y <= 0:
        player.y = 0


def dash(keys, now, player):

    #dash cooldown

    if keys[pygame.K_SPACE] and now - player.lastDash >= 500:
        player.v = speed * 30
        player.lastDash = now


    #dash duration (1 frame)

    if now - player.lastDash >= 1:
        player.v = speed


def overlay(player):

    if player.v == speed:
        surf.set_alpha(100)
    else:
        surf.set_alpha(255)

    surf.fill((0, 0, 0))
    screen.blit(surf, (0, 0))


def distance(x1, y1, x2, y2):

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


running = True

while running:

    # resetting everything for restart

    screen.fill(black)
    state = GameState()
    player = Player()

    menu = True

    while menu:
        
        screen.fill(black)

        # menu text

        # text = title.render("DASHFRAME", True, white)
        # textRect = text.get_rect()
        # textRect.center = (width // 2, height * 0.4)
        # screen.blit(text, textRect)

        logoRect = logo.get_rect()
        logoRect.center = (width // 2, height * 0.35)
        screen.blit(logo, logoRect)

        # text = undertitle.render("PRESS SPACE TO PLAY", True, white)
        # textRect = text.get_rect()
        # textRect.center = (width // 2, height * 0.6)
        # screen.blit(text, textRect)

        spacetoplayRect = spacetoplay.get_rect()
        spacetoplayRect.center = (width // 2, height * 0.6)
        screen.blit(spacetoplay, spacetoplayRect)

        pygame.display.flip()

        keys = pygame.key.get_pressed()


        # wait til no keys are pressed
        
        while any(pygame.key.get_pressed()):
            pygame.event.pump()


        # quit options / game start

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()

            if keys[pygame.K_SPACE]:

                menu = False
        

    start = pygame.time.get_ticks()
    alive = True
    
    while alive:

        # refreshing variables

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks() - start


        # quit options

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
            
            if keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()
        


        ###  --- PLAYER ---  ###


        # path behind player
        
        overlay(player)


        # wasd movement and adjustement for diagonal

        movement(keys , player)


        # dash cooldown and duration

        dash(keys, now, player)


        # screen borders

        borderCheck(player)


        # draw player
      
        pygame.draw.rect(screen , green , [int(player.x) , int(player.y) , spriteSize , spriteSize])



        ### --- PULSE --- ###


        # update Interval

        state.pulseSpawnInterval = max(800, 5000 - now / 40)


        # add pulse

        if now - state.lastPulse >= state.pulseSpawnInterval and now >= state.pulseSpawnInterval:

            state.pulse.append(Pulse())
            state.pulse[-1].pos = (random.randint(0 , width) , random.randint(0 , height))
            state.pulse[-1].spawntime = now
            state.pulse[-1].warningLength = state.pulseSpawnInterval / 4
            state.pulse[-1].real = False
            state.lastPulse = now



        for i in range (len(state.pulse)):

            
            # add check for warning becoming pulse

            if state.pulse[i].real == False and now >= state.pulse[i].warningLength + state.pulse[i].spawntime:

                state.pulse[i].real = True
                state.pulse[i].deltaRadius = (min(10, 3 + now // 40000))
                state.lastPulse = now


            # draw pulse

            if (state.pulse[i].real == False):

                if now >= state.pulse[i].spawntime + state.pulseSpawnInterval * 0.35:
                    blinkInterval = 200
                else:
                    blinkInterval = 400

                if now % blinkInterval < blinkInterval // 2:
                    pygame.draw.circle(screen, red, (state.pulse[i].pos), 20 , 50)
                else:
                    pygame.draw.circle(screen, dred, (state.pulse[i].pos), 20 , 50)

            else:

                pygame.draw.circle(screen, white, (state.pulse[i].pos), state.pulse[i].radius, 10)
                state.pulse[i].radius += state.pulse[i].deltaRadius


        # remove unnecessary pulses

        if len (state.pulse) > 0:

            if state.pulse[0].radius > distance(0 , 0 , width , height):

                state.pulse.pop(0)



        ###  --- LINE --- ###

        #update Interval
        
        #state.lineSpawnInterval = 1000

        # warning before line

        # if now - state.lastLine >= state.lineInterval / 2 and now - start >= state.lineInterval / 2 and len (state.lineWarning) < 1:

        #     randomSide = random.choice(["top" , "right" , "bottom" , "left"])

        #     if randomSide == "top":
        #         state.lineWarning.append(((0 , 5) , (width , 5)))
        #         state.lineSide.append("top")

        #     if randomSide == "bottom":
        #         state.lineWarning.append(((0 , height - 5) , (width , height - 5)))
        #         state.lineSide.append("bottom")

        #     if randomSide == "right":
        #         state.lineWarning.append(((width - 5 , 0) , (width - 5 , height)))
        #         state.lineSide.append("right")

        #     if randomSide == "left":
        #         state.lineWarning.append(((5 , 0) , (5 , height)))
        #         state.lineSide.append("left")
    
        #     state.lineWarningStart = now

        # add line

        # if now - state.lastLine >= state.lineInterval and now >= state.lineInterval and len(state.lineWarning) > 0:

        #     state.line.append(state.lineWarning[0])
        #     state.linePos.append(0)
        #     state.linePosD.append(min(10, 3 + now // 40000))
        #     state.lineWarning.pop(0)
        #     state.lastLine = now



        # remove unnecessary characters

        # if len (state.line) > 0:

        #     if state.linePos[0] > distance(0 , 0 , width , height):

        #         state.line.pop(0)
        #         state.linePos.pop(0) 
        #         state.linePosD.pop(0)
        #         state.lineSide.pop(0)

        # draw line

        # for i in range (len(state.lineWarning)):

        #     if now >= state.lineWarningStart + state.lineInterval * 0.35:
        #         blinkInterval = 200
        #     else:
        #         blinkInterval = 400
            
        #     if now % blinkInterval < blinkInterval // 2:
        #         pygame.draw.line(screen , red , state.lineWarning[i][0] , state.lineWarning[i][1] , 10)
        #     else:
        #         pygame.draw.line(screen , dred , state.lineWarning[i][0] , state.lineWarning[i][1] , 10)


        # for i in range (len(state.line)):

        #     pygame.draw.line(screen, white, state.line[i][0], state.line[i][1], 10)
        #     state.linePos[i] += state.linePosD[i]



        ### --- COIN --- ###

        # add coin

        if now >= 60000 and state.coin == None and now - state.coinGap >= 5000:

            state.coin = (random.randint(0 , width - coinSize) , random.randint(0 , height - coinSize))

           
        if state.coin != None:

            pygame.draw.rect(screen , yellow , [state.coin[0] , state.coin[1] , coinSize , coinSize])


        ### --- SCORE --- ###


        # update score

        score = str(math.floor(now/ 100) / 10 + state.extraScore)


        # print score

        # text = points.render(score , True , white)
        # textRect = text.get_rect()
        # textRect.center = (width // 2, height // 4)
        # screen.blit(text, textRect)

        numberWidth = digitImages["0"].get_width() + scoreGap * len(score)
        scoreWidth = sum(digitImages[c].get_width() for c in score)
        scoreStart = width // 2 - scoreWidth // 2

        for c in score:
            screen.blit(digitImages[c], (scoreStart, height // 9))
            scoreStart += digitImages[c].get_width() + scoreGap



        ### --- HITREG --- ###


        # coin reg

        if state.coin != None:

            coinRect = pygame.Rect(state.coin[0], state.coin[1], coinSize, coinSize)
            playerRect = pygame.Rect(player.x, player.y, spriteSize, spriteSize)

            if playerRect.colliderect(coinRect) and player.v == speed:

                state.coin = None
                state.extraScore += 10
                state.coinGap = now
                

        # pulse reg

        for i in range (len(state.pulse)):

            if -10 <= distance(player.x + spriteSize/2 , player.y + spriteSize/2 , state.pulse[i].pos[0] , state.pulse[i].pos[1]) - state.pulse[i].radius <= 10 and player.v == speed:

                alive = False

        


        # updates

        pygame.display.flip()
        clock.tick(60)

pygame.quit()