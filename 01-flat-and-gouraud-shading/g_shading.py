import numpy as np
import matplotlib.pyplot as plt
import math
from vector_interp import vector_interp


def g_shading(img, vertices, vcolors):
    updated_img = img

    # Define the Intersection class
    # The class includes the x and y coordinates of the intersection, and the color of the intersection (in [R, G, B] format).
    # Additionally, the class includes the color of the vertex that the intersection corresponds to.
    class Intersection:
        def __init__(self, x, y, C):
            self.x = x
            self.y = y
            self.C = C

    # Define the Edge class
    # The class includes the coordinates of the lowest point (x_min, y_min) and the highest point (x_max, y_max) of the edge.
    # It also includes the inverse slope of the edge. Inverse slope is inf if the edge is horizontal, 0 if the edge is vertical.
    # Additionally, it includes the intersection of the edge with the current scanline.
    # Finally, ck_min and ck_max are the colors of the (xk_min, yk_min) and (xk_max, yk_max) vertices (in [R, G, B] format).
    class Edge:
        def __init__(self, yk_min, xk_min, yk_max, xk_max, inv_slope, ck_min, ck_max):
            self.yk_min = yk_min
            self.xk_min = xk_min
            self.yk_max = yk_max
            self.xk_max = xk_max
            self.inv_slope = inv_slope
            self.intersection = None
            self.ck_min = ck_min
            self.ck_max = ck_max


    # List of triangle edges. These are calculated in the next "for" loop.
    edges = []

    # triangle -> K = 3
    for k in range(3):
        # Get the current vertex and the next vertex (with wrapping)
        v1 = vertices[k]
        c1 = vcolors[k]
        v2 = vertices[(k+1)%3]
        c2 = vcolors[(k+1)%3]

        # Sort the vertices so that v1 is the top vertex (the one with the highest y)
        if v1[1] < v2[1]:
            v1, v2 = v2, v1
            c1, c2 = c2, c1

        # Calculate the inverse slope
        if v2[1] == v1[1]:
            inv_slope = float('inf')
        else:
            inv_slope = (v2[0] - v1[0]) / (v2[1] - v1[1])

        # Add the edge to the list
        edges.append(Edge(v2[1], v2[0], v1[1], v1[0], inv_slope, c2, c1))

    y_min = min(edge.yk_min for edge in edges)
    y_max = max(edge.yk_max for edge in edges)

    # Calculating active edges for y == y_min. If an edge is horizontal (edge.inv_slope == inf) then it is not considered an active edge. Stored in a list.
    active_edges = [edge for edge in edges if (y_min == edge.yk_min and not math.isinf(edge.inv_slope))] 

    # Calculating active intersections (energa oriaka shmeia). They are instances of Intersection. They are stored in a list. 
    # They are stored in a list.
    active_intersections = []
    for edge in active_edges:
        C = edge.ck_min # active intersection color 
        active_intersections.append(Intersection(edge.xk_min, edge.yk_min, C))
        edge.intersection = active_intersections[-1]    

    y = y_min

    while y >= y_min and y < y_max: # for y in range(y_min, y_max)
        active_intersections_sorted = sorted(active_intersections, key=lambda x: x.x) # sort active vertices by x (their first element)

        # Iterate for all Xs on the scanline
        for x in np.arange(active_intersections_sorted[0].x, active_intersections_sorted[-1].x):
            if x >= math.floor(active_intersections_sorted[0].x):
                # Interpolate over x to get the color of the pixel at (y, x)
                color =  vector_interp((active_intersections_sorted[0].x, active_intersections_sorted[0].y), \
                                                    (active_intersections_sorted[-1].x, active_intersections_sorted[-1].y), \
                                                    active_intersections_sorted[0].C, active_intersections_sorted[-1].C, x, dim=1) # active intersection color
                    
                # Set the pixel at (y, x) to the given color. 
                # Note that y comes before x because in image processing, the convention is to reference pixels as (height, width) or (row, column).
                updated_img[y, math.floor(x)] = color
            
        y += 1
        # Update active edges and intersections
        for edge in edges:
            if edge.inv_slope != float('inf'): # if the edge isn't horizontal
                if y == edge.yk_max: 
                    active_edges.remove(edge)
                    active_intersections.remove(edge.intersection) # remove the intersection that corresponds to the edge
                    edge.intersection.C = None
                    edge.intersection = None

                elif y == edge.yk_min:
                    active_edges.append(edge)
                    active_intersections.append(Intersection(edge.xk_min, edge.yk_min, edge.ck_min))
                    edge.intersection = active_intersections[-1]

                elif edge in active_edges:  
                    if edge.inv_slope != 0: # if the edge isn't vertical
                        edge.intersection.x += edge.inv_slope
                    edge.intersection.y += 1
                    # update active intersection color
                    if edge.yk_min == edge.yk_max:   # if edge is horizontal (yk_min == yk_max), interpolate over x. Else, interpolate over y.
                        C = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.ck_min, edge.ck_max, edge.intersection.x, dim = 1) # active intersection color
                    else:
                        C = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.ck_min, edge.ck_max, edge.intersection.y, dim = 2) # active intersection color
                    edge.intersection.C = C

    return updated_img







