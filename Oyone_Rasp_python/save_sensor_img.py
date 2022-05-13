import json
import numpy as np
import os
import cv2
import shutil

# テスト用
import get_guide
import manual
import argparse

"""
Save sensor, keyboard input and image data to specified directory.
This class makes directories './data/video' and './data/sensor'.
Record images and keys only when the user is pushing the keyboard.
An id is attached to the image, key, and sensor value.
"""
class Data_Saver():
    def __init__(self , save_video=False,save_sensor=False,
            output_video_dir='./data/video', output_sensor_dir='./data/sensor'):
        self.frame_id = 0
        self.save_video = save_video
        self.save_sensor = save_sensor
        self.output_video_dir = output_video_dir
        self.output_sensor_dir = output_sensor_dir
        self.sensor_direction_path = os.path.join(output_sensor_dir, 'sensor_direction.jsonl')

        print(f'video will be save to {self.output_video_dir}.')
        print(f'sensor value and direction will be save to {self.output_sensor_dir}.')

        if os.path.exists(output_video_dir):
            shutil.rmtree(output_video_dir)
        if os.path.exists(output_sensor_dir):
            shutil.rmtree(output_sensor_dir)
        os.makedirs(output_video_dir)
        os.makedirs(output_sensor_dir)

    # save image, sensor value and direcrion
    def save(self, img:np.ndarray, sensor_dict:dict, direction:str)->None:
        # save image
        imgpath = os.path.join(self.output_video_dir, "frame_{}.jpg".format(self.frame_id))
        cv2.imwrite(imgpath, img)
        # save direcion and sensor value (dict)
        if self.frame_id==0:
            with open(self.sensor_direction_path,'w') as f:
                f.write(str(self.frame_id) + ',' +direction + '\n')
        else:
            with open(self.sensor_direction_path,'a') as f:
                f.write(str(self.frame_id) + ',' +direction + '\n')
        self.frame_id = self.frame_id + 1


## -----------------テスト------------------------
def manual_run(save_video=False, save_sensor=False, os='mac',
               output_video_dir=None, output_sensor_dir=None):
    data_saver = Data_Saver(save_video,save_sensor)
    manual_director = manual.ManualDirector(os)
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
            # cv2.imshow('edge image', edge_img)
            # cv2.imshow('final image',final)

            key = cv2.waitKey(10)
            sensor_dict = None # 後でセンサー値をaruduinoから取得する関数を作成する
            which = manual_director.get_direction(key)

            if (save_video and which!='-'):
                data_saver.save(input_img, sensor_dict, which)
                # print(which)
            
            # key27: esc
            if key == 27:
                break
    

if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    guide_line_getter = get_guide.Guide_getter()

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
        args.video_output_dir = '.data/video'
    if args.sensor_output_dir == None:
        args.sensor_output_dir = '.data/sensor'
    if args.os == None:
        args.os = 'mac'
    

    try:
        if(args.mode=='manual'):
            print('manual mode start.')
            manual_run(args.save_video, args.save_sensor, args.os,
                args.video_output_dir, args.sensor_output_dir)
        elif(args.mode=='auto' & args.desplay_video==True):
            print('auto mode(output image) start.\n')
            # autorun_with_image()
        elif(args.mode=='auto' & args.desplay_video==None):
            print('auto mode start.\n')
            # autorun()
        else:
            print(args.mode,"mode is not exit.")
    except:
        print("How to specify options is different.\
        please read help by -h or --help option.")
