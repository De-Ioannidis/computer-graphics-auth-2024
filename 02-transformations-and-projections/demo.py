# Dimitrios Ioannidis
import numpy as np
import matplotlib.pyplot as plt
from render_object import render_object
from transform import Transform


if __name__ == "__main__":
    # Load the data
    data = np.load('hw2.npy', allow_pickle=True)
    data_dict = data.item()
    # Extract data
    v_pos = data_dict['v_pos']
    v_clr = data_dict['v_clr']
    t_pos_idx = data_dict['t_pos_idx']
    eye = data_dict['eye']
    up = data_dict['up']
    target = data_dict['target']
    focal = data_dict['focal']
    plane_w = data_dict['plane_w']
    plane_h = data_dict['plane_h']
    res_w = data_dict['res_w']
    res_h = data_dict['res_h']
    theta_0 = data_dict['theta_0']
    rot_axis_0 = data_dict['rot_axis_0']
    t_0 = data_dict['t_0']
    t_1 = data_dict['t_1']

    # Render object before any rotation or translation
    image = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
    plt.figure("Before rotation or translation")
    plt.title("Before rotation or translation")
    plt.imshow(image)
    plt.imsave('assets/step_0.jpg', image)  # Save the image as a .jpg file

    # Rotate v_pos by theta_0 around rot_axis_0 and render object
    transform = Transform()
    transform.rotate(theta_0, rot_axis_0)
    v_pos = transform.transform_pts(v_pos)
    image = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
    plt.figure("After rotation")
    plt.title("After rotation")
    plt.imshow(image)
    plt.imsave('assets/step_1.jpg', image)  # Save the image as a .jpg file

    # Translate v_pos by t_0 and render object
    transform = Transform()
    transform.translate(t_0)
    v_pos = transform.transform_pts(v_pos)
    image = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
    plt.figure("After first translation")
    plt.title("After first translation")
    plt.imshow(image)
    plt.imsave('assets/step_2.jpg', image)  # Save the image as a .jpg file

    # Translate v_pos by t_1 and render object
    transform.translate(t_1)
    v_pos = transform.transform_pts(v_pos)
    image = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
    plt.figure("After second translation")
    plt.title("After second translation")
    plt.imshow(image)
    plt.imsave('assets/step_3.jpg', image)  # Save the image as a .jpg file

    # Show all figures
    plt.show()

