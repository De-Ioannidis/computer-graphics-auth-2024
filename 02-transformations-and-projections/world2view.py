# Dimitrios Ioannidis
import numpy as np

def world2view(pts: np.ndarray, R: np.ndarray, c0: np.ndarray) -> np.ndarray:
    # pts: 3xN (N points)
    N = np.shape(pts)[1]

    # pts_c: pts in the camera's coordinate system
    pts_c = np.zeros(pts.shape)

    # Apply the transformation to each point
    for i in range(N):
        pts_c[:, i] = R.T @ (pts[:, i] - c0)

    return pts_c

