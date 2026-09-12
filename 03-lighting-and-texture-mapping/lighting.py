# Dimitrios Ioannidis
import numpy as np



def light(point, normal, vcolor, cam_pos, k_a, k_d, k_s, n, l_pos, l_int, l_amb):

    # Normal vector normalization
    N = normal / np.linalg.norm(normal)

    # Initializing intensity to the ambient light
    # We multiply by the pixel color (vcolor) since the coefficents ka, kd, ks are scalars and don't have r, g, b components.
    I = k_a * l_amb * vcolor

    l_pos = np.array(l_pos) # Convert to numpy array if it isn't one

    if l_pos.ndim == 1:
        l_pos = l_pos[np.newaxis, :] # If we have a single light source, make sure the array is 2D (1 by 3)
                                     # Otherwise it isn't handled correctly by the for loop below.
    
    l_int = np.array(l_int) # Convert to numpy array if it isn't one

    if l_int.ndim == 1:
        l_int = l_int[np.newaxis] # If we have a single light source, make sure the array is 2D (1 by 3)

    for i in range(l_pos.shape[0]):
        # Vector from the point to the light source
        L = l_pos[i] - point
        L = L / np.linalg.norm(L)

        # Vector from the point to the camera
        V = cam_pos - point
        V = V / np.linalg.norm(V)

        # Reflection vector
        R = 2 * np.dot(N, L) * N - L
        R = R / np.linalg.norm(R)
        
        # Add the diffuse component
        I += k_d * l_int[i] * np.maximum(np.dot(N, L), 0) * vcolor # if the cosine is negative, the light is behind the surface 
        
        # Add the specular component
        I += k_s * l_int[i] * (np.maximum(np.dot(R, V), 0) ** n) * vcolor # if the cosine is negative, the light is behind the surface
    
    # Clip the intensity to [0, 1]
    I = np.clip(I, 0, 1) 
    
    return I

