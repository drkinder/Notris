from GameScreen import GameScreen
from MainMenu import MainMenu

class ScreenHandler:
    
    def __init__(self, scale=1):
        
        self.scale = scale
        self.init_screens()
        
        #self.live_screen = self.screens["GameScreen"](self.scale)
        self.live_screen = self.screens["MainMenuScreen"](self.scale)
        
    def init_screens(self):
        
        self.screens = {"GameScreen": GameScreen,
                        "MainMenuScreen": MainMenu}
                        #"High Scores": self.high_scores}
    
    def tick(self):
        
        if self.live_screen.isLive:
            self.live_screen.tick()
        else:
            new_screen = self.live_screen.new_screen
            self.live_screen = self.screens[new_screen](self.scale)

    def get_blit_list(self):
        return self.live_screen.get_blit_list()
    
    def pass_event(self, event):
        
        self.live_screen.event_handler(event)