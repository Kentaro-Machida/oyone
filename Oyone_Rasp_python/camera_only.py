"""
oyoneによるデータ収集の非常用ファイル
もし、モーターおよびArduinoがだめになったとしても
カメラとラズパイさえ生きていれば撮影ができるようにする
"""

import cv2
import save_sensor_img

FRAME_WIDTH = 2592  # MAX 2592
FRAME_HEIGHT = 1944 # MAX 1944

data_saver = save_sensor_img.Data_Saver(save_video=True, save_sensor=True)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(1)
    sensor_dict = None
    data_saver.save(frame, sensor_dict, '-')
