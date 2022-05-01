"""
Take a video from the camera and run oyone.
You can choose from three driving modes.
1. auto run 
2. auto run while outputting photos.
3. manual run: you can operate the ship with the arrow keys.
ex) 
python main.py auto
python main.py auto_with_image
python main.py manual
"""

import sys
import cv2
import get_guide
import serial_communication
import direction
from manual import manual_direction

cap = cv2.VideoCapture(0)
guide_line_getter = get_guide.Guide_getter()

def autorun():
    to_arduino = serial_communication.communicator()
    while True:
        ret, frame = cap.read()
        guide_line_getter.set_frame(frame)

        if ret == False:
            print('Camera is not detected.')
            break
        else:
            guide_line = guide_line_getter.get_guide_line()
            if guide_line==-1:
                stop = True
            else:
                stop = False

            center_line = guide_line_getter.get_center_index()
            which = direction.direction(guide_line, center_line, stop)
            to_arduino.serial_wirte(which)

            key = cv2.waitKey(10)
            # key27: esc
            if key == 27:
                break

def autorun_with_image():
    to_arduino = serial_communication.communicator()
    while True:
        ret, frame = cap.read()
        guide_line_getter.set_frame(frame)

        if ret == False:
            print('Camera is not detected.')
            break
        else:
            center_line = guide_line_getter.get_center_index()
            guide_line = guide_line_getter.get_guide_line()
            if guide_line==-1:
                stop = True
            else:
                stop = False
            which = direction.direction(guide_line, center_line, stop)
            rtn_which = to_arduino.serial_read()
            print(rtn_which)
            to_arduino.serial_wirte(which)

            edge_img = guide_line_getter.get_edges_frame()
            final = guide_line_getter.get_final_frame()

            cv2.imshow('input image',frame)
            cv2.imshow('edge image', edge_img)
            cv2.imshow('final image',final)
            key = cv2.waitKey(10)
            # key27: esc
            if key == 27:
                break
        
def manual_run():
    to_arduino = serial_communication.communicator()
    while True:
        ret, frame = cap.read()
        guide_line_getter.set_frame(frame)

        if ret == False:
            print('Camera is not detected.')
            break
        else:
            edge_img = guide_line_getter.get_edges_frame()
            final = guide_line_getter.get_final_frame()

            cv2.imshow('input image',frame)
            cv2.imshow('edge image', edge_img)
            cv2.imshow('final image',final)

            key = cv2.waitKey(1)
            which = manual_direction(key)
            to_arduino.serial_wirte(which)

            rtn_which = to_arduino.serial_read()
            print(rtn_which)
            
            # key27: esc
            if key == 27:
                break

def main()->None:
    args = sys.argv
    if len(args)<1:
        print('Please select a mode.\n \"auto\" or \"manual\" or \"auto_with_image\".')
    elif len(args)>2:
        print('Enter only one argument.\n \"auto\" or \"manual\" or \"auto_with_image\".')
    else:
        if(args[1]=='manual'):
            print('manual mode start.\n')
            manual_run()
        elif(args[1]=='auto_with_image'):
            print('auto mode(output image) start.\n')
            autorun_with_image()
        elif(args[1]=='auto'):
            print('auto mode start.\n')
            autorun()
        else:
            print(args[1],"mode is not exit.")

if __name__=='__main__':
    main()

cap.release()
cv2.destroyAllWindows()