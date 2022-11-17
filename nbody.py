import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

obj1 = {
    "m": 2,
    "p": np.array([0,0]),
    "v": np.array([0,-1])
}
obj2 = {
    "m": 1,
    "p": np.array([1,1]),
    "v": np.array([0,0])
}
obj3 = {
    "m": 2,
    "p": np.array([1, 0]),
    "v": np.array([0,1])
}
obj4m = 1
obj4 = {
    "m": obj4m,
    "p": np.array([0,1]),
    "v": (-obj1['m'] * obj1['v']-obj2['m'] * obj2['v']-obj3['m'] * obj3['v'])/obj4m
}

init = [obj1,obj2,obj3,obj4]

print(init)

G = 1 

n = len(init)

def x_accel(s,i,j):
    m2 = init[j]['m']
    x1 = s[i]
    y1 = s[i+n]
    x2 = s[j]
    y2 = s[j+n]
    return m2*(x2-x1)/((x2-x1)**2 + (y2-y1)**2)**(3/2)
def y_accel(s,i,j):
    m2 = init[j]['m']
    x1 = s[i]
    y1 = s[i+n]
    x2 = s[j]
    y2 = s[j+n]
    return m2*(y2-y1)/((x2-x1)**2 + (y2-y1)**2)**(3/2)
def xpp(s,i): 
    other_indices = list(range(n))
    other_indices.remove(i)
    return G*sum([x_accel(s,i,j) for j in other_indices])
def ypp(s,i): 
    other_indices = list(range(n))
    other_indices.remove(i)
    return G*sum([y_accel(s,i,j) for j in other_indices])
def F(s,t): 
    return np.concatenate(
        (s[2*n:3*n],s[3*n:4*n],
         [xpp(s,i) for i in range(n)],
         [ypp(s,i) for i in range(n)]))

x0 = [o['p'][0] for o in init]
y0 = [o['p'][1] for o in init]
vx0 = [o['v'][0] for o in init]
vy0 = [o['v'][1] for o in init]
s0 = np.concatenate((x0,y0,vx0,vy0))

t = np.linspace(0,200,3000)
solution = odeint(F,s0,t)





def animate(i):
    global solution
    timesetting = 10
    colors = ['r','g','b','y','k']
    ax.clear()
    
    for k in range(n):
        plt.plot(solution[:timesetting*i,k], solution[:timesetting*i,n+k], colors[k], linewidth=0.5)  
    
        plt.plot(solution[timesetting*i,k], solution[timesetting*i,n+k],colors[k]+'o',)
    
    ax.set_title(timesetting*i)

ani = FuncAnimation(plt.gcf(), animate, interval = 10)
ax = plt.gca()
ax.set_aspect(1)
ax.set_xlim(-0.1,1.1)
ax.set_ylim(-0.2,1)
plt.axis('off')
plt.show()
