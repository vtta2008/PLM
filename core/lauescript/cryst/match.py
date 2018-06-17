"""
Created on Jan 21, 2014

@author: Jens Luebben

Module implementing an Iterative Closest Point (IPC) algorithm
for registering 3D shapes.

Based on the work of Paul J. Besl:
(IEEE Transactions on Pattern Analysis and Machine Intelligence,
 14(2), 239 - 256, 1992.)
"""

from random import randint

import numpy as np

bestFit = None

def match_point_clouds(cloud1, cloud2, threshold=1, maxiter=0):
    """
    Matches two point clouds.
    'cloud1' and 'cloud2' are lists of numpy.arrays.
    The function tries to find the pairs of points
    in both sets that minimize the sum of their
    distances.

    :param cloud1: has to be equally long as cloud two or
    larger.
    :param cloud2: List of numpy arrays. Each array must be
    of length three.
    :param threshold: defines the average distance between
    the two sets that is accepted as solution.
    :param maxiter: Integer defining how often the algorithm should
    be called before the process is aborted.
    :param maxiter: Boolean: if  maxiter is 'None', the algorithm is never
    aborted.

    :return:If no solution is found after 'maxiter' iterations,
    the function returns 'None'. The function returns a matchlist
    listing the indices of points in 'cloud2' matching the points
    in 'cloud1' and a transformation matrix that transforms
    'cloud2' to the coordinate system of 'cloud1'.
    """

    R_old = 0
    iteration = 0
    cloud1 = center(list(cloud1))
    cloud2 = center(list(cloud2))
    ref_cloud = list(cloud2)
    quatx = np.array([1, 0, 0, 0])
    while True:
        matchlist = map_clouds(cloud1, cloud2)
        quat, R = get_quaternion(cloud1, cloud2, matchlist)
        cloud2 = rotate_by_quaternion(cloud2, quat)
        quatx = multiply_quaternion(quatx, quat)
        if abs(R - R_old) < 0.00000000001:
            if accept(cloud1, cloud2, matchlist, threshold):
                return [matchlist[:len(cloud2) + 1], get_rotation_matrix_from_quaternion(quatx)]
            elif iteration < maxiter or not maxiter:
                iteration += 1
                cloud2 = list(ref_cloud)
                cloud2, quatx = shake(cloud2)
                # R_old = 0
                # ===============================================================
                # quatx=np.array([1,0,0,0])
                #===============================================================

            else:
                return None
        R_old = R


def center(cloud):
    """
    Moves the center of 'cloud' to its center of mass.

    :param cloud: List of numpy arrays.

    :return: List of numpy arrays representing 'cloud' moved to its center of mass.
    """
    c = sum(cloud) / len(cloud)
    # ===========================================================================
    # print c
    #===========================================================================
    return [p - c for p in cloud]


def multiply_quaternion(q1, q2):
    """
    Multiplies two quaternions and returns the result.

    :param q1: Numpy array of length 4 representing a quaternion.
    :param q2: Numpy array of length 4 representing a quaternion.

    :return: Numpy of length 4 representing the quaternion product of q1 and q2.
    """
    t0 = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
    t1 = q1[0] * q2[1] + q1[1] * q2[0] - q1[2] * q2[3] + q1[3] * q2[2]
    t2 = q1[0] * q2[2] + q1[1] * q2[3] + q1[2] * q2[0] - q1[3] * q2[1]
    t3 = q1[0] * q2[3] - q1[1] * q2[2] + q1[2] * q2[1] + q1[3] * q2[0]
    return np.array([t0, t1, t2, t3])


def get_transformation(cloud1, cloud2, matchlist):
    """
    Returns the transformation matrix that transforms
    'cloud1' to 'cloud2'. 'matchlist' is a list of
    integers where the first element represents the
    index of the point corresponding to the first
    point in 'cloud1' in 'cloud2'.

    DEPRECATED
    :param cloud1: ...
    :param cloud2: ...
    :param matchlist: ...
    """
    print('Please don\'t use me. I am an innocent function in the \'match\' module and I am only kept alive because'\
          'someone else might still be using me.')
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

def get_best_fit():
    return bestFit


def accept(cloud1, cloud2, matchlist, threshold):
    """
    Returns 'True' if the average distance between all
    points is below the 'threshold'.

    :param cloud1: List of numpy arrays.
    :param cloud2: List of numpy arrays.
    :param matchlist: List of integers specifying which elements of
    cloud2 match the elements in cloud1.
    :param threshold: Float representing the maximum average distance
    of all matched points that is acceptable as a solution.

    :return: True/False depending on whether the solution is accepted.
    """
    dist_list = []
    for i, coord1 in enumerate(cloud1):
        coord2 = cloud2[matchlist[i]]
        dist_list.append(abs(np.linalg.norm(coord1 - coord2)))
    # print np.mean(dist_list)
    m = np.mean(dist_list)
    if m < threshold:
        global bestFit
        bestFit = m
        return True
    else:
        # =======================================================================
        # print np.mean(dist_list)
        #=======================================================================
        return False


