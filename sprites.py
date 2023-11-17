#File created by Akshaj Bozza
#importing libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import os
from settings import *
from random import randint
from pygame.math import Vector2 as vec
#creating a folder for all the images for the sprites' personas
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #creating a rectangle for the sprite and giving it the mentioned image based on the dimensions
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH / 2, HEIGHT / 2) #setting the initial position as a vector
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100 
    #method to determine how player moves given specific keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5 #left
        if keys[pg.K_d]:
            self.acc.x = 5 #right
        if keys[pg.K_SPACE]:
            self.jump()

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground) #if there is a collision, that means the player is in a position to jump (off a surface)
        if hits or ghits:
            self.vel.y = -PLAYER_JUMP #this sets the velocity to a negative value, simulating a jump (vertical motion in the opposite way)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV) #applying gravity
        self.controls() #handling controls
        self.acc.x += self.vel.x * -PLAYER_FRIC #friction
        self.vel += self.acc #updating velocity 
        self.pos += self.vel + 0.5 * self.acc #using physics equations to determine the displacement and therefore the new position
        self.rect.midbottom = self.pos 

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() #using the rectangular coordinates to create a sprite
        self.rect.x = x
        self.rect.y = y #this sets the position of the platform, who has all the attributes of the Sprite class
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5 #if the platform is moving, set its speed to 5

    def update(self):
        if self.category == "moving": #if it is a moving platform
            self.rect.x += self.speed #add its speed (speed*time = distance)
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed #changing its position based on how it is moving

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect() #similar to how we initialized the platforms
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH / 2, HEIGHT / 2) #using a vector to set its position as well

    def update(self):
        pass #right now the mobs are stationary

class PowerUp(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((POWERUP_SIZE, POWERUP_SIZE)) #initializing the power-up using the size in settings
        self.image.fill(BLUE)
        self.rect = self.image.get_rect() 
        self.rect.center = (randint(0, WIDTH), randint(0, HEIGHT)) #assigning a random position for the power-up during its initialization

    def update(self):
        hits = pg.sprite.collide_rect(self, self.game.player) #if the player touches the power-up, make the power-up disappear
        if hits:
            self.kill()

class Pewpew(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y #this is just the initialization for the PEWPEW class, no specific attributes have been added.
        #I plan to work on this to see if it's doable to give the player some capability to shoot the enemies 