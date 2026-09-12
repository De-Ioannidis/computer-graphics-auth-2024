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
    
    # Call render_img with Flat Shading option
    image_f = render_img(faces, vertices, vcolors, depth, "f")

    # Create a new figure
    plt.figure()

    # Display the image
    plt.imshow(image_f)

    # Set the title
    plt.title('Flat Shading')

    # Save the figure
    plt.savefig('assets/flat-shading-output.png')

    # Show the figure
    plt.show()