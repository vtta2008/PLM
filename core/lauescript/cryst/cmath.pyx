"""
Created on Jul 22, 2014

@author: jens
"""

cpdef double norm3(v):
    return (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** .5

if __name__ == '__main__':
    print norm3([1, 0, 0])
