import pygame


class Button:
    
    def __init__(self, button_filename, loc, command_key):
        
        self.display_img = pygame.image.load(button_filename)
        self.coordinates = loc
        
        self.init_bounding_box()
        
        self.command_key = command_key
        
    def init_bounding_box(self):
        
        button_size = self.display_img.get_rect().size
        self.bounding_box = (self.coordinates, (self.coordinates[0]+button_size[0], self.coordinates[1]+button_size[1]))
    
    def isPressed(self, click_pos):
        
        if (self.bounding_box[0][0] <= click_pos[0] <= self.bounding_box[1][0]
            and self.bounding_box[0][1] <= click_pos[1] <= self.bounding_box[1][1]):
            return True
        else:
            return False
