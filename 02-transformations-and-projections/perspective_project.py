# Dimitrios Ioannidis
import numpy as np 
from transform import Transform

def lookat(eye: np.ndarray, up: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # x_c, y_c and z_c are the unit vectors of the camera's coordinate system

    # Ιφ eye, target, and up are column vectors, convert them to 1D arrays if necessary
    eye = eye.flatten()
    target = target.flatten()
    up = up.flatten()

    CK = target-eye # CK vector, where C is the camera's center (eye) and K is the target
    z_c = (CK) / np.linalg.norm(CK) # z_c = CK / |CK|
    v = up - np.dot(up, z_c) * z_c
    y_c = v / np.linalg.norm(v) # y_c = v / |v|
    x_c = np.cross(z_c, y_c) # x_c = z_c x y_c. We take z_c x y_c instead of y_c x z_c so that x points right.

    R = np.column_stack((x_c, y_c, z_c))
    t = eye

    return (R, t)

def perspective_project(pts: np.ndarray, focal: float, R: np.ndarray, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Initialize transform matrix to camera's coordinate system
    transform = Transform()
    
    # Homogeneous transform matrix
    transform.mat[:3,:3] = R.T
    transform.mat[:3, 3] = -R.T @ t 

    # Apply transform (rotation and translation to the camera's coordinate system)
    transformed_pts = transform.transform_pts(pts)

    # Initialize projected_pts
    projected_pts = np.zeros((2, transformed_pts.shape[1]))

    # Perspective projection
    for i in range(transformed_pts.shape[1]):
        # perspective projection coordinates -> x_q = f * x_c / z_c, y_q = f * y_c / z_c
        projected_pts[:, i] = focal * transformed_pts[:2, i] / transformed_pts[2, i] 

    # Get depths
    depths = transformed_pts[2, :]

    return projected_pts, depths

