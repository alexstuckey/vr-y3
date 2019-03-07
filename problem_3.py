import numpy as np
import problem_1
import problem_2


# Estimate orientation from the gyroscope (rotational rate) and accelerometer.
def dead_reckoning_gyroscope_accelerometer(alpha=0.001):
    # Initial orientation
    qs = [(1.0, 0.0, 0.0, 0.0)]

    dataset = [{'time': 0.0}] + problem_1.load_dataset()

    for row in dataset:
        if 'gyroscope.X' in row.keys():
            row['omega'] = np.array([row['gyroscope.X'],
                                     row['gyroscope.Y'],
                                     row['gyroscope.Z']
                                     ])
            row['a'] = np.array([row['accelerometer.X'],
                                 row['accelerometer.Y'],
                                 row['accelerometer.Z']
                                 ])

    for k in range(1, len(dataset)):
        delta_t = dataset[k]['time'] - dataset[k - 1]['time']

        qs_k = problem_1.iv_quaternion_product(
            qs[k - 1],
            problem_2.make_q(
                dataset[k]['omega'] / np.linalg.norm(dataset[k]['omega']),
                np.linalg.norm(dataset[k]['omega']) * delta_t
            )
        )

        # Transform acceleration measurements into the global frame (2 marks)
        a = dataset[k]['a']
        a = problem_1.iv_quaternion_product(
            problem_1.iv_quaternion_product(
                problem_1.iii_quaternion_inverse_rotation(qs_k),
                problem_1.i_radians_to_quaternions(*a)
            ),
            qs_k
        )

        # Calculate the tilt axis (2 marks)
        t = (a[3], 0, a[1])

        # Find the angle φ between the up vector and the vector obtained from
        #   the accelerometer (2 marks)
        a_radians = problem_1.ii_quaternion_to_radians(a)
        phi = np.arccos(np.clip(
            np.dot((a_radians / np.linalg.norm(a_radians)), (0, 1, 0)),
            -1.0,
            1.0
        ))

        # Use the complementary filter to fuse the two signals (7 marks).
        qs_k = problem_1.iv_quaternion_product(
            problem_2.make_q(
                t,
                ((-alpha) * phi)
            ),
            qs[k - 1]
        )

        qs.append(qs_k)

    for k in range(len(dataset)):
        dataset[k]['est_g_a_q'] = qs[k]
        dataset[k]['est_g_a_rad'] = problem_1.ii_quaternion_to_radians(qs[k])
        dataset[k]['est_g_a_deg'] = tuple(
            np.rad2deg(dataset[k]['est_g_a_rad']))

    return dataset
