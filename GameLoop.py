import pygame
from ScreenHandler import ScreenHandler


class GameLoop:
    
    def __init__(self, scale = 1):
        
        self.init_display_size(scale)
        self.screen_handler = ScreenHandler(scale)
        self.init_screen_loops()
        
        self.live_screen_name = "MainMenuScreen"
        
        pygame.init()
        pygame.display.set_caption("Notetris")
        
        self.gameDisplay = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()
        
        self.isRunning = True
        
        self.main()
        
    def init_display_size(self, scale):
        
        self.root_display_size = (550, 750)
        self.display_size = (int(self.root_display_size[0]*scale), 
                             int(self.root_display_size[1]*scale))
        self.scale = scale
        
    def init_screen_loops(self):
        
        self.screen_loops = {"GameScreen": self.game_screen_loop,
                             "MainMenuScreen": self.main_menu_screen_loop}
        
    def main(self):
        
        while self.isRunning:
            
            self.event_handler()
            
            self.screen_loops[self.live_screen_name]()

            self.draw_screen()
            pygame.display.update()
            self.clock.tick(30)
            
            
    def game_screen_loop(self):
        
        self.screen_handler.tick()
        
    def main_menu_screen_loop(self):
        
        self.screen_handler.tick()
        
    def event_handler(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            else:
                self.screen_handler.pass_event(event)
                
    def draw_screen(self):
        
        self.gameDisplay.fill((255, 255, 255))
        
        self.blit_screen_background()
        
        self.blit_screen_objects()
        
    def resize_img(self, img):
        
        size = (int(self.root_display_size[0]*self.scale), 
                int(self.root_display_size[1]*self.scale))
        return pygame.transform.scale(img, size)
        
    def blit_screen_background(self):
        
        background_img = self.screen_handler.live_screen.background_img
        location = self.screen_handler.live_screen.background_img_coordinates
        self.gameDisplay.blit(background_img, location)
        
    def blit_screen_objects(self):
        
        blit_list = self.screen_handler.live_screen.get_blit_list()
        for item in blit_list:
            self.gameDisplay.blit(item.display_img, item.coordinates)


if __name__ == "__main__":
    gl = GameLoop(1)
    pygame.quit()
    quit()