"""
oyoneによるデータ収集の非常用ファイル
もし、モーターおよびArduinoがだめになったとしても
カメラとラズパイさえ生きていれば撮影ができるようにする
"""

import cv2
import save_sensor_img

data_saver = save_sensor_img.Data_Saver(save_video=True, save_sensor=True)
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(1)
    sensor_dict = None
    data_saver.save(frame, sensor_dict, '-')
