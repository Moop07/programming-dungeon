import pygame
import interpreter
import time

screen = None

def set_screen(input_screen):
    global screen
    screen = input_screen


class player(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.image.load(r"C:\Users\xande\Documents\Coding\Python Projects\NEA\main_character.png")
        self.image = pygame.transform.scale(self.image, (screen.get_size()[0]*0.1, screen.get_size()[1]*0.1))
        self.interpreter = None
        self.events = []

    def draw_self(self):
        screen.blit(self.image, (self.xpos, self.ypos))
    
    def follow_instruction(self):
        if len(self.events) != 0:
            instruction = self.events[0]
            if instruction == "move up":
                self.ypos -= screen.get_size()[1]//20
            elif instruction == "move down":
                self.ypos += screen.get_size()[1]//20
            elif instruction == "move left":
                self.xpos -= screen.get_size()[0]//20
            elif instruction == "move right":
                self.xpos += screen.get_size()[0]//20
            self.events = self.events[1:]
    
    def get_code(self, code):
        self.code = code
        self.interpreter = interpreter.interpreter(code)
        self.events = self.interpreter.interpret()
        #self.follow_instruction(self.code)

class wall:
    def __init__(self, xpos, ypos, wall_type):
        self.xpos = xpos
        self.ypos = ypos
        if wall_type == "back":
            self.image = pygame.image.load(r"C:\Users\xande\Documents\Coding\Python Projects\NEA\assets\back_wall.png")
            self.image = pygame.transform.scale(self.image, (screen.get_size()[0]*0.175, screen.get_size()[1]*0.1))
    
    def draw_self(self):
        screen.blit(self.image, (self.xpos, self.ypos))

class treasure:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.image.load(r"C:\Users\xande\Documents\Coding\Python Projects\NEA\assets\treasure.png")
        self.image = pygame.transform.scale(self.image, (screen.get_size()[0]*0.09, screen.get_size()[1]*0.09))
    
    def draw_self(self):
        screen.blit(self.image, (self.xpos, self.ypos))

def level(num):
    width, length = screen.get_size()
    if num == 1:
        return [wall(0.4*width, 0.4*length, "back"), wall(0.4*width, 0.6*length, "back"), wall(0.575*width, 0.4*length, "back"),
        wall(0.575*width, 0.6*length, "back"), wall(0.75*width, 0.4*length, "back"), wall(0.75*width, 0.6*length, "back"),
        wall(0.925*width, 0.4*length, "back"), wall(0.925*width, 0.6*length, "back"), treasure(0.9*width, 0.5*length)]

def check_win():
    if (player.xpos, player.ypos) == (treasure.xpos, treasure.ypos):
        print("win")
#player = player(500, 500)
#player.get_code('''let a = 5;
#let b = 2;
#print(a+b);
#''')
