import csv
import math


# My definition of a quaternion as a 4-tuple,
# of 4 real numbers
# (qw, qx i, qy j, qz k)

# Methods

# (i) convert Euler angle readings (radians) to quaternions (2 marks)
def i_radians_to_quaternions(x, y, z):
    # Implementation assistance from
    # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

    # Euler angle
    #  x-axis = roll
    cr = math.cos(x * 0.5)
    sr = math.sin(x * 0.5)
    #  y-axis = pitch
    cp = math.cos(y * 0.5)
    sp = math.sin(y * 0.5)
    #  z-axis = yaw
    cy = math.cos(z * 0.5)
    sy = math.sin(z * 0.5)

    q = (cy * cp * cr + sy * sp * sr,
         cy * cp * sr - sy * sp * cr,
         sy * cp * sr + cy * sp * cr,
         sy * cp * cr - cy * sp * sr)

    return q


# (ii) calculate Euler angles from a quaternion (2 marks)
def ii_quaternion_to_radians(q):
    # Implementation assistance from
    # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

    # roll (x-axis rotation)
    sinr_cosp = +2.0 * (q[0] * q[1] + q[2] * q[3])
    cosr_cosp = +1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2])
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = +2.0 * (q[0] * q[2] - q[3] * q[1])
    if (math.fabs(sinp) >= 1):
        # use 90 degrees if out of range
        pitch = math.copysign(math.pi / 2, sinp)
    else:
        pitch = math.asin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = +2.0 * (q[0] * q[3] + q[1] * q[2])
    cosy_cosp = +1.0 - 2.0 * (q[2] * q[2] + q[3] * q[3])
    yaw = math.atan2(siny_cosp, cosy_cosp)

    euler = (roll, pitch, yaw)
    return euler


# (iii) convert a quaternion to its conjugate (inverse rotation) (2 marks)
def iii_quaternion_inverse_rotation(a):
    q = (a[0],
         - a[1],
         - a[2],
         - a[3])

    return q


# (iv) calculate the quaternion product of quaternion a and b (2 marks)
def iv_quaternion_product(a, b):
    q = (a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
         a[0] * b[1] + b[0] * a[1] + a[2] * b[3] - b[2] * a[3],
         a[0] * b[2] + b[0] * a[2] + b[1] * a[3] - a[1] * b[3],
         a[0] * b[3] + b[0] * a[3] + a[1] * b[2] - b[1] * a[2])

    return q


def each_row(row):
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

    return newDict


def load_dataset():
    # Read and import the provided (.csv) dataset (5 marks)
    dataset = list()

    with open('imu-data.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        csv_reader.fieldnames = [field.strip()
                                 for field in csv_reader.fieldnames]

        for row in csv_reader:
            dataset.append(each_row(row))

    return dataset
