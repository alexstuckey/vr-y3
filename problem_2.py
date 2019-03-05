import math
import numpy as np
import problem_1


def norm_3(q):
    return math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2])


def norm(v):
    if len(v) > 0:
        normalised_v = v / np.sqrt(np.sum(v**2))
        return normalised_v
    else:
        return []


def make_q(v, theta):
    q = (math.cos(theta / 2),
         v[0] * math.sin(theta / 2),
         v[1] * math.sin(theta / 2),
         v[2] * math.sin(theta / 2))
    return q

# Estimate orientation from the gyroscope (rotational rate).
# Calculate current position by using a previously determined
# position (starting at the identity quaternion) and advancing that
# position based upon an estimated speed over the elapsed time).
# Implement the filter to estimate position by only integrating the gyroscope.
# Consider the initial orientation q[0] to be the identity quaternion [1,0,0,0]


def dead_reckoning_gyroscope():
    # Initial orientation
    qs = [(1.0, 0.0, 0.0, 0.0)]

    dataset = [{'time': 0.0}] + problem_1.load_dataset()

    for row in dataset:
        if 'gyroscope.X' in row.keys():
            row['omega'] = np.array([row['gyroscope.X'],
                                     row['gyroscope.Y'],
                                     row['gyroscope.Z']
                                     ])

    for k in range(1, len(dataset)):
        delta_t = dataset[k]['time'] - dataset[k - 1]['time']

        qs_k = problem_1.iv_quaternion_product(
            qs[k - 1],
            make_q(dataset[k]['omega'] / norm_3(dataset[k]['omega']),
                   norm_3(dataset[k]['omega']) * delta_t)
        )
        qs.append(qs_k)

    for k in range(len(dataset)):
        dataset[k]['est_gyro'] = qs[k]

    return dataset
