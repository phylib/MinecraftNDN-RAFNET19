import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class PlotPlayerPositionAndChunkChanges(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(PlotPlayerPositionAndChunkChanges, self).__init__()
        self.intervals_players = {}
        self.intervals_changedChunks = {}

        self.colors = ['r', 'b', 'g', 'orange']
        self.chunkRadius = 10

        self.fig = plt.figure()
        plt.axis('equal')
        plt.grid()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-60, 60)
        self.ax.set_ylim(-60, 60)
        #self.ttl = self.ax.text(.5, 1.05, '', transform=self.ax.transAxes, va='center')

        # Set up formatting for the movie files
        Writer = animation.writers['ffmpeg']
        self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


    def receiveIntervalData(self, intervalData):
        playerChunks = {}
        chunkSet = set()
        worldFullTime = intervalData.entries[0]["worldFullTime"]
        for entry in intervalData.entries:
            if entry["type"] != ChangeType.status:
                chunk = entry["chunk"]
                xz = chunk.split(",")
                x = int(xz[0])
                z = int(xz[1])
                chunkSet.add((x,z))

                if entry["type"] == ChangeType.entity:
                    if entry["typeStr"] == "PLAYER":
                        uuid = entry["uuid"]

                        # take only first position found
                        if uuid not in playerChunks:
                            playerChunks[uuid] = (x,z)


        self.intervals_players[worldFullTime] = playerChunks
        self.intervals_changedChunks[worldFullTime] = list(chunkSet)


    def initPlot(self):
        initPatches = []
        return initPatches


    def animate(self,i):
        #self.ttl.set_text("Interval #" + str(i))
        #print("Interval #" + str(i))

        # remove all preexisting patches
        [p.remove() for p in reversed(self.ax.patches)]
        addedPatches = []

        # draw player positions and "chunk-radius" around them
        for index in range(0, len(self.intervals_players[self.worldTicks[i]].keys())):
            xy = self.intervals_players[self.worldTicks[i]][list(self.intervals_players[self.worldTicks[i]].keys())[index]]
            rect = patches.Rectangle((xy[0]-10, xy[1]-10), 21, 21, fill=False, linewidth=1, edgecolor=self.colors[index])
            rect2 = patches.Rectangle((xy[0]-0.5, xy[1]-0.5), 1, 1, fill=True, linewidth=1,
                                     edgecolor="black", fc=self.colors[index])
            self.ax.add_patch(rect)
            self.ax.add_patch(rect2)
            addedPatches.append(rect)
            addedPatches.append(rect2)

        # draw changed chunks as black rectangles
        for chunk in self.intervals_changedChunks[self.worldTicks[i]]:
            chk_rect = patches.Rectangle((chunk[0]-0.5, chunk[1]-0.5), 1, 1, fill=True, linewidth=1, edgecolor="black",
                                             fc="grey")
            self.ax.add_patch(chk_rect)
            addedPatches.append(chk_rect)

        return addedPatches


    def noMoreIntervals(self):

       # remove "startup phase" where no players are present
       startupPhase = []
       for tick in sorted(self.intervals_players.keys()):
           if len(self.intervals_players[tick].keys()) == 0:
               startupPhase.append(tick)
           else:
               break

       for tick in startupPhase:
           self.intervals_players.pop(tick)

       self.worldTicks = sorted(self.intervals_players.keys())

       anim = animation.FuncAnimation(self.fig, self.animate,
                                      init_func=self.initPlot,
                                      frames=len(self.worldTicks),
                                      interval=100,
                                      blit=True)

       anim.save('out.mp4', writer=self.writer)
       #plt.show()