"""
実験場所でsshが使用できなかった場合の緊急用コード
oyoneを直進モードだけで動作させる
"""
import serial_communication
import save_sensor_img
import cv2

cap = cv2.VideoCapture(0)

def straight_only():
    to_arduino = serial_communication.communicator()
    data_saver = save_sensor_img.Data_Saver(save_video=True,
    save_sensor=True)
    while True:
        ret, frame = cap.read()

        if ret == False:
            print('Camera is not detected.')
            break
        else:
            cv2.imshow('input image',frame)
            key = cv2.waitKey(1)
            sensor_dict = None # 後でセンサー値をaruduinoから取得する関数を作成する
            which = "f"
            
            data_saver.save(frame, sensor_dict, which)
            print(which)
            to_arduino.serial_wirte(which)

            rtn_which = to_arduino.serial_read()

            # key27: esc
            if key == 27:
                to_arduino.serial_wirte("s")
                break

straight_only()
