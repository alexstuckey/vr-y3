import math
import numpy as np
import problem_1
import problem_2


def q_to_v_theta(q):
    theta = math.acos(q[0]) * 2
    v = [q[1] / math.sin(theta / 2),
         q[2] / math.sin(theta / 2),
         q[3] / math.sin(theta / 2)]
    v = q[1:] / np.sin(theta / 2)
    return (v, theta)


# Estimate orientation from the gyroscope (rotational rate) and accelerometer.
def dead_reckoning_tilt(alpha_tilt=0.001):
    # Initial orientation
    qs = [(1.0, 0.0, 0.0, 0.0)]

    dataset = problem_2.dead_reckoning_gyroscope()

    for k in range(1, len(dataset)):
        delta_t = dataset[k]['time'] - dataset[k - 1]['time']

        qs_k = dataset[k]['est_gyro_q']

        # Transform acceleration measurements into the global frame (2 marks)
        a = dataset[k]['a']
        a_hat = problem_1.iv_quaternion_product(
            problem_1.iii_quaternion_inverse_rotation(qs_k),
            problem_1.iv_quaternion_product(
                (0, *a),
                qs_k,
            )
        )

        # Trim off first element to make as vector
        a_hat = a_hat[1:]

        # project into XY plane
        a_hat = (a_hat[0], a_hat[1], 0)

        # Calculate the tilt axis (2 marks)
        t = (a_hat[1], -a_hat[0], 0)

        # Find the angle φ between the up vector and the vector obtained from
        #   the accelerometer (2 marks)
        phi = np.arccos(np.clip(
            np.dot(a_hat, (0, 0, 1)),
            -1.0,
            1.0
        ))

        # Use the complementary filter to fuse the two signals (7 marks).
        qs_k = problem_1.iv_quaternion_product(
            problem_2.make_q(
                t,
                ((-alpha_tilt) * phi)
            ),
            qs_k
        )
        qs.append(qs_k)

    for k in range(len(dataset)):
        dataset[k]['est_tilt_q'] = qs[k]
        dataset[k]['est_tilt_rad'] = problem_1.ii_quaternion_to_radians(qs[k])
        dataset[k]['est_tilt_deg'] = tuple(
            np.rad2deg(dataset[k]['est_tilt_rad']))

    return dataset
