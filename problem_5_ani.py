import problem_1
import problem_2
import problem_3
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

# Import data
dataset = problem_1.load_dataset()
filter_tilt = problem_2.dead_reckoning_gyroscope()
filter_yaw = problem_4.dead_reckoning_yaw(alpha_tilt=0.05, alpha_yaw=0.05)


my_dpi = 100
fig = plt.figure(figsize=(1350 / my_dpi, 450 / my_dpi),
                 dpi=my_dpi)
ax = [None, None, None]

ax[0] = fig.add_subplot(1, 3, 1, projection='3d')
ax[1] = fig.add_subplot(1, 3, 2, projection='3d')
ax[2] = fig.add_subplot(1, 3, 3, projection='3d')

plt.tight_layout()


def frame_ani(frame):
    ax[0].cla()
    ax[1].cla()
    ax[2].cla()

    ax[0].set_xlabel('X Axis')
    ax[0].set_ylabel('Y Axis')
    ax[0].set_title('Gyroscope')
    ax[1].set_xlabel('X Axis')
    ax[1].set_ylabel('Y Axis')
    ax[1].set_title('Accelerometer')
    ax[2].set_xlabel('X Axis')
    ax[2].set_ylabel('Y Axis')
    ax[2].set_title('Magnetometer')

    ax[0].set_xlim3d(0, 1)
    ax[0].set_ylim3d(0, 1)
    ax[0].set_zlim3d(0, 1)
    ax[1].set_xlim3d(0, 1)
    ax[1].set_ylim3d(0, 1)
    ax[1].set_zlim3d(0, 1)
    ax[2].set_xlim3d(0, 1)
    ax[2].set_ylim3d(0, 1)
    ax[2].set_zlim3d(0, 1)

    frameTick = dataset[frame]

    # Extract data from frame
    gyro = np.array([0,
                     frameTick['gyroscope.X'],
                     frameTick['gyroscope.Y'],
                     frameTick['gyroscope.Z']
                     ])
    acc = np.array([0,
                    frameTick['accelerometer.X'],
                    frameTick['accelerometer.Y'],
                    frameTick['accelerometer.Z']
                    ])
    mag = np.array([0,
                    frameTick['magnetometer.X'],
                    frameTick['magnetometer.Y'],
                    frameTick['magnetometer.Z']
                    ])

    # Convert to quaternions
    Gx = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(gyro),
        (0, 1, 0, 0)),
        gyro)
    Gy = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(gyro),
        (0, 0, 1, 0)),
        gyro)
    Gz = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(gyro),
        (0, 0, 0, 1)),
        gyro)

    Ax = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(acc),
        (0, 1, 0, 0)),
        acc)
    Ay = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(acc),
        (0, 0, 1, 0)),
        acc)
    Az = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(acc),
        (0, 0, 0, 1)),
        acc)

    Mx = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(mag),
        (0, 1, 0, 0)),
        mag)
    My = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(mag),
        (0, 0, 1, 0)),
        mag)
    Mz = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        problem_1.iii_quaternion_inverse_rotation(mag),
        (0, 0, 0, 1)),
        mag)

    # Render axes
    ax[0].quiver(1, 0, 1,
                 *Gx[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[0].quiver(1, 0, 1,
                 *Gy[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[0].quiver(1, 0, 1,
                 *Gz[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])

    ax[1].quiver(1, 0, 1,
                 *Ax[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[1].quiver(1, 0, 1,
                 *Ay[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[1].quiver(1, 0, 1,
                 *Az[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])

    ax[2].quiver(1, 0, 1,
                 *Mx[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[2].quiver(1, 0, 1,
                 *My[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])
    ax[2].quiver(1, 0, 1,
                 *Mz[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 0)])


ani = FuncAnimation(fig, frame_ani, frames=range(0, len(dataset), 8),
                    blit=False)


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
fullspeed_writer = Writer(fps=32, metadata=dict(artist='Me'), bitrate=1000)
halfspeed_writer = Writer(fps=64, metadata=dict(artist='Me'), bitrate=1000)

ani.save('ani_fullspeed.mp4', writer=fullspeed_writer)
ani.save('ani_halfspeed.mp4', writer=halfspeed_writer)

# frame_ani(4)
# plt.savefig("ani.png")
