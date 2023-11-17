#This file was created by Akshaj Bozza

# game settings 
WIDTH = 1000
HEIGHT = 800  # Reduced height for a more compact display
FPS = 30

PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
PLAYER_FRIC = 0.2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) #using types to define color

GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal") #properties of the ground

PLATFORM_LIST = [
    (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20, "normal"),
    (125, HEIGHT - 350, 100, 20, "moving"),
    (222, 200, 100, 20, "normal"),
    (175, 100, 50, 20, "normal")
] #these are the properties of every platform created and can be randomly choosen between them

POWERUP_SIZE = 20 #the size of the power-up instance (20x20 square)