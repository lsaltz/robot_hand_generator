import numpy as np
def coordinate_array(val):
    finger_z = 0.2
    
    
    total_height = 0.2
    coords1 = []
    coords2 = []
    bottom_x = -abs(total_height)
    bottom_y = 0
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = int(row_length/val)
    column_points = int(column_length/val)
    n = 8
    rad = 0.019
    
    center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    
    x1 = [(c[0] + (np.cos(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
    
   
    y1 = [(c[1] + (np.sin(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
    z1 = np.linspace(0, 0, len(x1))
    coords1 = list(zip(x1, y1, z1))
    x2 = [(c[0] + (np.cos(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    y2 = [(c[1] - (np.sin(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    
    z2 = np.linspace(0, 0, len(x2))
    coords2 = list(zip(x2, y2, z2))
    c1 = np.reshape(np.asarray(coords1), (-1, n+1, 3)).tolist()
    c2 = np.reshape(np.asarray(coords2), (-1, n+1, 3)).tolist()
    all_coords = list(zip(center_pt, c1, c2)) 
    return coords1, coords2, all_coords
co1, c2, ac = coordinate_array(0.05)

#print(co1[0])
#print(ac[0])
print(ac[0])

for x in ac:
    if list(co1[1]) in x[1]:
        print(ac.index(x))



