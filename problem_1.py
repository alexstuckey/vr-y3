import csv


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
with open('imu-data.csv') as csvfile:
    csvcontents = csv.DictReader(csvfile)
    for line in csvcontents:
        print(line)

# Convert rotational rate to radians/sec and normalize the magnitude
# of both the accelerometer and magnetometer values
# taking special care of NaN divisions (5 marks)
