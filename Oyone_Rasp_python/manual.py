"""
Code for manual operation.
"""
class ManualDirector():
    def __init__(self, os:str)->None:
        # arrows key value of opencv waitkey (MacOS)
        if (os=='mac'):
            self.up=0
            self.down=1
            self.left=2
            self.right=3
        elif (os=='linux'):
            self.up=82
            self.down=84
            self.left=81
            self.right=83

# Convert from arrow keys to characters required by arduino
    def get_direction(self,key:int) -> str:
        if(key==self.up):
            return 'f'
        elif(key==self.down):
            return 'b'
        elif(key==self.right):
            return 'r'
        elif(key==self.left):
            return 'l'
        else:
            return 's'
