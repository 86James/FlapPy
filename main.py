import pygame
import math
from sys import exit # Closes code once called
from random import randint
from time import sleep
#from flappy import Flappy
global current_state


class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        flap_1 = pygame.image.load('sprites\yellowbird-downflap.png').convert_alpha()
        flap_1 = pygame.transform.scale_by(flap_1,2)
        flap_2 = pygame.image.load('sprites\yellowbird-midflap.png').convert_alpha()
        flap_2 = pygame.transform.scale_by(flap_2,2)
        flap_3 = pygame.image.load('sprites\yellowbird-upflap.png').convert_alpha()
        flap_3 = pygame.transform.scale_by(flap_3,2)
        flap_4 = pygame.image.load('sprites\yellowbird-midflap.png').convert_alpha()
        flap_4 = pygame.transform.scale_by(flap_4,2)
        self.flap_anim = [flap_1, flap_2, flap_3, flap_4]
        self.flap_index = 0
        self.x = 150
        self.y = 200
        self.image = self.flap_anim[self.flap_index]
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.gravity = 0
        self.angle = 0
        self.multiplier = 0
        self.flap_sound = pygame.mixer.Sound('audio/wing.wav')
        self.flap_sound.set_volume(0.1)
        self.jumpinput = True
        self.ground_hit = False

    def player_input(self):
        global firstflap
        global jumpinput # There is definitely an easier way to do this
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if jumpinput == True:
                self.angle = 50
                self.gravity = -15
                self.multiplier = 0
                self.flap_sound.play()
                jumpinput = False
                firstflap = True
        if keys[pygame.K_SPACE] == False:
            jumpinput = True
            
    def apply_gravity(self):
        global current_state
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom>= 785:
            self.rect.bottom = 785
            self.ground_hit = True

    def animation_state(self):
        self.flap_index += 0.3
        if self.flap_index >= len(self.flap_anim):
            self.flap_index = 0
        #self.image = self.flap_anim[int(self.flap_index)] 
    def rotate_bird(self):
        self.multiplier += 0.1 # have to do this because self angle wont take away from self angle if self angle is negative, therefore NO NOSEDIVE
        self.angle -= 2
        self.angle -= self.multiplier
        self.image = pygame.transform.rotate(self.flap_anim[int(self.flap_index)], self.angle) # This code handles both animation AND rotation, 
        if self.angle <= -90: # This code is kinda messy but it'll do :D
            self.angle = -90
            self.multiplier = 0

    def update(self):
        if current_state == 'game':
            if firstflap == False:
                self.x = 150
                self.y = 400
                self.player_input()
                self.animation_state()
                self.image = self.flap_anim[int(self.flap_index)]
                self.rect = self.image.get_rect(midbottom = (self.x, self.y))
            else:
                self.x = 150
                self.y = 400
                self.player_input()
                self.animation_state()
                self.apply_gravity()
                self.rotate_bird()
        elif current_state == 'game_over':
            self.apply_gravity()
            self.rotate_bird()
        elif current_state == 'menu':
            self.x = 500
            self.y = 200
            self.animation_state()
            self.image = self.flap_anim[int(self.flap_index)]
            self.rect = self.image.get_rect(midbottom = (self.x, self.y))

        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        global pipey
        #creating pipe, default is bottom pipe
        self.image = pygame.image.load('sprites\pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image,2)
        if type == 'top':
            self.rect = self.image.get_rect(center = (700,pipey))
        #Rotation for top pipe
        else:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center = (700,pipey - 875))

    def update(self):
        self.rect.x -= 4
        if self.rect.x >= 124 and self.rect.x < 125:
            bing.play()
            scorecount()
            
            int(round(score))
            print(score)
            
        self.destroy
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill   

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/base.png').convert()
        self.image = pygame.transform.scale_by(self.image, 2.1)
        self.rect = self.image.get_rect(center = (325,900)) # when creating rectangles, use imagefile.get_rect
    def ground_movement(self):
        self.rect.x -= 4
        if self.rect.x <= -45:
            self.rect.x = 0

    def update(self):
        self.ground_movement()

class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text=''):    # Define Button creation system
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = True

    def draw(self, screen, outline=None):   
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0) # Draws a rectangle for the button
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.Font('fonts/flappy-bird.ttf', 50) # Applies a font for all buttons
            text = font.render(self.text, 1, (255, 255, 255)) # Renders the text that is entered 
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2))) # Blits text size and position

    def isOver(self, pos):  # Define clicking a button function
        if not self.enabled:  # If button is disabled, return False
            return False
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

def collision_sprite():
    if pygame.sprite.spritecollide(flappy.sprite,obstacle_group,False): #or pygame.sprite.collide_rect(flappy.sprite,ground_rect):
        print("bimmer") 
        if current_state == "game":
            die.play()
            collide.play()
            return 'game_over'
    if pygame.sprite.spritecollide(flappy.sprite,ground,False):
        if current_state == "game":
            collide.play()
            return 'game_over'
    else:
        return 'game'

