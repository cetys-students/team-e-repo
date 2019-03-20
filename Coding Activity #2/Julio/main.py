from AltIMU_v3 import AltIMUv3

altimu = AltIMUv3()
altimu.enable()

while True:
    accel = altimu.get_accelerometer_raw()
    print(accel)
    rot = altimu.get_gyroscope_raw()
    print(rot)
