"""
Take a video from the camera and run oyone.
You can choose from three driving modes.
1. auto run 
2. auto run while outputting photos.
3. manual run: you can operate the ship with the arrow keys.

When the manual mode is selected, the captured image,
the sensor value at that time, and the key can be saved 
in a state of being linked by id.
ex) python3 main.py -mode manual -s -ss

You can get help by running 'main.py' with the -h option.
"""

import sys
import cv2
import argparse

import get_guide
import serial_communication
import direction
import manual
import save_sensor_img

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
        
def manual_run(save_video=False, save_sensor=False, os='mac',
               output_video_dir='./data/video', output_sensor_dir='./data/sensor'):
    to_arduino = serial_communication.communicator()
    manual_director = manual.ManualDirector(os)
    data_saver = save_sensor_img.Data_Saver(save_video,save_sensor,output_video_dir,output_sensor_dir)
    while True:
        ret, frame = cap.read()
        guide_line_getter.set_frame(frame)

        if ret == False:
            print('Camera is not detected.')
            break
        else:
            guide_line = guide_line_getter.get_guide_line()
            input_img = guide_line_getter.get_input_frame()
            edge_img = guide_line_getter.get_edges_frame()
            final = guide_line_getter.get_final_frame()

            cv2.imshow('input image',frame)
            cv2.imshow('edge image', edge_img)
            cv2.imshow('final image',final)

            key = cv2.waitKey(1)
            sensor_dict = None # 後でセンサー値をaruduinoから取得する関数を作成する
            which = manual_director.get_direction(key)
            print(which)
            to_arduino.serial_wirte(which)

            rtn_which = to_arduino.serial_read()
            if save_video:
                data_saver.save(input_img, sensor_dict, which)
            
            # key27: esc
            if key == 27:
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode","-m",
                        help="select mode. 'auto' or 'manual'.",
                        type=str, choices=['auto', 'manual'])
    parser.add_argument("--display_video", "-d",
                        help="Display videos.",
                        action='store_true')
    parser.add_argument("--save_video","-s",
                        help="Save videos.",
                        action='store_true')
    parser.add_argument("--save_sensor","-ss",
                        help="Save sensor value.",
                        action='store_true')
    parser.add_argument("--video_output_dir","-vo",
                        help="path to directory to save videos. default: '.data/video'",
                        type=str)
    parser.add_argument("--sensor_output_dir","-so",
                        help="path to directory to save sensor values. default: '.data/sensor'",
                        type=str)
    parser.add_argument("--os","-os",
                        help="operating system you use.",
                        type=str, choices=['mac', 'linux', 'window'])
    args = parser.parse_args()
    # default args
    if args.video_output_dir == None:
        args.video_output_dir = './data/video'
    if args.sensor_output_dir == None:
        args.sensor_output_dir = './data/sensor'
    if args.os == None:
        args.os = 'mac'
    

    
    if(args.mode=='manual'):
        print('manual mode start.')
        manual_run(args.save_video, args.save_sensor, args.os,
            args.video_output_dir, args.sensor_output_dir)
    elif(args.mode=='auto' & args.desplay_video==True):
        print('auto mode(output image) start.\n')
        autorun_with_image()
    elif(args.mode=='auto' & args.desplay_video==None):
        print('auto mode start.\n')
        autorun()
    else:
        print(args.mode,"mode is not exit.")
        print("How to specify options is different.\
        please read help by -h or --help option.")

if __name__=='__main__':
    main()

cap.release()
cv2.destroyAllWindows()
