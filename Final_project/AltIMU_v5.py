from I2C import I2C
from constants import *


class AltIMUv5(I2C):

    # Output registers used by the accelerometer
    accel_registers = [
        LSM6DS33.OUTX_L_XL,
        LSM6DS33.OUTX_H_XL,
        LSM6DS33.OUTY_L_XL,
        LSM6DS33.OUTY_H_XL,
        LSM6DS33.OUTZ_L_XL,
        LSM6DS33.OUTZ_H_XL,
    ]

    # Output registers used by the gyroscope
    gyro_registers = [
        LSM6DS33.OUTX_L_G,
        LSM6DS33.OUTX_H_G,
        LSM6DS33.OUTY_L_G,
        LSM6DS33.OUTY_H_G,
        LSM6DS33.OUTZ_L_G,
        LSM6DS33.OUTZ_H_G,
    ]

    def __init__(self, bus_id=1):
        """ 
        Set up I2C connection and initialize some flags and values.
        """

        super(AltIMUv5, self).__init__(bus_id)
        self.is_accel_enabled = False
        self.is_gyro_enabled = False

    def __del__(self):
        """ 
        Clean up.
        """
        try:
            # Power down MEMS
            #self.write_register(LSM6DS33, LSM303D.CTRL1, 0x00)

            super(AltIMUv5, self).__del__()
        except:
            pass

    def enable(self, accelerometer=True, gyroscope=True):
        if accelerometer:
            self.write_register(LSM6DS33_Address, LSM6DS33.CTRL1_XL, 0xAA)  #4G
            self.write_register(LSM6DS33_Address, LSM6DS33.CTRL3_C, 0x04)
            self.is_accel_enabled = True
        if gyroscope:
            self.write_register(LSM6DS33_Address, LSM6DS33.CTRL2_G, 0x88)   #1000 dps
            self.is_gyro_enabled = True

    def get_accelerometer_raw(self):
        """
        Return a 3D vector of raw accelerometer data.
        """

        # Check if accelerometer has been enabled
        if not self.is_accel_enabled:
            raise(Exception('Accelerometer is not enabled!'))

        return self.read_sensor(LSM6DS33_Address, self.accel_registers)

    def get_accelerometer_cal(self):
        """
        Return a 3D vector of calibrated accelerometer data.
        """
        raw = self.get_accelerometer_raw()
        scaling = 0.122 / 1000

        cal_x = raw[0] * scaling
        cal_y = raw[1] * scaling
        cal_z = raw[2] * scaling

        return [cal_x, cal_y, cal_z]

    def get_gyroscope_raw(self):
        """
        Return a 3D vector of raw gyroscope data.
        """

        # Check if gyroscope has been enabled
        if not self.is_gyro_enabled:
            raise(Exception('Gyroscope is not enabled!'))

        return self.read_sensor(LSM6DS33_Address, self.gyro_registers)

    def get_gyroscope_cal(self):
        """
        Return a 3D vector of calibrated gyroscope data.
        """
        raw = self.get_gyroscope_raw()
        scaling = 35 / 1000

        cal_x = raw[0] * scaling
        cal_y = raw[1] * scaling
        cal_z = raw[2] * scaling

        return [cal_x, cal_y, cal_z]
