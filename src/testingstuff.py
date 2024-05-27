import numpy as np    

def straight_coordinates():
    finger_z = 0.288
    val = 0.01
        
    total_height = 0.288
    coords1 = []
    coords2 = []
    bottom_x = -abs(total_height + 0.1)
    bottom_y = -abs(total_height + 0.1)
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = int(row_length/val)
    column_points = int(column_length/val)
    n = 8
    rad = 0.039/2
      
    center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        
    
                
    x1 = [(c[0] + rad) for c in center_pt]
    y1 = [c[1] for c in center_pt]
        
        
    coords1 = list(zip(x1, y1))
        
    x2 = [(c[0] - rad) for c in center_pt]
    y2 = [c[1] for c in center_pt]
        
    coords2 = list(zip(x2, y2))
        
        
    r = np.asarray(coords1)
    l = np.asarray(coords2)
        
    print(len(center_pt))

straight_coordinates()