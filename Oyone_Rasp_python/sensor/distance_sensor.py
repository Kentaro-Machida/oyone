import pigpio
import time
import struct

# ToFセンサー
import VL53L1X
import signal

class Srf02():
    """
    超音波センサー: SRF02
    I2C通信を想定
    """
    def __init__(
        self,
        i2c_instance:'SDA and SCL number'=1):

        self.SRF02_ADDRESS = 0x70  # SRF02のI2Cアドレス
        self.pi = pigpio.pi()
        self.h = pi.i2c_open(i2c_instance, SRF02_ADDRESS)

    def get_distance(self):
        self.pi.i2c_write_byte_data(self.h, 0, 0x51)  # 0x00と0x51を送信して測定開始
        time.sleep(70/1000)  # 測定完了まで少し待機
        (data_size, data) = self.pi.i2c_read_i2c_block_data(h, 2, 2) #  結果の受信
        val = struct.unpack('>H', data)[0]  # 2バイトの測定結果を数値に変換
        distance = val*10  # 10枚して単位をmmに変換
        return distance

class Gp2y0e03():
    """
    赤外線距離センサー: GP2Y0E03
    I2C通信を想定
    """
    def __init__(
        self,
        i2c_instance:'SDA and SCL number'=1):

        self.GP2Y0E03_ADDRESS = 0x40
        self.pi = pigpio.pi()
        self.h = pi.i2c_open(i2c_instance, self.GP2Y0E03_ADDRESS)
        self.shift_bit = self.pi.i2c_read_byte_data(self.h, 0x35) & 0x07  # Shift Bit取得

    def get_distance(self):
        (data_size, data) = self.pi.i2c_read_i2c_block_data(h, 0x5e, 2) #  結果の受信
        return (data[0]*16 + data[1]%16)/(16*2**shift_bit) * 10  # 測定データから距離を計算

class AE_VL53L1X():
    """
    ToF距離センサー: AE-VL53L1X
    I2C通信を想定
    """
    def __init__(
        self,
        i2c_instance:'SDA and SCL number'=1
    ):
    
    self.AE_VL53L1X_ADDRESS = 0x29
    self.tof = VL53L1X.VL53L1X(i2c_bus=i2c_instance, i2c_address=self.AE_VL53L1X_ADDRESS)
    self.tof.open()
    self.tof.start_ranging(1)  # 1:short, 2:medium, 3:long 測定開始

    def get_distance(self):
        # 距離の取得
        return self.tof.get_distance()

    def stop(self):
        """
        測定の停止
        おそらく測定ループを抜けたら刈らず実行する必要がある
        """
        self.tor.stop_ranging()

# テストコード
def test():
    sensor = SRF02()
    while True:
        print(sensor.get_distance())