def scorecount():
    global score
    score = score + 0.5
    return score

score = 0 
pygame.init() # Initialises the pygame functions
screen = pygame.display.set_mode((640,960)) # Window Size
pygame.display.set_caption('FlapPy Bird') # Window Name
clock = pygame.time.Clock() # Variable for setting FPS
background = pygame.image.load('sprites/background-day.png').convert()
background = pygame.transform.scale(background,(640,960))
getready = pygame.image.load('sprites/message.png').convert_alpha()
getready = pygame.transform.scale_by(getready, 2)
firstflap = False
current_state = 'menu'
dividedscore = score / 2
logo = pygame.image.load('sprites/logo.png').convert_alpha()
logo = pygame.transform.scale_by(logo, 0.15)
scorecard = pygame.image.load('sprites\scorecard.png').convert_alpha()
scorecard = pygame.transform.scale_by(scorecard, 2)
highscore = 0

font = pygame.font.Font('fonts/flappy-bird.ttf', 120) # Applies a font for all buttons
 # Renders the text that is entered 
swoosh = pygame.mixer.Sound('audio/swoosh.wav')
collide = pygame.mixer.Sound('audio/hit.wav')
die = pygame.mixer.Sound('audio/die.wav')
bing = pygame.mixer.Sound('audio/point.wav')
bing.set_volume(0.2)
die.set_volume(0.2)
collide.set_volume(0.2)

print(Flappy.__dict__)
ground = pygame.sprite.GroupSingle()
ground.add(Ground())
#Flappy bird class
flappy = pygame.sprite.GroupSingle()
flappy.add(Flappy())
jumpinput = True
pipey = 800
#Pipe Group
obstacle_group = pygame.sprite.Group()
#Timer
obstacle_timer = pygame.USEREVENT + 1 # Pygame has reserved events, so we need to make sure we do this to add our own events, this is a custom event.
pygame.time.set_timer(obstacle_timer,1800)

delay_timer = pygame.USEREVENT + 2

#buttons
startButton = Button((236, 105, 21), 150, 700, 100, 50, 'Start')
quitButton = Button((236, 105, 21), 350, 700, 100, 50, 'Quit')
okButton = Button((236, 105, 21), 250, 700, 100, 50, 'Ok')

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == obstacle_timer:
            if firstflap == True:
                obstacle_group.add(Obstacle('top'))
                obstacle_group.add(Obstacle('bottom'))
                pipey = randint(600, 1000)
    if current_state == 'menu':
        obstacle_group.empty()
        screen.blit(background,(0,0))
        ground.draw(screen)
        flappy.draw(screen)
        flappy.update()
        screen.blit(logo,(75,130))
        startButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))
        if startButton.isOver(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                swoosh.play()
                score = 0
                current_state = "game"
        if quitButton.isOver(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                swoosh.play()
                sleep(0.6)
                pygame.quit()
                exit()
        #screen.blit(ground,ground_rect) #surface,rect REMEMBER
        
    if current_state == 'game':
        screen.blit(background,(0,0))
        obstacle_group.draw(screen)
        obstacle_group.update()
        flappy.draw(screen) 
        flappy.update()
        ground.draw(screen)
        ground.update()
        if firstflap == False:
            screen.blit(getready,(200,10))
        else:
            text = font.render(str(round(score)), 1, (255, 255, 255)) # rounds up the score and converts it to a string.
            screen.blit(text,(300,100))

        #else:
            #screen.blit(background,(0,0))
            #obstacle_group.draw(screen)
            #obstacle_group.update()
            #flappy.draw(screen) 
        #screen.blit(ground,ground_rect)
        #current_state = flappy.apply_gravity()
        '''
        ground_rect.x -= 4
        if ground_rect.x <= -45:
            ground_rect.x = 0
        '''
        current_state = collision_sprite() 
    if current_state == 'game_over':
        if score > highscore:
            highscore = score
        screen.blit(background,(0,0))
        obstacle_group.draw(screen)
        flappy.draw(screen)
        flappy.update()
        ground.draw(screen)
        firstflap = False
        okButton.draw(screen, (0, 0, 0))
        #TODO This scoring system, add a high score variable and display the score and high score in the "scorecard.png", also add "gameover.png" text in game over state.
        screen.blit(scorecard, (200,300))
        text = font.render(str(round(score)), 1, (255, 255, 255)) # rounds up the score and converts it to a string.
        screen.blit(text,(300,360))
        highscoretext = font.render(str(round(highscore)), 1, (255, 255, 255))
        screen.blit(highscoretext,(300,470))
        

        if okButton.isOver(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                swoosh.play()
                current_state = "menu"


        
    
    pygame.display.update()
    clock.tick(60)