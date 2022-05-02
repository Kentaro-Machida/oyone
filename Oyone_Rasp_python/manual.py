"""
Code for manual operation.
"""

# arrows key value of opencv waitkey (MacOS)
#up=0
#down=1
#left=2
#right=3

# arrows key value of opencv waitkey (external keyboard)
up=82
down=84
left=81
right=83

# Convert from arrow keys to characters required by arduino
def manual_direction(key:int) -> str:
    if(key==up):
        return 'f'
    elif(key==down):
        return 's'
    elif(key==right):
        return 'r'
    elif(key==left):
        return 'l'
    else:
        return '-'
