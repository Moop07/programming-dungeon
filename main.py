import pygame
import menu
import level

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_length = screen.get_size()
clock = pygame.time.Clock()
current_buttons = []
input_boxes = []
running = True
menu.set_screen(screen, screen_width, screen_length)
pygame.display.set_caption("Programming Dungeon")
level.set_screen(screen)
player = level.player(screen_width*0.4, screen_length*0.5)
player_tick = 0

settings = {
    "volume" : 50,
    "simulation speed" : 50,
    "fullscreen" : False
}
#will store any events the buttons return to be enacted later
button_events = []
#start the mouse position at 0,0 so the program doesn't crash trying to reference it before
#retrieving the mouse position for the first time
mouse_position = (0, 0)
current_buttons += menu.initalise_menu_screen()
current_menu = "main menu"

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in current_buttons:
                    if button.detect_mouse(mouse_position):
                        button_events.append(button.button_function())
                        print(button_events)
            for box in input_boxes:
                code = box.handle_event(event)
                if code != None:
                    player.get_code(code)

        screen.fill((255, 255, 255))
        mouse_position = pygame.mouse.get_pos()


        for button in current_buttons:
            button.draw_self()

        for box in input_boxes:
            box.draw_self()
            
        if current_menu == "level":
            player.draw_self()
            if player_tick == settings["simulation speed"]:
                player.follow_instruction()
                player_tick = 0
            player_tick += 1
            for item in level_objects:
                item.draw_self()
            level.check_win()

        #if a button has returned an event it will be in button events
        for event in button_events:
            #exits the main loop and uninitialises pygame to exit the game without error
            if event == "quit":
                running = False
                pygame.quit
            elif event == "open options":
                #if options has been opened we store what the previous buttons were
                #this is so we can return easily, since the options menu is just a sub menu
                #after that we can just clear the current buttons and add the buttons
                #for the options menu
                current_buttons = menu.open_options_menu()
                current_menu = "options menu"
            elif event == "close options" or event == "close level select":
                current_buttons = menu.initalise_menu_screen()
                current_menu = "main menu"
            elif event == "set volume":
                #finds the slider responsible for the volume
                for slider in current_buttons:
                    if slider.variable == "volume":
                        #adjusts the volume to the value of the slider
                        settings["volume"] = slider.value
            elif event == "set simulation speed":
                #finds the slider responsible for the sim speed
                for slider in current_buttons:
                    if slider.variable == "simulation speed":
                        #adjusts the sim speed to the value of the slider
                        settings["simulation speed"] = 100 - slider.value
            elif event == "toggle fullscreen":
                # flip the flag
                settings["fullscreen"] = not settings["fullscreen"]

                #recreate the window
                if settings["fullscreen"]:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_length))

                # update the width and the height
                new_width, new_height = screen.get_size()
                menu.set_screen(screen, new_width, new_height)

                if current_menu == "options menu":
                    current_buttons = menu.open_options_menu()
                else: #if they weren't anywhere in particular just put them in the main menu
                    current_buttons = menu.initalise_menu_screen()
            elif event == "open level select":
                current_buttons = menu.open_level_select()
                input_boxes = []
                current_menu = "level select"
            elif event[:11] == "start level": #somewhat temporary until each level is developed

                #get all the objects for the menu gui
                level_data = menu.level_gui()
                level_objects = level.level(int(event[-1]))
                #the input box is always at the end, so we pop that off the level_data array
                input_boxes = [level_data.pop()]
                #once the input box is removed we place the rest of our objects in the buttons array
                current_buttons = level_data
                current_menu = "level"
            #functionality for more buttons can be easily added later by adding more elif statements here
            else:
                pass
        #clear the list of events to avoid acting on a single button press multiple times
        button_events = []

        pygame.display.update()

        clock.tick(60)
