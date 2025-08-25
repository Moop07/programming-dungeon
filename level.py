import pygame

screen = None

def set_screen(input_screen):
    global screen
    screen = input_screen

class player:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.image.load("main_character.png")

    def draw_self(self):
        screen.blit(self.image, (self.xpos, self.ypos))