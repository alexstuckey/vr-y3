import problem_4
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import data
# dataset is added to through each problem 1, 2, 3, 4
# problem_1.load_dataset(), problem_2.dead_reckoning_gyroscope(),
#    problem_3.dead_reckoning_tilt(alpha=0.001)
dataset = problem_4.dead_reckoning_yaw(alpha_tilt=0.006, alpha_yaw=0.0005)[1:]

my_dpi = 100
fig, ax = plt.subplots(figsize=(1280 / my_dpi, 720 / my_dpi),
                       dpi=my_dpi,
                       nrows=2, ncols=3)

# Render lines
ax[0][0].set_xlabel('Time')
ax[0][0].set_ylabel(r'Rotational Rate (°$\,s^{-1}$)')
ax[0][0].set_title('Tri-Axial Angular Rate')
ax[0][0].plot([row['time'] for row in dataset],
              [row['gyroscope.X-deg'] for row in dataset],
              label='X')
ax[0][0].plot([row['time'] for row in dataset],
              [row['gyroscope.Y-deg'] for row in dataset],
              label='Y')
ax[0][0].plot([row['time'] for row in dataset],
              [row['gyroscope.Z-deg'] for row in dataset],
              label='Z')


ax[0][1].set_xlabel('Time')
ax[0][1].set_ylabel(r'Acceleration (ms$^{-2}$)')
ax[0][1].set_title('Tri-Axial Acceleration in g')
ax[0][1].plot([row['time'] for row in dataset],
              [row['accelerometer.X'] for row in dataset],
              label='X')
ax[0][1].plot([row['time'] for row in dataset],
              [row['accelerometer.Y'] for row in dataset],
              label='Y')
ax[0][1].plot([row['time'] for row in dataset],
              [row['accelerometer.Z'] for row in dataset],
              label='Z')


ax[0][2].set_xlabel('Time')
ax[0][2].set_ylabel(r'Flux (Gauss, $G$)')
ax[0][2].set_title('Tri-Axial Magnetic Flux')
ax[0][2].plot([row['time'] for row in dataset],
              [row['magnetometer.X'] for row in dataset],
              label='X')
ax[0][2].plot([row['time'] for row in dataset],
              [row['magnetometer.Y'] for row in dataset],
              label='Y')
ax[0][2].plot([row['time'] for row in dataset],
              [row['magnetometer.Z'] for row in dataset],
              label='Z')


ax[1][0].set_xlabel('Time')
ax[1][0].set_ylabel(r'Orientation (°$\,s^{-1}$)')
ax[1][0].set_title('Gyroscope')
ax[1][0].plot([row['time'] for row in dataset],
              [row['est_gyro_deg'] for row in dataset])


ax[1][1].set_xlabel('Time')
ax[1][1].set_ylabel(r'Orientation (°$\,s^{-1}$)')
ax[1][1].set_title('Gyroscope + Tilt Filter (alpha=0.006)')
ax[1][1].plot([row['time'] for row in dataset],
              [row['est_tilt_deg'] for row in dataset])

ax[1][2].set_xlabel('Time')
ax[1][2].set_ylabel(r'Orientation (°$\,s^{-1}$)')
ax[1][2].set_title('Gyroscope + Tilt Filter + Yaw Filter (alpha=0.0005)')
ax[1][2].plot([row['time'] for row in dataset],
              [row['est_yaw_deg'] for row in dataset])


plt.tight_layout()
plt.savefig('p5.pdf')
plt.close('all')
