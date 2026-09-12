# Dimitrios Ioannidis
from shading import *
from lookat import lookat
from perspective_project import perspective_project
from rasterize import rasterize
import numpy as np 

def render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target) -> np.ndarray:
    # Getting the rotation matrix and trasposition vector  
    R, t = lookat(eye, up, target)

    # Projecting the transformed vertices onto the image plane
    v_pos_proj, depths = perspective_project(v_pos, focal, R, t)

    # Converting the projected vertices to pixel coordinates
    v_pos_pix = rasterize(v_pos_proj, plane_w, plane_h, res_w, res_h).T # Transposing the output of rasterize to accomodate the format render_img expects

    # Using the render_img function with the Gouraud shading option to render the image
    image = render_img(t_pos_idx, v_pos_pix, v_clr, depths, shading='g')

    return image

