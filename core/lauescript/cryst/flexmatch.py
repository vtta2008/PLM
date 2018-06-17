"""
Created on Jan 21, 2014

@author: Jens Luebben

Experimental reimplementation of the match module.

WORK IN PROGRESS
"""

from random import randint

import numpy as np


class OldMatcher(object):
    def __call__(self, cloud1, cloud2, threshold=1, maxiter=None):
        """
        Matches two point clouds.
        'cloud1' and 'cloud2' are lists of numpy.arrays.
        The function tries to find the pairs of points
        in both sets that minimize the sum of their
        distances.
        'cloud1' has to be equally long as cluoud two or
        larger.
        'threshold' defines the average distance between
        the two sets that is accepted as solution.
        'maxiter' defines how often the algorithm should
        be called before the process is aborted.
        If 'maxiter' is 'None', the algorithm is never
        aborted.

        If no solution is found after 'maxiter' iterations,
        the function returns 'None'.

        The function returns a matchlist listing the indices
        of points in 'cloud2' matching the points in 'cloud1'
        and a transformation matrix that transforms
        'cloud2' to the coordinate system of 'cloud1'.
        """

        R_old = 0
        iteration = 0
        cloud1 = self.center(list(cloud1))
        cloud2 = self.center(list(cloud2))
        ref_cloud = list(cloud2)
        quatx = np.array([1, 0, 0, 0])
        while True:
            matchlist = self.map_clouds(cloud1, cloud2)
            quat, R = self.get_quaternion(cloud1, cloud2, matchlist)
            cloud2 = self.rotate_by_quaternion(cloud2, quat)
            quatx = self.multiply_quaternion(quatx, quat)
            if abs(R - R_old) < 0.00000000001:
                if self.accept(cloud1, cloud2, matchlist, threshold):
                    return [matchlist[:len(cloud2) + 1], self.get_rotation_matrix_from_quaternion(quatx)]
                elif iteration < maxiter or not maxiter:
                    iteration += 1
                    cloud2 = list(ref_cloud)
                    cloud2 = self.shake(cloud2)
                    R_old = 0
                    quatx = np.array([1, 0, 0, 0])

                else:
                    return None
            R_old = R

    def center(self, cloud):
        c = sum(cloud) / len(cloud)
        return [p - c for p in cloud]

    def multiply_quaternion(self, q1, q2):
        t0 = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
        t1 = q1[0] * q2[1] + q1[1] * q2[0] - q1[2] * q2[3] + q1[3] * q2[2]
        t2 = q1[0] * q2[2] + q1[1] * q2[3] + q1[2] * q2[0] - q1[3] * q2[1]
        t3 = q1[0] * q2[3] - q1[1] * q2[2] + q1[2] * q2[1] + q1[3] * q2[0]
        return np.array([t0, t1, t2, t3])

    def get_transformation(self, cloud1, cloud2, matchlist):
        cloud22 = [cloud2[i] for i in matchlist]
        p1 = cloud1[0]
        p2 = cloud1[-1]
        p3 = cloud1[len(cloud1) / 2]
        v1 = p2 - p1
        v1 /= np.linalg.norm(v1)
        v2 = np.cross(v1, p3 - p1)
        v2 /= np.linalg.norm(v2)
        v3 = np.cross(v1, v2)
        m1 = np.matrix([[v1[0], v2[0], v3[0]],
                        [v1[1], v2[1], v3[1]],
                        [v1[2], v2[2], v3[2]]])
        p1 = cloud22[0]
        p2 = cloud22[-1]
        p3 = cloud22[len(cloud22) / 2]
        v1 = p2 - p1
        v1 /= np.linalg.norm(v1)
        v2 = np.cross(v1, p3 - p1)
        v2 /= np.linalg.norm(v2)
        v3 = np.cross(v1, v2)
        m2 = np.matrix([[v1[0], v2[0], v3[0]],
                        [v1[1], v2[1], v3[1]],
                        [v1[2], v2[2], v3[2]]])
        return np.dot(m1.T, m2)


    def accept(self, cloud1, cloud2, matchlist, threshold):
        dist_list = []
        for i, coord1 in enumerate(cloud1):
            coord2 = cloud2[matchlist[i]]
            dist_list.append(abs(np.linalg.norm(coord1 - coord2)))
        if np.mean(dist_list) < threshold:
            return True
        else:
            return False


    def map_clouds(self, cloud1, cloud2):
        matchlist = []
        for coord1 in cloud1:
            best_dist = 999
            for i, coord2 in enumerate(cloud2):
                dist = abs(np.linalg.norm(coord1 - coord2))
                if dist < best_dist:
                    best_hit = i
                    best_dist = dist
            matchlist.append(best_hit)
        return matchlist

    def get_quaternion(self, lst1, lst2, matchlist):
        M = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        for i, coord1 in enumerate(lst1):
            x = np.matrix(np.outer(coord1, lst2[matchlist[i]]))
            M = M + x

        N11 = float(M[0][:, 0] + M[1][:, 1] + M[2][:, 2])
        N22 = float(M[0][:, 0] - M[1][:, 1] - M[2][:, 2])
        N33 = float(-M[0][:, 0] + M[1][:, 1] - M[2][:, 2])
        N44 = float(-M[0][:, 0] - M[1][:, 1] + M[2][:, 2])
        N12 = float(M[1][:, 2] - M[2][:, 1])
        N13 = float(M[2][:, 0] - M[0][:, 2])
        N14 = float(M[0][:, 1] - M[1][:, 0])
        N21 = float(N12)
        N23 = float(M[0][:, 1] + M[1][:, 0])
        N24 = float(M[2][:, 0] + M[0][:, 2])
        N31 = float(N13)
        N32 = float(N23)
        N34 = float(M[1][:, 2] + M[2][:, 1])
        N41 = float(N14)
        N42 = float(N24)
        N43 = float(N34)

        N = np.matrix([[N11, N12, N13, N14],
                       [N21, N22, N23, N24],
                       [N31, N32, N33, N34],
                       [N41, N42, N43, N44]])

        values, vectors = np.linalg.eig(N)
        w = list(values)
        mw = max(w)
        quat = vectors[:, w.index(mw)]
        quat = np.array(quat).reshape(-1, ).tolist()
        return quat, mw

    def rotate_by_quaternion(self, cloud, quat):
        rotmat = self.get_rotation_matrix_from_quaternion(quat)
        return self.rotate_by_matrix(list(cloud), rotmat)


    def rotate_by_matrix(self, cloud, rotmat):
        return [np.array(np.dot(coord, rotmat).tolist())[0] for coord in cloud]


    def get_rotation_matrix_from_quaternion(self, q):
        """
        Returns the rotation matrix equivalent of the given quaternion.

        This function is used by the get_refined_rotation() function.
        """
        R = np.matrix([[q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3],
                        2 * (q[1] * q[2] - q[0] * q[3]),
                        2 * (q[1] * q[3] + q[0] * q[2])],
                       [2 * (q[2] * q[1] + q[0] * q[3]),
                        q[0] * q[0] - q[1] * q[1] + q[2] * q[2] - q[3] * q[3],
                        2 * (q[2] * q[3] - q[0] * q[1])],
                       [2 * (q[3] * q[1] - q[0] * q[2]),
                        2 * (q[3] * q[2] + q[0] * q[1]),
                        q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]]])
        return R

    def shake(self, cloud):

        quat = np.array([randint(1, 10) / 10., randint(-10, 10) / 10., randint(-10, 10) / 10., randint(-10, 10) / 10.])
        quat /= np.linalg.norm(quat)
        rotmat = self.get_rotation_matrix_from_quaternion(quat)
        return self.rotate_by_matrix(list(cloud), rotmat)


