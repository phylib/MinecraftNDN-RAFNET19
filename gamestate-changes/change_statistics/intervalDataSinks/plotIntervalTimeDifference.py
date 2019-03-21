import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class InterIntervalTimeChanges(IntervalDataSink.IntervalDataSink):

    def __init__(self, ticksPerSecond):
        super(InterIntervalTimeChanges, self).__init__()
        self.lastServerWorldFullTime = None
        self.lastIntervalBeginLogTime = None
        self.ticksPerSecond = ticksPerSecond
        self.interIntervalDurations = []
        self.serverWorldFullTimes = []
        self.interIntervalLogTimes = []


    def receiveIntervalData(self, intervalData):
        intervalBeginLogTime = intervalData.entries[0]["logTime"]
        worldFullTime = intervalData.entries[0]["worldFullTime"]
        if self.lastServerWorldFullTime is None:  # first entry, no diff possible yet
            self.lastServerWorldFullTime = worldFullTime
            self.lastIntervalBeginLogTime = intervalBeginLogTime
            return

        tick_diff = worldFullTime - self.lastServerWorldFullTime
        time_diff = intervalBeginLogTime - self.lastIntervalBeginLogTime
        self.interIntervalLogTimes.append(time_diff.total_seconds())
        self.lastIntervalBeginLogTime = intervalBeginLogTime

        diff_span = "from "+ str(self.lastServerWorldFullTime) + " to " + str(worldFullTime)
        self.interIntervalDurations.append(tick_diff)
        self.lastServerWorldFullTime = worldFullTime

        if tick_diff > 20 or tick_diff < 0:
            print("difference in Ticks > 20( diff=", tick_diff," ticks =/ticksPerSecond==> " + str(tick_diff/self.ticksPerSecond) + " seconds , [" + diff_span +"], time between log-entries: " + str(time_diff) +"): ", intervalData.entries[0])

        for entry in intervalData.entries:
            time = entry["worldFullTime"]/self.ticksPerSecond
            self.serverWorldFullTimes.append(time)

            if len(self.serverWorldFullTimes) > 0:
                if time < self.serverWorldFullTimes[-1]:
                    raise ValueError("smaller time index than prev: " + entry)


    def noMoreIntervals(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3,1)
        ax1.plot(range(0,len(self.interIntervalDurations)), self.interIntervalDurations, label='time between intervals (based on ticks)', linestyle="-", color='b')

        ax1.set(xlabel='Interval Number', ylabel='Time in ticks', title='Change in time between intervals (ticks)')
        ax1.grid()

        ax2.set(xlabel='Interval Number', ylabel='Time in seconds', title='Change in time between intervals (seconds)')
        ax2.plot(range(0, len(self.interIntervalLogTimes)), self.interIntervalLogTimes,
                 label='time between intervals (log entry time)', linestyle="-", color='r')

        ax3.set(xlabel='Individual Change Number', ylabel='World tick in seconds', title='World tick time of changes')
        ax3.plot(range(0, len(self.serverWorldFullTimes)), self.serverWorldFullTimes, label='actual world-ticks of changes', linestyle="-", color='g')
        ax3.grid()

        datacursor()
        plt.tight_layout()
        plt.show()