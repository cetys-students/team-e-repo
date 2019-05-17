from enum import IntEnum

# I2C device addresses

LSM6DS33_Address = 0x6B  # Accelerometer & Gyroscope
LIS3MDL_Address = 0x1E  # Magnetometer
LPS25H_Address = 0x5D # Barometer

class LSM6DS33(IntEnum):
    OUTX_L_G = 0x22
    OUTX_H_G = 0x23
    OUTY_L_G = 0x24
    OUTY_H_G = 0X25
    OUTZ_L_G = 0x26
    OUTZ_H_G = 0x27
    WHO_AM_I = 0x0F
    CTRL1_XL = 0x10
    CTRL2_G = 0x11
    CTRL3_C = 0x12
    CTRL4_C = 0x13
    CTRL5_C = 0x14
    CTRL6_C = 0x15
    CTRL7_G = 0x16
    CTRL8_XL = 0x17
    CTRL9_XL = 0x18
    CTRL10_C = 0x19
    OUTX_L_XL = 0x28
    OUTX_H_XL = 0x29
    OUTY_L_XL = 0x2A
    OUTY_H_XL = 0x2B
    OUTZ_L_XL = 0x2C
    OUTZ_H_XL = 0x2D

