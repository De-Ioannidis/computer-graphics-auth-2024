def vector_interp(p1, p2, V1, V2, coord, dim):    
    # Extract x and y coordinates from points p1 and p2
    x1, y1 = p1
    x2, y2 = p2
    
    # Calculate lambda for point p
    if dim == 1:
        if x2 == x1:
            raise ValueError('Division by zero.')
        t = (coord - x1) / (x2 - x1)
    elif dim == 2:
        if y2 == y1:
            raise ValueError('Division by zero.')
        t = (coord - y1) / (y2 - y1)
    else:
        raise ValueError('Invalid dimension. Dimension must be 1 or 2.')
    
    # Linear interpolation between vectors V1 and V2
    V = (1 - t) * V1 + t * V2
    return V




