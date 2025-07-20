import pygame
import sys
screen = 0
def set_screen(input_screen):
    global screen
    screen = input_screen
class button:
    def __init__(self, xpos, ypos, width, height, colour, text, screen, function):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.screen = screen
        self.function = function

    #detects if the player's mouse is over the button
    #for things like changing colour and detecting clicks
    def detect_mouse(self, mouse_position):
        if self.xpos+self.width >= mouse_position[0] >= self.xpos and self.ypos+self.height >= mouse_position[1] >= self.ypos:
            return True
        else:
            return False

    def draw_self(self):
        pygame.draw.rect(self.screen, self.colour, (self.xpos, self.ypos, self.width, self.height))
        font = pygame.font.SysFont('Corbel',35)
        text = font.render(self.text, True, (255, 255, 255))
        rectangle = text.get_rect()
        rectangle.center = (self.xpos+self.width//2, self.ypos+self.height//2)
        self.screen.blit(text, rectangle)

    #doesn't do anything by itself, designed to be changed by its children
    def button_function(self):
        return self.function

def draw_submenu_overlay():
    #draw submenu box
    menu_width, menu_height = 360, 300
    menu_x, menu_y = (720 - menu_width) // 2, (720 - menu_height) // 2
    pygame.draw.rect(screen, (30, 30, 30), (menu_x, menu_y, menu_width, menu_height), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 3, border_radius=10)

def initalise_menu_screen(): #returns a list of objects that get rendered
    return [button(260, 600, 200, 76, (0, 0, 0), "Exit", screen, "quit"), button(260, 500, 200, 76, (0, 0, 0), "Options", screen, "open options"),
    button(260, 400, 200, 76, (0, 0, 0), "Tutorial", screen, "open tutorial"), button(260, 300, 200, 76, (0, 0, 0), "Endless", screen, "open endless"),
    button(260, 200, 200, 76, (0, 0, 0), "Level Select", screen, "open level select")]


def open_options_menu(): #creates a surface and then places the options menus buttons on it
    return[button(260, 320, 200, 76, (0, 0, 0), "Close", screen, "close options")]