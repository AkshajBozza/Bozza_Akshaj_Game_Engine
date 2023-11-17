# File created by Akshaj Bozza

'''
Goals: to have the user be able to use a and d keys to move the sprite left and right and also allow the sprite to jump from platform to platform with the space key.
Then, the platforms should form randomly above the player's current position so the player can continuously ascend to a new height.
For every new platform touched, the platform beneath it to disappear (so if the player misses a platform, he falls all the way to the bottom and loses) and the player should get a point for every new platform.
Enemy sprites should also be formed randomly and should result in the player deducing points
New features:
A power-up class that spawns randomly and has every instance disappear upon collision with the sprite. Colliding with the power-up enables a score change of +2 and colliding with an enemy sprite
leads to points being deducted.
A new feature was also having the screen move up as the player rises through platforms. 
The score feature was also added -- but it is not perfect yet.
Rules:
Use a, d, and space keys to jump and move left/right to get to as many platforms as possible. Avoid the red enemies and try to get the power-ups.
Falling from a platform leads to game over (since you fall all the way to the bottom)
Feedback:
The score calculation is buggy -- it is increasing and decreasing incredibly quickly, and I am interested in further debugging this for the final project. Also adding more dispersion in the enemies
and more strategic randomness since the power-up and mobs often have a very close position. Some of the new platforms formed are also not moving, so it is difficult to ascend, preventing testing of the screen moving up feature.
Freedom:
The player can choose which platform and where to jump as well as which keys to use. They can also continue the game for as long as they want, provided they adhere to the rules and do not fall from their platform.
'''


# content from kids can code: http://kidscancode.org/blog/
# content from https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
from random import randint
import os
from settings import *
from sprites import *
import math

vec = pg.math.Vector2 # this allows usage of 2D vectors and makes it easier to add/subtract them to determine direction in the game

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images') #getting access to all the images in the images folder
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # creating the screen with the width and height from settings
        pg.display.set_caption("Platformer Game") #setting the title of the game
        self.clock = pg.time.Clock()
        self.running = True # the game is running
    
    def new(self): 
        # create a group for all sprites
        self.score = 0 #setting the starting score to 0
        self.all_sprites = pg.sprite.Group() #creating a sprite group to manage all game sprites
        self.all_platforms = pg.sprite.Group() #a group specifically for platforms
        self.all_mobs = pg.sprite.Group() # a group for the enemies
        self.all_powerups = pg.sprite.Group() # a group for each power-up generated
        self.platform_generated = False #since the game involves generating platforms infinitely as the game goes on, this variable assesses whether platforms should be generated at a specific point or not

        # instantiate classes
        self.player = Player(self)
        self.ground = Platform(*GROUND) 
        powerup = PowerUp(self)
        
        # add instances to groups
        self.all_sprites.add(self.player, self.ground, powerup)
        self.all_powerups.add(powerup)

        for p in PLATFORM_LIST:
            plat = Platform(*p) #creating platform instances and adding them to the platforms and sprites group
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        for m in range(0, 10): # instantiating mobs with random positions throughout the screen
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT / 2)), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m) #adding each mob to the group

        self.run() #this starts the game loop
        self.last_platform_y = 0 # this keeps track of the last y-coordinate of the platform to avoid generating new platforms below this y-coordinate
    
    def run(self): #the game loop that runs while the game is playing
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        # Updating game state - sprite movements, collisions, and score changes.
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False) #checking collisions between platform and ground
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if hits or ghits:
            # Handling collisions with platforms and the ground.
            if self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y #reversing the velocity if it is moving upward to account for gravity (must come down)
            elif self.player.vel.y > 0:
                if hits:
                    # Increase the score only when reaching a new platform
                    if hits[0].rect.top < self.player.rect.bottom:
                        self.score += 1
                        # Deleting all platforms below the higher one
                        for plat in self.all_platforms:
                            if plat.rect.top > hits[0].rect.top: #for all the platforms in the platform group, if it has a lower y-coordinate than the current plat, delete it
                                plat.kill()
                        # Create a new platform only if one hasn't been generated already
                        if not self.platform_generated:
                            new_platform = Platform(
                                randint(0, WIDTH - 100),  # Adjust as needed (any random x-coordinate)
                                hits[0].rect.top - 50,  # Slightly higher than the current platform (cant be too high since player needs to jump to the new platform)
                                100,
                                20,
                                "normal"
                            ) #then adding it to the group
                            self.all_sprites.add(new_platform)
                            self.all_platforms.add(new_platform)
                            self.last_platform_y = new_platform.rect.top  # Update the last platform's y-coordinate
                            self.platform_generated = True  # Set the platform generation flag
                        # Resetting the flag when the player starts descending -- if it is descending, a new platform should not be created
                        elif self.player.rect.bottom > hits[0].rect.bottom:
                            self.platform_generated = False 
                    #setting the player's position based on the collision of the ground or with another platform
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player.vel.x = hits[0].speed * 1.5
                if ghits: #this is for collision with the ground
                    self.player.pos.y = self.ground.rect.top
                    self.player.vel.y = 0


        # Check for collision with power-up
        powerup_hits = pg.sprite.spritecollide(self.player, self.all_powerups, True)
        self.score += 2 * len(powerup_hits)  # Increase score for each power-up collected by 2 points

        # Check for collision with mobs
        mob_hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
        if mob_hits:
            self.score -= 1  # Deduct score by -1 for each mob hit
            if self.score < 0:
                self.score = 0 #there is not going to be a "negative" score for this game

        # Adjust screen position based on player's y-coordinate
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)  # Move the player up
            # Generate new platform only when the player reaches a higher y-position and a platform has not been generated
            if self.player.rect.top < self.last_platform_y and not self.platform_generated:
                p = Platform(randint(0, WIDTH - 100), self.last_platform_y - 50, 100, 20, "normal")
                self.all_sprites.add(p)
                self.all_platforms.add(p) #this is the new platform created
                self.last_platform_y = p.rect.top  # Update the last platform's y-coordinate
                self.platform_generated = True  # Set the platform generation flag

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: #if this command is hit, the game should no longer be running
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 20)
        pg.display.flip() #adding the score to be displayed on the game

    def draw_text(self, text, size, color, x, y): #this is the program to write text with parameters of the position, font, and size/color
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size) #determining font and size
        text_surface = font.render(text, True, color) #getting rectangular dimensions
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect) #drawing the text surface onto the game screen at the specified position

g = Game()
while g.running:
    g.new()

pg.quit()