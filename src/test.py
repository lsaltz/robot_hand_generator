import numpy as np
import matplotlib.pyplot as plt

f0l1 = 0.05904
f0l2 = 0.0576
f0l3 = 0.02736

f1l1 = 0.0576
f1l2 = 0.0864
f1l3 = 0

N = 1000

f0l1_theta_1 = -45
f0l1_theta_2 = 135
f0l2_theta_1 = -45
f0l2_theta_2 = 135
f0l3_theta_1 = -45
f0l3_theta_2  = 135

f1l1_theta_1 = 45
f1l1_theta_2 = 225
f1l2_theta_1 = 45
f1l2_theta_2 = 225
f1l3_theta_1 = 45
f1l3_theta_2 = 225

width = 0.05326

f0_theta1 = [f0l1_theta_1, f0l1_theta_2]
f0_theta1 = [i * np.pi/180 for i in f0_theta1]

f0_theta2 = [f0l2_theta_1, f0l2_theta_2]
f0_theta2 = [i * np.pi/180 for i in f0_theta2]

f0_theta3 = [f0l3_theta_1, f0l3_theta_2]
f0_theta3 = [i * np.pi/180 for i in f0_theta3]

f1_theta1 = [f1l1_theta_1, f1l1_theta_2]
f1_theta1 = [i * np.pi/180 for i in f1_theta1]

f1_theta2 = [f1l2_theta_1, f1l2_theta_2]
f1_theta2 = [i * np.pi/180 for i in f1_theta2]

f1_theta3 = [f1l3_theta_1, f1l3_theta_2]
f1_theta3 = [i * np.pi/180 for i in f1_theta3]

f0theta_1 = np.linspace(f0l1_theta_1,f0l1_theta_2, N)
f0theta_1 = f0theta_1 * np.pi/180
f0theta_2 = np.linspace(f0l2_theta_1, f0l2_theta_2, N)
f0theta_2 = f0theta_2 * np.pi/180
f0theta_3 = np.linspace(f0l3_theta_1, f0l3_theta_1, N)
f0theta_3 = f0theta_3 * np.pi/180

f1theta_1 = np.linspace(f1l1_theta_1,f1l1_theta_2, N)
f1theta_1 = f1theta_1 * np.pi/180
f1theta_2 = np.linspace(f1l2_theta_1, f1l2_theta_2, N)
f1theta_2 = f1theta_2 * np.pi/180
f1theta_3 = np.linspace(f1l3_theta_1, f1l3_theta_1, N)
f1theta_3 = f1theta_3 * np.pi/180

x0 = np.zeros((2*len(f0theta_1), len(f0theta_2)))
y0 = np.zeros((2*len(f0theta_1), len(f0theta_2)))

x1 = np.zeros((2*len(f0theta_1), len(f0theta_2)))
y1 = np.zeros((2*len(f0theta_1), len(f0theta_2)))
for i in range(0,2):
    for j in range(0, len(f0theta_1)):
        x0[i,j] = width + f0l1*np.cos(f0theta_1[j]) + f0l2*np.cos(f0theta_1[j]+ f0_theta2[i]) + f0l3*np.cos(f0theta_1[j]+ f0_theta1[i] + f0_theta1[i])
        y0[i, j] = f0l1*np.sin(f0theta_1[j]) + f0l2*np.sin(f0theta_1[j]+ f0_theta2[i]) + f0l3*np.sin(f0theta_1[j]+ f0_theta1[i] + f0_theta1[i])
    for k in range(0, len(f0theta_1)):
        x0[i+2,k] = width + f0l1*np.cos(f0_theta1[i]) + f0l2*np.cos(f0theta_2[k]+ f0_theta1[i]) + f0l3*np.cos(f0theta_1[k]+ f0_theta1[i] + f0theta_1[k])
        y0[i+2, k] = f0l1*np.sin(f0_theta1[i]) + f0l2*np.sin(f0theta_2[k]+ f0_theta1[i]) + f0l3*np.sin(f0theta_1[k]+ f0_theta1[i] + f0theta_1[k])
    for l in range(0, len(f0theta_1)):
        x1[i,l] = f1l1*np.cos(f1theta_1[l]) - f1l2*np.cos(f1theta_1[l]+ f1_theta2[i]) + f1l3*np.cos(f1theta_1[l]+ f1_theta1[i] + f1_theta1[i])
        y1[i, l] = f1l1*np.sin(f1theta_1[l]) - f1l2*np.sin(f1theta_1[l]+ f1_theta2[i]) + f1l3*np.sin(f1theta_1[l]+ f1_theta1[i] + f1_theta1[i])
    for m in range(0, len(f0theta_1)):
        x1[i+2,m] = f1l1*np.cos(f1_theta1[i]) - f1l2*np.cos(f1theta_2[m]+ f1_theta1[i]) + f1l3*np.cos(f1theta_1[m]+ f1_theta1[i] + f1theta_1[m])
        y1[i+2, m] = f1l1*np.sin(f1_theta1[i]) - f1l2*np.sin(f1theta_2[m]+ f1_theta1[i]) + f1l3*np.sin(f1theta_1[m]+ f1_theta1[i] + f1theta_1[m])
        
x0 = np.array(x0)
y0 = np.array(y0)

x1 = np.array(x1)
y1 = np.array(y1)

plt.plot(x0.T, y0.T, color='blue')
plt.plot(x1.T, y1.T, color='red')
plt.show()

