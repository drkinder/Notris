class NoteName:
    
    def __init__(self, NoteBlock):
        
        self.note = NoteBlock.true_note
        self.display_img = ""
        
        self.init_coordinates(NoteBlock)
        
    def init_coordinates(self, root):
        
        x = int(root.coordinates[0] + root.block_size/3) # Some Hardcoding here!
        y = int(root.coordinates[0] + root.block_size/3)
        self.coordinates = (x, y)
