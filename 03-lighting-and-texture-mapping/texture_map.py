# Dimitrios Ioannidis
import numpy as np
from shading import calculate_normals, shade_gouraud
from perspective_project import perspective_project
from perspective_project import lookat as lookat_func
from rasterize import rasterize
from lighting import light
from g_shading import vector_interp
import math

def bilerp(uv, texture_map):
    h, w, _ = texture_map.shape
    u, v = uv
    u = u * (w - 1)
    v = v * (h - 1)
    
    x0 = int(np.floor(u))
    x1 = min(x0 + 1, w - 1)
    y0 = int(np.floor(v))
    y1 = min(y0 + 1, h - 1)

    # Fetch the four neighboring pixels
    top_left = texture_map[y0, x0]
    top_right = texture_map[y0, x1]
    bottom_left = texture_map[y1, x0]
    bottom_right = texture_map[y1, x1]

    # Perform the bilinear interpolation
    color = top_left / 4 + top_right / 4 + bottom_left / 4 + bottom_right / 4

    return color


def render_object_with_texture_map(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, faces, ka, kd, ks, n, l_pos, l_int, l_amb, uvs, face_uv_indices, texture_map):
    # Calculate the normal vectors of the vertices
    normals = calculate_normals(verts, faces)

    # Compute the rotation matrix and translation vector for the camera
    R, t = lookat_func(eye, up, lookat)

    # Project the vertices to the camera's frame
    projected_verts, depths = perspective_project(verts, focal, R, t)
    
    # Rasterize the projected vertices
    rasterized_verts = rasterize(projected_verts, W, H, M, N)

    # Initialize the image to the background color
    img = np.tile(bg_color[np.newaxis, np.newaxis, :], (M, N, 1))
    
    # For each face, sorted by depth
    for i in sorted(range(faces.shape[1]), key=lambda i: -np.mean(depths[faces[:, i]])):
        # Vertices of the face
        verts_3D = verts[:, faces[:, i]]

        # The projected and rasterized vertices of the face
        vertsp = rasterized_verts[:, faces[:, i]]

        # Center of gravity of the face
        bcoords = np.mean(verts_3D, axis=1)
        
        # UV coordinates of the vertices
        uv_coords = uvs[:, face_uv_indices[:, i]]

        # Normals of the vertices
        vertsn = normals[:, faces[:, i]]
        cam_pos = eye

        # Shading face 
        if shader == 'gouraud':
            # Colors of the vertices from texture map - computed in advance in the case of gouraud shading.
            # In the case of Phong shading, first we will interpolate the UV coordinates and then we will use them to fetch the colors from the texture map.
            vertsc = np.array([bilerp(uv, texture_map) for uv in uv_coords.T]).T
            img = shade_gouraud(vertsp, vertsn, vertsc, bcoords, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb, img)
        elif shader == 'phong':
            img = shade_phong_with_texture_map(vertsp, vertsn, uv_coords, bcoords, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb, img, texture_map)
        
    # Clipping color values to [0, 1]
    img = np.clip(img, 0, 1)

    return img

def shade_phong_with_texture_map(vertsp, vertsn, uv_coords, bcoords, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb, X, texture_map):

    # Perform Phong shading on the triangle using the p_shading function
    Y = p_shading_with_texture_map(X, vertsp.T, vertsn.T, uv_coords.T, bcoords, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb, texture_map)
    
    return Y
    
