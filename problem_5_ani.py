import problem_1
import problem_2
import problem_3
import problem_4
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

# Import data
dataset = problem_4.dead_reckoning_yaw(alpha_tilt=0.05, alpha_yaw=0.0005)


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
    ax[0].set_title('Gyroscope Filter')
    ax[1].set_xlabel('X Axis')
    ax[1].set_ylabel('Y Axis')
    ax[1].set_title('Gyro + Acc Drift Filter')
    ax[2].set_xlabel('X Axis')
    ax[2].set_ylabel('Y Axis')
    ax[2].set_title('Gyro + Acc + Mag Yaw Filter')

    ax[0].set_xlim3d(-0.6, 0.6)
    ax[0].set_ylim3d(-0.6, 0.6)
    ax[0].set_zlim3d(-0.6, 0.6)
    ax[1].set_xlim3d(-0.6, 0.6)
    ax[1].set_ylim3d(-0.6, 0.6)
    ax[1].set_zlim3d(-0.6, 0.6)
    ax[2].set_xlim3d(-0.6, 0.6)
    ax[2].set_ylim3d(-0.6, 0.6)
    ax[2].set_zlim3d(-0.6, 0.6)

    frameTick = dataset[frame]
    gyro = frameTick['est_gyro_q']
    gyro_tilt = frameTick['est_tilt_q']
    gyro_yaw = frameTick['est_yaw_q']

    # Quaternions multiplication
    Gx = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro,
        (0, 1, 0, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro))
    Gy = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro,
        (0, 0, 1, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro))
    Gz = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro,
        (0, 0, 0, 1)),
        problem_1.iii_quaternion_inverse_rotation(gyro))

    Driftx = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_tilt,
        (0, 1, 0, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))
    Drifty = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_tilt,
        (0, 0, 1, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))
    Driftz = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_tilt,
        (0, 0, 0, 1)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))

    Yawx = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_yaw,
        (0, 1, 0, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))
    Yawy = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_yaw,
        (0, 0, 1, 0)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))
    Yawz = problem_1.iv_quaternion_product(problem_1.iv_quaternion_product(
        gyro_yaw,
        (0, 0, 0, 1)),
        problem_1.iii_quaternion_inverse_rotation(gyro_tilt))

    # Render axes
    ax[0].quiver(0, 0, 0,
                 *Gx[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(1, 0, 0)])
    ax[0].quiver(0, 0, 0,
                 *Gy[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 1, 0)])
    ax[0].quiver(0, 0, 0,
                 *Gz[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 1)])

    ax[1].quiver(0, 0, 0,
                 *Driftx[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(1, 0, 0)])
    ax[1].quiver(0, 0, 0,
                 *Drifty[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 1, 0)])
    ax[1].quiver(0, 0, 0,
                 *Driftz[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 1)])

    ax[2].quiver(0, 0, 0,
                 *Yawx[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(1, 0, 0)])
    ax[2].quiver(0, 0, 0,
                 *Yawy[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 1, 0)])
    ax[2].quiver(0, 0, 0,
                 *Yawz[1:],
                 length=1.0,
                 normalize=True,
                 arrow_length_ratio=0.05,
                 colors=[(0, 0, 1)])


# Render animation
ani = FuncAnimation(fig, frame_ani, frames=range(0, len(dataset), 8),
                    blit=False)

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
fullspeed_writer = Writer(fps=32, metadata=dict(artist='Me'), bitrate=1200)
halfspeed_writer = Writer(fps=16, metadata=dict(artist='Me'), bitrate=1200)

ani.save('ani_fullspeed.mp4', writer=fullspeed_writer)
# ani.save('ani_halfspeed.mp4', writer=halfspeed_writer)

# frame_ani(4)
# plt.savefig("ani.png")
