"""
Shoot a movie with the camera and determine the direction oyone should take
"""

import cv2
import get_guide
import serial_communication
import direction

cap = cv2.VideoCapture(0)
guide_line_getter = get_guide.Guide_getter()

def run_only():
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

def run_with_image():
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
        
    cap.release()
    cv2.destroyAllWindows()

run_with_image()