class MatchingAlgorithm(object):
    """
    The default implementation of the matching algorithm.

    To make the class structure more flexible the PointMapper
    functionality is capsuled in a different class. This way
    Only every subclass can easily implement all available
    mapper without further subclassing.
    """

    def __init__(self):
        self.pointmapper = PointMapper()

    def __call__(self):
        pass


class ElementAwareAlgorithm(MatchingAlgorithm):
    """
    A matching algorithm for point clouds representing
    atoms where the atoms's elements are known.
    """
    pass


class Matcher(object):
    """
    An Interface class for matching two point clouds.
    The Interface analyses the available information
    and assembles the best algorithm accordingly.

    The class is some kind of Builder/Factory pattern
    implementation.
    """

    def __init__(self,
                 cloud1=None,
                 elements1=None,
                 cloud2=None,
                 elements2=None):
        self.algorithm = MatchingAlgorithm()


    def __call__(self):
        self.algorithm()


class PointMapper(object):
    """
    Algorithm for matching each point of cloud1 with it's closest
    neighbor in cloud2 in space.

    Every MatchingAlgorithm must register one class of the PointMapper
    hierachy.
    """

    def __call__(self, cloud1, cloud2):
        return None


class MaskedPointMapper(PointMapper):
    """
    Masks parts of the cartesian space for each point to improve speed
    for large point clouds.
    """
    pass


if __name__ == '__main__':
    def random_coord():

        return np.array([randint(1, 100), randint(1, 100), randint(1, 100)])

    no = 0
    wrong = 0
    tries = 1
    for _ in range(tries):
        sample_cloud = [random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(),
                        random_coord(), ]
        sample_cloud = center(sample_cloud)

        angle = 23. * np.pi / 180

        sample_rotmat = np.matrix([[np.cos(angle), -np.sin(angle), 0],
                                   [np.sin(angle), np.cos(angle), 0],
                                   [0, 0, 1]])

        rotated_cloud = rotate_by_matrix(sample_cloud, sample_rotmat)
        xx = match_point_clouds(sample_cloud, rotated_cloud, threshold=2)
        x = xx[0]
        print x
        print xx[1]

        if not x:
            no += 1
        if not x == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
            wrong += 1
    print 'No solutions:', no
    print 'wrong solution:', wrong
    print 'Cycles:', tries
    print 'Success:', (1 - float(wrong) / float(tries)) * 100, '%'
    print
    nc = rotate_by_matrix(rotated_cloud, xx[1])
    for i, c in enumerate(sample_cloud):
        print c, nc[i]






