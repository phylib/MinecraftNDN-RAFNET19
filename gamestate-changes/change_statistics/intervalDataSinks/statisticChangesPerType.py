import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class StatisticChangesPerType(IntervalDataSink.IntervalDataSink):

    def __init__(self, ticksPerSecond):
        super(StatisticChangesPerType, self).__init__()
        self.intervals = OrderedDict()
        self.intervalSums = OrderedDict()
        self.intervalStartTick = 0
        self.ticksPerSecond = ticksPerSecond    # e.g. 20 ticks per second
        self.numberOfNonStatusEntries = 0

    def receiveIntervalData(self, intervalData):
        worldFullTime = intervalData.entries[0]["worldFullTime"]
        self.intervalStartTick = worldFullTime
        self.intervals[self.intervalStartTick] = {ChangeType.entity: 0, ChangeType.tile_entity: 0,
                                                  ChangeType.block: 0}

        for entry in intervalData.entries:
            type = entry["type"]
            if type not in [ChangeType.entity, ChangeType.tile_entity, ChangeType.block, ChangeType.status]:
                raise ValueError("type " + str(type) + " not handled")

            if type == ChangeType.status:
                continue
            # else (change to block, block_entity or entity)
            self.numberOfNonStatusEntries += 1

            # increment the change count per type
            self.intervals[self.intervalStartTick][type] += 1


    def noMoreIntervals(self):
        print("#intervals: " + str(len(self.intervals)))
        self.sumUpIntervals() # simple sanity check

        # bring interval data into a form easily digestible by pandas (bamboo ;-) )
        columns = {ChangeType.block: [], ChangeType.tile_entity: [], ChangeType.entity: []}
        for interval, intervalDict in self.intervals.items():

            for type, count in intervalDict.items():
                columns[type].append(count)

        data_frame = pd.DataFrame(columns)

        # print data frame
        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #    print(data_frame)

        # let pandas describe the data_frame
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(data_frame.describe())

        # display boxplots of selected columns
        self.showBoxplot(data_frame, ChangeType.block, 'Block changes')
        self.showBoxplot(data_frame, ChangeType.tile_entity, 'TileEntity changes')
        self.showBoxplot(data_frame, ChangeType.entity, 'Entity changes')


    def showBoxplot(self, data_frame, key, title):
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
        data_frame.boxplot(key, ax=ax1, return_type='axes')
        plt.suptitle(title)
        ax1.set_title('With outliers')

        data_frame.boxplot(key, ax=ax2, return_type='axes',  showfliers=False)
        ax2.set_title('Without outliers')

        plt.show(block=True)


    def sumUpIntervals(self):
        self.intervalSums = {ChangeType.entity: 0, ChangeType.tile_entity: 0,
                                                          ChangeType.block: 0}

        for interval, intervalDict in self.intervals.items():
            for type, count in intervalDict.items():
                self.intervalSums[type] += count

        # sum up all changes in order to sanity-check sums
        changeSum = 0
        for type in self.intervalSums.keys():
            changeSum += self.intervalSums[type]

        print("Number of non-status entries: " + str(self.numberOfNonStatusEntries))
        print("Total sum of changes: " + str(changeSum))
        if changeSum != self.numberOfNonStatusEntries:
            raise ValueError("Sum of changes (" + str(changeSum) +") does not match the number of non-status change entries (" + str(self.numberOfNonStatusEntries) + ")")


