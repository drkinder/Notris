# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:38:31 2018

@author: Dylan
"""

import pygame

class NoteBlock:
    
    def __init__(self, game_size, game_offset, note_code, scale = 1):
        """ game_size should be a tuple (x, y) - x represents how many
        blocks wide the play area should be, y represents how many blocks
        high the play area should be. game_offset should be a tuple (x, y) -
        x represents how many pixels to shift the game to the left, y 
        represents how many pixels to shift the game down.
        """
        pygame.mixer.init()
        
        self.init_block_size(scale)
        
        self.init_play_area(game_size, game_offset)

        self.true_note = self.get_note(note_code)
        self.true_audio = "sounds\\{}.wav".format(self.true_note)
        
        self.init_coordinates()
        self.init_collision()
        
        print(self.true_note)
        
        self.isMoving = True
        self.isVisible = True
        self.isLocked = False       
        
        self.displayed_note_code = 1
        self.get_displayed_note_attributes()
        
        self.play_true_note()
        
    def init_block_size(self, scale):
               
        block_size = pygame.image.load("graphics\\border.png").get_rect().size
        self.block_size = int(block_size[0]*scale)
        self.scale = scale
        
        
    def init_play_area(self, game_size, game_offset):
        
        self.play_area = {
                          "max":{"width": (int(self.block_size*game_size[0] +
                                           game_offset[0])),
                                 "height": (int(self.block_size*game_size[1] +
                                                game_offset[1]))},
    
                          "min":{"width": game_offset[0],
                                 "height": game_offset[1]}                         
                                                                              }
                          
    def init_coordinates(self):
        
        play_width = (self.play_area["max"]["width"] - 
                      self.play_area["min"]["width"])
        self.coordinates = (int(play_width/2 - self.block_size/2) + 
                                 self.play_area["min"]["width"],
                            self.play_area["min"]["height"])    

        
    def init_collision(self):

        self.bottom_collision = False
        self.left_collision = False
        self.right_collision = False
        
    def get_note(self, note_code):
        
        note_codes = {1: "a",
                      2: "b",
                      3: "c",
                      4: "d",
                      5: "e",
                      6: "f",
                      7: "g"}
        
        try:
            return note_codes[note_code]
        except KeyError:
            raise KeyError("'{}' is not a known note_code".format(note_code))
            
    def advance_live_note_code(self):
        
        if self.displayed_note_code < 7:
            self.displayed_note_code += 1
        else:
            self.displayed_note_code = 1
            
        self.get_displayed_note_attributes()
            
    def get_displayed_note_attributes(self):
        
        self.displayed_note = self.get_note(self.displayed_note_code)
        img_file = "graphics\\{}_border.png".format(self.displayed_note)
        self.display_img = pygame.image.load(img_file)
        
    def move_down(self, board, amount = 1):
        
        if amount == 1:
            self.check_bottom_collision(board)
        else:
            self.bottom_collision = False

        if not self.bottom_collision:
            self.coordinates = (self.coordinates[0], self.coordinates[1]+amount)
            
    def move_left(self, board):
        
        self.check_left_collision(board)
        
        if not self.left_collision:
            self.coordinates = (self.coordinates[0] - self.block_size, self.coordinates[1])
            
    def move_right(self, board):
        
        self.check_right_collision(board)
        
        if not self.right_collision:
            self.coordinates = (self.coordinates[0] + self.block_size, self.coordinates[1])

    def offset_x(self, value):
        
        return value + self.play_area["min"]["width"]
    
    def offset_y(self, value):
        
        return value + self.play_area["min"]["height"]
    
    def handle_locking(self):
        
        if self.displayed_note != self.true_note:
            self.isLocked = True
            img_file = "graphics\\{}_border_locked.png".format(self.true_note)
            self.display_img = pygame.image.load(img_file)
    
    def check_bottom_collision(self, board):
        
        self.check_collision = False
        
        self.check_bottom_border_collision()
            
        if not self.bottom_collision:
            for row in board:
                for slot in row:
                    if self.is_bottom_touching(slot):
                        self.bottom_collision = True
                        self.isMoving = False
                        return
            
    def check_bottom_border_collision(self):
        
        if self.coordinates[1] == (self.play_area["max"]["height"] - self.block_size):
            self.bottom_collision = True
            self.isMoving = False
    
    def is_bottom_touching(self, note_block):
        
        try:
            coordinates_above = (note_block.coordinates[0],
                                 note_block.coordinates[1] - self.block_size)
            
            if coordinates_above == self.coordinates:
                return True
        except AttributeError:
            pass
        return False
    
    def check_left_collision(self, board):
        
        self.check_left_border_collision()
        
        if not self.left_collision:
            for row in board:
                for slot in row:
                    if self.is_left_touching(slot):
                        self.left_collision = True
                        return
        else:
            return
                    
        self.left_collision = False
                    
    def check_left_border_collision(self):
        
        if self.coordinates[0] == self.play_area["min"]["width"]:
            self.left_collision = True
        else:
            self.left_collision = False
            
    def is_left_touching(self, slot):
        
        try:
            if slot.coordinates[0] + self.block_size == self.coordinates[0]:
                if (slot.coordinates[1] - self.block_size < 
                    self.coordinates[1] < 
                    slot.coordinates[1] + self.block_size):
                    return True
                
        except AttributeError:
            pass
        return False
    
    def check_right_collision(self, board):
        
        self.check_right_border_collision()
        
        if not self.right_collision:
            for row in board:
                for slot in row:
                    if self.is_right_touching(slot):
                        self.right_collision = True
                        return
        else:
            return
                    
        self.right_collision = False
                    
    def check_right_border_collision(self):
        
        if self.coordinates[0] == self.play_area["max"]["width"] - self.block_size:
            
            self.right_collision = True
        else:
            self.right_collision = False
            
    def is_right_touching(self, slot):
        
        try:
            if slot.coordinates[0] - self.block_size == self.coordinates[0]:
                if (slot.coordinates[1] - self.block_size < 
                    self.coordinates[1] < 
                    slot.coordinates[1] + self.block_size):
                        return True
        except AttributeError:
            pass
        return False
    
    def is_min_width_left_collision(self):
        
        if self.coordinates[0] == self.play_area["min"]["width"]:
            self.left_collision = True
            
    def is_max_width_right_collision(self):
        
        if self.coordinates[0] == (self.play_area["max"]["width"] - 
                                   self.block_size):
            self.right_collision = True
            
    def play_true_note(self):
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.true_audio)
            pygame.mixer.music.play()
