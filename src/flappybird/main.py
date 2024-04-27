import pygame
from pygame.locals import *
from pygame.sprite import *

pygame.init()

clock = pygame.time.Clock()
fps = 60 #locks the game to 60 fps

#Create Game Window
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#game_variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

#bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        #loop the image using array to animate the bird
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom <768:
                self.rect.y += int(self.vel)
                
        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #jumps when mouse is clicked
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0: #disables long press fly
                self.clicked = False


            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird in jump
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
           self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top -1 is from the bottom
        if position == 1: 
            self.imae = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y]
        if position == -1:
            self.rect.topleft = [x, y]


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

btm_pipe = Pipe(300, int(screen_height / 2))
pipe_group.add(btm_pipe)


run = True #sets the games if running

#loop while game is running
while run:

    clock.tick(fps) #controls the fps to 60

    #draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    #scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))


    #birl collision check
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False
    if game_over == False:
        ground_scroll -= scroll_speed #scrolls the ground
        if abs(ground_scroll) > 35: #loops the ground scroll to illutionate infinte scrolling
            ground_scroll = 0

    for event in pygame.event.get():
        #quit the game
        if event.type ==pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()