# --------------------------------------------------------------------------------------------------------------------------------------------

# TEST FOR GOURAUD SHADING
if __name__ == "__main__":
    
    # Define the dimensions of the image
    M = 100  # height
    N = 200  # width

    # Create a dummy image
    image = np.ones((M, N, 3))

    vertices = np.array([[10,20],[90,20], [190,50]])
    vcolors = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # Assign colors to the vertices in the image
    for vertex, color in zip(vertices, vcolors):
        image[vertex[1], vertex[0]] = color

    vertices2 = np.array([[10,20],[190,50], [90,95]])
    vcolors2 = np.array([[1,0,0],[0,0,1],[0,1,1]])
    # Assign colors to the vertices in the image
    for vertex, color in zip(vertices2, vcolors2):
        image[vertex[1], vertex[0]] = color

    vertices3 = np.array([[0,0],[90,20], [10,20]])
    vcolors3 = np.array([[1,1,0],[0,1,0],[1,0,0]])
    # Assign colors to the vertices in the image
    for vertex, color in zip(vertices3, vcolors3):
        image[vertex[1], vertex[0]] = color

    vertices4 = np.array([[190,50],[90,20], [199,0]])
    vcolors4 = np.array([[0,0,1],[0,1,0],[1,0.5,1]])
    # Assign colors to the vertices in the image
    for vertex, color in zip(vertices4, vcolors4):
        image[vertex[1], vertex[0]] = color

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 3)

    # Display the image before using g_shading in the first subplot
    axs[0,0].imshow(image)
    axs[0,0].set_title('Before g_shading')

    updated_img = g_shading(image, vertices, vcolors)
    # Display the image in the second subplot after drawing the first triangle with g_shading
    axs[0,1].imshow(updated_img)
    axs[0,1].set_title('After g_shading')

    updated_img = g_shading(updated_img, vertices2, vcolors2)
    # Display the image in the third subplot after drawing the second triangle with g_shading
    axs[0,2].imshow(updated_img)
    axs[0,2].set_title('After g_shading #2')

    updated_img = g_shading(updated_img, vertices3, vcolors3)
    # Display the image in the fourth subplot after drawing the third triangle with g_shading
    axs[1,0].imshow(updated_img)
    axs[1,0].set_title('After g_shading #3')

    updated_img = g_shading(updated_img, vertices4, vcolors4)
    # Display the image in the fifth subplot after drawing the fourth triangle with g_shading
    axs[1,1].imshow(updated_img)
    axs[1,1].set_title('After g_shading #4')

    # Display the figure with the subplots
    plt.show()



    