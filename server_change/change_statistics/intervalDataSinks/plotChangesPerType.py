import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class ChangesPerTypePlot(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(ChangesPerTypePlot, self).__init__()
        self.serverWorldTimeTicks = []
        self.changedEntities = []
        self.changedTileEntities = []
        self.changedBlocks = []
        self.changedSections = []
        self.changedChunks = []


    def receiveIntervalData(self, intervalData):
        changedBlocks = []          # identified by world-name + chunk coordinates + section index + block coordinates (in chunk)
        changedSections = []        # identified by world-name + chunk coordinates + section index
        changedChunks = []          # identified by world-name + chunk coordinates
        changedEntities = []        # identified  by uuid
        changedTileEntities = []    # identified  by uuid
        worldFullTime = intervalData.status_entries[0]["worldFullTime"] if (len(intervalData.status_entries) == len(intervalData.entries)) else intervalData.entries[0]["worldFullTime"]
        for entry in intervalData.entries:
            type = entry["type"]
            if type == ChangeType.entity:
                key = entry["uuid"]
                if key not in changedEntities:
                    changedEntities.append(key)

            elif type == ChangeType.tile_entity:
                key = entry["uuid"]
                if key not in changedTileEntities:
                    changedTileEntities.append(key)

            elif type == ChangeType.block:
                key = entry["world"] + "/" + entry["chunk"]
                if key not in changedChunks:
                    changedChunks.append(key)

                key +=  "/" + entry["section"]
                if key not in changedSections:
                    changedSections.append(key)

                key += "/" + entry["xpos"] + "," + entry["ypos"] + "," + entry["zpos"]
                if key not in changedBlocks:
                    changedBlocks.append(key)

        # add to statistic
        self.serverWorldTimeTicks.append(worldFullTime)

        if len(intervalData.entries) == len(intervalData.status_entries):
            # no log entries besides status message present
            self.changedEntities.append(0)
            self.changedTileEntities.append(0)
            self.changedBlocks.append(0)
            self.changedSections.append(0)
            self.changedChunks.append(0)
        else:
            self.changedEntities.append(len(changedEntities))
            self.changedTileEntities.append(len(changedTileEntities))
            self.changedBlocks.append(len(changedBlocks))
            self.changedSections.append(len(changedSections))
            self.changedChunks.append(len(changedChunks))


    def noMoreIntervals(self):
        pass
        fig, ax = plt.subplots()
        ax.plot(self.serverWorldTimeTicks, self.changedEntities, label='# changed entities', linestyle="-", color='g')

        ax.plot(self.serverWorldTimeTicks, self.changedTileEntities, label='# changed tile entities', color='orange')
        ax.plot(self.serverWorldTimeTicks, self.changedBlocks, label='# changed blocks', color='red')
        ax.plot(self.serverWorldTimeTicks, self.changedSections, label='# changed sections', linestyle='-', color='blue')
        ax.plot(self.serverWorldTimeTicks, self.changedChunks, label='# changed chunks', color='black')

        plt.legend()
        ax.set(xlabel='Time (server tick)', title='Change over time')
        ax.grid()
        datacursor()
        plt.show()