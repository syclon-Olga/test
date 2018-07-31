import numpy as np
import sys
import nqueens as nq

#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt

xrange = np.arange(0, 1, 0.1)
yrange = np.arange(0, 1, 0.1)  
x, y = np.meshgrid(xrange, yrange)
z=np.zeros([len(x),len(y)],float)
step=100

def func (x, y):
    #best_fit= None
    for i in range(len(x)):
        for j in range(len(x[0])):
            solver= nq.Solver_8_queens(pop_size=100, cross_prob=x[i][j], mut_prob=y[i][j])
            best_fit, epoch_num, visualization = solver.solve()
            z[i,j]= best_fit          
    return z

z= np.mean([func(x, y) for n in range(step)], axis=0)
i, j= np.unravel_index(np.argmax(z), z.shape)
print ("\n", z, "\n"+"index z_max: ", i, j)

#fig = plt.figure()
#ax = Axes3D(fig)
#ax.plot_surface(x, y, z)
#plt.show()