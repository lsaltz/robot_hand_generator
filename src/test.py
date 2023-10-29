import numpy as np
import matplotlib.pyplot as plt
def coordinate_array():
    finger_z = 0.3
    val = 0.05
    palm_z = 0.53
    total_height = 0.3
    coords1 = []
    coords2 = []
    bottom_x = -abs(total_height)
    bottom_y = -abs(palm_z/2)
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = int(row_length/val)
    column_points = int(column_length/val)
    n = 8
    rad = 0.019
    #center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    center_pt = [0.3, 0.3, 0]
    #x1 = [(c[0] + (np.cos(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, 8)]
    x1 = [center_pt[0] + (np.cos(2*np.pi/n*x)+rad) for x in range(0, n+1)]
    y1 = [center_pt[1] + (np.sin(2*np.pi/n*x)+rad) for x in range(0, n+1)]
    #y1 = [(c[1] + (np.sin(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, 8)]
    #z1 = np.linspace(0, 0, len(x1))
    coords1 = np.asarray(list(zip(x1, y1)))
    #x2 = [(c[0] + (np.cos((2*np.pi/n*x)+np.pi)*rad)) for c in center_pt for x in range(0, 8)]
    #y2 = [(c[1] - (np.sin((2*np.pi/n*x)+np.pi)*rad)) for c in center_pt for x in range(0, 8)]
    x2 = [center_pt[0] + ((np.cos(2*np.pi/n*x+np.pi)+rad)) for x in range(0, n+1)]
    y2 = [center_pt[1] - ((np.sin(2*np.pi/n*x+np.pi)+rad)) for x in range(0, n+1)]
    #z2 = np.linspace(0, 0)
    coords2 = np.asarray(list(zip(x2, y2)))
    return(coords2, coords1)

co1, co0 = coordinate_array()

for i in range(len(co1)):
    plt.scatter(co1[i][0], co1[i][1], s=2, color="blue")
    plt.scatter(co0[i][0], co0[i][1], s=2, color="red")
print(co1)
print(co0)
plt.show()