def map_clouds(cloud1, cloud2):
    """
    Returns a list which holds for every point in 'cloud1'
    an integer representing the list index in 'cloud2' that
    has the shortest distance to the point in 'cloud1'.
    The returned list has the same length as 'cloud1'.
    """
    matchlist = []
    best_hit = None
    for coord1 in cloud1:
        best_dist = 999
        for i, coord2 in enumerate(cloud2):
            dist = abs(np.linalg.norm(coord1 - coord2))
            if dist < best_dist:
                best_hit = i
                best_dist = dist
        matchlist.append(best_hit)
    return matchlist


def get_quaternion(lst1, lst2, matchlist):
    """
    Returns the quaternion representing the best possible
    transformation to minimize the distance between all
    points in 'cloud1' and 'cloud2'.
    The second return value is the fitting criteria
    representing how well both clouds match.
    (the larger the value the better.)
    """
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


def rotate_by_quaternion(cloud, quat):
    """
    Rotations the points in 'cloud' with the
    transformation represented by the quaternion
    'quat'.
    """
    rotmat = get_rotation_matrix_from_quaternion(quat)
    return rotate_by_matrix(list(cloud), rotmat)


def rotate_by_matrix(cloud, rotmat):
    """
    Rotates the points in 'cloud' by the transformation represented
    by the rotation matrix 'rotmat'.
    """
    return [np.array(np.dot(coord, rotmat).tolist())[0] for coord in cloud]


def get_rotation_matrix_from_quaternion(q):
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


def shake(cloud):
    """
    Randomly roates the points in 'cloud' two (hopefully) avoid
    a local minimum.
    The rotated cloud is returned as well as the quaternion representing
    the transformation.
    """
    quat = np.array([randint(1, 10) / 10., randint(-10, 10) / 10., randint(-10, 10) / 10., randint(-10, 10) / 10.])
    quat /= np.linalg.norm(quat)
    rotmat = get_rotation_matrix_from_quaternion(quat)
    return rotate_by_matrix(list(cloud), rotmat), quat


def get_transform(points1, points2, matchlist=None, use=3, matrix=False):
    """
    Returns the Quaternion/Matrix representation of
    of the transformation that transforms the points in
    'points1' to the coordinate system of 'points2'.

    The first three points in each list are used by default.
    It is assumed that the first point in list 1 matches
    the first point in list 2 and so forth...
    This behavior can be modified by using the 'matchlist'
    option that must be a list of integers specifying
    which points to map. 'matchlist=[2,1,0]' implies that
    the first element of 'points1' is mapped to the third
    element of 'points2' and so forth.

    The optional argument 'use' determines how many elements
    of the point lists should be used to determine the
    transformation. The default is three. A value of '0'
    implies the use of all elements.

    The boolean 'matrix' determines whether the
    transformation is returned in quaternion
    representation or in matrix representation.
    """
    if use == 0:
        use = len(points1)
    lst1 = points1[:use]
    lst2 = points2[:use]
    if not matchlist:
        matchlist = range(use)
    quat, _ = get_quaternion(lst1, lst2, matchlist)
    if not matrix:
        return quat
    else:
        return get_rotation_matrix_from_quaternion(quat)


def test():
    import time

    start = time.time()

    def test_match_clouds():
        """
        Function for testing the functionality of the module.
        """

        def random_coord():

            return np.array([randint(1, 100), randint(1, 100), randint(1, 100)])

        no = 0
        wrong = 0
        tries = 500
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
            # ===================================================================
            # print x
            # print xx[1]
            #===================================================================

            if not x:
                no += 1
            if not x == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
                wrong += 1
        print('No solutions:', no)
        print('wrong solution:', wrong)
        print('Cycles:', tries)
        print('Success:', (1 - float(wrong) / float(tries)) * 100, '%')
        # =======================================================================
        # print
        # nc= rotate_by_matrix(rotated_cloud,xx[1])
        # for i,c in enumerate(sample_cloud):
        #     print c,nc[i]
        #=======================================================================

        # ===============================================================================

    #     def test_get_transform():
    #         lst1=[np.array([0,0,0]),
    #               np.array([0,1,0]),
    #               np.array([0,0,1])]
    #         lst2=[np.array([0,0,0]),
    #               np.array([0,-1,0]),
    #               np.array([0,0,-1])]
    #         print get_transform(lst1,lst2)
    #         print get_transform(lst1,lst2,True)
    #         print np.dot(lst1,get_transform(lst1,lst2,True))
    #
    #     test_get_transform()
    #===============================================================================
    test_match_clouds()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    test()





