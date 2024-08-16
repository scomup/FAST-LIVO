import numpy as np
from mathR.utilities.math_tools import *
from mathR.graph_optimization.graph_solver import *


xci = np.array([0.1, 0.3, 0.5, 0.1, 0.2, 0.3])
xwi = np.array([-0.1, 0.1, -0.2, -0.3, 0.1, 0.1])

xiw, dxiw_dxwi = pose_inv(xwi, calcJ=True)
xcw, _, dxcw_dxiw = pose_plus(xci, xiw, True)



dxcw_dxwi = dxcw_dxiw @ dxiw_dxwi
