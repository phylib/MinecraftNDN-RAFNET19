import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import numpy as np


class PlotChunkChanges(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(PlotChunkChanges, self).__init__()
        self.intervals=[]

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        Writer = animation.writers['ffmpeg']
        self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


    def receiveIntervalData(self, intervalData):
        uuids = set()
        playerChunks = set()
        xyz = {"x":[], "y":[], "z":[], "colors": []}
        chunk_changes = {}

        for entry in intervalData.entries:
            if entry["type"] != ChangeType.status:
                chunk = entry["chunk"]
                if chunk not in chunk_changes:
                    chunk_changes[chunk] = 1
                else:
                    chunk_changes[chunk] += 1

                if entry["type"] == ChangeType.entity:
                    if entry["typeStr"] == "PLAYER":
                        uuid = entry["uuid"]

                        # take only first position found
                        if uuid not in uuids:
                            playerChunks.add(chunk)
                            uuids.add(uuid)


        for chunk, count in chunk_changes.items():
            xz = chunk.split(",")
            x = int(xz[0])
            z = int(xz[1])
            xyz["x"].append(x)
            xyz["y"].append(z)
            xyz["z"].append(count)
            xyz["colors"].append("red" if chunk in playerChunks else "blue")

        self.intervals.append(xyz)


    def animate(self,i):

        xyz = self.intervals[i]
        x = np.array(xyz["x"])
        y = np.array(xyz["y"])
        z = np.zeros(len(x))

        dx = np.ones(len(x))
        dy = np.ones(len(x))
        dz = np.array(xyz["z"])

        # https://pythonprogramming.net/3d-bar-chart-matplotlib-tutorial/
        self.ax.clear()
        surf = self.ax.bar3d(x, y, z, dx, dy, dz, color=xyz["colors"])
        return surf,


    def noMoreIntervals(self):
       anim = animation.FuncAnimation(self.fig, self.animate,
                                      frames=len(self.intervals),
                                      interval=100,
                                      blit=False)

       anim.save('outbars.mp4', writer=self.writer)
       #plt.show()