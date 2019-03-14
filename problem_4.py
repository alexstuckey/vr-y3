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

    # Reference from first magnetometer sample
    m_ref = (0.0, *dataset[1]['m'])
    q_ref = (1.0, 0.0, 0.0, 0.0)

    for k in range(1, len(dataset)):
        delta_t = dataset[k]['time'] - dataset[k - 1]['time']

        qs_k = dataset[k]['est_tilt_q']

        m_prime = (0.0, *dataset[k]['m'])
        m_prime = problem_1.iv_quaternion_product(
            problem_1.iii_quaternion_inverse_rotation(qs_k),
            problem_1.iv_quaternion_product(
                (0, *m_prime),
                qs_k
            )
        )
        m_ref = problem_1.iv_quaternion_product(
            problem_1.iii_quaternion_inverse_rotation(qs_k),
            problem_1.iv_quaternion_product(
                (0, *m_ref),
                qs_k,
            )
        )

        # Project into XY plane
        m_ref = (m_ref[0], m_ref[1], 0)
        m_prime = (m_prime[0], m_prime[1], 0)

        # Calculate thetas, to be used to find difference
        theta = math.atan2(m_prime[1], -m_prime[0])
        theta_r = math.atan2(m_ref[1], -m_ref[0])

        # Using (0,0,1) instead of (0,1,0) due to up-direction in data
        qs_k = problem_1.iv_quaternion_product(
            problem_2.make_q(
                (0, 0, 1),
                ((-alpha_yaw) * (theta - theta_r))
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
