"""
Determine the control of motors.
"""
def direction(guide_line:int, center_line:int, stop=False) -> str:
    if (stop==True):
        return "s"

    right_thresh = -20
    left_thresh = 20

    difference = center_line - guide_line

    if (difference > left_thresh):
        return "l"

    elif(difference < right_thresh):
        return "r"
        
    else:
        return "f"
