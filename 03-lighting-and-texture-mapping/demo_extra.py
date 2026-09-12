# Dimitrios Ioannidis
import numpy as np
from texture_map import *
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    ## ---- Loading Data ---- ##
    data = np.load('h3.npy', allow_pickle=True)
    data_dict = data.item()

    verts = data_dict['verts']
    vertex_colors = data_dict['vertex_colors']
    face_indices = data_dict['face_indices']
    uvs = data_dict['uvs']
    face_uv_indices = data_dict['face_uv_indices']
    cam_eye = data_dict['cam_eye']
    cam_up = data_dict['cam_up']
    cam_lookat = data_dict['cam_lookat']
    ka = data_dict['ka']
    kd = data_dict['kd']
    ks = data_dict['ks']
    n = data_dict['n']
    light_positions = data_dict['light_positions']
    light_intensities = data_dict['light_intensities']
    Ia = data_dict['Ia']
    M = data_dict['M']
    N = data_dict['N']
    W = data_dict['W']
    H = data_dict['H']
    bg_color = data_dict['bg_color']
    focal = data_dict['focal']

    # Ensure the output image directory exists
    os.makedirs('assets/with_texture_map', exist_ok=True)

    # Loading Texture Map
    texture_map = plt.imread('cat_diff.png')

    # ---- Rendering with only ambient light ---- ##
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, 0, 0, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, 0, 0, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_ambient_only.png', image_g)
    plt.imsave('assets/with_texture_map/phong_ambient_only.png', image_p)
    fig, axs = plt.subplots(1,2)
    fig.suptitle(f'Ambient Light Only')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    # ---- Rendering with only diffuse light ---- ##
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, 0, kd, 0, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, 0, kd, 0, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_diffuse_only.png', image_g)
    plt.imsave('assets/with_texture_map/phong_diffuse_only.png', image_p)
    fig, axs = plt.subplots(1,2)
    fig.suptitle(f'Diffuse Light Only')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    # ---- Rendering with only specular light ---- ##
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, 0, 0, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, 0, 0, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_specular_only.png', image_g)
    plt.imsave('assets/with_texture_map/phong_specular_only.png', image_p)
    fig, axs = plt.subplots(1,2)
    fig.suptitle(f'Specular Light Only')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    # ---- Rendering with all light components ---- ##
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_all_components.png', image_g)
    plt.imsave('assets/with_texture_map/phong_all_components.png', image_p)
    fig, axs = plt.subplots(1,2)
    fig.suptitle(f'All Lighting Components')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    # ---- Rendering with the first light source only ---- ##
    l_pos = light_positions[0]
    l_int = light_intensities[0]
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)

    plt.imsave('assets/with_texture_map/gouraud_light_first.png', image_g)
    plt.imsave('assets/with_texture_map/phong_light_first.png', image_p)

    fig, axs = plt.subplots(1, 2)
    fig.suptitle(f'Light Position: {l_pos}, Light Intensity: {l_int}')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')
  
    ## ---- Rendering with the second light source only ---- ##
    l_pos = light_positions[1]
    l_int = light_intensities[1]

    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_light_second.png', image_g)
    plt.imsave('assets/with_texture_map/phong_light_second.png', image_p)

    fig, axs = plt.subplots(1, 2)
    fig.suptitle(f'Light Position: {l_pos}, Light Intensity: {l_int}')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')


    ## ---- Rendering with the third light source only ---- ##
    l_pos = light_positions[2]
    l_int = light_intensities[2]

    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, l_pos, l_int, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_light_third.png', image_g)
    plt.imsave('assets/with_texture_map/phong_light_third.png', image_p)

    fig, axs = plt.subplots(1, 2)
    fig.suptitle(f'Light Position: {l_pos}, Light Intensity: {l_int}')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    ## -- Rendering with all light sources -- ##
    image_g = render_object_with_texture_map("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    image_p = render_object_with_texture_map("phong", focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia, uvs, face_uv_indices, texture_map)
    plt.imsave('assets/with_texture_map/gouraud_all_lights.png', image_g)
    plt.imsave('assets/with_texture_map/phong_all_lights.png', image_p)
    
    fig, axs = plt.subplots(1, 2)
    fig.suptitle('All light sources')

    axs[0].imshow(image_g)
    axs[0].set_title('Gouraud shading')

    axs[1].imshow(image_p)
    axs[1].set_title('Phong shading')

    plt.show()

