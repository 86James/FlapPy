import pygame
global current_state
current_state = 'game'
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
        global jumpinput # There is definitely an easier way to do this
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if jumpinput == True:
                self.angle = 50
                self.gravity = -15
                self.multiplier = 0
                self.flap_sound.play()
                jumpinput = False
        if keys[pygame.K_SPACE] == False:
            jumpinput = True
            
    def apply_gravity(self):
        global current_state
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom>= 775:
            self.rect.bottom = 775
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
            self.player_input()
            self.apply_gravity()
            self.animation_state()
            self.rotate_bird()
        else:
            self.apply_gravity()
            self.rotate_bird()