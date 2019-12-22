import pygame
from NoteBlock import NoteBlock


class GameBoard:
    
    def __init__(self, game_size, game_offset, scale = 1):
        
        self.game_size = game_size
        self.game_offset = game_offset
        self.scale = scale
        
        self.init_block_size(scale)
        self.generate_board(game_size)
        
        self.live_block_code = 1
        self.live_block = self.get_NoteBlock(self.live_block_code)
        
        self.isOver = False
        self.landed_blocks = []
        
    def set_combination_size(self, match_size):
        
        self.combination_size = match_size
        
    def advance_live_block_code(self):
        # Temp Solution - Requires more advanced shuffling
        
        if self.live_block_code < 3:
            self.live_block_code += 1
        else:
            self.live_block_code = 1
            
    def get_next_live_block(self):
        
        code = self.get_new_block_code()
        self.check_isOver(self.get_NoteBlock(code))
        if not self.isOver:
            self.live_block = self.get_NoteBlock(code)
        
    def check_isOver(self, next_NoteBlock):
        
        if self.live_block.coordinates == next_NoteBlock.coordinates:
            self.isOver = True
        else:
            self.isOver = False
        
    def init_block_size(self, scale):
               
        block_size = pygame.image.load("graphics\\border.png").get_rect().size
        self.block_size = int(block_size[0]*scale)
        
    def generate_board(self, game_size):
        
        self.board = []
        
        for y in range(game_size[1]):
            self.board.append([])
            for x in range(game_size[0]):
                self.board[y].append(0)
                
    def get_NoteBlock(self, note_code):
        
        return NoteBlock(self.game_size, self.game_offset, note_code, 
                         self.scale)
        
    def update_live_block_idx(self):
        
        # NEEDS REVISION - BLOCK CAN BE HALFWAY BETWEEN 2 OTHERS TO SIDE
        
        self.live_block_idx = (int((self.live_block.coordinates[0] - self.game_offset[0]) / self.block_size),
                               int((self.live_block.coordinates[1] - self.game_offset[1]) / self.block_size))
         
    def land_live_block(self):
        
        self.update_live_block_idx()
        self.landed_blocks.append(self.live_block)
        y, x = self.live_block_idx[1], self.live_block_idx[0]
        self.board[y][x] = self.live_block
        
        self.live_block.handle_locking()
        
    def drop_rows(self):
        
        for i in range(len(self.board)):
            for y_idx, row in enumerate(self.board):
                for x_idx, block in enumerate(row):
                    try:
                        if self.board[y_idx][x_idx] and self.board[y_idx+1][x_idx] == 0:
                            self.board[y_idx][x_idx].move_down(self.board, self.block_size)
                            self.move_block_idx_down((x_idx, y_idx))
                            
                    except (IndexError, AttributeError) as error:
                        print(error)
        
    def move_block_idx_Down(self, idxs):
        
        self.board[idxs[1]+1][idxs[0]] = self.board[idxs[1]][idxs[0]]
        self.clear_board_idx(idxs)
        
    def clear_board_idx(self, indexes):
        """ Indexes should be (x, y) tuple.
        """
        
        self.board[indexes[1]][indexes[0]] = 0

    def get_blocks2blit(self):
        
        return ([self.live_block] + self.landed_blocks)
    
    def move_down(self):
        
        self.live_block.move_down(self.board)
        
    def move_left(self):
        
        self.live_block.move_left(self.board)
        
    def move_right(self):
        
        self.live_block.move_right(self.board)
        
    def check_all_combinations(self):
        
        """ REDESIGN!!! --- GATHER ALL INDEXES PART OF COMBINATION -> REMOVE
        ---THIS WAY IF YOU HAVE BOTH HORIZONTAL AND VERTICAL COMBINATION,
        THE VERTICAL DOESN'T STEAL AWAY THE BLOCK BEFORE THE HORIZONTAL."""
       
        vert_check = self.check_vertical_combinations()
        hor_check = self.check_horizontal_combinations()
        
        if vert_check:
            self.delete_vertical_combinations(vert_check)
        if hor_check:
            self.delete_horizontal_combinations(hor_check)
            self.drop_rows()
        
    def check_horizontal_combinations(self):
        
        found_combinations = []
        for y_idx, row in enumerate(self.board):
            for x_idx, slot in enumerate(row):
                if self.check_right((x_idx, y_idx)):
                    found_combinations.append((x_idx, y_idx))
        return found_combinations
    
    def check_right(self, indexes):
        
        try:
            check = ([self.board[indexes[1]][i] for i in
                      range(indexes[0], indexes[0]+self.combination_size)])
            if (all(x.true_note == check[0].true_note and 
                    x.isLocked == False for x in check)):
                return True
        except (IndexError, AttributeError) as error:
            pass
        return False
    
    def delete_horizontal_combinations(self, combinations):
        
        for indexes in combinations:
            for i in range(indexes[0], indexes[0]+self.combination_size):
                self.clear_board_idx((i, indexes[1]))
                self.remove_invisible_blocks((i, indexes[1]))
              
    def check_vertical_combinations(self):
        
        found_combinations = []
        for y_idx, row in enumerate(self.board):
            for x_idx, slot in enumerate(row):
                if self.check_down((x_idx, y_idx)):
                    found_combinations.append((x_idx, y_idx))

        return found_combinations
    
    def check_down(self, indexes):
        
        try:
            # Get all values in self.board for given index + self.combination_size to y
            check = ([self.board[i][indexes[0]] for i in range(indexes[1], indexes[1]+self.combination_size)])
            if all(x.true_note == check[0].true_note and x.isLocked == False for x in check):
                return True
        except (IndexError, AttributeError) as error:
            pass
        return False
    
    def delete_vertical_combinations(self, combinations):
        
        for indexes in combinations:
            for i in range(indexes[1], indexes[1]+self.combination_size):
                self.clear_board_idx((indexes[0], i))
                self.remove_invisible_blocks((indexes[0], i))

    def remove_invisible_blocks(self, indexes):
        
        for i, block in enumerate(self.landed_blocks):
            if self.convert_idx2block_coords(indexes) == block.coordinates:
                self.landed_blocks.pop(i)
                
    def convert_idx2block_coords(self, indexes):
        
        return (indexes[0]*self.block_size + self.game_offset[0],
                indexes[1]*self.block_size + self.game_offset[1])
        
    def get_new_block_code(self):
        
        self.advance_live_block_code()
        return self.live_block_code
    
    def play_true_note(self, indexes):
        """ Goes to (y, x) indexes of self.board and plays the note of that
        index if there's a NoteBlock there.
        """

        if self.board[indexes[1]][indexes[0]]:
            self.board[indexes[1]][indexes[0]].play_true_note()
