import numpy as np
from mathR.utilities.math_tools import *

def rot_plus(x1, x2):
    R1 = expSO3(x1)
    R2 = expSO3(x2)
    return logSO3(R1 @ R2)


def rot_minus(x1, x2):
    R1 = expSO3(x1)
    R2 = expSO3(x2)
    return logSO3(R2.transpose() @ R1)


def get_Rcw(rwi, rci, calcJ=False):
    Rwi = expSO3(rwi)
    Rci = expSO3(rci)
    rcw = logSO3(Rci @ Rwi.transpose())
    if (calcJ is True):
        return rcw, -Rwi
    else:
        return rcw


def get_tcw(rwi, twi, rci, tci, calcJ=False):
    Rwi = expSO3(rwi)
    Rci = expSO3(rci)
    tcw = -Rci @ Rwi.transpose() @ twi + tci
    if (calcJ is True):
        drwi = -Rci @ skew(Rwi.transpose() @ twi)
        dtwi = -Rci @ Rwi.transpose()
        return tcw, drwi, dtwi
    else:
        return tcw


def get_pc(rcw, tcw, pw, calcJ=False):
    Rcw = expSO3(rcw)
    pc = Rcw @ pw + tcw
    if (calcJ is True):
        drcw = Rcw @ skew(-pw)
        dtcw = np.eye(3)
        return pc, drcw, dtcw
    else:
        return pc


def project(pc, K, calcJ=False):
    fx = K[0, 0]
    fy = K[1, 1]
    cx = K[0, 2]
    cy = K[1, 2]
    x, y, z = pc
    z_2 = z * z
    r = np.array([(x * fx / z + cx),
                  (y * fy / z + cy)])
    if (calcJ is True):
        J = np.array([[fx / z,    0, -fx * x / z_2],
                      [0, fy / z, -fy * y / z_2]])
        return r, J
    else:
        return r


def get_u(rwi, twi, rci, tci, pw, K, calcJ=False):
    rcw, drcw_drwi = get_Rcw(rwi, rci, True)
    tcw, dtcw_drwi, dtcw_dtwi = get_tcw(rwi, twi, rci, tci, True)
    pc, dpc_drcw, dpc_dtcw = get_pc(rcw, tcw, pw, True)
    u, du_dpc = project(pc, K, True)
    if (calcJ is True):
        dpc_drwi = du_dpc @ dpc_drcw @ drcw_drwi + \
                   du_dpc @ dpc_dtcw @ dtcw_drwi
        dpc_dtwi = du_dpc @ dpc_dtcw @ dtcw_dtwi
        return u, dpc_drwi, dpc_dtwi
    else:
        return u
    

if __name__ == '__main__':

    fx = 400.
    fy = 300.
    cx = 200.
    cy = 100.
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1.]])

    rci = np.array([0.1, 0.2, 0.3])
    tci = np.array([0.1, 0.3, 0.5])
    rwi = np.array([-0.3, 0.1, 0.1])
    twi = np.array([-0.1, 0.1, -0.2])

    pw = np.array([-3, 1, 2.])

    dRcw_drwi_n = numericalDerivative(get_Rcw, [rwi, rci], 0, rot_plus, rot_minus)
    rcw, dRcw_drwi = get_Rcw(rwi, rci, True)
    print("%s check dRcw_drwi" % check(dRcw_drwi_n, dRcw_drwi))

    dtcw_drwi_n = numericalDerivative(get_tcw, [rwi, twi, rci, tci], 0, rot_plus)
    dtcw_dtwi_n = numericalDerivative(get_tcw, [rwi, twi, rci, tci], 1)
    tcw, dtcw_drwi, dtcw_dtwi = get_tcw(rwi, twi, rci, tci, True)
    print("%s check dtcw_drwi" % check(dtcw_drwi_n, dtcw_drwi))
    print("%s check dtcw_dtwi" % check(dtcw_dtwi_n, dtcw_dtwi))

    pc, dpc_drcw, dpc_dtcw = get_pc(rcw, tcw, pw, True)
    dpc_drcw_n = numericalDerivative(get_pc, [rcw, tcw, pw], 0, rot_plus)
    dpc_dtcw_n = numericalDerivative(get_pc, [rcw, tcw, pw], 1)
    print("%s check dpc_drcw" % check(dpc_drcw_n, dpc_drcw))
    print("%s check dpc_dtcw" % check(dpc_dtcw_n, dpc_dtcw))

    pc, dpc_drwi, dpc_dtwi = get_u(rwi, twi, rci, tci, pw, K, True)
    dpc_drwi_n = numericalDerivative(get_u, [rwi, twi, rci, tci, pw, K], 0, rot_plus, delta=1e-8)
    dpc_dtwi_n = numericalDerivative(get_u, [rwi, twi, rci, tci, pw, K], 1, delta=1e-8)
    print("%s check du_drwi" % check(dpc_drwi_n, dpc_drwi))
    print("%s check du_dtwi" % check(dpc_dtwi_n, dpc_dtwi))

