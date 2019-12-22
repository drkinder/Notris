# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 00:10:19 2018

@author: Dylan
"""

import pygame
from random import randint
from GameBoard import GameBoard
from Button import Button

class GameScreen:
    
    """Every ----Screen class must have an event_handler method.
    CONSIDER POLYMORPHISM FOR SCREENS.
    !!!MUST ALSO HAVE get_blit_list method - Can return empty list if nothing
    to blit!
    !!!MUST ALSO HAVE tick -- What to do each pass of gameloop
    """
    
    def __init__(self, scale = 1):
        
        self.fall_speed = 3   
        self.combination_size = 3
        self.code = 2 # TESTING SPAWNING NEW BLOCKS
        
        self.init_background_img()   
        self.init_game_board(scale)
        
        self.isLive = True # POSSIBLE WAY TO HANDLE SWITCHING SCREENS
        self.isPopUp = False
        
    def init_background_img(self):
        # NEED TO INCORPORATE SCALING
        
        self.background_img = pygame.image.load("graphics\\level_frame1.png")
        self.background_img_coordinates = (0, 0)
        
    def init_game_board(self, scale):
        
        game_size = (5, 7) # (x, y) will be multiplied by game_block size
        game_offset = (25, 25) # Hard-Coded based on level_frame.png
        self.game_board = GameBoard(game_size, game_offset, scale)
        self.game_board.set_combination_size(self.combination_size)
        self.scale = scale
    
    def get_blit_list(self):
        
        if not self.isPopUp:
            return self.game_board.get_blocks2blit()
        else:
            return (self.game_board.get_blocks2blit() + [self.pop_up] +
                    self.pop_up.get_blit_list())
        
    def event_handler(self, event):
        
        if not self.isPopUp:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # self.game_board.check_all_collision() #all or just left?
                    self.game_board.move_left()
                if event.key == pygame.K_RIGHT:
                    # self.game_board.check_all_collision() #all or just right?
                    self.game_board.move_right()
                if event.key == pygame.K_UP:
                    self.game_board.live_block.advance_live_note_code()
                if event.key == pygame.K_DOWN:
                    self.fall_speed = 15
                if event.key == pygame.K_SPACE:
                    self.game_board.live_block.play_true_note()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.fall_speed = 3
                
        else:
            self.pop_up.event_handler(event)
            
    def tick(self):
        
        if self.game_board.isOver and not self.isPopUp:
            self.isPopUp = True
            self.pop_up = GameOverPopUp(self.scale)
        
        if self.game_board.live_block.isMoving:
            for i in range(self.fall_speed):
                self.game_board.move_down()
                
        elif self.game_board.isOver:
            if self.pop_up.play_again:
                self.isLive = False
                self.new_screen = "GameScreen"
        else:
            self.game_board.land_live_block()
            self.game_board.check_all_combinations()
            self.game_board.get_next_live_block()


class GameOverPopUp:
    
    def __init__(self, scale):
        
        #IMPLEMENT SCALING!
        self.display_img = pygame.image.load("graphics\\game_over.png")
        self.init_coordinates()
        
        self.init_buttons()
        
        self.play_again = False
            
    def init_coordinates(self):
        
        self.image_size = self.display_img.get_rect().size
        self.coordinates = (int(550/2 - self.image_size[0]/2), int(750/2 - self.image_size[1]/2))
        
    def init_buttons(self):
        
        path = "graphics\\play_again_button.png"
        loc = (self.coordinates[0] + self.image_size[0]/2 - 60,
               self.coordinates[1] + self.image_size[1]/2)
        self.play_again_button = Button(path, loc, "playAgain")

        self.buttons = [self.play_again_button]
        self.commands = {"playAgain": self.play_again}
        
    def event_handler(self, event):
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.check_button_pressed(pygame.mouse.get_pos())
            
    def check_button_pressed(self, pos):
        
        for button in self.buttons:
            if button.isPressed(pos):
                self.commands[button.command_key]()
                return
            
    def get_blit_list(self):
        return self.buttons
            
    def play_again(self):
        
        self.play_again = True
