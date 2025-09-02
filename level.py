import pygame
import interpreter

screen = None

def set_screen(input_screen):
    global screen
    screen = input_screen

class player:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.image.load("main_character.png")
        self.interpreter = None

    def draw_self(self):
        screen.blit(self.image, (self.xpos, self.ypos))
    
    def follow_instructions(self, code):
        self.interpreter = interpreter.interpreter(code)
        self.events = self.interpreter.interpret()
        print(self.events)
    
    def get_code(self, code):
        self.code = code
        self.follow_instructions(self.code)

player = player(500, 500)
player.get_code('''let a = 0;
while (a < 10){
    if (a < 5 ){
        move_player_up();
    }
    if (a > 5){
        move_player_down();
    }
    a = a + 1;
    }
''')
