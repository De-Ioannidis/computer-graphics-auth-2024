import numpy as np
import matplotlib.pyplot as plt
from render_img import render_img


if __name__ == "__main__":
    # Load the data
    data = np.load('hw1.npy', allow_pickle=True)
    data_dict = data.item()

    # Extract vertices, vertex colors, faces, and depth
    vertices = data_dict['vertices']
    vcolors = data_dict['vcolors']
    faces = data_dict['faces']
    depth = data_dict['depth']

    # Call render_img with Gouraud Shading option
    image_f = render_img(faces, vertices, vcolors, depth, "g")

    # Create a new figure
    plt.figure()

    # Display the image
    plt.imshow(image_f)

    # Set the title
    plt.title('Gouraud Shading')

    # Save the figure
    plt.savefig('assets/gouraud-shading-output.png')

    # Show the figure
    plt.show()