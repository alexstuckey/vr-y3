import csv
import math


# Methods

# (i) convert Euler angle readings (radians) to quaternions (2 marks)
def i_radians_to_quaternions():
    return


# (ii) calculate Euler angles from a quaternion (2 marks)
def ii_quaternion_to_radians():
    return


# (iii) convert a quaternion to its conjugate (inverse rotation) (2 marks)
def iii_quaternion_inverse_rotation():
    return


# (iv) calculate the quaternion product of quaternion a and b (2 marks)
def iv_quaternion_product(a, b):
    return


# Read and import the provided (.csv) dataset (5 marks)
dataset = list()

with open('imu-data.csv') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]

    for row in csv_reader:
        newDict = {}
        newDict['time'] = float(row['time'])

        # Convert rotational rate to radians/sec
        newDict['gyroscope.X'] = math.radians(float(row['gyroscope.X']))
        newDict['gyroscope.Y'] = math.radians(float(row['gyroscope.Y']))
        newDict['gyroscope.Z'] = math.radians(float(row['gyroscope.Z']))

        # Normalize magnitude of both the accelerometer and magnetometer values
        # taking special care of NaN divisions (5 marks)
        acc_sum = \
            (float(row['accelerometer.X']) * float(row['accelerometer.X'])) \
            + (float(row['accelerometer.Y']) * float(row['accelerometer.Y'])) \
            + (float(row['accelerometer.Z']) * float(row['accelerometer.Z']))
        acc_norm = math.sqrt(acc_sum)
        newDict['accelerometer.X'] = float(row['accelerometer.X']) / acc_norm
        newDict['accelerometer.Y'] = float(row['accelerometer.Y']) / acc_norm
        newDict['accelerometer.Z'] = float(row['accelerometer.Z']) / acc_norm

        mag_sum = \
            (float(row['magnetometer.X']) * float(row['magnetometer.X'])) \
            + (float(row['magnetometer.Y']) * float(row['magnetometer.Y'])) \
            + (float(row['magnetometer.Z']) * float(row['magnetometer.Z']))
        mag_norm = math.sqrt(mag_sum)
        newDict['magnetometer.X'] = float(row['magnetometer.X']) / mag_norm
        newDict['magnetometer.Y'] = float(row['magnetometer.Y']) / mag_norm
        newDict['magnetometer.Z'] = float(row['magnetometer.Z']) / mag_norm

        print(newDict)
