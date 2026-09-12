import numpy as np
import matplotlib.pyplot as plt
from f_shading import f_shading
from g_shading import g_shading


# --------------------------------------------------------------------------------------------------------------------------------------------
def render_img(faces, vertices, vcolors, depth, shading):
    # Define the dimensions of the image
    M = 512  # height
    N = 512  # width

    # White background
    image = np.ones((M, N, 3))
    
    # Get the depth of each vertex in each face
    face_depths = depth[faces]

    # Calculate the mean depth for each face
    mean_depths = np.mean(face_depths, axis=1)

    # Get the indices that would sort the mean depths in descending order
    sorted_indices = np.argsort(mean_depths)[::-1]

    # Loop through the faces in descending order of depth
    for i in sorted_indices:
        face = faces[i]
        face_vertices = vertices[face]
        face_colors = vcolors[face]

        # Call the shading function
        if shading == "f":
            image = f_shading(image, face_vertices, face_colors)
        elif shading == "g":
            image = g_shading(image, face_vertices, face_colors)
        else:
            raise ValueError("Invalid shading type. Choose either 'f' or 'g'.")
    
    return image




# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------

# TEST FOR RENDER_IMG
if __name__ == "__main__":
    # Load the data
    data = np.load('hw1.npy', allow_pickle=True)
    data_dict = data.item()

    # Extract vertices, vertex colors, faces, and depth
    vertices = data_dict['vertices']
    vcolors = data_dict['vcolors']
    faces = data_dict['faces']
    depth = data_dict['depth']

    image_f = render_img(faces, vertices, vcolors, depth, "f")
    image_g = render_img(faces, vertices, vcolors, depth, "g")

    fig, axs = plt.subplots(1, 2)

    axs[0].imshow(image_f)
    axs[0].set_title('Flat shading')

    axs[1].imshow(image_g)
    axs[1].set_title('Gouraud shading')

    # plt.savefig('render_TEST.png')
    plt.show()

    vcolors = data_dict['vcolors']
    faces = data_dict['faces']
    depth = data_dict['depth']

    image_f = render_img(faces, vertices, vcolors, depth, "f")
    image_g = render_img(faces, vertices, vcolors, depth, "g")

    fig, axs = plt.subplots(1, 2)

    axs[0].imshow(image_f)
    axs[0].set_title('Flat shading')

    axs[1].imshow(image_g)
    axs[1].set_title('Gouraud shading')

    # plt.savefig('render_TEST.png')
    plt.show()
