# Dimitrios Ioannidis
import numpy as np 

def rasterize(pts_2d: np.ndarray, plane_w: int, plane_h: int, res_w: int, res_h: int) -> np.ndarray:
    # Normalize points to range [0, 1]
    pts_2d_normalized = (pts_2d + np.array([[plane_w/2], [plane_h/2]])) / np.array([[plane_w], [plane_h]]) # Note: '/' does element-wise division

    # Cut off all points outside of the image plane using np.clip
    pts_2d_normalized = np.clip(pts_2d_normalized, 0, 1)

    # Scaling to the image resolution and rounding
    pts_rasterized = np.round(pts_2d_normalized * np.array([[res_w], [res_h]])).astype(int) # Note: '*' does element-wise multiplication

    return pts_rasterized





