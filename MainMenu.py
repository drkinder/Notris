import pygame
from Button import Button


class MainMenu:
    
    def __init__(self, scale=1):
        
        self.init_background_img()
        
        self.init_buttons()
        
        self.isLive = True
       
    def init_background_img(self):
        # NEED TO INCORPORATE SCALING
        path = "graphics\\main_menu_background.png"
        self.background_img = pygame.image.load(path)
        self.background_img_coordinates = (0, 0)
        
    def init_buttons(self):
        
        self.play_button = Button("graphics\\play_button.png", (125, 180), 
                                  "play")
        
        self.commands = {"play": (self.switch_screen, "GameScreen")}
        self.buttons = [self.play_button]
    
    def get_blit_list(self):
        
        return self.buttons
    
    def event_handler(self, event):
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.check_button_pressed(pygame.mouse.get_pos())
            
    def switch_screen(self, new_screen):
        
        if new_screen in ["GameScreen"]:
            print("beep")
            self.isLive = False
            self.new_screen = new_screen
            
    def check_button_pressed(self, pos):
        
        for button in self.buttons:
            if button.isPressed(pos):
                function = self.commands[button.command_key][0]
                parameter = self.commands[button.command_key][1]
                function(parameter)
                print("PRESSED!")
                return
            
    def tick(self):
        
        pass
