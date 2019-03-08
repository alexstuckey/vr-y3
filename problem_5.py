import problem_1
import problem_2
import problem_3
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import data
dataset = problem_1.load_dataset()
filter_gyro = problem_2.dead_reckoning_gyroscope()
filter_gyro_acc = problem_3.dead_reckoning_gyroscope_accelerometer(alpha=0.01)


my_dpi = 100
fig, ax = plt.subplots(figsize=(1280 / my_dpi, 720 / my_dpi),
                       dpi=my_dpi,
                       nrows=3, ncols=3)

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
ax[1][0].plot([row['time'] for row in filter_gyro],
              [row['est_gyro_deg'] for row in filter_gyro])


ax[1][1].set_xlabel('Time')
ax[1][1].set_ylabel(r'Orientation (°$\,s^{-1}$)')
ax[1][1].set_title('Gyroscope + Accelerometer')
ax[1][1].plot([row['time'] for row in filter_gyro_acc],
              [row['est_g_a_deg'] for row in filter_gyro_acc])

ax[1][2].set_xlabel('Time')
ax[1][2].set_ylabel(r'Orientation (°$\,s^{-1}$)')
ax[1][2].set_title('Gyroscope + Accelerometer + Magnetometer')

plt.delaxes(ax[2][0])
ax[2][0] = fig.add_subplot(3, 3, 7, projection='3d')
# for frame in range(0, len(filter_gyro)):
#     print(filter_gyro[frame]['time'],
#           filter_gyro[frame]['est_gyro'])
#     plt.plot(filter_gyro[frame]['time'],
#              filter_gyro[frame]['est_gyro'])

plt.tight_layout()
plt.savefig('testplot.png')
