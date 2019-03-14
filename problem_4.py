import math
import numpy as np
import problem_1
import problem_2
import problem_3


# Estimate orientation from the gyroscope (rotational rate) and accelerometer.
def dead_reckoning_yaw(alpha_yaw=0.001, alpha_tilt=0.001):
    # Initial orientation
    qs = [(1.0, 0.0, 0.0, 0.0)]

    dataset = problem_3.dead_reckoning_tilt(alpha_tilt=alpha_tilt)

    for k in range(1, len(dataset)):
        delta_t = dataset[k]['time'] - dataset[k - 1]['time']

        qs_k = dataset[k]['est_tilt_q']

        # Transform acceleration measurements into the global frame (2 marks)
        a = dataset[k]['a']
        a = problem_1.iv_quaternion_product(
            problem_1.iv_quaternion_product(
                problem_1.iii_quaternion_inverse_rotation(qs_k),
                (0, *a)
            ),
            qs_k
        )

        # Trim off first element to make as vector
        a = a[1:]

        # project into XY plane
        a = (a[0], a[1], 0)

        # Calculate the tilt axis (2 marks)
        t = (a[1], -a[0], 0)

        # Normalise a
        a_norm = a / np.linalg.norm(a)

        # Find the angle φ between the up vector and the vector obtained from
        #   the accelerometer (2 marks)
        phi = np.arccos(np.clip(
            np.dot(a_norm, (0, 0, 1)),
            -1.0,
            1.0
        ))

        # Use the complementary filter to fuse the two signals (7 marks).
        qs_k = problem_1.iv_quaternion_product(
            problem_2.make_q(
                t,
                ((-alpha) * phi)
            ),
            qs_k
        )
        qs.append(qs_k)

    for k in range(len(dataset)):
        dataset[k]['est_yaw_q'] = qs[k]
        dataset[k]['est_yaw_rad'] = problem_1.ii_quaternion_to_radians(qs[k])
        dataset[k]['est_yaw_deg'] = tuple(
            np.rad2deg(dataset[k]['est_yaw_rad']))

    return dataset
