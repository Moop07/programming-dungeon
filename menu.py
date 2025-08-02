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
        self.variable = None #to differentiate the button from a slider

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

class slider(button):
    #variable is the variable this slider is responsible for
    #it should be a string to act as a key for the dictionary which stores
    #the user's settings
    def __init__(self, xpos, ypos, width, height, colour, screen, function, variable):
        super().__init__(xpos, ypos, width, height, colour, "", screen, function) #no text on the slider and the function is handled differently
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.colour = colour
        self.screen = screen
        self.function = function
        self.value = 50
        self.variable = variable

    def draw_self(self):
        pygame.draw.rect(self.screen, self.colour, (self.xpos, self.ypos, self.width, self.height))
        #draws a second rectangle of the opposite colour to show the slider's value
        pygame.draw.rect(self.screen, (255 - self.colour[0], 255-self.colour[1], 255-self.colour[2]), (self.xpos, self.ypos, self.width*self.value/100, self.height))

    def detect_mouse(self, mouse_position):
        if self.xpos+self.width >= mouse_position[0] >= self.xpos and self.ypos+self.height >= mouse_position[1] >= self.ypos:
            self.value = (mouse_position[0]-self.xpos)*100/self.width
            return True
        else:
            return False



def initalise_menu_screen(): #returns a list of objects that get rendered
    return [button(260, 600, 200, 76, (0, 0, 0), "Exit", screen, "quit"), button(260, 500, 200, 76, (0, 0, 0), "Options", screen, "open options"),
    button(260, 400, 200, 76, (0, 0, 0), "Tutorial", screen, "open tutorial"), button(260, 300, 200, 76, (0, 0, 0), "Endless", screen, "open endless"),
    button(260, 200, 200, 76, (0, 0, 0), "Level Select", screen, "open level select")]


def open_options_menu(): #creates a surface and then places the options menus buttons on it
    return[button(260, 600, 200, 76, (0, 0, 0), "Close", screen, "close options"),
    button(210, 500, 300, 76, (0, 0, 0), "Toggle Fullscreen", screen, "toggle fullscreen"),
    slider(210, 300, 300, 76, (255, 255, 255), screen, "set volume", "volume"),
    slider(210, 400, 300, 76, (255, 255, 255), screen, "set simulation speed", "simulation speed")]
