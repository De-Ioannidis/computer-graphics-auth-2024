# Dimitrios Ioannidis
import numpy as np

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

