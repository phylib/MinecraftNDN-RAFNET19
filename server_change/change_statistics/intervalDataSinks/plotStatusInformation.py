import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from change_statistics import IntervalDataSink


class StatusInformationPlot(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(StatusInformationPlot, self).__init__()
        self.timepoints = []
        self.worldFullTimeTicks = []
        self.loaded_chunks = []
        self.changed_chunks = []
        self.tile_entities = []
        self.changed_tile_entities = []
        self.entities = []
        self.changed_entities = []
        self.online_players = []
        self.diff_times = []  # ms


    def receiveIntervalData(self, intervalData):
        for entry in intervalData.status_entries:
            self.timepoints.append(entry["logTime"])
            self.worldFullTimeTicks.append(entry["worldFullTime"])
            self.loaded_chunks.append(entry["loadedChunks"])
            self.changed_chunks.append(entry["changedChunks"])
            self.tile_entities.append(entry["tileEntities"])
            self.changed_tile_entities.append(entry["changedTileEntities"])
            self.entities.append(entry["entities"])
            self.changed_entities.append(entry["changedEntities"])
            self.online_players.append(entry["onlinePlayers"])
            self.diff_times.append(entry["totalStateDiffTime"])


    def noMoreIntervals(self):
        fig, ax = plt.subplots()
        ax.plot(self.timepoints, self.loaded_chunks, label='#loaded chunks', linestyle="-", color='g')

        ax.plot(self.timepoints, self.tile_entities, label='#tile entities', color='orange')
        ax.plot(self.timepoints, self.entities, label='#entities', color='red')
        #ax.plot(self.timepoints, self.changed_entities, label='#changed entities', linestyle='--', color='red')

        ax.plot(self.timepoints, self.diff_times, label='#time for statediff [ms]', color='black')

        ax2 = ax.twinx()
        ax2.plot(self.timepoints, self.online_players, label='#online players', color='b')
        #ax2.plot(self.timepoints, self.changed_chunks, label='#changed chunks', linestyle='--', color='g')
        #ax2.plot(self.timepoints, self.changed_tile_entities, label='#changed tile entities', linestyle='--', color='orange')

        # fix legend
        # lines, labels = ax.get_legend_handles_labels()
        # lines2, labels2 = ax2.get_legend_handles_labels()
        # ax.legend(lines + lines2, labels + labels2, loc=2)
        ax.legend(loc=2)  # upper left
        ax2.legend(loc=1)  # upper right

        ax.set(xlabel='Time', title='Status information')
        ax.grid()
        datacursor()
        plt.show()