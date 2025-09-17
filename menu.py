import pygame
import sys
screen = 0
WIDTH = 0
LENGTH = 0
def set_screen(input_screen, width, length):
    global WIDTH
    global LENGTH
    global screen
    screen = input_screen
    WIDTH = width
    LENGTH = length

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
            self.value = (mouse_position[0]-self.xpos)*100//self.width
            return True
        else:
            return False

#no functionality, just displays text on the screen
class text_box:
    def __init__(self, xpos, ypos, width, height, text, text_size, screen):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.screen = screen
        self.variable = None

    def draw_self(self):
        font = pygame.font.SysFont('Corbel', self.text_size)
        text = font.render(self.text, True, (0, 0, 0))
        rectangle = text.get_rect()
        rectangle.center = (self.xpos+self.width//2, self.ypos+self.height//2)
        self.screen.blit(text, rectangle)
    
    def detect_mouse(self, mouse_position):
        return False


class input_box:
    def __init__(self, xpos, ypos, width, height):
        #set up the rectangle that the input box is on
        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.color = (0, 0, 0) #black
        self.text = ""
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render("", True, self.color)
        self.active = False #by default it is inactive; the user must click on the textbox to start typing
        self.cursor_position = 0 

    def handle_event(self, event):
        #if the user clicks on the the input box then active
        #otherwise inactive
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        #we add the key the user presses to the text
        #if self.cursor_position is anything other than len(self.text) we put it in the appropiate position
        #left and right keys can move the cursor
        #backspace deletes, enter starts a new line, and ctrl submits (for now)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.text = self.text[:self.cursor_position] + '\n' + self.text[self.cursor_position:]
                self.cursor_position += 1
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
            elif event.key == pygame.K_LCTRL:
                print(self.text)
                return self.text
            else:
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += len(event.unicode)

    def update(self):
        self.txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw_self(self):
        lines = self.text.split('\n')
        y_offset = self.rect.y + 5
        cursor_x, cursor_y = self.rect.x + 5, y_offset

        character_count = 0
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, self.color)
            screen.blit(line_surface, (self.rect.x + 5, y_offset + i * 32))

            #determine the cursor's position
            if character_count <= self.cursor_position <= character_count + len(line):
                cursor_text = line[:self.cursor_position - character_count]
                cursor_x = self.rect.x + 5 + self.font.size(cursor_text)[0]
                cursor_y = y_offset + i * 32
            character_count += len(line) + 1  #add one for the newline

        if self.active:
            pygame.draw.line(screen, self.color, (cursor_x, cursor_y), (cursor_x, cursor_y + 32), 2)

        pygame.draw.rect(screen, self.color, self.rect, 2)



def initalise_menu_screen(): #returns a list of objects that get rendered
    return [button((WIDTH//2)-100, 600, 200, 76, (0, 0, 0), "Exit", screen, "quit"), button(WIDTH//2 - 100, 500, 200, 76, (0, 0, 0), "Options", screen, "open options"),
    button(WIDTH//2 - 100, 400, 200, 76, (0, 0, 0), "Tutorial", screen, "open tutorial"), button(WIDTH//2 - 100, 300, 200, 76, (0, 0, 0), "Endless", screen, "open endless"),
    button(WIDTH//2 - 100, 200, 200, 76, (0, 0, 0), "Level Select", screen, "open level select")]


def open_options_menu(): #creates a surface and then places the options menus buttons on it
    return[button(WIDTH//2 - 100, 600, 200, 76, (0, 0, 0), "Close", screen, "close options"),
    button(WIDTH//2 - 150, 500, 300, 76, (0, 0, 0), "Toggle Fullscreen", screen, "toggle fullscreen"),
    slider(WIDTH//2 - 150, 300, 300, 76, (255, 255, 255), screen, "set volume", "volume"),
    text_box(WIDTH//2-250, 300, 100, 76, "volume", 35, screen),
    slider(WIDTH//2 -150, 400, 300, 76, (255, 255, 255), screen, "set simulation speed", "simulation speed"),
    text_box(WIDTH//2-300, 400, 100, 76, "simulation speed", 25, screen)]

def open_level_select():
    return [button(WIDTH//10, LENGTH//10, WIDTH//11+55, WIDTH//11, (0, 0, 0), "Level 1", screen, "start level 1"),
    button(2.7*WIDTH//10, LENGTH//10, WIDTH//11+55, WIDTH//11, (0, 0, 0), "Level 2", screen, "start level 2"),
    button(4.4*WIDTH//10, LENGTH//10, WIDTH//11+55, WIDTH//11, (0, 0, 0), "Level 3", screen, "start level 3"),
    button(6.1*WIDTH//10, LENGTH//10, WIDTH//11+55, WIDTH//11, (0, 0, 0), "Level 4", screen, "start level 4"),
    button(7.8*WIDTH//10, LENGTH//10, WIDTH//11+55, WIDTH//11, (0, 0, 0), "Level 5", screen, "start level 5"),
    button(WIDTH//20, LENGTH//20, WIDTH//25+35, LENGTH//25, (0, 0, 0), "Back", screen, "close level select")]

def level_gui():
    return [
    button(0, 0, WIDTH//25+35, LENGTH//25, (0, 0, 0), "Back", screen, "open level select"),
    input_box(0, LENGTH//25, 4*WIDTH//10, 24*LENGTH//25)
    ]
