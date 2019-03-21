import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class EntityAddRemovePlot(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(EntityAddRemovePlot, self).__init__()
        self.serverWorldTimeTicks = []
        self.addedEntites = []
        self.removedEntities = []
        self.onlinePlayers = []


    def receiveIntervalData(self, intervalData):
        addedEntitites = 0
        removedEntities = 0
        worldFullTime = intervalData.status_entries[0]["worldFullTime"] if (len(intervalData.status_entries) == len(intervalData.entries)) else intervalData.entries[0]["worldFullTime"]
        for entry in intervalData.entries:
            type = entry["type"]
            if type == ChangeType.entity or type == ChangeType.tile_entity:
               if "<added>" in entry["changes"]:
                   addedEntitites += 1
               elif "<removed>" in entry["changes"]:
                   removedEntities += 1


        # add to statistic
        self.serverWorldTimeTicks.append(worldFullTime)

        playercounts = []
        for statusentry in intervalData.status_entries:
            playercounts.append(statusentry["onlinePlayers"])
        avgOnlinePlayers = sum(playercounts)/len(playercounts) if (len(playercounts) > 0) else 0
        self.onlinePlayers.append(avgOnlinePlayers)

        self.addedEntites.append(addedEntitites)

        self.removedEntities.append(removedEntities)



    def noMoreIntervals(self):
        fig, ax = plt.subplots()
        ax.plot(self.serverWorldTimeTicks, self.onlinePlayers, label='# players online', linestyle="--", color='grey')

        ax2 = ax.twinx()
        ax2.plot(self.serverWorldTimeTicks, self.addedEntites, label='# added entities', linestyle="-", color='g')
        ax2.plot(self.serverWorldTimeTicks, self.removedEntities, label='# removed entities', linestyle="-", color='r')


        ax.legend(loc=2)  # upper left
        ax2.legend(loc=1)  # upper right

        ax.set(xlabel='Time (server tick)', title='Addition/Removal of Entities over time over time')
        ax.grid()
        datacursor()
        plt.show()