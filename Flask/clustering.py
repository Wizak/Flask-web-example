import random
import numpy as np
import matplotlib.pyplot as plt


def avaragek(count_clasters=2, count_points=1000, random_num=[0, 1]):
    def distance(point_x, point_y):
        return np.sqrt((point_x[0] - point_y[0])**2 + (point_x[1] - point_y[1])**2)

    def avarage(clasters):
        return [[sum([p[0] for p in c])/len(c), sum([p[1] for p in c])/len(c)] for c in clasters]

    points = [[random.uniform(*random_num), random.uniform(*random_num)] for _ in range(count_points)]
    centers = [random.choice(points) for _ in range(count_clasters)]
    distance_points = [[distance(p, c) for p in points] for c in centers]

    clasters = [[c] for c in centers]
    for p in range(len(points)):
        m_d = [distance_points[i][p] for i in range(len(centers))]
        minimum_distance = min(m_d)
        minimum_distance_i = m_d.index(minimum_distance)
        clasters[minimum_distance_i].append(points[p])

    for _ in range(100):
        new_centers = avarage(clasters)
        distance_points = [[distance(p, c) for p in points]
                           for c in new_centers]

        clasters = [[c] for c in new_centers]
        for p in range(len(points)):
            m_d = [distance_points[i][p] for i in range(len(centers))]
            minimum_distance = min(m_d)
            minimum_distance_i = m_d.index(minimum_distance)
            clasters[minimum_distance_i].append(points[p])

    cl_x = [[x[0] for x in cl] for cl in clasters]
    cl_y = [[y[1] for y in cl] for cl in clasters]
    nc_x = [c[0] for c in new_centers]
    nc_y = [c[1] for c in new_centers]

    return cl_x, cl_y, nc_x, nc_y, new_centers