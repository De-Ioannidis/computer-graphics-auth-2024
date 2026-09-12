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
