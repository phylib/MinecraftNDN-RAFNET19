# https://stackoverflow.com/questions/31921313/matplotlib-animation-moving-square
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

x = [0, 1, 2]
y = [0, 10, 20]
y2 = [40, 30, 20]
colors = ['r','b','g','orange']

fig = plt.figure()
plt.axis('equal')
plt.grid()
ax = fig.add_subplot(111)
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

patch1 = patches.Rectangle((0, 0), 0, 0, fill=False, edgecolor=colors[0])
patch1.set_width(21)
patch1.set_height(21)

patch2 = patches.Rectangle((0, 0), 0, 0, fill=False, edgecolor=colors[1])
patch2.set_width(21)
patch2.set_height(21)


def init():
    ax.add_patch(patch1)
    ax.add_patch(patch2)
    return patch1, patch2,

def animate(i):
    patch1.set_xy([x[i], y[i]])
    patch2.set_xy([x[i], y2[i]])
    return patch1, patch2,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=len(x),
                               interval=500,
                               blit=True)
plt.show()