# Dimitrios Ioannidis
import numpy as np 


class Transform:
    def __init__(self):
        self.mat = np.eye(4) # transformation matrix

    def rotate(self, theta: float, u: np.ndarray) -> None:
        # compute the cosine and sine of the angle
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        # compute the rotation matrix
        R = np.array([
            [(1 - cos_theta)*u[0]**2 + cos_theta , (1 - cos_theta) * u[0] * u[1] - sin_theta * u[2], (1 - cos_theta) * u[0] * u[2] + sin_theta * u[1]],
            [(1 - cos_theta) * u[1] * u[0] + sin_theta * u[2], (1 - cos_theta) * u[1]**2 + cos_theta, (1 - cos_theta)*u[1] * u[2] - sin_theta * u[0]],
            [(1 - cos_theta) * u[2] * u[0] - sin_theta * u[1], (1 - cos_theta) * u[2] * u[1] + sin_theta * u[0], (1 - cos_theta) * u[2]**2 +  cos_theta]])

        self.mat[0:3, 0:3] = R # update the transformation matrix with the rotation matrix R

    def translate(self, t: np.ndarray) -> None:
        self.mat[0:3, 3] = t # update the transformation matrix with the translation vector t

    def transform_pts(self, pts: np.ndarray) -> np.ndarray:
        N = pts.shape[1] # pts -> 3xN matrix of points (N points)
        pts_homogeneous = np.concatenate([pts, np.ones((1, N))], axis=0) # points in homogeneous coordinates
        transformed_pts = self.mat @ pts_homogeneous # Transform(homogeneous) * pts_homogeneous
        return transformed_pts[:3, :] # keeping first 3 rows (reverting back from homogeneous coordinates)
    

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
