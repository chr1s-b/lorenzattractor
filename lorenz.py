# Chris Boddy 03/20

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np

# Aided by matplotlib documentation and stackoverflow

steps = 10000
speed = 100
skip_speed = 3
line_width = 0.3
show_axis = False
auto_rotate = True
rotate_speed = 0.1 # in degrees
dt = 0.01 # keep low else crude/overflow
show_config = False

def lorenz(x,y,z,dt,rho=28.,sigma=10.,beta=8/3.):
    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y - beta*z
    return [dx*dt, dy*dt, dz*dt]

# Hide toolbar
mpl.rcParams['toolbar'] = 'None'

# Create figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Show/hide Axis
if not show_axis: plt.axis('off')

# Labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz Attractor')

# Text
t="Right click and drag to zoom"
if show_config:
    t+= f"\nSteps: {steps}\nSpeed: {speed}/{skip_speed}\ndt: {dt}"
    if auto_rotate: t+= f"\nRotation speed: {rotate_speed}"
if not auto_rotate:
    t = "Left click and drag to rotate\n"+t
ax.text2D(0.01, 0.01, t, transform=ax.transAxes, wrap=True)

# Framing
ax.set_xlim3d([-20.0, 20.0])
ax.set_ylim3d([-20.0, 40.0])
ax.set_zlim3d([0.0, 50.0])

# Animation function
def update(n, data, line, skip, ax):
    line.set_data(data[:2, :n*skip])
    line.set_3d_properties(data[2, :n*skip])
    if auto_rotate: ax.view_init(0, rotate_speed*n)
    return line

# Starting point
xyz = np.zeros((3,steps))
xyz[:3,0] = [0.,1.,1.05]

# Calculate
for i in range(len(xyz[0])-1):
    xyz[:3,i+1] = xyz[:3,i] + lorenz(*xyz[:3,i],dt)

# Plot
plot = ax.plot(*xyz,lw=line_width)[0]
anim = animation.FuncAnimation(fig, update, steps//skip_speed, fargs=(xyz,plot,skip_speed,ax),
                               interval=100//speed, blit=False)

plt.show()