def p_shading_with_texture_map(img, vertsp, vertsn, uv_coords, bcoords, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb, texture_map):
    updated_img = img 

    # Define the Intersection class
    # The class includes the x and y coordinates of the intersection, and the color of the intersection (in [R, G, B] format).
    # Additionally, the class includes the color of the vertex that the intersection corresponds to.
    # For phong shading, we need to store the normal vector of the intersection as well.
    class Intersection:
        def __init__(self, x, y, uv, N):
            self.x = x # x coordinate of the intersection
            self.y = y # y coordinate of the intersection
            self.uv = uv # uv texture map coordinates of the intersection
            self.N = N # normal vector of the intersection


    # Define the Edge class
    # The class includes the coordinates of the lowest point (x_min, y_min) and the highest point (x_max, y_max) of the edge.
    # It also includes the inverse slope of the edge. Inverse slope is inf if the edge is horizontal, 0 if the edge is vertical.
    # Additionally, it includes the intersection of the edge with the current scanline.
    # uv_min and uv_max are the colors of the (xk_min, yk_min) and (xk_max, yk_max) vertices (in [R, G, B] format).
    # Finally, nk_min and nk_max are the normal vectors of the (xk_min, yk_min) and (xk_max, yk_max) vertices.
    class Edge:
        def __init__(self, yk_min, xk_min, yk_max, xk_max, inv_slope, uv_min, uv_max, nk_min, nk_max):
            self.yk_min = yk_min # y coordinate of the lowest point
            self.xk_min = xk_min # x coordinate of the lowest point
            self.yk_max = yk_max # y coordinate of the highest point
            self.xk_max = xk_max # x coordinate of the highest point
            self.inv_slope = inv_slope # inverse slope of the edge
            self.intersection = None # intersection of the edge with the current scanline
            self.uv_min = uv_min # uv texture map coordinates of the lowest point
            self.uv_max = uv_max # uv texture map coordinates of the highest point
            self.nk_min = nk_min # normal vector of the lowest point
            self.nk_max = nk_max # normal vector of the highest point 

    # List of triangle edges. These are calculated in the next "for" loop.
    edges = []

    # triangle -> K = 3
    for k in range(3):
        # Get the current vertex and the next vertex (with wrapping)
        v1 = vertsp[k]
        uv1 = uv_coords[k]
        n1 = vertsn[k]
        v2 = vertsp[(k+1)%3]
        uv2 = uv_coords[(k+1)%3]
        n2 = vertsn[(k+1)%3]

        # Sort the vertices so that v1 is the top vertex (the one with the highest y)
        if v1[1] < v2[1]:
            v1, v2 = v2, v1
            uv1, uv2 = uv2, uv1
            n1, n2 = n2, n1

        # Calculate the inverse slope
        if v2[1] == v1[1]:
            inv_slope = float('inf')
        else:
            inv_slope = (v2[0] - v1[0]) / (v2[1] - v1[1])

        # Add the edge to the list
        edges.append(Edge(v2[1], v2[0], v1[1], v1[0], inv_slope, uv2, uv1, n2, n1))

    y_min = min(edge.yk_min for edge in edges)
    y_max = max(edge.yk_max for edge in edges)

    # Calculating active edges for y == y_min. If an edge is horizontal (edge.inv_slope == inf) then it is not considered an active edge. Stored in a list.
    active_edges = [edge for edge in edges if (y_min == edge.yk_min and not math.isinf(edge.inv_slope))] 

    # Calculating active intersections (energa oriaka shmeia). They are instances of Intersection. They are stored in a list. 
    # They are stored in a list.
    active_intersections = []
    for edge in active_edges:
        C = edge.uv_min # active intersection color 
        N = edge.nk_min
        active_intersections.append(Intersection(edge.xk_min, edge.yk_min, C, N))
        edge.intersection = active_intersections[-1]    

    y = y_min

    while y >= y_min and y < y_max: # for y in range(y_min, y_max)
        active_intersections_sorted = sorted(active_intersections, key=lambda x: x.x) # sort active vertices by x (their first element)

        # Iterate for all Xs on the scanline
        for x in np.arange(active_intersections_sorted[0].x, active_intersections_sorted[-1].x):
            if x >= math.floor(active_intersections_sorted[0].x):
                # Interpolate over x to get the uv coordinates of the pixel at (y, x)
                uv_interp =  vector_interp((active_intersections_sorted[0].x, active_intersections_sorted[0].y), \
                                                    (active_intersections_sorted[-1].x, active_intersections_sorted[-1].y), \
                                                    active_intersections_sorted[0].uv, active_intersections_sorted[-1].uv, x, dim=1) # active intersection color
                
                color = bilerp(uv_interp, texture_map)

                # Interpolate over x to get the normal vector of the pixel at (y, x)
                normal =  vector_interp((active_intersections_sorted[0].x, active_intersections_sorted[0].y), \
                                                    (active_intersections_sorted[-1].x, active_intersections_sorted[-1].y), \
                                                    active_intersections_sorted[0].N, active_intersections_sorted[-1].N, x, dim=1)
                
                # Calculate the lighting at the pixel
                color = light(bcoords, normal, color, cam_pos, ka, kd, ks, n, l_pos, l_int, l_amb)

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
                    edge.intersection.uv = None
                    edge.intersection.N = None
                    edge.intersection = None

                elif y == edge.yk_min:
                    active_edges.append(edge)
                    active_intersections.append(Intersection(edge.xk_min, edge.yk_min, edge.uv_min, edge.nk_min))
                    edge.intersection = active_intersections[-1]

                elif edge in active_edges:  
                    if edge.inv_slope != 0: # if the edge isn't vertical
                        edge.intersection.x += edge.inv_slope
                    edge.intersection.y += 1
                    # update active intersection color
                    if edge.yk_min == edge.yk_max:   # if edge is horizontal (yk_min == yk_max), interpolate over x. Else, interpolate over y.
                        uv = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.uv_min, edge.uv_max, edge.intersection.x, dim = 1) # active intersection color
                        N = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.nk_min, edge.nk_max, edge.intersection.x, dim = 1) # active intersection normal
                    else:
                        uv = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.uv_min, edge.uv_max, edge.intersection.y, dim = 2) # active intersection color
                        N = vector_interp((edge.xk_min, edge.yk_min), (edge.xk_max, edge.yk_max), edge.nk_min, edge.nk_max, edge.intersection.y, dim = 2) # active intersection normal
                    edge.intersection.uv = uv
                    edge.intersection.N = N

    return updated_img



